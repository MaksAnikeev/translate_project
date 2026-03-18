import asyncio
import logging
import aiohttp
import aiofiles

from pathlib import Path

from src.config import settings
from src.tasks.celery_app import celery_instance

@celery_instance.task
def translate_file_task(input_path: str, output_path: str):
    try:
        asyncio.run(translate_file_task_async(input_path, output_path))
        return {"status": "success", "output_path": output_path}
    except Exception as e:
        logging.exception("Критическая ошибка в задаче перевода")
        raise


async def send_chunk(session: aiohttp.ClientSession, text_chunk: str) -> str:
    """
    Отправляет кусок текста асинхронно и возвращает переведённый текст.
    Читает ответ потоком (stream).
    """
    payload = {
        "text": text_chunk,
        **settings.REQUEST_PARAMS
    }

    try:
        async with session.post(
            settings.TRANSLATE_API_URL,
            headers=settings.HEADERS,
            json=payload,
            timeout=aiohttp.ClientTimeout(total=60)
        ) as response:
            response.raise_for_status()

            translated = ""
            # Читаем ответ потоком (по частям)
            async for chunk in response.content.iter_any():
                translated += chunk.decode('utf-8', errors='replace')
            return translated

    except aiohttp.ClientError as e:
        logging.error(f"Ошибка при запросе: {e}")
        logging.error(f"Кусок текста, который не перевёлся:\n{text_chunk[:200]}...")
        return f"[ОШИБКА ПЕРЕВОДА: {text_chunk[:100]}...]"


def devise_chunks(full_text):
    """
    Разбиваем весь текст на кусочки заданной длины MAX_CHUNK_SIZE
    """
    chunks = []
    current = ""
    for line in full_text.splitlines(keepends=True):
        if len(current) + len(line) >settings.MAX_CHUNK_SIZE:
            chunks.append(current)
            current = line
        else:
            current += line
    if current:
        chunks.append(current)
    return chunks


async def translate_file_task_async(input_path: str, output_path: str):
    """
    Осуществляем подключение к внешнему сервису и производим перевод с обработкой ошибок
    """
    input_path = Path(input_path)
    output_path = Path(output_path)

    if not input_path.is_file():
        logging.warning(f"Файл не найден: {input_path}")
        return

    try:
        async with aiofiles.open(input_path, 'r', encoding='utf-8') as f:
            full_text = await f.read()
    except Exception as e:
        logging.error(f"Не удалось прочитать файл: {e}")
        return

    chunks = devise_chunks(full_text)
    logging.info(f"Разбили текст на {len(chunks)} частей")

    translated_chunks = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, chunk in enumerate(chunks, 1):
            logging.info(f"Отправляем часть {i}/{len(chunks)} ({len(chunk)} символов)...")
            tasks.append(send_chunk(session, chunk))
            await asyncio.sleep(0.4)

        translated_chunks = await asyncio.gather(*tasks, return_exceptions=True)

    final_text = ""
    for i, result in enumerate(translated_chunks, 1):
        if isinstance(result, Exception):
            logging.info(f"Часть {i} не перевелась: {result}")
            final_text += f"[ОШИБКА ПЕРЕВОДА ЧАСТИ {i}]\n"
        else:
            final_text += result

    # Сохраняем результат
    try:
        async with aiofiles.open(output_path, 'w', encoding='utf-8') as f:
            await f.write(final_text)
        logging.info(f"\nГотово! Перевод сохранён в:\n{output_path}")
        logging.info(f"Оригинал: {len(full_text)} символов")
        logging.info(f"Перевод: {len(final_text)} символов")
    except Exception as e:
        logging.error(f"Ошибка при сохранении: {e}")

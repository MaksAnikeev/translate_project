# Это тестовое задание на собеседовании - создать бекенд для перевода текстов. Сам сервис переводов уже существует

Файл `.env` в корне проекта:

~~~pycon
TRANSLATE_API_URL="https://your-service.com/api/translate"
TRANSLATE_API_TOKEN='test'
SOURCE_LANG="ru"
TARGET_LANG="en"

MAX_CHUNK_SIZE=4500
~~~

Проект создавался максимально быстро, время реализации 1 час 33 минуты

В дальнейшем можно обработать логи в файл, написать отдельный логер, а также все упаковать в DockerFile
и запускать через docker compose

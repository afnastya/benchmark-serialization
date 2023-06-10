# benchmark-serialization

## Запуск

```
docker-compose build
docker-compose up
```

Посылать запросы прокси-серверу можно с помощью netcat:
```
nc -u 0.0.0.0 2000
```
На вход ей нужно подавать запросы вида {"type": REQUEST_TYPE}, где REQUEST_TYPE - одно из "JSON", "XML", "MSGPACK", "YAML", "NATIVE", "ALL".

Пример запроса:
```
{"type": "ALL"}
```

Пример вывода (команда "ALL"):
```
JSON-0.12ms-0.15ms
NATIVE-0.59ms-0.06ms
MSGPACK-0.93ms-0.52ms
XML-1.02ms-1.01ms
YAML-17.34ms-9.56ms
```
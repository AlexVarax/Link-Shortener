<div align="center"> 
  <img src="https://github.com/AlexVarax/Link-Shortener/blob/master/FrontEnd/img/logo_proect.png" width="80">
</div>

# Link-Shortener
Программа предназначенная для сокращения URL-адресов

## Об идее
У многих компаний есть сервисы сокращения ссылок, для сбора метрик по переходам. Так например в письмах ссылки скоращенные, чтобы понимать сколько человек перешели по ней именно из писем.

## Функционал приложения
- **Генерация рабочей сокращенной ссылки**
- **Счетчик переходов** (реализован бекенд)
- **Создание учетных записей** (реализован бекенд)

## Стек технологий
- python
- HTTP
- HTML/ CSS/ JS/ JSON
- sqlite
- socket

## Структура
```
+---BackEnd
|   |   DB_Connect.py
|   |   Hash_function.py
|   |   link-short.db
|   |   main.py
|   |   Server.py
|   |
|   \---__pycache__
|           DB_Connect.cpython-312.pyc
|           Hash_function.cpython-312.pyc
|           Server.cpython-312.pyc
|
\---FrontEnd
    |   index.html
    |   script.js
    |   style.css
    |
    \---img
            logo_corp.png
            logo_proect.png
```

## Интерфейс
<div align="center" style="border: 1px solid black"> 
  <img src="https://github.com/AlexVarax/Link-Shortener/blob/master/Снимок%20экрана%202025-11-17%20022316.png" width="500">
</div>

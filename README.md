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
|   |   main.py
|   |   Server.py
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

## Запуск программы

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/AlexVarax/Link-Shortener.git
    cd Link-Shortener
    ```

2.  **Запустите бэкенд-сервер:**
    ```bash
    cd BackEnd
    python main.py
    ```
    *Сервер запустится на localhost:80*


## Интерфейс
<div align="center" style="border: 1px solid black"> 
  <img src="https://github.com/AlexVarax/Link-Shortener/blob/master/Снимок%20экрана%202025-11-17%20022316.png" width="500">
</div>

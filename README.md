# Summer School MCU Deployment Script

Скрипт для развертывания нейтронно-физического кода MCU 
(разработка НИЦ Курчатовский институт) на
многопроцессорном кластере НИЯУ МИФИ (по SSH)

### Список файлов и папок: 

1. main.py - точка входа в программу 
2. files/code/mcu00/ - хранится файл настроек MCU
3. /files/input_files/run.sh - скрипт для запуска MCU
4. /files/input_files/runtest/burnup - файл-задача, которая копируется в папки пользователей (выгорание)
5. auth - папка, содаржащая файлы авторизации пользователей (admin.txt и users.txt)
6. config.ini - файл настроек
7. proxies.txt - файл, содаржащий прокси (если прокси включены)

Прокси можно получить по адресу: 
https://hidemy.name/ru/proxy-list/?type=5#list
Неактуальные прокси просто удаляете из файла proxies.txt.


### Настройки

Настройки хранятся в файле config.ini:
```
# Номер pool-папки, в которой развертываем исполняемые файлы mcu
pool_dir_exec = 4
# Номер pool-папки, в которой будет производится счет пользователями
pool_dir_user = 3
# Начальное значение пользователя
starting_user = 1
# Максимальное кол-во пользователей
number_of_users = 59
# Использовать ли прокси (1 - включено, 0 - выключено)
proxy_enabled = 1
```


### Запуск
Для установки зависимостей:
`pip install -r requirements`

Для запуска скрипта:
`python main.py`
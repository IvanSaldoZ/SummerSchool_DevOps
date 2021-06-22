# SummerSchool2019_mcucopy

Скрипт для развертывания нейтронно-физического кода MCU (разработка НИЦ Курчатовский институт) на многопроцессорном кластере НИЯУ МИФИ (по SSH)

Файлы: 

1. main.py - точка входа в программу 
2. files/code/mcu00/ - хранится файл настроек MCU
3. /files/input_files/run.sh - скрипт для запуска MCU
4. /files/input_files/runtest/burnup - файл-задача, которая копируется в папки пользователей (выгорание)


### Настройки

Для корректной работы скрипта нужно модифицировать настройки доступа в файле main.py:

    admin_login = 'issaldikov'  # Логин
    admin_pass = ''  # Пароль
    summer_school_exec_dir = '/mnt/pool/2/issaldikov/summer_school/'  # Папка, в которой хранится mcu
    summer_school_user_dir = '/mnt/pool/1/'  # Папка, в которой хранятся папки пользователей
    pool_dir_exec: int = 2  # Номер pool-папки, в которой развертываем исполняемые файлы mcu
    pool_dir_user: int = 1  # Номер pool-папки, в которой будет производится счет пользователями
    number_of_users = 30  # Кол-во пользователей (from 00 to 29)

from helpers.ssh import SSH
import os
from paramiko import BadAuthenticationType  # Для отлова исключения при подключении к кластеру


# Класс для развертывания MCU на удаленном компьютере (кластере МИФИ)
class MCU:
    admin_login = 'issaldikov'
    admin_pass = ''
    summer_school_exec_dir = '/mnt/pool/2/issaldikov/summer_school/'
    summer_school_user_dir = '/mnt/pool/1/'
    pool_dir_exec: int = 2  # Номер pool-папки, в которой развертываем исполняемые файлы mcu
    pool_dir_user: int = 1  # Номер pool-папки, в которой будет производится счет пользователями
    number_of_users = 30  # Кол-во пользователей (from 00 to 29)

    # Конструктор
    def __init__(self, pool_dir_exec_in, pool_dir_user_in, number_of_users_in):
        self.pool_dir_exec = pool_dir_exec_in
        self.pool_dir_user = pool_dir_user_in
        self.number_of_users = number_of_users_in
        self.set_executable_dir(self.pool_dir_exec)  # Задаем текущий каталог для развертывания экзешников
        self.set_user_dir(self.pool_dir_user)  # Задаем текущий pool-каталог для развертывания входных файлов

    # Задаем путь до расположения исполняемых файлов MCU (куда развертывать дистрибутивы программы)
    def set_executable_dir(self, pool_dir_num):
        self.summer_school_exec_dir = '/mnt/pool/{0}/issaldikov/summer_school/'.format(pool_dir_num)

    # Задаем путь до расположения исполняемых файлов MCU (куда развертывать дистрибутивы программы)
    def set_user_dir(self, pool_dir_num):
        self.summer_school_user_dir = '/mnt/pool/{0}/'.format(pool_dir_num)

    # Копируем все файлы MCU (исполняемый и MCU5.INI) на удаленную машину
    def copy_mcu_to_remote_machine(self):
        ssh = SSH(self.admin_login, self.admin_pass)  # Создаем туннель для подключения по SSH для админа
        local_path_mcu = os.path.join('files', 'code', 'mcu00', 'mcu5', 'mcu5_free')
        dir_school = self.summer_school_exec_dir
        # По очереди копируем mcu в каждую директорию на удаленном компьюере
        for i in range(1, self.number_of_users):
            user_id_str = "%02d" % i  # Номер пользователя с ведущими нулями

            # Копируем исполняемый файл mcu
            ssh.create_dir(dir_school, 'mcu'+user_id_str)  # Создаем папку mcu05 в директории SummerSchool
            print('INFO: Deploying executables into ' + dir_school + 'mcu' + user_id_str)
            # Перед этим очищаем папку, если там что-то было
            mcu_user_dir = dir_school + 'mcu'+user_id_str
            ssh.clean_dir(mcu_user_dir)
            # Создаем папку mcu05 в директории SummerSchool
            ssh.create_dir(dir_school+'mcu'+user_id_str, 'mcu5')
            mcu5_folder = dir_school + 'mcu'+user_id_str + '/mcu5/'
            # Расположение mcu5_free
            remote_path = mcu5_folder+'/mcu5_free'
            # Загружаем файл mcu5_free во все папки
            ssh.upload_sftp(local_path_mcu, remote_path)
            # ssh.chmod(remote_path, 'og-r') # Убираем (минус) права для other (осатльные)
            # и group (группы) на чтение (read)
            # ssh.chmod(remote_path, 'ugo+x') # Добавляем(плюс) права для user, group, other на выполнение (eXecute)
            # ssh.chmod(mcu5_folder, '-R og-r') # Убираем (минус) права для other (осатльные)
            # и group (группы) на чтение (read), -R - рекурсивно, т.е и для вложенных файлов/папок
            # ssh.chmod(mcu5_folder, '-R ugo+x') # Добавляем(плюс) права для user, group, other на выполнение (eXecute),
            # -R - рекурсивно, т.е и для вложенных файлов/папок
            ssh.chmod(mcu_user_dir, '777')  # Всё можно делать (там где хранится MCU5.INI)
            ssh.chmod(mcu5_folder, '-R 711')  # rwx--x--x: выполнение для всех, чтение и запись только для владельца

    # Копируем входные файлы на удаленную машину в папку пользователя
    def copy_input_files_to_remote_machine(self, users_auth: list):
        local_path_burnup = os.path.join('files', 'input_files', 'runtest', 'burnup')
        local_path_sh = os.path.join('files', 'input_files', 'run.sh')
        local_path_ini = os.path.join('files', 'code', 'mcu00', 'MCU5.INI')
        # По очереди копируем входные файлы в каждую директорию на удаленном компьюере
        for i in range(1, self.number_of_users):
            user_data = users_auth[i].strip()  # Удаляем символ перевода строки \n в конце строки
            user_data = user_data.split('   ')
            login = user_data[0]
            password = user_data[1]
            user_dir = self.summer_school_user_dir + login + '/'
            print('INFO: Copying input files to remote machine for user '+login)
            try:
                # Создаем туннель для подключения по SSH для пользователя
                ssh = SSH(username=login, password=password)
            # Если такого пользователя нет
            except BadAuthenticationType:
                ssh = False
                i += 1  # Пропускаем ход
                pass

            # Если подключение прошло успешно
            if ssh:
                user_id_str = "%02d" % i  # Номер пользователя с ведущими нулями

                # Перед какими-либо действиями: удаляем всё содержимое папки пользователя
                ssh.clean_dir(user_dir)
                # Устанавливаем права на чтение только для пользователя на каталог пользователя
                ssh.chmod(user_dir, '711')
                # Создаем папку mcu в директории /mnt/pool/1/dep_573_tmp00
                ssh.create_dir(user_dir, 'mcu')
                # Создаем папку runtest в директории /mnt/pool/1/dep_573_tmp00/mcu
                ssh.create_dir(user_dir+'mcu', 'runtest')
                # Копируем входной файл в папку runtest
                runtest_folder = user_dir + 'mcu/runtest/'
                # Полный путь до входного файла
                remote_path = runtest_folder+'burnup'
                ssh.upload_sftp(local_path_burnup, remote_path)  # Загружаем файл mcu5_free во все папки

                # Теперь run.sh:
                remote_path = user_dir + 'mcu/run.sh'
                self.form_new_run_sh_file(local_path_sh, user_id_str)
                self.convert_from_windows_to_unix(local_path_sh)
                ssh.upload_sftp(local_path_sh, remote_path)  # Загружаем файл run.sh во все папки
                # https://linuxrussia.com/terminal-chmod-chown.html
                # Устанавливаем права на чтение и выполнение всеми, но на запись только владельцем (rwxr-xr-x)
                ssh.chmod(remote_path, '755')
                # ssh.chmod(remote_path, 'go-rw') # Добавляем (плюс) права для user, group и other на чтение (read)
                # и запись (write)
                # ssh.chmod(remote_path, 'ugo+x') # Убираем (минус) права для user, group, other на выполнение (eXecute)

                # Теперь MCU5.INI:
                remote_path = self.summer_school_exec_dir + 'mcu'+user_id_str + '/MCU5.INI'
                self.form_new_mcu5_ini_file(local_path_ini, user_id_str)
                ssh.upload_sftp(local_path_ini, remote_path)  # Загружаем файл mcu5_free во все папки
                # ssh.chmod(remote_path, 'ugo+rw') # Добавляем (плюс) права для user, group и other на чтение (read)
                # и запись (write)
                # ssh.chmod(remote_path, 'ugo-x') # Убираем (минус) права для user, group, other на выполнение (eXecute)
                ssh.chmod(remote_path, '666')  # rw-rw-rw-, т.е. чтение и запись для всех, выполнение - ни для кого

    # Формируем файл run.sh каждый раз перед отправкой на сервер
    def form_new_run_sh_file(self, path_to_runsh, user_id):
        file = open(path_to_runsh, "w")
        file.write('#!/bin/bash\n')
        file.write('#\n')
        file.write('#PBS -q short\n')
        file.write('#PBS -l nodes=1:ppn=1,walltime=00:15:00\n')
        # cd /mnt/pool/2/issaldikov/summer_school/mcu00/
        file.write('cd '+self.summer_school_exec_dir+'mcu'+user_id+'/\n')
        # mpirun ./mcu5/mcu5_free 1>/mnt/pool/1/dep_573_tmp00/mcu/out.txt 2>/mnt/pool/1/dep_573_tmp00/mcu/err.txt
        file.write('mpirun ./mcu5/mcu5_free 1>' + self.summer_school_user_dir
                   + 'dep_573_tmp' + user_id + '/mcu/out.txt 2>' +
                   self.summer_school_user_dir+'dep_573_tmp'+user_id+'/mcu/err.txt\n')
        file.close()

    # Формируем файл MCU5.INI каждый раз перед отправкой на сервер
    def form_new_mcu5_ini_file(self, path_to_mcu5ini, new_user_id_str):
        mcu5ini_file = open(path_to_mcu5ini, "w")
        # old_line = mcu5ini_file.readline()
        # /mnt/pool/1/dep_573_tmp00/mcu/runtest/burnup
        new_line = self.summer_school_user_dir + 'dep_573_tmp' + new_user_id_str + '/mcu/runtest/burnup'
        mcu5ini_file.writelines(new_line+'\n')
        # /mnt/pool/2/issaldikov/summer_school/MDBFREE50/
        mcu5ini_file.writelines(self.summer_school_exec_dir + 'MDBFREE50/\n')
        mcu5ini_file.writelines('a\n')
        mcu5ini_file.close()

    # Задание параметров аккаунта администратора
    def set_admin_auth(self, admin_user_login_pass)->bool:
        admin_user_login_pass = admin_user_login_pass.strip()  # Удаляем символ перевода строки \n в конце строки
        admin_data = admin_user_login_pass.split('   ')
        self.admin_login = admin_data[0]
        self.admin_pass = admin_data[1]
        return True

    # Метод для получения списка пользователей из файла формата "login     password"
    @ staticmethod
    def get_user_auth_data(user_pass_file_path)->list:
        file = open(user_pass_file_path, "r")
        users_auth = []
        for line in file.readlines():
            users_auth.append(line)
        file.close()
        return users_auth

    # Получение логин-пароля админа из файла формата "login     password"
    @ staticmethod
    def get_admin_auth_data(admin_pass_file_path)->str:
        file = open(admin_pass_file_path, "r")
        admin_user_login_pass = file.read().strip()
        file.close()
        return admin_user_login_pass

    # Преобразуем файл из формата Windows в UNIX
    # (чтобы корректно запускался на удаленке, потому что разные переводы строк)
    @ staticmethod
    def convert_from_windows_to_unix(filepath):
        # replacement strings
        windows_line_ending = b'\r\n'
        unix_line_ending = b'\n'
        # relative or absolute file path, e.g.:
        file_path = filepath
        with open(file_path, 'rb') as open_file:
            content = open_file.read()
        content = content.replace(windows_line_ending, unix_line_ending)
        with open(file_path, 'wb') as open_file:
            open_file.write(content)


if __name__ == '__main__':

    print('Deploying started...!')

    pool_dir_exec = 4  # Номер pool-папки, в которой развертываем исполняемые файлы mcu
    pool_dir_user = 3  # Номер pool-папки, в которой будет производится счет пользователями
    number_of_users = 30  # Максимальное кол-во пользователей
    mcu = MCU(pool_dir_exec, pool_dir_user, number_of_users)

    admin_auth_file_path = os.path.join('auth', 'admin.txt')
    admin_user = mcu.get_admin_auth_data(admin_auth_file_path)
    # Устанавливаем данные для доступа для админа
    mcu.set_admin_auth(admin_user)

    # Развертываем MCU на кластере в pool # pool_dir_exec
    mcu.copy_mcu_to_remote_machine()

    user_auth_file_path = os.path.join('auth', 'users.txt')
    # Считываем данные по логин-паролям пользователей
    users = mcu.get_user_auth_data(user_auth_file_path)

    # Развертываем входные файлы на кластере в pool № pool_dir_user
    mcu.copy_input_files_to_remote_machine(users)

    print('Deploying finished!')
import paramiko


class SSH:

    # Конструктор - инициализация параметров подключения и подключение к удаленному компьютеру
    def __init__(self, username, password, hostname='hpc.mephi.ru'):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def open_connection(self):
        """
        Открываем соединение
        :return:
        """
        self.client.connect(hostname=self.hostname, username=self.username, password=self.password, port=22)

    def close_connection(self):
        """
        Закрываем соединение, чтобы не банили
        :return:
        """
        self.client.close()

    # Показываем содержимое определенного каталога на удаленном сервере
    def show_dir(self, dir):
        # stdin, stdout, stderr = client.exec_command('ssh basov')
        stdin, stdout, stderr = self.client.exec_command('cd '+dir+';ls -n')
        data = stdout.read()
        s = data.decode('utf-8')
        print(s, sep='\n')

    # Создаем определенную директорию
    def create_dir(self, path, dir_name):
        # stdin, stdout, stderr = client.exec_command('ssh basov')
        stdin, stdout, stderr = self.client.exec_command('cd "'+path+'";mkdir "'+dir_name+'"')
        data = stdout.read()
        s = data.decode('utf-8')
        return s

    # Очищаем определенную директорию
    # https://losst.ru/kak-udalit-fajl-cherez-terminal-linux
    def clean_dir(self, path):
        stdin, stdout, stderr = self.client.exec_command('rm -Rf '+path+'/*')
        data = stdout.read()
        s = data.decode('utf-8')
        return s

    # Задаем определенные права на файл/директорию path
    # (например, permission_mask=og-r - убираем (минус) права для other (осатльные) и group (группы) на чтение (read))
    def chmod(self, path, permission_mask):
        # stdin, stdout, stderr = client.exec_command('ssh basov')
        cmd = 'chmod '+permission_mask+' "'+path+'"'
        stdin, stdout, stderr = self.client.exec_command(cmd)
        data = stdout.read()
        s = data.decode('utf-8')
        return s

    def upload_sftp(self, localpath, remotepath):
        sftp = self.client.open_sftp()
        sftp.put(localpath, remotepath)
        sftp.close()

    def __del__(self):
        self.close_connection()
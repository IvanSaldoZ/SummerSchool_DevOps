import paramiko
import socks  # pip install PySocks

class SSH:

    # Конструктор - инициализация параметров подключения и подключение к удаленному компьютеру
    def __init__(self, username, password, hostname='hpc.mephi.ru', is_proxy=False):
        sock = None
        # Список прокси: https://hidemy.name/ru/proxy-list/?type=5#list
        if is_proxy:
            proxy_address, proxy_ip = self.get_proxy_addr_and_ip()
            sock = socks.socksocket()
            sock.set_proxy(
                proxy_type=socks.SOCKS5,
                addr=proxy_address,
                port=int(proxy_ip),
                username="",
                password=""
            )
            sock.connect((hostname, 22))

        self.sock = sock
        self.hostname = hostname
        self.username = username
        self.password = password
        self.client = paramiko.SSHClient()
        self.client.known_hosts = None
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def open_connection(self):
        """
        Открываем соединение
        :return:
        """
        self.client.connect(hostname=self.hostname,
                            username=self.username,
                            password=self.password,
                            port=22,
                            sock=self.sock)

    def close_connection(self):
        """
        Закрываем соединение, чтобы не банили
        :return:
        """
        self.client.close()

    def get_proxy_addr_and_ip(self):
        """
        Читаем прокси SOCKS5 из первой строки файла в формате IP:port
        """
        try:
            with open('proxies.txt', "rt") as f:
                # ищем первый прокси
                first_proxy = f.readlines()[0].strip()
            ret = first_proxy.split(':')
            return ret
        except:
            return None

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
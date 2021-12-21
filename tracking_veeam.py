import subprocess
import time
import psutil
import platform
import sys


class Tracking:

    def __init__(self, file_path: str):
        """Запускает подпроцесс (self.process), получает PID процесса (self.pid) и передает его в psutil.Process
        для дальнейшего получения параметров процесса"""
        self.process = subprocess.Popen(file_path)
        self.pid = self.process.pid
        self.py = psutil.Process(self.pid)

    def run_tracking(self, interval_time: float):
        """Отслеживает параметры процесса во время его исполнения и записывает полученные данные в текстовый файл.
        Отслеживаемые параметры для Windows: загрузка CPU, Working Set, Private Bytes, Handles; для Linux: загрузка CPU,
        Resident Set Size, Virtual Memory Size, File Descriptors."""
        file = open('tracking.txt', 'w')
        try:
            if platform.system() == 'Windows':
                file.write(f'CPU, %; Working Set ; Private Bytes; Number of handles\n')
                while True:
                    self.process.poll()  # проверяем состояние процесса
                    if self.process.returncode is None:  # returncode = None, если процесс еще не окончен
                        w_set = self.py.memory_info()[0]
                        p_bytes = self.py.memory_info()[-1]
                        num_handles = self.py.num_handles()
                        cpu_use = self.py.cpu_percent()
                        file.write(f'{cpu_use}; {w_set}; {p_bytes}; {num_handles} \n')
                    else:
                        break
                    time.sleep(interval_time)  # ждем заданное пользователем время
            elif platform.system() == 'Linux':
                file.write(f'CPU, %; Resident Set Size; Virtual Memory Size; File Descriptors\n')
                while True:
                    self.process.poll()
                    if self.process.returncode is None:
                        f_descriptors = self.py.num_fds()
                        rss = self.py.memory_info()[0]
                        vms = self.py.memory_info()[1]
                        cpu_use = self.py.cpu_percent()
                        file.write(f'{cpu_use}; {rss}; {vms}; {f_descriptors} \n')
                    else:
                        break
                    time.sleep(interval_time)
        except psutil.NoSuchProcess:
            """при малых значениях interval_time (~0.1 second) может получить ошибку при закрытии процесса в Windows"""
            print('Process closed, tracking stopped!')
        finally:
            self.process.kill()  # убиваем процесс
            file.close()


if __name__ == '__main__':
    FILE_PATH = str(sys.argv[-2])
    INTERVAL_TIME = float(sys.argv[-1])

    tracking = Tracking(FILE_PATH)
    tracking.run_tracking(INTERVAL_TIME)


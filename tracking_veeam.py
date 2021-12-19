import subprocess
import psutil
from psutil import NoSuchProcess
import sys
import platform


class Tracking:

    def __init__(self, file_path):
        self.process = subprocess.Popen(file_path, stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE)
        self.pid = self.process.pid
        self.py = psutil.Process(self.pid)
        self.file = open('tracking.txt', 'w')

    def run_tracking(self, interval_time):
        try:
            if platform.system() == 'Windows':
                self.file.write(f'CPU, %; Working Set ; Private Bytes; Number of handles\n')
                while True:
                    w_set = self.py.memory_info()[0]
                    p_bytes = self.py.memory_info()[-1]
                    cpu_use = self.py.cpu_percent(interval=interval_time)
                    num_handles = self.py.num_handles()
                    self.file.write(f'{cpu_use}; {w_set}; {p_bytes}; {num_handles} \n')
            elif platform.system() == 'Linux':
                self.file.write(f'CPU, %; Resident Set Size; Virtual Memory Size; File Descriptors\n')
                while True:
                    cpu_use = self.py.cpu_percent(interval=interval_time)
                    f_descriptors = self.py.num_fds()
                    rss = self.py.memory_info()[0]
                    vms = self.py.memory_info()[1]
                    self.file.write(f'{cpu_use}; {rss}; {vms}; {f_descriptors} \n')
        except NoSuchProcess:
            print('Process closed, tracking stopped!')
        finally:
            self.file.close()


FILE_PATH = str(sys.argv[-2])
INTERVAL_TIME = int(sys.argv[-1])

tracking = Tracking(FILE_PATH)
tracking.run_tracking(INTERVAL_TIME)
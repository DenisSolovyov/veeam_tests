# veeam_tests
Программа запускается из командной строки, первым аргументом принимает путь к файлу, вторым аргументом - вещественное число - интервал времени отслеживания.
Данные по отслеживанию сохранятся в файл tracking.txt.
Example for Windows:
python tracking_veeam.py 'C:\\Windows\\system32\\notepad.exe' 2
Example for Linux:
sudo python3.9 tracking_veeam.py './sleep.sh' 1 (для запуска bash скрипта необходимо дать права на его выполение с помощью команды: chmod +x file_name)

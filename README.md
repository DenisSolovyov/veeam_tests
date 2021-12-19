# veeam_tests
Программа запускается из командной строки, первым аргументом принимает путь к файлу, вторым аргументом - целое число - интервал времени отслеживания.
После завршения процесса в консоли выведется сообщение 'Process closed, tracking stopped!', данные по отслеживанию сохранятся в файл tracking.txt.
For example:
python tracking_veeam.py 'C:\\Windows\\system32\\notepad.exe' 2

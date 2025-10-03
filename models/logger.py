""" Logging class """
import logging
import os

def loginit(name: str, path: str = "/log"):
    """ log init """
    logger1 = logging.getLogger(name)
    # Задание уровня логирования
    logger1.setLevel(logging.INFO)
    # Задание дескриптора файла, в который будет писаться лог (в данном случае будет писаться в 
    # поддиректорию log/, имя файла совпадает с именем модуля, расширение .log, режим записи
    # 'w', то есть на каждом запуске лог будет переписан заново; если выбрать 'a' тогда лог будет 
    # дополняться)
    umpath = path.split('/')[0]
    if not os.path.exists(umpath):
        os.mkdir(umpath)
    log_handler = logging.FileHandler(path, mode = 'a')
    # Задание формата исходящего сообщения: %(name)s - вывод имени модуля, %(asctime)s - вывод
    # времени логирования, %(levelname)s - вывод уровня логирования, %(message)s - вывод
    # сообщения; помимо этого можно выводить еще %(funcName)s - имя активной функции 
    log_format = logging.Formatter("[%(name)s] [%(asctime)s] [%(levelname)s] [%(message)s]")
    # Подключаем формат к дескриптору лог-файла
    log_handler.setFormatter(log_format)
    # Подключаем дескриптор лог-файла к логгеру
    logger1.addHandler(log_handler)
    # Вывод сообщения в лог-файл
    logger1.info('******* Work is beginning. Module name is %s', (name))
    return logger1

# filer.py

import json
import os
import shutil

class Filer:
    """ Work with files """
    def __init__(self, filename):
        self.filename = filename
    
    def isExists(self) -> bool:
        if os.path.exists(self.filename):
            return True
        else:
            return False

    def getCleanFilename(self):
        return self.filename.split('/')[-1]

    # Удаление файла
    def deleteFile(self):
        try:
            os.remove(self.filename)
        except Exception as ex:
            raise Exception(str(ex))

    # Создание директории
    def makeDir(self):
        try:
            if not self.isExists():        # Если такого каталога нет
                os.mkdir(self.filename)                  # Создаем его
            else:
                raise Exception('Такая директория уже существует')
        except Exception as ex:                     # Если не получается
            raise Exception(str(ex))                     # Вызываем исключение

    # Удаление директории
    def removeDir(self):
        try:
            shutil.rmtree(self.filename)
        except Exception as ex:                     # Если не получается
            raise Exception(str(ex))                     # Вызываем исключение

    # Запись файла
    def saveFile(self, code):
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(code)
    
    # Загрузка файла
    def loadFile(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as ex:
            raise Exception(str(ex))

    # Запись в виде json файла
    def saveDictAsJson(self, dic):
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:      # Пытаемся сохранить
                json.dump(dic, f, 
                        indent = 2, 
                        ensure_ascii=False)
        except Exception as ex:                                 # Если не получается
            raise Exception(str(ex))                                           # Вызываем исключение

    # Загрузка json файла
    def loadDictFromJson(self):
        try:                                                    # Пробуем загрузить
            with open(self.filename, 'r', encoding='utf-8') as f:       # Если получилось
                return json.load(f)
        except Exception as ex:                                 # Если не получилось
            raise Exception(str(ex))                                 # Вызываем исключение

    # Запись списка в файл
    def saveListToFile(self, lst):
    # Проверка объекта данных на итерируемость
        try:
            iter(lst)
        except:                                                     # Если проверка не прошла
            raise Exception('Object is not iterable')               # Вызываем исключение        
        try:        # Формируем контекст и проверяем возможность записи такого файла
            with open(self.filename, 'w', encoding='utf-8') as f:
                for line in lst:
                    if line != '':
                        f.write(line + '\n')
        except:                                                      # Если запись не получилась
            raise Exception('Cannot save list to file')              # Вызываем исключение

    # Извлечение списка из файла
    def loadListFromFile(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:           # Формируем контекст
                doms = f.read()                                             # Считываем информацию
            domms = doms.split('\n')                            # Разбиваем на отдельные элементы        
            return [x for x in domms if len(x) > 1]             # Возвращаем все, кроме пустых
        except Exception as ex:                                 # Если не получилось
            raise Exception(str(ex))                                            # Вызываем исключение
    
    # Дополнение списка в файле
    def appendPartToList(self, lst):
        if self.isExists():                 # Если такой файл существует
            try:                            # Пробуем
                self.saveListToFile(self.loadListFromFile() + lst)  # Записываем дополненный список
            except Exception as ex:                                 # Если не получилось
                raise Exception(str(ex))                                            # Вызываем исключение
        else:
            raise Exception('Такой файл отсутствует!')

    # Дополнение словаря в файле
    def appendPartToJson(self, dic):
        if self.isExists():                 # Если такой файл существует
            try:
                if type(self.loadDictFromJson()) == list:           # Если в файле записан список
                    self.saveDictAsJson(self.loadDictFromJson().append(dic))    # Пытаемся его дополнить
                elif type(self.loadDictFromJson()) == dict:           # Если в файле записан словарь
                    self.saveDictAsJson({**self.loadDictFromJson(), **dic})  # Объединяем словари
                else:
                    raise Exception('Невозможно выполнить операцию дополнения!')
            except Exception as ex:                                 # Если не получилось
                raise Exception(str(ex))                                            # Вызываем исключение


    def getAllFilesFromDir(self):                   # Передаем в функцию имя интересующей нас папки
        if not self.isExists():                     # Если такой папки не существует
            raise Exception('Path not found')       # Вызываем исключение
        content = os.listdir(self.filename)         # Загружаем в переменную все ее содержимое
        files = []                                  # Инициализация списка каталогов
        for line in content:                        # Цикл по содержимому папки
            if os.path.isfile(self.filename + line):# Если это файл
                files.append(self.filename + line)  # Добавляем к списку файлов
        return files                                # Возвращаем список файлов


    def getAllDirsFromDir(self):                    # Передаем в функцию имя интересующей нас папки
        if not self.isExists():                     # Если такой папки не существует
            raise Exception('Path not found')       # Вызываем исключение
        content = os.listdir(self.filename)         # Загружаем в переменную все ее содержимое
        dirs = []                                   # Инициализация списка каталогов
        for line in content:                        # Цикл по содержимому папки
            if os.path.isdir(self.filename + line): # Если это каталог
                dirs.append(self.filename + line)   # Добавляем к списку каталогов
        return dirs                                 # Возвращаем оба списка

    def copyFileTo(self, path):                     # Передаем в функцию путь к новому расположению файла
        if not Filer(path).isExists():              # Если такой папки не существует
            raise Exception('Path not found')       # Вызываем исключение
        else:                                       # Иначе
            shutil.copyfile(self.filename,          # Копирование файла в указанное место
                            path + '/' + self.getCleanFilename())

    def moveFileTo(self, path):                     # Передаем в функцию путь к новому расположению файла
        if not Filer(path).isExists():              # Если такой папки не существует
            raise Exception('Path not found')       # Вызываем исключение
        else:                                       # Иначе
            shutil.copyfile(self.filename,          # Копирование файла в указанное место
                            path + '/' + self.getCleanFilename())
            self.deleteFile()

    def createEmptyFile(self) -> None:
        """ Create Empty File """
        with open(self.filename, 'w') as f:
            f.write('\n')
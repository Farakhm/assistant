""" Decorators """
import os
from time import time
import datetime
from models.filer import Filer

def worktime(F):
    """ WorkTime decorator """
    t1 = time()
    def wrapper(*args):
        return F(*args)
    if not os.path.exists('log/timecodes.log'):
        Filer('log/timecodes.log').createEmptyFile()
    timelist = Filer('log/timecodes.log').loadListFromFile()
    timelist.append(f"{datetime.datetime.now()} Function: {str(F).split(' ')[1]} worked {time()-t1} s")
    Filer('log/timecodes.log').saveListToFile(timelist)
    return wrapper

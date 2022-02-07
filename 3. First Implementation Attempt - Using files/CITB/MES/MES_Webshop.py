import os
import glob
import sys
import time


def GetOrders():
    print("Getting orders...")
    time.sleep(2)
    os.chdir('../')
    os.chdir('Orders')
    path = os.getcwd()
    file_searcher = glob.glob( os.path.join(path,"*.txt"))
    print("Orders loaded.")
    print()
    return file_searcher
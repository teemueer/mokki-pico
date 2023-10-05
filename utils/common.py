import os
import ubinascii
import machine

def file_exists(filepath):
    try:
        os.stat(filepath)
        return True
    except:
        return False
    
def get_unique_id():
    return ubinascii.hexlify(machine.unique_id()).decode('utf-8')
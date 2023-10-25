from ubinascii import hexlify
from _thread import start_new_thread
from machine import reset, unique_id

def restart():
    print("*** Restarting...")
    start_new_thread(reset, ())

def get_unique_id():
    return hexlify(unique_id()).decode()
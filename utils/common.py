import urandom
import json
from ubinascii import hexlify
from _thread import start_new_thread
from machine import reset, unique_id

def restart():
    start_new_thread(reset, ())

def get_unique_id():
    return hexlify(unique_id()).decode()

def get_random_string(length=8):
    keys = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    return "".join((urandom.choice(keys) for _ in range(length)))
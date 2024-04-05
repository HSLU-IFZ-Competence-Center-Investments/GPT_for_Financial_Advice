import pandas as pd
import numpy as np
from configs.misc_config import cfg
from typing import Optional
import contextlib, time, re, os, logging, datetime


def logprint(*args, **kwargs):
    # could use logging module here instead of print
    msg = " ".join(map(str,args))
    if kwargs.pop('title',False): msg = "-"*10+msg.capitalize()+"-"*10
    if kwargs.pop('upper',False): msg = msg.upper()
    if kwargs.pop('warning',False): msg = f"\n{'*'*10} WARNING {'*'*10}\n{msg}\n{'*'*10} WARNING {'*'*10}\n"
    if cfg.LOG:
        with open(cfg.PATH.PROJECT+'/log.txt','a') as f:
            print(msg, file=f)
    if not cfg.HIDE_MSG:
        print(msg, **kwargs)

def start_logging():
    if not cfg.LOG: return
    # Create the log file if it doesn't exist
    log_file_path = cfg.PATH.PROJECT+'/log.txt'
    if not os.path.exists(log_file_path):
        with open(log_file_path, 'w') as f:
            pass  # Do nothing, just create an empty file
    else:
        with open(log_file_path, 'w') as file:
            file.truncate(0)


@contextlib.contextmanager
def timer(ident="?"):
    if not cfg.MUTE_TIMER:
        logprint(ident)

    x = time.time()
    yield
    x = time.time() - x

    if not cfg.MUTE_TIMER:
        logprint(f'Completed in {x//60:02n}:{round(x-(x//60)*60):02n}.')

def get_unique_filename(filename, dir, save_with_dt=False):
    if save_with_dt:
        now = datetime.datetime.now()
        filename = filename + now.strftime("%Y_%m_%d_%H_%M_%S")
    files = os.listdir(dir)

    if filename not in files:
        return filename
    i = 1
    while True:
        new_filename = f"{os.path.splitext(filename)[0]}_{i}{os.path.splitext(filename)[1]}"
        if new_filename not in files:
            return new_filename
        i += 1

def make_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
        return True
    return False
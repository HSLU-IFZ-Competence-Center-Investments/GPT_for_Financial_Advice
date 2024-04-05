import os
from pathlib import Path
from easydict import EasyDict as edict


#%% for DEV

PROJECT_NAME = 'AI-and-Impact-Investing' # must be same as project folder name

SUPPORTED_MODELS = ['OLS']


#%% SETTING WORKSPACE PATHS
WORKSPACE = 'GitHub'  # Currently only 'GitHub'

HOME_DIR = str(Path.home())

GITHUB = os.path.join(HOME_DIR,"GitHub")

if WORKSPACE == "GitHub":
    PROJECT_DIR = os.path.join(GITHUB,PROJECT_NAME)
else:
    raise NotImplementedError(f"Workspace '{WORKSPACE}' not implemented.")

try:
    assert os.path.exists(PROJECT_DIR), f"Project folder '{PROJECT_DIR}' not found. Check PROJECT_NAME in __config.py."
except AssertionError:
    PROJECT_DIR = input("Enter the project folder path: ")

#%% ALL CONFIG DICTS

__C = edict()
cfg = __C

__C.PATH = edict()

__C.PREP = edict()

# ML
__C.DATASET = edict()
__C.MODEL = edict()
__C.OPTIMIZER = edict()
__C.TUNE = edict()
__C.TRAIN = edict()
__C.TEST = edict()


#%% PREAMBLES

__C.PATH.PROJECT = PROJECT_DIR # project folder path
__C.PATH.DATA = os.path.join(PROJECT_DIR,'DATA') # data folder path
__C.PATH.CODE = os.path.join(PROJECT_DIR,'CODE') # code folder path
__C.PATH.OUTPUT = os.path.join(__C.PATH.CODE,'output')

__C.PATH.PREP = os.path.join(__C.PATH.OUTPUT,'data')
__C.PATH.MODELS = os.path.join(__C.PATH.OUTPUT,'models')
__C.PATH.HTMLS = os.path.join(__C.PATH.DATA,'websites')
__C.PATH.CRAWLER = os.path.join(__C.PATH.DATA,'CRAWLER')

__C.SUPPORTED_MODELS = SUPPORTED_MODELS
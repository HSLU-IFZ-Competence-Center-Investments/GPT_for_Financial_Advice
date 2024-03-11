from configs.__config import cfg


# Print
# TODO: needs testing
cfg.HIDE_MSG = False #hide messages from console
cfg.MUTE_TIMER = False #mute timer messages
cfg.LOG = True #log to file



# Model
cfg.MODEL.SAVE_WITH_DATE = True # save model parameters with date as suffix

#Tune
cfg.TUNE.SAVE_WITH_DATE = True # save tuning files with date as suffix

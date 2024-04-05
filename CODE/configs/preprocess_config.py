from configs.misc_config import cfg

cfg.PREP.NPROCESSORS = -1 # set to 0 or None to disable multiprocessing. -1 to use all available processors.
cfg.PREP.EXPORT_NAME = ... # specify the name of the file to export the preprocessed data to.
# Put your data preprocessing configurations here.
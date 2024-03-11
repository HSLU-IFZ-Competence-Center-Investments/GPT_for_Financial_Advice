import sys,multiprocessing
sys.path.append('../')
from configs.preprocess_config import cfg
from utils.misc import *
from utils.parallelization import parallelize


output_folder = cfg.PATH.PREP
make_dir(output_folder)

def preprocess_data(df,item):
    # item: in case the user needs to preprocess the data in different ways resulting in multiple preprocessings.

    make_dir(output_folder)


    
    # DO STUFF



    with timer("Exporting the final sample..."):
        
        output_path = f"{output_folder}/{cfg.PREP.EXPORT_NAME}.txt"
        make_dir(output_path.rsplit('/', 1)[0])
        df.to_csv(output_path, sep = " ", index = False)

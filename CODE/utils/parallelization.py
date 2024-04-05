from tqdm.contrib.concurrent import process_map
from configs.preprocess_config import cfg

def parallelize(func,args):
    if cfg.PREP.NPROCESSORS is not None:
        
        if cfg.PREP.NPROCESSORS == -1:
            return process_map(func,args)
        
        return process_map(func,args,max_workers=cfg.PREP.NPROCESSORS)
 
import os
from configs.misc_config import cfg


def get_companyfilepaths(company_foldername):
    file_paths = []
    for root, dirs, files in os.walk(cfg.PATH.CRAWLER+ f"/{company_foldername}"):
        for file in files:
            file_paths.append(os.path.join(root, file))

    return file_paths
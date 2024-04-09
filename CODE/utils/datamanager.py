 
import os
from configs.misc_config import cfg


def get_companyfilepaths(company_foldername):
    file_paths = []
    for root, dirs, files in os.walk(cfg.PATH.CRAWLER+ f"/{company_foldername}"):
        for file in files:
            file_paths.append(os.path.join(root, file))

    # if folder 1_master_files exists, search for company file 
    if os.path.exists(cfg.PATH.CRAWLER+ "/1_master_files"):
        # check for txt file of company_foldername in 1_master_files (+"txt")
        for root, dirs, files in os.walk(cfg.PATH.CRAWLER+ "/1_master_files"):
            for file in files:
                if company_foldername in file:
                    # overwrite file_paths with the file path of the company_foldername
                    file_paths = [os.path.join(root, file)]

    return file_paths
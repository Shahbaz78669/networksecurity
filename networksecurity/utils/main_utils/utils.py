from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import numpy as np
import dill
import sys,os
import yaml
import pickle

def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path) as file_obj:
            return yaml.safe_load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e


def wirte_yaml_file(file_path:str,content:object,replace:bool=False)->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'w')as file:
            yaml.dump(content,file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)





def save_numpy_array_data(file_path:str,array:np.array):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,'wb') as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e



def save_obejct(file_path:str,obj:object):
    try:
        logging.info("entered the save_object method of file and main_utils folder")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'wb') as file_obj:
            pickle.dump(obj,file_obj)
        logging.info("exited the save_object funtion")

    except Exception as e:
        raise NetworkSecurityException(e,sys) from e



#!/usr/bin/python

import json
import os
import numpy as np

def openFile(filename):
  with open(filename) as f:
    config = json.load(f)
  
  return config
  
import glob

def get_db_names(path):
  files_path = glob.glob(path)
  files_path = np.sort(files_path).tolist()
  #files_name = [file.replace("../data/sql/crimebb-","").replace(f"{date}.sql","") for file in files_path]
  files_name = [(file_.split("/"))[-1].replace("crimebb-","").replace(f".sql","") for file_ in files_path]
  
  zip_iterator = zip(files_name, files_path)
  files_dict = dict(zip_iterator)
  
  files_path = [f"{os.getcwd()}/{file_}" for file_ in files_path]
    
  return files_name, files_path, files_dict

def verifyFile(files_list):
  return os.path.isfile(files_list)

def verifyType(file_name):
  if os.path.isdir(file_name):
    return "dir"
  elif os.path.isfile(file_name):
    return "file"
  else:
    return None

def verifyDir(dir_path):
  if not os.path.exists(dir_path):
    os.makedirs(dir_path)

import time
import os
from crimebb.utils import verifyDir

def cmd_db_restore(db_name, db_path, passwd=None, time_to_sleep=30):
  print(f"Backuping ... {db_name}")
  
  input_path=f"{os.getcwd()}/{db_path}/"
  command_psql = f"psql -d {db_name} -a -f {input_path}"
  
  command_os = f'su -l postgres -c "{command_psql}"' 
  
  #"su -l postgres" #can be any command but don't forget -S as it enables input from stdin
  #os.system(f"psql -d {db_name} -a -f {dict_dbs[db_name]}")
  
  os.popen(command_os, 'w').write(passwd+'\n')#getpass.getpass()+'\n')
  time.sleep(time_to_sleep)
  #os.system("")

def cmd_table_to_csv(db_name, table_name, csv_path, passwd=None, time_to_sleep=30):
  print(f"Table to CSV ... {db_name}-{table_name}")

  out_path=f"{os.getcwd()}/{csv_path}/"
  verifyDir(out_path)
  out_name=f"{out_path}{table_name}.csv"

  #psql -d antichat-2021-01-10 -c "\copy boards to filename.csv csv header"
  command_psql = f"psql -d {db_name} -c '\copy {table_name} to {out_name} csv header'"

  command_os = f'su -l postgres -c "{command_psql}"'
  print("Excecuting command ... ", command_os)
  
  os.popen(command_os, 'w').write(passwd+'\n')
  time.sleep(time_to_sleep)

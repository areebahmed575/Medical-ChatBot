import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')


list_of_files = [
    "src/__init__.py",
    "src/helper.py",
    "src/prompt.py",
    ".env",
    "setup.py",
    "research/trials.ipynb",
    "app.py",
    "store_index.py",
    "static/.gitkeep",
    "templates/chat.html"

]

#In Windows,we used someting called backward slash.Here we using foward slash.Here is the advantage of using path class what will happen if you execute this code in any OS everywhere it will work.This path class will first detect the OS then it convert the path with respect to operating system you using
for filepath in list_of_files:
   filepath = Path(filepath)
   filedir, filename = os.path.split(filepath) # Then I need to seperate filedir and filename

   if filedir !="":
      os.makedirs(filedir, exist_ok=True)
      logging.info(f"Creating directory; {filedir} for the file {filename}")

   if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):#This code checks if a file at the specified filepath either does not exist or is empty. If either condition is true, it creates an empty file at that path (if it does not exist, it will be created; if it exists and is not empty, it will be emptied). 
      with open(filepath, 'w') as f:
         pass
         logging.info(f"Creating empty file: {filepath}")

   else:
      logging.info(f"{filename} is already created")
      
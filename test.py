import os
from shutil import copy
import random

def main():
  input_folder = 'output/trawler/taio/myusu'
  output_folder = 'output/normalizer'

  for dir in os.listdir(input_folder):
    current_folder = os.path.join(output_folder, dir)
    if not os.path.exists(current_folder):
      os.makedirs(current_folder)
    #copy random 800 files from input_folder to current_folder
    for i in range(800):
      file_name = random.choice(os.listdir(os.path.join(input_folder, dir)))
      #if the file exist in the output directory repeat the process
      if os.path.exists(os.path.join(current_folder, file_name)):
        i -= 1
      copy(os.path.join(input_folder, dir, file_name), os.path.join(current_folder, file_name))
    
    


if __name__ == '__main__':
  main()

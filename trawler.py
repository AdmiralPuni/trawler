import videoFrame as vf
import cropper
import taioLite as tl
import modelBuilder as mb
import os

def wait_for_input():
  if input('Insert y to continue : ') == 'y':
    return True
  else:
    wait_for_input()

def single_file():
  video_filename = input('Video filename     : ')
  cropper_input = 'output/video/' + video_filename[:-4]
  cropper_output = 'output/cropper/' + video_filename[:-4] + '/'

  vf.video_to_frame(video_filename)
  cropper.crop(cropper_input, cropper_output)

def files_in_folder(video_folder, taio_model_name, image_per_second=12):
  print('Running in automatic mode for files in', video_folder)
  for file in os.listdir(video_folder):
    video_filename = file
    cropper_input = 'output/trawler/video/' + video_filename[:-4]
    cropper_output = 'output/trawler/cropper/' + video_filename[:-4] + '/'

    print('Extracting frames from', video_filename)
    vf.video_to_frame(video_filename,image_per_second)
    print('Cropping faces in', cropper_output)
    cropper.crop(cropper_input, cropper_output)
    print('Running taio with model', taio_model_name)
    tl.run_auto(cropper_output, 'output/trawler/taio', taio_model_name)
    print("it's advised to correct false detection in taio output folder")
    #wait_for_input()

def main():
  files_in_folder('input/video/', 'myusu',30)

if __name__=="__main__":
  main()
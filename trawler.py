import videoFrame as vf
import cropper
import taioLite as tl
import modelBuilder as mb
import booruThumbnails as bt
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

def do_everything(video_folder, taio_model_name, character_list, image_per_second=12):
  print('Downloading references')
  bt.download_thumbnails(character_list, 'https://gelbooru.com/index.php?page=post&s=list&tags=sort%3ascore%3adesc+rating%3asafe+solo+1girl+', 'output/btb/goshiusa/')

  print('Cropping reference faces')
  for dir in os.listdir('output/btb/' + taio_model_name):
    if dir in character_list:
      cropper.crop('output/btb/' + taio_model_name + '/' + dir, 'output/btb/cropped/' + taio_model_name + '/' + dir)

  print('Building model')
  mb.build_model('output/btb/cropped/' + taio_model_name, taio_model_name)
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
    tl.run_auto(cropper_output, 'output/trawler/taio', taio_model_name, character_list)
    print("it's advised to correct false detection in taio output folder")
    #wait_for_input()

def main():
  #files_in_folder('input/video/', 'myusu',30)
  character_list = ['kafuu_chino','hoto_cocoa','kirima_sharo','tedeza_rize','ujimatsu_chiya']
  character_list.sort()
  do_everything('input/video', 'gochiusa',character_list, 12)

if __name__=="__main__":
  main()
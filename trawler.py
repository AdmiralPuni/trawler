import videoFrame as vf
import cropper
import modelBuilder as mb

def wait_for_input():
  if input('Insert y to continue : '):
    return True
  else:
    wait_for_input()

def main():
  video_filename = input('Video filename     : ')
  cropper_input = 'output/video/' + video_filename[:-4]
  cropper_output = 'output/cropper/' + video_filename[:-4] + '/'
  modelBuilder_input = 'output/modelBuilder/comicgirls'

  vf.video_to_frame(video_filename)
  cropper.crop(cropper_input, cropper_output)
  print('Please sort out the characters in', cropper_output, 'to', modelBuilder_input)

if __name__=="__main__":
  main()
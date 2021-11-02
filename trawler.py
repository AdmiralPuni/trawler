import videoFrame as vf
import cropper

def main():
  video_filename = input('Video filename     : ')
  cropper_input = 'output/video/' + video_filename[:-4]
  cropper_output = 'output/cropper/' + video_filename[:-4] + '/'

  vf.video_to_frame(video_filename)
  cropper.crop(cropper_input, cropper_output)

if __name__=="__main__":
  main()
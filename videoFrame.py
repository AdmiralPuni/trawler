import cv2
import os
from tqdm import tqdm

def video_to_frame(filename, cut_every = 10):
  video = cv2.VideoCapture('input/video/' + filename)
  output_folder = 'output/video/' + filename[:-4]
  frame_index=0
  frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
  progress_bar = tqdm(total = frame_count)

  if not os.path.exists(output_folder):
    os.makedirs(output_folder)
  
  print('Extracting frame from', filename)
  while(video.isOpened()):
    ret, frame = video.read()
    if ret == False:
      break
    if frame_index%cut_every == 0:
      cv2.imwrite(os.path.join(output_folder, str(round(frame_index/cut_every)) + '.jpg'),frame)
    frame_index+=1
    progress_bar.update(1)

  video.release()
  cv2.destroyAllWindows()

def main():
  video_to_frame('A2.mp4')

if __name__=="__main__":
  main()
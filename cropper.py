#@title Imports and function definitions
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
# For running inference on the TF-Hub module.
import tensorflow as tf

import tensorflow_hub as hub

import threading

from tqdm import tqdm

# For drawing onto the image.
import numpy as np
from PIL import Image

def draw_boxes(output, image, boxes, class_names, scores, max_boxes=10, min_score=0.3):
  for i in range(min(boxes.shape[0], max_boxes)):
    if scores[i] >= min_score:
      if class_names[i].decode("ascii") == "Human face" or class_names[i].decode("ascii") == "Human head":
        ymin, xmin, ymax, xmax = tuple(boxes[i])
        image_pil = Image.fromarray(np.uint8(image)).convert("RGB")
        im_width, im_height = image_pil.size
        image_pil = image_pil.crop((xmin * im_width,ymin * im_height, xmax * im_width, ymax * im_height))
        image_pil.save(output)

module_handle = "mobilenet/"

detector = hub.load(module_handle).signatures['default']

def load_img(path):
  img = tf.io.read_file(path)
  img = tf.image.decode_jpeg(img, channels=3)
  return img

def run_detector(detector, path, output):
  try:
    img = load_img(path)
  except:
    return

  converted_img  = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]
  result = detector(converted_img)

  result = {key:value.numpy() for key,value in result.items()}

  draw_boxes(output, img.numpy(), result["detection_boxes"], result["detection_class_entities"], result["detection_scores"])

path_thread_0 = []
path_thread_1 = []
path_thread_2 = []
path_thread_3 = []

image_paths_list = []

path_count = 0

input_folder = 'output/video/'
output_folder = 'output/cropper/video-4/'

class image_paths:
  def __init__(self, input, output):
    self.input = input
    self.output = output

#Dumb method find better one
if not os.path.exists(output_folder):
  os.makedirs(output_folder)

for file in os.listdir(input_folder):
  if path_count == 4:
    path_count = 0
  if path_count == 0:
    path_thread_0.append(image_paths(input_folder + file, output_folder + file))
  elif path_count == 1:
    path_thread_1.append(image_paths(input_folder + file, output_folder + file))
  elif path_count == 2:
    path_thread_2.append(image_paths(input_folder + file, output_folder + file))
  elif path_count == 3:
    path_thread_3.append(image_paths(input_folder + file, output_folder + file))
  path_count +=1

class myThread (threading.Thread):
   def __init__(self, path_collection_number):
      threading.Thread.__init__(self)
      self.path_collection_number = path_collection_number
   def run(self):
    if self.path_collection_number == 0:
      for files in tqdm(path_thread_0, leave=False):
        run_detector(detector, files.input, files.output)
    if self.path_collection_number == 1:
      for files in tqdm(path_thread_1, leave=False):
        run_detector(detector, files.input, files.output)
    if self.path_collection_number == 2:
      for files in tqdm(path_thread_2, leave=False):
        run_detector(detector, files.input, files.output)
    if self.path_collection_number == 3:
      for files in tqdm(path_thread_3, leave=False):
        run_detector(detector, files.input, files.output)


myThread(0).start()
myThread(1).start()
myThread(2).start()
myThread(3).start()
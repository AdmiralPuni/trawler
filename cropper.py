import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf
import tensorflow_hub as hub
from tqdm import tqdm
import numpy as np
from PIL import Image

module_handle = "models/mobilenet/"
detector = hub.load(module_handle).signatures['default']

def crop_face(output, image, boxes, class_names, scores, max_boxes=10, min_score=0.5):
  face_count = 0
  for i in range(min(boxes.shape[0], max_boxes)):
    if scores[i] >= min_score:
      if class_names[i].decode("ascii") == "Human face":
        ymin, xmin, ymax, xmax = tuple(boxes[i])
        image_pil = Image.fromarray(np.uint8(image)).convert("RGB")
        im_width, im_height = image_pil.size
        image_pil = image_pil.crop((xmin * im_width,ymin * im_height, xmax * im_width, ymax * im_height))
        image_pil.save(output[:-4] + '-F' + str(face_count) + '.jpg')
        face_count += 1

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
  crop_face(output, img.numpy(), result["detection_boxes"], result["detection_class_entities"], result["detection_scores"])

def crop(input_folder, output_folder):
  if input_folder[-1:] != '/':
    input_folder += '/'
  if output_folder[-1:] != '/':
    output_folder += '/'

  if not os.path.exists(output_folder):
    os.makedirs(output_folder)

  for file in tqdm(os.listdir(input_folder)):
    run_detector(detector, input_folder + file, output_folder + file)
      
def main():
  input_folder = 'output/video/cg1'
  output_folder = 'output/cropper/video-A2/'
  crop(input_folder, output_folder)

if __name__=="__main__":
  main()
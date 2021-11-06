import os
import PIL

from PIL import Image

def multiply(image_directory):
    for file in os.listdir(os.path.join(image_directory)):
      open_path = os.path.join(image_directory, file)
      save_path = os.path.join(image_directory, 'FLIPV-' + file)
      Image.open(open_path).transpose(PIL.Image.FLIP_LEFT_RIGHT).save(save_path)
      save_path = os.path.join(image_directory, 'ROTATE10-' + file)
      Image.open(open_path).rotate(10).save(save_path)
      save_path = os.path.join(image_directory, 'ROTATE20-' + file)
      Image.open(open_path).rotate(20).save(save_path)
      save_path = os.path.join(image_directory, 'ROTATE350-' + file)
      Image.open(open_path).rotate(350).save(save_path)
      save_path = os.path.join(image_directory, 'ROTATE340-' + file)
      Image.open(open_path).rotate(340).save(save_path)
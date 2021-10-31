import os
import PIL

from PIL import Image

image_directory = 'output/flip/myusu'

for dir in os.listdir(image_directory):
    for file in os.listdir(os.path.join(image_directory, dir)):
        open_path = os.path.join(image_directory, dir, file)
        save_path = os.path.join(image_directory, dir, 'FLIPV-' + file)
        Image.open(open_path).transpose(PIL.Image.FLIP_LEFT_RIGHT).save(save_path)
        #save_path = os.path.join(image_directory, dir, 'ROTATE90-' + file)
        #Image.open(open_path).rotate(90).save(save_path)
        #save_path = os.path.join(image_directory, dir, 'ROTATE270-' + file)
        #Image.open(open_path).rotate(270).save(save_path)
        save_path = os.path.join(image_directory, dir, 'ROTATE10-' + file)
        Image.open(open_path).rotate(10).save(save_path)
        save_path = os.path.join(image_directory, dir, 'ROTATE20-' + file)
        Image.open(open_path).rotate(20).save(save_path)
        save_path = os.path.join(image_directory, dir, 'ROTATE350-' + file)
        Image.open(open_path).rotate(350).save(save_path)
        save_path = os.path.join(image_directory, dir, 'ROTATE340-' + file)
        Image.open(open_path).rotate(340).save(save_path)
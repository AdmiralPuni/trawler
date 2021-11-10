import os
from PIL import Image

#resize image to a given size but keep aspect ratio
def shrink(image, size):
  width, height = image.size
  if width > height:
    height = int(height * size / width)
    width = size
  else:
    width = int(width * size / height)
    height = size
  return image.resize((width, height), Image.ANTIALIAS)

def combine():
  combined_image = Image.new('RGB', (128, 128))
  for file in os.listdir('output/cave/test/honoka/'):
    image = Image.open('output/cave/test/honoka/' + file)
    combined_image.merge(image, (0, 0))
  combined_image.save('output/cave/test/honoka/combined.png')

def main():

  combine()
  exit()
  folder_list = ['output/cave/test/' + folder + '/' for folder in os.listdir('output/cave/test/')]

  for folder in folder_list:
    for file in os.listdir(folder):
      shrink_image = shrink(Image.open(folder + file), 128)
      shrink_image.save(folder + file)
  return

if __name__ == '__main__':
  main()
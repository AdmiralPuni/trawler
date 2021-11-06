import numpy as np
import os
from PIL import Image
from tqdm import tqdm
import pickle
from pairing import pair

def main():
  def image_weight(path, resolution=(64,64)):
    loaded_image = Image.open(path).resize(resolution)
    image_array = np.array(loaded_image)
    
    np_return = []

    for x in range(resolution[0]):
      np_return.append([])
      for y in range(resolution[1]):
        np_return[x].append(round((pair(image_array[x][y][0], 1) + pair(image_array[x][y][1], 2) + pair(image_array[x][y][2], 3))/3))
    
    return np_return

  #Todo : Abandon common color like skin
  def compare_weight(model_image, input_image, resolution=(64,64)):
    result = model_image
    result_2 = []
    for index in range(len(model_image)):
      compressed_result = 0
      for x in range(resolution[0]):
        for y in range(resolution[1]):
          
          result[index][x][y] = abs(input_image[x][y] - model_image[index][x][y])
          compressed_result += result[index][x][y]
      result_2.append(compressed_result)

    return result_2

  def print_space(name):
    output = name
    for i in range(15-len(name)):
      output += ' '
    return output + '|'

  class prediction:
    def __init__(self, name, accuracy):
      self.name = name
      self.accuracy = accuracy
  
  character_list = []
  model = []
  for index, dir in enumerate(tqdm(os.listdir('output/taio/myusu3/'),desc='Loading model    ')):
    model.append([])
    character_list.append(dir)
    for file in os.listdir('output/taio/myusu3/' + dir + '/'):
      model[index].append(image_weight('output/taio/myusu3/' + dir + '/' + file))

  result = []
  for index, char in enumerate(tqdm(model, desc='Matching colors  ')):
    result.append(prediction(character_list[index],compare_weight(char, image_weight('input/274.png'))))

  for index, accuracy in enumerate(result):
    normalized = round(sum(accuracy.accuracy)/len(accuracy.accuracy))
    result[index].accuracy = ((normalized - min(accuracy.accuracy))/(max(accuracy.accuracy) - min(accuracy.accuracy)))*100
  
  result.sort(key=lambda x: x.accuracy, reverse=True)

  print(print_space(result[0].name),round(result[0].accuracy, 2),'%')

  model = None

if __name__=="__main__":
  main()
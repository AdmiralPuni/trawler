from PIL import Image
from pairing import pair
import os
from tqdm import tqdm
import pickle
import threading
from shutil import move

#global variable for predition_list
prediction_list = []
global_input = ''

def get_average(path, resolution=128):
  image = Image.open(path)
  image = image.resize((resolution, resolution))
  blocks = []
  for i in range(0, resolution, 16):
    for j in range(0, resolution, 16):
      blocks.append(image.crop((i, j, i + 16, j + 16)))
  
  averages = []
  for block in blocks:
    current_block_average = []
    pixels = block.getdata()
    for rgb in pixels:
      current_block_average.append((pair(rgb[0],1) + pair(rgb[1],2)+ pair(rgb[2],3))/3)
    averages.append(round(sum(current_block_average)/len(current_block_average)))

  averages_top = []
  averages_top.append(averages[0])
  averages_top.append(averages[4])
  averages_top.append(averages[8])
  averages_top.append(averages[16])

  return averages_top

def compare_averages(avg1, avg2):
  return sum(abs(avg1[i] - avg2[i]) for i in range(len(avg1)))

def fixed_compare_averages(avg1, avg2):
  temp_averages = []
  for index in range(len(avg1)):
    if avg1[index] == avg2[index]:
      return 0
    else:
      temp_averages.append(abs(avg1[index] - avg2[index]))
  return round(abs(sum(temp_averages)/len(temp_averages)))

def print_space(name):
    output = name
    for i in range(15-len(name)):
      output += ' '
    return output + '|'

class prediction():
  def __init__(self, predicted_name, accuracy, path):
    self.predicted_name = predicted_name
    self.accuracy = accuracy
    self.path = path

def detect(name, path_list, model, character_list, images_to_compare = 30):
  for file in tqdm(path_list[name]):
    comparison = []
    for averages in model:
      weight = 0
      for index, avg in enumerate(averages):
        if index<images_to_compare:
          input_average = get_average(global_input + '/' + file)
          weight += compare_averages(input_average, avg)
      comparison.append(weight)

    #normalized compatison to 0-100
    comparison = [i / max(comparison) * 100 for i in comparison]
    #invert comparison
    comparison = [100 - i for i in comparison]
    
    prediction_list.append(prediction(character_list[comparison.index(max(comparison))], round(max(comparison),2), file))

class detection_thread(threading.Thread):
  def __init__(self, threadID, name, path_list, model, character_list):
    threading.Thread.__init__(self)
    self.threadID = threadID
    self.name = name
    self.path_list = path_list
    self.model = model
    self.character_list = character_list

  def run(self):
    detect(self.threadID, self.path_list, self.model, self.character_list)

def build_model(model_folder, model_filename):
  model = []
  character_list = []
  for index, dir in enumerate(tqdm(os.listdir(model_folder))):
    model.append([])
    character_list.append(dir)
    for file in os.listdir(model_folder + '/' + dir):
      model[index].append(get_average(model_folder + '/' + dir + '/' + file))

  #save model and character list
  with open('models/' + model_filename + '.pkl', 'wb') as f:
    pickle.dump(model, f)
  with open('models/' + model_filename + '_characters.pkl', 'wb') as f:
    pickle.dump(character_list, f)

  return model, character_list
  
def load_model(model_filename):
  with open('models/' + model_filename + '.pkl', 'rb') as f:
    model = pickle.load(f)
  with open('models/' + model_filename + '_characters.pkl', 'rb') as f:
    character_list = pickle.load(f)
  return model, character_list

def run_through_files(model_name, input_folder, output_folder, renew_model = False):
  model = []
  character_list = []
  set_global_variable(input_folder)

  if renew_model:
    print('Building model...')
    model , character_list = build_model('output/caveModel/' + model_name, model_name)
  else:
    if not os.path.isfile('models/' + model_name + '.pkl'):
      print('Building model...')
      model , character_list = build_model('output/caveModel/' + model_name, model_name)
    else:
      print('Loading model...')
      model , character_list = load_model(model_name)

  path_list = []
  for i in range(4):
    path_list.append([])
  path_list_count = 0

  for file in os.listdir(input_folder):
    if path_list_count == 4:
      path_list_count = 0
    path_list[path_list_count].append(file)
    path_list_count += 1

  threads = []
  for i in range(4):
    thread = detection_thread(i, 'Thread-' + str(i), path_list, model, character_list)
    thread.start()
    threads.append(thread)
  for thread in threads:
    thread.join()
  
  for prediction in prediction_list:
    print(print_space(prediction.predicted_name), print_space(str(prediction.accuracy)), prediction.path)
    if not os.path.exists(output_folder + '/' + prediction.predicted_name):
      os.makedirs(output_folder + '/' + prediction.predicted_name)
    if(prediction.accuracy > 10):
      #move(input_folder + '/' + prediction.path, output_folder + '/' + prediction.predicted_name + '/' + prediction.path)
      continue

def set_global_variable(input):
  global global_input
  global_input = input

def main():
  model_name = 'myusu3'
  input_folder = 'input/images'
  output_folder = 'output/cave/'
  
  #print(fixed_compare_averages(get_average('input/images/rin.png'), get_average('input/images/honoka3.jpg')))

  #run_through_files(model_name, input_folder, output_folder, True)
  #run_through_files('comicgirls', 'output/cropper/cg3', 'output/cave/comicgirls/')
  print(get_average('input/images/eli.png'))
  exit()

if __name__ == '__main__':
  main()
from PIL import Image
from pairing import pair
import os
from tqdm import tqdm
import pickle
import threading
from shutil import move
from multiprocessing import Process

#global variable for predition_list
prediction_list = []

def get_average(path):
  image = Image.open(path)
  image = image.resize((256, 256), Image.ANTIALIAS)
  blocks = []
  for i in range(0, 256, 32):
    for j in range(0, 256, 32):
      blocks.append(image.crop((i, j, i + 32, j + 32)))

  avg_colors = []

  for i in range(len(blocks)):
    avg_colors.append(blocks[i].getpixel((16, 16)))

  avg_colors = [list(i) for i in avg_colors]

  for index in range(len(avg_colors)):
    for i in range(3):
      avg_colors[index][i] = pair(avg_colors[index][i], i)

  averages = []

  for i in range(len(avg_colors)):
    averages.append(round(sum(avg_colors[i]) / len(avg_colors[i])))

  return averages

def compare_averages(avg1, avg2):
  return sum(abs(avg1[i] - avg2[i]) for i in range(len(avg1)))

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

def detect(name, path_list, model, character_list, images_to_compare = 50):
  for file in tqdm(path_list[name]):
    comparison = []
    for averages in model:
      weight = 0
      for index, avg in enumerate(averages):
        if index<images_to_compare:
          weight += compare_averages(get_average('output/cropper/cg3/' + file), avg)
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
    
#change detection_thread to use process instead
class detection_process(Process):
  def __init__(self, threadID, name, path_list, model, character_list):
    Process.__init__(self)
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

def run_through_files(model_name, input_folder, output_folder):
  model = []
  character_list = []

  #if model is empty, create it
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
      move('output/cropper/cg3/' + prediction.path, output_folder + '/' + prediction.predicted_name + '/' + prediction.path)
    

def main():
  #run_through_files('myusu3', 'input/images', 'output/cave/')
  run_through_files('comicgirls', 'output/cropper/cg3', 'output/cave/comicgirls/')
  exit()

if __name__ == '__main__':
  main()
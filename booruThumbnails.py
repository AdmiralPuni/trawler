import threading
import os
from tqdm import tqdm

from bs4 import BeautifulSoup
import re
import requests

class download_thread(threading.Thread):
  def __init__(self, site, name, pid, output_folder):
    threading.Thread.__init__(self)
    self.site = site
    self.name = name
    self.pid = pid
    self.output_folder = output_folder
  def run(self):
    response = requests.get(self.site + '&pid=' + str(self.pid))
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')

    urls = [img['src'] for img in img_tags]
    
    for url in tqdm(urls, leave=False):
      if 'thumbnail' in url:
        filename = re.search(r'/([\w_-]+[.](jpg|gif|png))', url)
        if not filename:
          continue
        with open(os.path.join(self.output_folder + self.name, filename.group(1)), 'wb') as f:
          if 'http' not in url:
            url = '{}{}'.format(self.site, url)
          response = requests.get(url)
          f.write(response.content)

class name_thread(threading.Thread):
  def __init__(self, name, site, output_folder, pages=5, pid=42):
    threading.Thread.__init__(self)
    self.name = name
    self.site = site
    self.pages = pages
    self.pid = pid
    self.output_folder = output_folder
  def run(self):
    thread_list_download=[]
    for i in range(self.pages):
      thread_list_download.append(download_thread(self.site, self.name, self.pid, self.output_folder))
      self.pid += 42
      thread_list_download[i].start()
    for thread in thread_list_download:
      thread.join()
    return True

def download_thumbnails(character_list, site, output_folder):
  thread_list = []
  for index, name in enumerate(character_list):
    if not os.path.exists(output_folder + name):
      os.makedirs(output_folder + name)
    print('Downloading images for', name)
    thread_list.append(name_thread(name, site + name, output_folder))
    thread_list[index].start()
    thread_list[index].join()

def main():
  character_list = ['ichii_yui']
  site = 'https://gelbooru.com/index.php?page=post&s=list&tags=sort%3ascore%3adesc+rating%3asafe+solo+1girl+'
  output_folder = 'output/btb/yuyushiki/'
  download_thumbnails(character_list, site, output_folder)

if __name__=="__main__":
  main()
import threading
import re
import requests
import os
from bs4 import BeautifulSoup
from tqdm import tqdm

def get_thread_number(url):
    thread_number = ''
    for char in reversed(url):
        if char == '/':
            return thread_number[::-1]
        thread_number += str(char)

class download_thread(threading.Thread):
  def __init__(self, site, download_folder):
    threading.Thread.__init__(self)
    self.site = site
    self.download_folder = download_folder
  def run(self):
    image_count = 0
    response = requests.get(self.site)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('a',{"class": "fileThumb"})

    urls = [a['href'] for a in img_tags]
    
    for url in tqdm(urls, leave=False):
      filename = re.search(r'/([\w_-]+[.](jpg|gif|png))', url)
      if not filename:
        continue
      with open(os.path.join(self.download_folder, filename.group(1)), 'wb') as f:
        image_count += 1
        url = url[2:]
        if 'https' not in url:
            url = 'https://' + url
        url
        response = requests.get(url)
        f.write(response.content)

def main():
  download_folder = ''

  site = input('Site             : ')
  download_folder = get_thread_number(site)

  if not os.path.exists('output/4cdn/' + download_folder):
      os.makedirs('output/4cdn/' + download_folder)

  download_folder = 'output/4cdn/' + download_folder

  print('Output           :', download_folder)

  thread_list = []

  thread_list.append(download_thread(site, download_folder))
  thread_list[0].start()
  

if __name__=="__main__":
  main()
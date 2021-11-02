import threading
import os
from tqdm import tqdm

from bs4 import BeautifulSoup
import re
import requests

class download_thread(threading.Thread):
  def __init__(self, site, name, pid):
    threading.Thread.__init__(self)
    self.site = site
    self.name = name
    self.pid = pid
  def run(self):
    response = requests.get(self.site + '&pid=' + str(self.pid))
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')

    urls = [img['src'] for img in img_tags]
    
    for url in tqdm(urls, leave=False):
      filename = re.search(r'/([\w_-]+[.](jpg|gif|png))', url)
      if not filename:
        continue
      with open(os.path.join('btb/output/myusu-2/' + self.name, filename.group(1)), 'wb') as f:
        if 'http' not in url:
          url = '{}{}'.format(self.site, url)
        response = requests.get(url)
        f.write(response.content)

class name_thread(threading.Thread):
  def __init__(self, name, site, pages=5, pid=42):
    threading.Thread.__init__(self)
    self.name = name
    self.site = site
    self.pages = pages
    self.pid = pid
  def run(self):
    print('')
    print(self.name)
    thread_list_download=[]
    for i in range(self.pages):
      thread_list_download.append(download_thread(self.site, self.name, self.pid))
      self.pid += 42
      thread_list_download[i].start()
    for thread in thread_list_download:
      thread.join()
    return True

def main():
  character_list = ['kunikida-hanamaru','kurosawa-dia','kurosawa-ruby']
  thread_list = []
  site = 'https://gelbooru.com/index.php?page=post&s=list&tags=sort%3ascore%3adesc+rating%3asafe+solo+'
  for index, name in enumerate(character_list):
    if not os.path.exists('btb/output/myusu-2/' + name):
      os.makedirs('btb/output/myusu-2/' + name)
    thread_list.append(name_thread(name, site + name.replace('-','_')))
    thread_list[index].start()
    thread_list[index].join()

if __name__=="__main__":
  main()
import threading
import time
import datetime
import logging
import requests
import os

def download_gambar(url=None, i=None):
    if (url is None):
        return False
    ff = requests.get(url)
    tipe = dict()
    tipe['image/png']='png'
    tipe['image/jpg']='jpg'
    tipe['image/jpeg']='jpg'

    content_type = ff.headers['Content-Type']
    logging.warning(content_type)
    if (content_type in list(tipe.keys())):
        namafile = os.path.basename(url)
        ekstensi = tipe[content_type]
        logging.warning(f"writing {namafile}.{ekstensi}")
        fp = open(f"Image{i}.{ekstensi}","wb")
        fp.write(ff.content)
        fp.close()
    else:
        return False


if __name__=='__main__':
    url_download = ['https://images.pexels.com/photos/313690/pexels-photo-313690.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260',
                    'https://blog.hubspot.com/hubfs/remote-work-tips.jpg']

    threads = []
    i=1
    for url in url_download:
        t = threading.Thread(target=download_gambar, args=(url,i,))
        threads.append(t)
        i+=1
        
    for thr in threads:
        thr.start()
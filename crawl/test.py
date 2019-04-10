import requests
import os
url = 'http://search.cnki.net/down/default.aspx?filename=SZTJ201801088&dbcode=CJFD&year=2018&dflag=pdfdown'
r = requests.get(url)
file_path = 'f:/file/newfile/zc/pdf/'
if not os.path.exists(file_path):
        os.makedirs(file_path)
if str(url).endswith('pdfdown'):
    file_path = file_path + 'zc.pdf'
with open(file_path, "wb") as f:
     f.write(r.content)
f.close()
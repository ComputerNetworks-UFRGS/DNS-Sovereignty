import os
import wget
import zipfile
import gzip
import shutil
import glob
from datetime import datetime
from bs4 import BeautifulSoup
import requests

# Get month to use in prefix2as url
month = datetime.now().month
year = datetime.now().year

def listFD(url, ext=''):
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    return [url + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]

def gunzip_shutil(source_filepath, dest_filepath, block_size=65536):
    with gzip.open(source_filepath, 'rb') as s_file, \
            open(dest_filepath, 'wb') as d_file:
        shutil.copyfileobj(s_file, d_file, block_size)

url_prefix2as_ipv4 = f'https://publicdata.caida.org/datasets/routing/routeviews-prefix2as/{year}/0{month}/'
ext = 'gz'

url_prefix2as_ipv6 = f'https://publicdata.caida.org/datasets/routing/routeviews6-prefix2as/{year}/0{month}/'
ext = 'gz'

result = listFD(url_prefix2as_ipv4, ext)
prefix2as_ipv4 = result[-1]

result = listFD(url_prefix2as_ipv6, ext)
prefix2as_ipv6 = result[-1]

url_as2organization = f'https://publicdata.caida.org/datasets/as-organizations/'
ext_as2organization = 'txt.gz'

result = listFD(url_as2organization, ext_as2organization)
as2organization = result[-1]

tranco = 'https://tranco-list.s3.amazonaws.com/tranco_VXYGN-1m.csv.zip'

print('Downloading Tranco List\n')
wget.download(tranco)
print('\nDownloading Prefix2ASIPv4\n')
wget.download(prefix2as_ipv4)
print('\nDownloading Prefix2ASIPv6\n')
wget.download(prefix2as_ipv6)
print('\nDownloading AS2Organization\n')
wget.download(as2organization)


print('Unzipping Tranco List')
with zipfile.ZipFile("tranco_VXYGN-1m.csv.zip","r") as zip_ref:
    zip_ref.extractall(".")
    
os.remove("tranco_VXYGN-1m.csv.zip")

files_gz = glob.glob('*.gz')

for file in files_gz:
    print(f'Unzipping {file}')
    gunzip_shutil(file, file[:-3])
    os.remove(file)
    

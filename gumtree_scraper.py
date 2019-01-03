from bs4 import BeautifulSoup
import requests

source = requests.get('https://www.onthemarket.com/to-rent/property/bristol/').text
soup = BeautifulSoup(source, 'lxml')
results = soup.find('li', class_='')
print(results)

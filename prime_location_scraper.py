from bs4 import BeautifulSoup
import requests

for i in range(31):
    source = requests.get('https://www.primelocation.com/to-rent/property/bristol/?identifier=bristol&page_size=50&q=Bristol&search_source=refine&radius=0&view_type=grid&pn=' + str(i)).text
    soup = BeautifulSoup(source, 'lxml')

    for results in soup.find_all('div', class_='listing-results-wrapper'):
        right_grid = results.find('div', class_='listing-results-grid-right').find('div', class_='listing-results-grid-content')
        left_grid = results.find('div', class_='listing-results-grid-left').find('div', class_='status-wrapper')

        property_price = right_grid.find('div', class_='grid-cell-price').a.text
        print(property_price)

        location = right_grid.find('p', class_='').a.text
        print(location)

        try:
            property_image = left_grid.a.img['src']
        except Exception as e:
            property_image = None
        print(property_image)
        print('')

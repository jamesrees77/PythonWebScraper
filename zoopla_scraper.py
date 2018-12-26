from bs4 import BeautifulSoup
import requests
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('/Users/james/Desktop/WebScraperProject/pythonscraperproject-firebase-adminsdk-2ujy0-749a94c698.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

# ZOOPLA
for i in range(1):
    source = requests.get('https://www.zoopla.co.uk/to-rent/property/bristol/?identifier=bristol&page_size=10&q=Bristol&search_source=to-rent&radius=0&price_frequency=per_month&pn=' + str(i)).text

    soup = BeautifulSoup(source, 'lxml')

    for results in soup.find_all('div', class_='listing-results-wrapper'):

        right_results = results.find('div', class_='listing-results-right')
        left_results = results.find('div', class_='listing-results-left')

        property_price = right_results.a.text

        scraped_address = right_results.find('a', class_='listing-results-address').text
        # remove postcode from address
        address = scraped_address[:-4]
        # take last 4 characters of address for post code
        postcode = scraped_address[-4:]

        # check if post code is only 3 characters - if it is remove whitespace at start.
        if postcode[0] == " ":
            postcode = postcode[-3:]

        # Ensure that property image exists - if not return None
        try:
            property_image = left_results.div.a.img['src']
        except Exception as e:
            property_image = None

        doc_ref = db.collection(u'properties').document()
        doc_ref.set({
            u'property_photo': property_image,
            u'property_address': address,
            u'property_rent': property_price,
            u'post_code': postcode
        })

        print('all properties successfully uploaded')

# RIGHT MOVE

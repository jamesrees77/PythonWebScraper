from bs4 import BeautifulSoup
import requests
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('/Users/james/Desktop/WebScraperProject/pythonscraperproject-firebase-adminsdk-2ujy0-749a94c698.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

# loop through amount of pages in query
for i in range(1):
    source = requests.get('https://www.zoopla.co.uk/to-rent/property/bristol/?identifier=bristol&page_size=10&q=Bristol&search_source=to-rent&radius=0&price_frequency=per_month&pn=' + str(i)).text

    soup = BeautifulSoup(source, 'lxml')

    # loop through all classes of listing-results-wrapper
    for results in soup.find_all('div', class_='listing-results-wrapper'):

        right_results = results.find('div', class_='listing-results-right')
        left_results = results.find('div', class_='listing-results-left')

        # get number of beds
        try:
            number_beds = right_results.h3.find('span', class_='num-beds').text
        except Exception as e:
            number_beds = None

        print("number of beds: ", number_beds)

        # get number of bathrooms
        try:
            number_baths = right_results.h3.find('span', class_='num-baths').text
        except Exception as e:
            number_baths = None

        print("number of bathrooms: ", number_baths)

        # rent price of property
        property_price = right_results.a.text
        print("rent amount: ", property_price)

        # get full address
        scraped_address = right_results.find('a', class_='listing-results-address').text

        # remove postcode from address
        address = scraped_address[:-4]
        print("address: ", address)

        # take last 4 characters of address for post code
        postcode = scraped_address[-4:]

        # check if post code is only 3 characters - if it is remove whitespace at start.
        if postcode[0] == " ":
            postcode = postcode[-3:]

        print("postcode: ", postcode)
        # Ensure that property image exists - if not return None
        try:
            property_image = left_results.div.a.img['src']
        except Exception as e:
            property_image = None

        print("Property Image: ", property_image)

        # point to document called properties in firebase
        doc_ref = db.collection(u'properties').document()
        #  set object and push to firebase
        doc_ref.set({
            u'property_address': address,
            u'number_of_beds': number_beds,
            u'number_of_baths': number_baths,
            u'property_rent': property_price,
            u'post_code': postcode,
            u'property_photo': property_image,
        })
        print('')
        print('')
        print('')

#  run statement when all uploaded to firebase
print('all properties successfully uploaded to firebase')

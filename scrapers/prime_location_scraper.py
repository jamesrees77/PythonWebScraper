from bs4 import BeautifulSoup
import requests
import firebase_admin
from firebase_admin import credentials, firestore
from algoliasearch import algoliasearch

client = algoliasearch.Client("SXINQ9YIRL", '51a8ef4df6aee483c0b9887b43e28b88')
index = client.init_index('properties')


cred = credentials.Certificate('/Users/james/Desktop/WebScraperProject/firestore/pythonscraperproject-firebase-adminsdk-2ujy0-749a94c698.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

print('starting')
class primeLocationScraper():
    for i in range(31):
        source = requests.get('https://www.primelocation.com/to-rent/property/bristol/?identifier=bristol&page_size=50&q=Bristol&search_source=refine&radius=0&view_type=grid&pn=' + str(i)).text
        soup = BeautifulSoup(source, 'lxml')

        for results in soup.find_all('div', class_='listing-results-wrapper'):
            right_grid = results.find('div', class_='listing-results-grid-right').find('div', class_='listing-results-grid-content')
            left_grid = results.find('div', class_='listing-results-grid-left').find('div', class_='status-wrapper')

            property_price = right_grid.find('div', class_='grid-cell-price').a.text
            if len(property_price) >= 40:
                property_price = int(property_price[16:-19].replace(',', ''));
            else: property_price = int(property_price[16:-18].replace(',', ''));

            print(property_price)


            scraped_address = right_grid.find('p', class_='').a.text
            address = scraped_address[:-4]
            print("address: ", address)

            url = 'https://www.primelocation.com' + right_grid.find('p', class_='').a.get('href')
            print('URL: ', url)

            # take last 4 characters of address for post code
            postcode = scraped_address[-4:]

            # check if post code is only 3 characters - if it is remove whitespace at start.
            if postcode[0] == " ":
                postcode = postcode[-3:]

            print("postcode: ", postcode)

            try:
                number_beds = int(float(right_grid.find('div', class_='grid-listing-attributes').find('span', class_='num-beds').text))
            except Exception as e:
                number_beds = None
            print(number_beds)

            try:
                number_baths = int(float(right_grid.find('div', class_='grid-listing-attributes').find('span', class_='num-baths').text))
            except Exception as e:
                number_baths = None
            print(number_baths)

            try:
                property_image = left_grid.a.img['src'].decode('utf-8')
            except Exception as e:
                property_image = None
            print(property_image)
            print('')

            description = right_grid.findAll('p', class_='')[1].text
            print('desciption: ', description)

            term = 'student'

            if term in description.lower():
                is_student_property = True
            else:
                is_student_property = False

            print('student?: ', is_student_property)

            doc_ref = db.collection(u'prime_location').document()
            print('ID: ', doc_ref.id)


            property_rent = property_price / number_beds
            print(property_rent)

            item = {
                u'property_id': doc_ref.id.decode('utf-8'),
                u'property_address': address,
                u'number_of_beds': number_beds,
                u'number_of_baths': number_baths,
                u'property_rent': property_rent,
                u'post_code': postcode,
                u'property_photo': property_image,
                u'url': url.decode('utf-8'),
                u'original_site': 'Prime Location'.decode('utf-8'),
                u'is_student_property': is_student_property,
                u'description': description.decode('utf-8'),
            }
            print(item)
             # set object and push to firebase
            db.collection(u'properties').document(doc_ref.id).set(item)
            print('')
            print('')
            print('')

            res = index.add_object(item)
            print "ObjectID=%s" % res["objectID"]


    #  run statement when all uploaded to firebase
    print('all properties successfully uploaded to firebase')

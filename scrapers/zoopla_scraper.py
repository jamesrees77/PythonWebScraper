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


# loop through amount of pages in query
print('starting')
class zooplaScraper():
    for i in range(17):

        source = requests.get('https://www.zoopla.co.uk/to-rent/property/bristol/?identifier=bristol&page_size=100&q=Bristol&search_source=to-rent&radius=0&price_frequency=per_month&pn=' + str(i)).text

        soup = BeautifulSoup(source, 'lxml')

        # loop through all classes of listing-results-wrapper
        for results in soup.find_all('div', class_='listing-results-wrapper'):

            right_results = results.find('div', class_='listing-results-right')
            left_results = results.find('div', class_='listing-results-left')

            # get number of beds
            try:
                number_beds = int(float(right_results.h3.find('span', class_='num-beds').text))
            except Exception as e:
                number_beds = None
            print("number of beds: ", number_beds)

            # get number of bathrooms
            try:
                number_baths = int(float(right_results.h3.find('span', class_='num-baths').text))
                print("number of bathrooms: ", number_baths)
            except Exception as e:
                number_baths = None
                print("number of bathrooms: ", number_baths)

            # rent price of property
            property_price = right_results.a.text
            try:
                property_rent = int(property_price[14:-17].replace(',', '')) / number_beds
            except Exception as e:
                property_rent = None


            print(property_rent)

            # get full address
            scraped_address = right_results.find('a', class_='listing-results-address').text
            print(scraped_address)
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
                property_image = left_results.div.a.img['data-src']
            except Exception as e:
                property_image = None

            print(property_image)
            description = right_results.find('p', class_='').text
            description = description.strip();
            print(description)

            term = 'student'

            if term in description.lower():
                is_student_property = True
            else:
                is_student_property = False

            print(is_student_property)

            url = 'https://www.zoopla.co.uk' + right_results.a.get('href')
            print('URL: ', url)

            # point to document called properties in firebase
            doc_ref = db.collection(u'properties').document()
            #  set object and push to firebase
            item = {
                u'property_id': doc_ref.id.decode('utf-8'),
                u'property_address': address,
                u'number_of_beds': number_beds,
                u'number_of_baths': number_baths,
                u'property_rent': property_rent,
                u'post_code': postcode,
                u'property_photo': property_image.decode('utf-8'),
                u'url': url.decode('utf-8'),
                u'original_site': 'Zoopla'.decode('utf-8'),
                u'is_student_property': is_student_property,
                u'description': description.encode("utf-8").decode('utf-8'),
            }
            print('')
            print('')
            print('')

            db.collection(u'properties').document(doc_ref.id).set(item)

            print(doc_ref.id)
            print('')
            print('')
            res = index.add_object(item)
            print "ObjectID=%s" % res["objectID"]

    #  run statement when all uploaded to firebase
    print('all properties successfully uploaded to firebase')

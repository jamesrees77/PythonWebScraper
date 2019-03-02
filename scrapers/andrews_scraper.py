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
class andrewsOnlinescraper():

    source = requests.get('https://www.andrewsonline.co.uk/rent/Bristol/properties/?orderBy=pricedesc&pageSize=100&letAgreed=true&letAgreed=false&distance=0&garden=False&baths=0&parking=False&character=False').text
    soup = BeautifulSoup(source, 'lxml')

    for results in soup.find_all('li', class_='search-result'):
        right_side = results.find('div', class_='right-side-column')

        property_price = right_side.find('div', class_='contact-column').h2.text
        property_price = int(property_price[2:-10].replace(',', ''))
        print(property_price)

        scraped_address = right_side.find('div', class_='details-column').a.h3.text
        address = scraped_address[:-4]
        print("address: ", address)
        # take last 4 characters of address for post code
        postcode = scraped_address[-4:]

        url = 'https://www.andrewsonline.co.uk' + right_side.find('div', class_='details-column').a.get('href')
        print('URL: ', url)
        # check if post code is only 3 characters - if it is remove whitespace at start.
        if postcode[0] == " ":
            postcode = postcode[-3:]
        print("postcode: ", postcode)

        title = right_side.find('div', class_='details-column').a.h2.text
        number_beds = int(float(title[0]))
        print('bedrooms: ', number_beds)

        description = right_side.find('div', class_='details-column').ul.text
        print('description: ', description)

        term = 'student'

        if term in description.lower():
            is_student_property = True
        else:
            is_student_property = False

        print('student?: ', is_student_property)

        try:
            property_image = results.find('div', class_='photo-column').find('div', class_='photo').a.img['src']
        except Exception as e:
            property_image = None

        print('property_photo', property_image)

        property_rent = property_price / number_beds
        print(property_rent)

        doc_ref = db.collection(u'andrews_online').document()
        #  set object and push to firebase
        item = {
            u'property_id': doc_ref.id.decode('utf-8'),
            u'property_address': address,
            u'number_of_beds': number_beds,
            u'property_rent': property_rent,
            u'post_code': postcode,
            u'property_photo': property_image.decode('utf-8'),
            u'url': url.decode('utf-8'),
            u'original_site': 'Andrews Online'.decode('utf-8'),
            u'is_student_property': is_student_property,
            u'description': description.decode('utf-8'),
        }

        db.collection(u'properties').document(doc_ref.id).set(item)

        print('')
        print('')
        print('')
        res = index.add_object(item)
        print "ObjectID=%s" % res["objectID"]

    #  run statement when all uploaded to firebase
    print('all properties successfully uploaded to firebase')

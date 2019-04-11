from bs4 import BeautifulSoup
import requests
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('/Users/james/Desktop/WebScraperProject/firestore/pythonscraperproject-firebase-adminsdk-2ujy0-749a94c698.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

# db.collection(u'properties').document().delete();
# loop through amount of pages in query
print('starting')
class rightMoveScraper():
    for i in range(0, 360, 24):
        source = requests.get('https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E219&index=' + str(i)).text

        soup = BeautifulSoup(source, 'lxml')

        # loop through all classes of listing-results-wrapper
        for results in soup.find_all('div', class_='propertyCard-wrapper'):

            right_results = results.find('div', class_='propertyCard-section')
            left_results = results.find('div', class_='propertyCard-images')

            # get number of beds
            try:
                number_beds = int(float(right_results.find('div', class_='propertyCard-details').a.h2.text[:1]))
            except Exception as e:
                number_beds = None

            # print("number of beds: ", int(float(number_beds)))


            # rent price of property
            property_price = results.find('div', class_='propertyCard-header').div.a.div.span.text
            property_price = int(property_price[1:-4].replace(',', ''))
            print("rent amount: ", property_price)

            # get full address
            scraped_address = right_results.find('div', class_='propertyCard-details').a.address.text
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
                property_image = left_results.div.a.img['src']
            except Exception as e:
                property_image = None

            print("Property Image: ", property_image)

            # point to document called properties in firebase
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
                u'description': description,
            }
            # Add to firebase
            db.collection(u'properties').document(doc_ref.id).set(item)

            print('')
            print('')
            print('')

            print(doc_ref.id)
            print('')
            print('')
            res = index.add_object(item)
            print "ObjectID=%s" % res["objectID"]

    #  run statement when all uploaded to firebase
    print('all properties successfully uploaded to firebase')

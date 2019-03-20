from bs4 import BeautifulSoup
from comapnies import companies
import requests
import csv
print(companies)
with open('persons.csv', 'wb') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['Company Number', 'Name'])
    for number in companies:
        print(number)
        source = requests.get('https://beta.companieshouse.gov.uk/company/' + number + '/officers').text
        soup = BeautifulSoup(source, 'lxml')
        print('here')

        names = []

        for i in range(31):
            for results in soup.find_all('div', class_='appointment-' + str(i)):
                officer_name = results.find('h2', class_='heading-medium').span.a.text
                print(officer_name)

                role = results.find('div', class_='grid-row').dl.dt.span.text

                if(role == 'Active'):
                    names.append(officer_name)


        filewriter.writerow([number, names])

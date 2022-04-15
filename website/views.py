from http.client import InvalidURL
from flask import Blueprint, render_template, request, flash
from urllib.request import urlopen
from urllib.error import *
import requests
from bs4 import BeautifulSoup

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    result_list = []
    if request.method == 'POST':
        search = request.form.get('search')
        result_list = getSearch(search)
        
    return render_template("home.html", results=result_list)

@views.route('/choose-cities', methods=['GET', 'POST', 'DELETE'])
def cities():
    if request.method == 'POST':
        city = request.form.get('city')

        # check if the city exists and add it to list
        city = city.replace(" ", "")
        url = "https://" + city + ".craigslist.org/"
        try:
            html = urlopen(url)
        except HTTPError as e:
            print("City does not exist", e)          
        except URLError as e:
            print("City does not exist", e)
        except InvalidURL as e:
            print("City does not exist", e)
        else:
            cityList.append(city)
            print('City added')

    # delete cities, not functioning currently
    if request.method == 'DELETE':
        deleteCities()
        print("delete")

    return render_template("cities.html", cities=getCities())

# city list stuff
cityList = []

def getCities():
    return cityList

def deleteCities():
    cityList.clear()
    print("clearing list")

class Result:
    title = ""
    price = ""
    location = ""
    photo = ""
    link = ""

    def __init__(self, title, price, location, photo, link):
        self.title = title
        self.price = price
        self.location = location
        self.photo = photo
        self.link = link
    
    def make_result(title,  price, location, photo, link):
        result = Result(title,  price, location, photo, link)
        return result

# function to search craigslist
def getSearch(search):
    result_list = []
    for city in cityList:
        print(city)
        URL = "https://" + city + ".craigslist.org/search/sss?query=" + search
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.findAll('li', class_='result-row')

        for result in results:
            # get the metadata for an ad
            title = result.find('h3').text
            price = result.find('span').text
            try:
                location = result.find('span', class_='result-hood').text
            except AttributeError as e:
                location = ""
            link = result.find('a').attrs['href']
            rpage = requests.get(result.find('a').attrs['href'])
            rsoup = BeautifulSoup(rpage.content, "html.parser")
            try:
                photo = rsoup.find('img').attrs['src']
            except AttributeError as e:
                photo = "No Image"
            result = Result(title, price, location, photo, link)
            result_list.append(result)

    return result_list
        



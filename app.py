from flask import Flask, request, jsonify
from urllib.request import Request, urlopen
import bs4 as bs
import urllib.request

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


# init app
app = Flask(__name__)
basedr = os.path.abspath(os.path.dirname(__file__))
# setup db
DB_USERNAME=os.environ.get('DB_USERNAME')
DB_PASSWORD=os.environ.get('DB_PASSWORD')
DB_ENDPOINT=os.environ.get('DB_ENDPOINT')
DB_NAME=os.environ.get('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_ENDPOINT + '/' + DB_NAME
#'sqlite:///' + os.path.join(basedr, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)
# Init marshmallow
ma = Marshmallow(app)

# Declare schema
class AnnouncementSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'link', 'photo')

class GuidesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'category', 'title', 'description', 'link', 'photo')

# Init schema
Announcement_Schema = AnnouncementSchema()
Announcements_Schema = AnnouncementSchema(many=True)

guide_schema = GuidesSchema()
guides_schema = GuidesSchema(many=True)

# Tables
class Announcements(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(500))
    description = db.Column(db.String(2000))
    link = db.Column(db.String(2000))
    photo = db.Column(db.String(2000))
  
    def __init__(self, title, description, link, photo):
        self.title = title
        self.description = description
        self.link = link
        self.photo = photo 

class Guides(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    category = db.Column(db.Integer)
    title = db.Column(db.String(500))
    description = db.Column(db.String(2000))
    link = db.Column(db.String(2000))
    photo = db.Column(db.String(2000))
  
    def __init__(self, category, title, description, link, photo):
        self.category = category
        self.title = title
        self.description = description
        self.link = link
        self.photo = photo 

# API Endpoints

@app.route('/india')
def indiaInfo():
        sauce = urllib.request.urlopen('https://www.mohfw.gov.in/')
        soup = bs.BeautifulSoup(sauce, 'html')

        table = soup.find(class_='content newtab')
        table_rows = table.find_all('tr')
        # driver = webdriver.Chrome()
        # driver.get('https://www.mohfw.gov.in/')
        # driver.find_element_by_xpath('//*[@id="cases"]/button').click()
        values = list()
        result = list()
        keys = ["id","State", "Confirmed(Indian)", "Confirmed(Foreigner)", "Cured/Migrated", "Death"]
        for tr in table_rows:
            td = tr.find_all('td')
            values = [i.text for i in td]
            my_dict = dict(zip(keys, values))
            result.append(my_dict)

        result.pop(0)    
        return jsonify(result)


@app.route('/', methods=['GET'])
def home_page():
       
    return '<h1>Deployed</h1>'


@app.route('/home', methods=['GET'])
def generalInfo():

        url = "http://www.worldometers.info/coronavirus/"
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        sauce = urllib.request.urlopen(req)
        soup = bs.BeautifulSoup(sauce, 'html.parser')
        
        total = soup.find_all('div', attrs={'class':'maincounter-number'})
        values= list()
        for t in total:
            values.append(t.text.strip())

        activeCases = soup.find(class_='number-table-main').text.strip()
        values.append(activeCases)
        closedCases = soup.find_all(class_='number-table-main')[1].text.strip()
        values.append(closedCases)
        keys = ["totalCases", "totalDeaths", "totalRecovered", "activeCases", "closedCases"]

        values = [int(i.replace(',', '')) for i in values]
        response = dict(zip(keys, values))
    
        return jsonify(response)


@app.route('/announcements', methods=['GET'])
def get_announcements():

    all_announcements = Announcements.query.all()
    result = Announcements_Schema.dump(all_announcements)
   
    return jsonify({"Announcements" : result})


@app.route('/guide', methods=['GET'])
def get_guidance():

    all_guidance = Guides.query.all()
    result = guides_schema.dump(all_guidance)
   
    return jsonify({"Guidance" : result})    

@app.route('/notifications', methods=['GET'])
def get_notifications():

    sauce = urllib.request.urlopen('https://www.mygov.in/covid-19/')
    soup = bs.BeautifulSoup(sauce, 'html.parser')
        
    notifications = soup.find_all(class_='push_notification_list')
    dic = dict()
    keys = ["title","image", "link"]

    for noti in notifications:
        noti = soup.find_all(class_='push_title')
        image = soup.select('.push_image img')
        ref = soup.select('.push_row a')

    notificationTitle = [i.text for i in noti]
    notificationImage = [j['src'] for j in image]
    notificationRef = [i['href'] for i in ref]
    response=list()
    values = list()
    
    for i in range(len(notificationRef)):
        values.append(notificationTitle[i])
        values.append(notificationImage[i])
        values.append(notificationRef[i])
        my_dict = dict(zip(keys, values))
        response.append(my_dict)
        values.clear()
    
    return jsonify(response)    


@app.route('/world', methods=['GET'])
def worldInfo():

    url = "http://www.worldometers.info/coronavirus/"
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    sauce = urllib.request.urlopen(req)
    soup = bs.BeautifulSoup(sauce, 'html')

    table = soup.find('table', id="main_table_countries_today")
    table_rows = table.find_all('tr')
    count = 0
    values = list()
    result = list()
    keys = ["country","totalCases", "newCases", "totalDeaths", "newDeaths", "totalRecovered", "activeCases", "critical", "totalCases1MPop", "totalDeaths1MPop"]
    for tr in table_rows:
        if count == 0:
            count += 1
            continue
        td = tr.find_all('td')
        values = [i.text.strip() for i in td]
        my_dict = dict(zip(keys, values))
        if my_dict["totalCases"] != "":
            my_dict['totalCases'] = int(my_dict['totalCases'].replace(',',''))
        else:
            my_dict['totalCases'] = 0
        if my_dict['totalDeaths'] != "":
            my_dict['totalDeaths'] = int(my_dict['totalDeaths'].replace(',',''))
        else: 
            my_dict['totalDeaths'] = 0    
        if my_dict['totalRecovered'] != "":
            my_dict['totalRecovered'] = int(my_dict['totalRecovered'].replace(',',''))
        else: 
            my_dict['totalRecovered'] = 0    
        result.append(my_dict)

    result.pop(0)    
    return jsonify(result)

# Run Server
if __name__ == '__main__':
    app.run(debug=True)
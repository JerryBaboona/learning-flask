from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
import pdb
import geocoder
import urllib2
import json

GOOGLE_MAPS_API_KEY = "AIzaSyAXcPQi2JuUTkjR6Pjzz2HIHetqrQLPZIA"

db = SQLAlchemy()

# Data model for the users tale
class User(db.Model):
    __tablename__ ="users"
    uid= db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    pwdhash = db.Column(db.String(54))

    # Build a custom constructor to ensure all properties (row values)
    # are stored exactly as we want them - we don't take any old junk!
    # E.g. we want our first names and last names to have a capitalised
    # first letter and our email to be all lower case
    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

class Place(object):
    def meters_to_walking_time(self, meters):
        # 80 meters is one minute of walking time
        return int(meters / 80)

    def wiki_path(self, slug):
        return urllib2.urlparse.urljoin("http://en.wikipedia.org.wiki/", slug.replace(" ", "_"))

    def address_to_latlng(self, address):
        g = geocoder.google(address, key=GOOGLE_MAPS_API_KEY)
        return (g.lat, g.lng)

    def query(self, address):
        lat, lng = self.address_to_latlng(address)
        print lat, lng

        query_url = ("https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gsradius=5000&gscoord="
        + str(lat) + "%7C" + str(lng) + "&gslimit=20&format=json")
        print query_url
        g = urllib2.urlopen(query_url)
        results = g.read()
        g.close()
        data = json.loads(results)
        print data

        places = []
        if "query" in data.keys():
            for place in data["query"]["geosearch"]:
                name = place["title"]
                meters = place["dist"]
                lat = place["lat"]
                lng = place["lon"]

                wiki_url = self.wiki_path(name)
                walking_time = self.meters_to_walking_time(meters)

                d = {
                    "name": name,
                    "url": wiki_url,
                    "time": walking_time,
                    "lat": lat,
                    "lng": lng
                }

                places.append(d)

        return places

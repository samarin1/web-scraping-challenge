from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)


app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
#mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# connect to mongo db and collection
@app.route("/")
def index():
    mars_results = mongo.db.mars.find_one()
    return render_template("index.html", mars_results = mars_results)

@app.route("/scrape_mars")
def scrape():
    mars_results = mongo.db.mars_results
    mars_data = scrape_mars.scrape()
    mars_results.mongo.db.collection.update({}, mars_data, upsert=True)
    return "Scraping Successful"

if __name__ == "__main__":
    app.run(debug=True)
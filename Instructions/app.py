from flask import Flask, render_template,redirect
from flask_pymongo import PyMongo
import scraping_mars


app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config['MONGO_URI']= "mongodb://localhost:27017/mars_app"
mongo=PyMongo(app)

# Set Up Routes
@app.route("/")
def index():
    mars=mongo.db.mars.find_one()
    return render_template('index.html', mars=mars)

@app.route("/scrape")
def scrape():
    print("I am scraping")
    mars=mongo.db.mars

    #holds newly scraped data, referencing scrape_all() function in scraping.py file
    mars_data=scraping_mars.scrape_all()
    print("=====================")
    print(mars_data)
    print("=====================")
    mars.update_one({}, {"$set": mars_data}, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run()

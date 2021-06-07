from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)


app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)

# Create route that renders index.html template and finds documents from mongo
@app.route("/")
def home(): 

    # Find data
    mars_news = mongo.db.mars_news.find_one()

    # Return template and data
    return render_template("index.html", mars_data=mars_news)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape(): 

    # Run scrapped functions
    mars_news = mongo.db.mars_news
    mars_data = scrape_mars.scrape_mars_news()
    mars_data = scrape_mars.scrape_mars_image()
    mars_facts= scrape_mars.scrape_mars_facts()
    mars_data = scrape_mars.scrape_mars_hemispheres()
    mars_news.update({}, mars_data, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)

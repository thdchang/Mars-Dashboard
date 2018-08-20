from flask import Flask, render_template, redirect, url_for, jsonify
import pymongo
import scrape_mars

#create instance of flask app
app = Flask(__name__)

#using flask pymong to set up mongo connection
conn = "mongodb://localhost:27017"

#create mongodb client in python
client = pymongo.MongoClient(conn)

#create a mars_db database in mongodb 
db = client.mars_db




#create route to render webpage with mars data
@app.route('/')
def index():
    
    #store mongodb mars_data document into a list 
    mars_data = list(db.mars_data.find())

    #latest news title and paragraph variables
    news_title = mars_data[0]["mars_news"][0]
    news_p = mars_data[0]["mars_news"][2]

    #jpl featured image url 
    jpl_url = mars_data[0]["jpl_featured_image_url"]

    #mars weather tweet
    tweet = mars_data[0]["weather_tweet"]

    #hemisphere image title and url
    title_1 = mars_data[0]["hemisphere_image"][0]["title"]
    url_1 = mars_data[0]["hemisphere_image"][0]["img_url"]
    title_2 = mars_data[0]["hemisphere_image"][1]["title"]
    url_2 = mars_data[0]["hemisphere_image"][1]["img_url"]
    title_3 = mars_data[0]["hemisphere_image"][2]["title"]
    url_3 = mars_data[0]["hemisphere_image"][2]["img_url"]
    title_4 = mars_data[0]["hemisphere_image"][3]["title"]
    url_4 = mars_data[0]["hemisphere_image"][3]["img_url"]


    return render_template('index.html', news_title=news_title, news_p=news_p, jp_url=jpl_url, tweet=tweet, url_1=url_1, title_1=title_1, url_2=url_2, title_2=title_2, url_3=url_2, title_3=title_2, url_4=url_4, title_4=title_4)



# create route that scrape's Mars related data 
@app.route('/scrape')
def webscrape():
    
    #drop any documents inside mars_data collection
    db.mars_data.drop()

    #call scrape function in scrape_mars.py
    mars_data = scrape_mars.scrape()

    #insert mars data into mongodb mars_db 
    db.mars_data.insert_one(mars_data)

    #return back to homepage with web-scraped mars data updated
    return redirect(url_for('index'))


#initialize flask app
if __name__ == "__main__":
    app.run(debug=True)
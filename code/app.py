from flask import Flask, jsonify, request, redirect, render_template
import requests, json
import sqlite3

app = Flask(__name__)

search_tag = ""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/album', methods=['POST'])
def create_album():
    global search_tag

    search_tag = request.form['tag']
    get_photos()
    return render_template('index.html')

@app.route('/photos')
def get_photos():

    #tags = albums[0]['name']
    print(f'Looking for {search_tag}')

    if search_tag != "":
        response = get_flickr_data(search_tag)
        photos = response['photos']['photo']
        # size : some valid values s,m,b for small, medeium, large respectively
        size = 'm'
        image_dict = {}
        for photo in photos:
            owner = photo['owner']
            id = photo['id']
            farm = photo['farm']
            server = photo['server']
            secret = photo['secret']
            #url = f'https://www.flickr.com/photos/{owner}/{id}'
            #print(url)
            image_dict[id] = f"https://farm{farm}.staticflickr.com/{server}/{id}_{secret}_{size}.jpg"

        create_tables(image_dict)

        return jsonify(image_dict)
    else:
        return jsonify({'no_images':'true'})


def get_flickr_data(tags_string):
    proxies = {} 
    api_key = ''

    baseurl = 'https://api.flickr.com/services/rest'
    flickr_params = {
        'api_key':api_key,
        'tags': tags_string,
        'media' :'photos',
        'tag_mode':'all',
        'method':'flickr.photos.search',
        'format': 'json',
        'per_page':12,
        'nojsoncallback':1,
        'extras':'url_o'
    }

    flickr_resp = requests.get(baseurl, params=flickr_params,proxies=proxies)
    print(flickr_resp.url)
    return(flickr_resp.json())

def create_tables(data):
    # connect to the database
    conn = sqlite3.connect('database.sqlite')
    # create a cursor => handle to access the db
    cur = conn.cursor()

    # Create a Table if it doesn't already exist
    create_table = "CREATE TABLE IF NOT EXISTS Images(image_id INTEGER, url TEXT)"
    cur.execute(create_table)

    # write to the table
    for k in data.keys():
        attributes = (k, data[k])
        cur.execute('SELECT image_id FROM Images WHERE image_id = ?', (k,))
        row = cur.fetchone()
        if row is None:
            insert_image = "INSERT INTO Images(image_id, url) VALUES(?,?)"
            cur.execute(insert_image,attributes)

    # retrieve items from table
    sqlstr = 'SELECT image_id, url FROM Images'

    for row in cur.execute(sqlstr):
        print(f'{row[0]} => {row[1]}')

    # close database
    conn.commit()
    conn.close()

if __name__ == '__main__':
    app.run(port=5000)

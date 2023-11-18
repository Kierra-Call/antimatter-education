from flask import render_template, redirect, request, session
from flask_app import app
import requests

@app.route('/')
def get_apod_index():
    apod_url = "https://api.nasa.gov/planetary/apod"
    api_key = "API KEY HERE"
    params = {
        "api_key": api_key,
        "hd": True,
    }
    response = requests.get(apod_url, params=params)
    if response.status_code == 200:
        data = response.json()
        info = {
        'date' : data["date"],
        'title' : data["title"],
        'explanation' : data["explanation"],
        'hd_image_url' : data.get("hdurl"),
        'image_url' : data["url"]
        }
        print(info)
        return render_template('index.html', info=info)
    else:
        print(f"API request failed with status code {response.status_code}")
        return redirect('/')

@app.route('/gallery')
def gallery_search():
    return render_template('gallery.html')

@app.post('/gallery/search')
def gallery():
    ivl_url = "https://images-api.nasa.gov/search?q="
    search_query = request.form['search-gallery']
    params = {
        "q": search_query,
        "media_type": "image,video"  # Search for both images and videos
    }

    try:
        response = requests.get(ivl_url, params=params)

        if response.status_code == 200:
            search = response.json()
            info = search['collection']['items']
            print(info)
            return render_template('gallery.html', info=info)

        else:
            print("Failed to retrieve search results. Status code:", response.status_code)

    except requests.exceptions.RequestException as e:
        print("Failed to connect to the NASA IVL API:", e)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', e=e), 404





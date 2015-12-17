import json
import bs4
import requests
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def main():
    root_url = 'http://www.randomsimpsonsquote.com'
    response = requests.get(root_url)
    soup = bs4.BeautifulSoup(response.text,'lxml')
    #character = soup.select('#main > img')[0]['src']
    quote = soup.select('#main > blockquote')[0]
    return render_template('index.html', quote=quote)


@app.route("/seasons/<season>")
def seasons(season):
      with open('static/data/Season_{0}.json'.format(season)) as f:
          db = json.load(f)
          return render_template('seasons.html', dict=db['Episodes'])

@app.route("/playback")
def playback():
    url = request.args['url']
    if 'cdn.php?ref=' in url:
        print url
        return render_template('video.html', url=url)
    elif 'view.php?ref=' in url:
        return render_template('video.html', url=url)
    else:
        return render_template('video.html', url='')



@app.route('/video_download')
def user_download():
    url = request.args['url']  # user provides url in query string
    r = requests.get(url)

    # write to a file in the app's instance folder
    # come up with a better file name
    with app.open_instance_resource('downloaded_file', 'wb') as f:
        f.write(r.content)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run()

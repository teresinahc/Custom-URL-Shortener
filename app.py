from flask import Flask, render_template, request, redirect
import requests

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

database = client['custom_url']

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')


@app.route('/shortener', methods=['GET', 'POST'])
def short():
    if request.method == 'POST':
        longurl = request.form['longurl']
        custom = request.form['custom']
        if not longurl and custom:
            return 'Error <script>alert("Invalid Credentials");</script>'
        if longurl.startswith("http://"):
            longurl = longurl.replace("http://", "")
        elif longurl.startswith("https://"):
            longurl = longurl.replace("https://", "")

        longurl = str("https://"+str(longurl))

        try:
            r = requests.get(longurl)
            if r.status_code == 200:
                pass
            else:
                return 'Invalid URL <script>alert("Invalid URL");</script>'
        except ValueError:
            return """Invalid URL <script>alert("Invalid URL");
            var meta = document.createElement('meta');
            meta.httpEquiv = "REFRESH";
            meta.content = "0;URL=/";
            document.getElementsByTagName('head')[0].appendChild(meta);
            </script>"""

        data = {'longurl': longurl, 'custom': custom}
        custom_url = database.urls.insert(data)
        print(custom_url)

        url = "http://127.0.0.1:5000/shortener/"+custom
        print(url)
        return 'Live at <a target="_blank" href="'+url+'">'+url+'</a>'
    return ""


@app.route('/shortener/<custom>', methods=['GET', 'POST'])
def final(custom):
    data = database.urls.find({'custom': (str(custom))})
    print(data)
    for return_this in data:
        return_this = return_this.get('longurl')

    return redirect(return_this, code=302)


if __name__ == '__main__':
    app.run(port=5000)

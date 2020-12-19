from flask import Flask, render_template
import requests, json
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

# better to replace this with your own key from https://api.nasa.gov/
my_key = 'D8FJrAVDcE5RHJ29uwD5lRftLXMDO6Tw3iGnj19V'

payload = {
  'api_key': my_key,
  'start_date': '2020-11-05',
  'end_date': '2020-11-08'
}

endpoint = 'https://api.nasa.gov/planetary/apod'

endpoint2 = 'http://www.boredapi.com/api/activity/'

@app.route('/')
def main():
    try:
        #r = requests.get(endpoint, params=payload)
        r = requests.get(endpoint)
        data = r.json()
        print(data)
    except:
        print('please try again')
    return render_template('boredapi.html', data=data)
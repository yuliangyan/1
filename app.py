from flask import Flask, request,jsonify
from cassandra.cluster import Cluster
import requests

cluster = Cluster(['cassandra'])
session = cluster.connect()
app = Flask(__name__)

#to test if there is anymistake in google shell
@app.route('/')
def hello():
    name = request.args.get("name","World")
    return('<h1>Hello, {}!</h1>'.format(name))


@app.route('/predict', methods=['GET'])
def gett():
    air_url_template ='https://api.breezometer.com/pollen/v2/forecast/daily?lat=30.003362&lon=-95.594209&days=3&key={YOUR_API_KEY}'
    KEY = '918f06be8ff145e6bcd4422faea391c4'
    air_url = air_url_template.format(YOUR_API_KEY = KEY)
    resp = requests.get(air_url)

    if resp.ok:
        cc_url = resp.json()
    else:
        print(resp.reason)
    
    categories = {categ["date"]:categ["types"]["tree"]["index"]["value"] for categ in cc_url["data"]}
    #write in the data crabbed from the API
    for i in categories:
        rows = session.execute( """insert into air.stats(date,value) values('{}',{})""".format(i,categories[i]))
    return('<h1>Predict values have been created.</h1>')

@app.route('/predict/tree/<date>')
def profile(date):
    #filter by date
    rows = session.execute( """select * from air.stats where date = '{}' allow filtering""".format(date))
    for k in rows:
        return jsonify(k)
        #return('<h1>The forecast pollen condition value of {} is {}!</h1>'.format(date,k.value))
    return('<h1>Not included!</h1>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080,debug = True)

from firebase import firebase
from flask import Flask
import pandas as pd

from get_recs import get_recs

app = Flask(__name__)

firebase = firebase.FirebaseApplication('https://binary-bird-default-rtdb.europe-west1.firebasedatabase.app/', None)


@app.route("/")
def goods():
    goods = firebase.get('/goods', None)
    goods = pd.DataFrame(goods)
    response = get_recs(goods)
    return str(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

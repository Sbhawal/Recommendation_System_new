from flask import Flask, render_template, request
from flask import json

import pandas as pd
import numpy as np
import pickle
import scipy
import requests


RAPIDAPI_KEY  = "f0b674f502msh2fd7bf7d01e3e9bp127b2ajsn16ff895b22f0"
RAPIDAPI_HOST =  "imdb8.p.rapidapi.com"

url = "https://imdb8.p.rapidapi.com/title/get-overview-details"

headers = {
    'x-rapidapi-host': RAPIDAPI_HOST,
    'x-rapidapi-key': RAPIDAPI_KEY
    }


def return_details(imdbID):
    details = {}
    index = df[df['imdb_id']==imdbID].index.values
    details['imdb_id'] = df.at[int(index),'imdb_id']
    details['image_url'] = df.at[int(index),'image_url']
    details['title'] = df.at[int(index),'title']
    try:
        try:
            details['summary'] = df.at[int(index),'summary']
        except:
            details['summary'] = df.at[int(index),'story']
    except:
        details['summary'] = "Unfortunately no Summary Found !"
    if len(details['summary']) > 445:
        details['summary'] = details['summary'][:445] + "..."
    details['rating'] = df.at[int(index),'rating']
    details['genres'] = (df.at[int(index),'genres']).replace(",",", ")     
    return details 



sig1 = sig1 = np.load('sugg_data.npy')
df = pd.read_pickle("title_list.pkl")
index = pd.Series(df.index, index = df.title).drop_duplicates()

def recommend(title, sig=sig1):
    idx = index[title]
    scores = list(enumerate(sig1[idx]))
    scores = sorted(scores, key=lambda x:x[1], reverse=True)
    scores= scores[1:11]
    mov_index = [i[0] for i in scores]
    return df.iloc[mov_index]['imdb_id']



# def to_dict(rec_list):
# 	a = return_details(rec_list[0])
# 	return {1 : a ,2 : a ,3 : a ,4 : a ,5 : a}


def to_dict(rec_list):
	return {1 : return_details(rec_list[0]),
    2 : return_details(rec_list[1]),
    3 : return_details(rec_list[2]),
    4 : return_details(rec_list[3]),
    5 : return_details(rec_list[4]),
    6 : return_details(rec_list[5]),
    7 : return_details(rec_list[6]),
    8 : return_details(rec_list[7]),
    9 : return_details(rec_list[8]),
    10 : return_details(rec_list[9]), }




app = Flask(__name__)


@app.route('/')
def home():
	return render_template('index.html')


@app.route('/recommendations', methods=["POST"])
def recommendations():
	series = request.form['submit-form']
	rec = recommend(series).tolist()
	return render_template('recs.html', data=to_dict(rec))



# @app.route('/print', methods=["POST"])
# def print():
# 	series = request.form['a']
# 	rec = recommend(series).tolist()
# 	return to_dict(rec)



if __name__ == "__main__":
	app.run(debug=True)

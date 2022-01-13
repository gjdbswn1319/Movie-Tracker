from flask import Flask, render_template, url_for, request
from tmdbv3api import *
import pandas as pd

tmdb = TMDb()
tmdb.api_key = 'fcdb87b8e3a4e9fd5a5686f6bcceba17'

movie = Movie()
discover = Discover()
person = Person()
genres = Genre()

movie_log = pd.read_csv('/Users/EllyHur/Desktop/interview/log.csv', sep='|')

app = Flask(__name__)

def getDirector(title):
	movie_title = movie.search(title)
	first_result = movie_title[0]
	credits = movie.credits(first_result.id)
	for credit in credits.crew:
		if credit['job'] == 'Director':
			return credit.name

def getImage(title):
	movie_title = movie.search(title)
	first_result = movie_title[0]
	detail = movie.details(first_result.id)
	return 'https://image.tmdb.org/t/p/original' + detail.poster_path

@app.route('/')
@app.route('/home')


def home():
	return render_template('index2.html')

@app.route('/result', methods = ['POST', 'GET'])
def result():
	director = ''
	output = request.form.to_dict()
	director = getDirector(output['movie_title'])
	poster = getImage(output['movie_title'])
	return render_template('index2.html', director = director, poster = poster)


if __name__ == "__main__":
	app.run(debug=True)




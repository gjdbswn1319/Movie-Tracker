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
	director = []
	movie_title = movie.search(title)
	#first_result = movie_title[0]
	for result in movie_title:
		credits = movie.credits(result.id)
	#credits = movie.credits(first_result.id)
		for credit in credits.crew:
			if credit['job'] == 'Director':
				director.append(credit.name)
	return director

def getImage(title):
	path = []
	movie_title = movie.search(title)
	for result in movie_title:
		detail = movie.details(result.id)

		path.append('https://image.tmdb.org/t/p/original' + str(detail.poster_path))
	#first_result = movie_title[0]
	#detail = movie.details(first_result.id)
	#return 'https://image.tmdb.org/t/p/original' + detail.poster_path
	return path

@app.route('/')
@app.route('/home')


def home():
	return render_template('index2.html')

@app.route('/result', methods = ['POST', 'GET'])

def result():
	director = []
	poster = []
	output = request.form.to_dict()
	director = getDirector(output['movie_title'])
	poster = getImage(output['movie_title'])
	
	return render_template('index2.html', director = director, poster = poster)


if __name__ == "__main__":
	app.run(debug=True)

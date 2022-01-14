from flask import Flask, render_template, url_for, request, Response, redirect
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

def getID(title):
	movie_title = movie.search(title)

def getDetail(movie_id, attribute):
	detail = movie.details(movie_id)
	result = detail[attribute]
	return result

def getDirector(title):
	director = []
	print(title)
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
		temp = []
		temp.append('https://image.tmdb.org/t/p/original' + str(detail.poster_path))
		temp.append(result.id)
		path.append(temp)
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
	print(output)
	director = getDirector(output['movie_title'])
	poster = getImage(output['movie_title'])
	
	return render_template('movie_list.html', director = director, poster = poster)

@app.route('/movieInfo', methods = ['POST', 'GET'])
def movieInfo():
	output = request.form.to_dict()
	movieID = output['movie_id']
	title = getDetail(movieID, 'title')
	genre = getDetail(movieID, 'genres')
	overview = getDetail(movieID, 'overview')

	return render_template('movieInfo.html', title=title, genre=genre, overview=overview)
	


if __name__ == "__main__":
	app.run(debug=True)

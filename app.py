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


def getCountryByID(detail):
	movie_country = ''
	for i in range(len(detail.production_countries)):
		if i == len(detail.production_countries) - 1:
			movie_country = movie_country + detail.production_countries[i].name
		else:
			movie_country = movie_country + detail.production_countries[i].name + ', '
	return movie_country

def getCastByID(credits):
	casts = ''
	for i in range(len(credits.cast)):
		if i == len(credits.cast) - 1:
			casts = casts + credits.cast[i].name
		else: 
			casts = casts + credits.cast[i].name + ', '
	return casts

def getDetailByID(movie_id, attribute):
	genre = ''
	detail = movie.details(movie_id)
	credits = movie.credits(movie_id)
	if attribute == 'genres':
		for i in range(len(detail.genres)):
			if i == len(detail.genres) - 1:
				genre = genre + detail.genres[i].name
			else:
				genre = genre + detail.genres[i].name + ', '
		return genre
	if attribute == 'country':
		return getCountryByID(detail)
	if attribute == 'director':
		return getDirectorByID(credits)
	if attribute == 'poster':
		return getImageByID(detail)
	if attribute == 'cast':
		return getCastByID(credits)
	result = detail[attribute]
	return result

def getDirectorByID(credits):
	director = ''
	for credit in credits.crew:
		if credit['job'] == 'Director':
			if director == '':
				director = credit.name
			else:
				director = director + ', ' + credit.name
	return director

def getImageByID(detail):
	path = 'https://image.tmdb.org/t/p/original' + str(detail.poster_path)
	return path

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
	title = getDetailByID(movieID, 'title')
	genre = getDetailByID(movieID, 'genres')
	overview = getDetailByID(movieID, 'overview')
	director = getDetailByID(movieID, 'director')
	poster = getDetailByID(movieID, 'poster')
	country = getDetailByID(movieID, 'country')
	date = getDetailByID(movieID, 'release_date')
	casts = getDetailByID(movieID, 'cast')
	runtime = getDetailByID(movieID, 'runtime')


	return render_template('movieInfo.html', title=title, genre=genre, overview=overview, 
		director=director, poster=poster, country=country, date=date, casts=casts, runtime=runtime)
	


if __name__ == "__main__":
	app.run(debug=True)

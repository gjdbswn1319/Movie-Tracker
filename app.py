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

def searchByDirector(name):
	director_name = person.search(name, {'language': 'kr'})
	first_result = director_name[0]
	movies = discover.discover_movies({'with_crew': first_result.id})
	return movies


def getCountryByID(detail):
	movie_country = []
	for country in detail.production_countries:
		movie_country.append(country.name)
	return movie_country

def getCastByID(credits):
	casts = []
	for cast in credits.cast:
		casts.append(cast.name)
	return casts

def getDetailByID(movie_id, attribute):
	genre = []
	detail = movie.details(movie_id)
	credits = movie.credits(movie_id)
	if attribute == 'genres':
		for g in detail.genres:
			genre.append(g.name)
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
	director = []
	for credit in credits.crew:
		if credit['job'] == 'Director':
			director.append(credit.name)
	return director

def getImageByID(detail):
	path = 'https://image.tmdb.org/t/p/original' + str(detail.poster_path)
	return path

def findMovie(title):
	result = []
	movie_title = movie.search(title)
	for mv in movie_title:
		temp = []
		credits = movie.credits(mv.id)
		detail = movie.details(mv.id)
		director = ''
		for credit in credits.crew:
			if credit['job'] == 'Director':
				if director == '':
					director = credit.name
				else:
					director = director + ', ' + credit.name
		temp.append(director)
		path = 'https://image.tmdb.org/t/p/original' + str(detail.poster_path)
		temp.append(path)
		temp.append(mv.id)
		temp.append(mv.title)
		result.append(temp)
	return result

def popularMovie():
	pm = movie.popular()
	return pm

@app.route('/')



@app.route('/home')


def home():
	return render_template('index2.html')

@app.route('/result', methods = ['POST', 'GET'])

def result():
	director = []
	poster = []
	output = request.form.to_dict()
	result = findMovie(output['movie_title'])
	
	return render_template('movie_list.html', result=result)
	#result[0] = director/ result[1] = poster_path/ result[2] = movie_id/ result[3] = movie_title

@app.route('/movieInfo', methods=['POST', 'GET'])
def movieInfo():
	output = request.form.to_dict()
	print('############################')
	print(output)
	print('############################')
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
	rate = getDetailByID(movieID, 'vote_average')


	return render_template('movieInfo.html', title=title, genre=genre, overview=overview, 
		director=director, poster=poster, country=country, date=date, casts=casts, 
		runtime=runtime, rate=rate)

@app.route('/showinfo', methods=['POST', 'GET'])	
def showinfo():
	output = request.values.get('gfjlsdf')
	output1 = request.form.get('sfsdffsdfd')
	output2 = request.args.get('ddfsdge')
	print('***************************')
	print(output)
	print(output1)
	print(output2)
	print('***************************')

	return render_template('showinfo.html')

@app.route('/movieOfTheWeek', methods=['POST', 'GET'])
def movieOfTheWeek():
	popular_movie = popularMovie()
	return render_template('movieOfTheWeek.html', popular=popular_movie)



if __name__ == "__main__":
	app.run(debug=True)

from tmdbv3api import *
import csv
import pandas as pd
import plotly.express as px

tmdb = TMDb()
tmdb.api_key = 'fcdb87b8e3a4e9fd5a5686f6bcceba17'

movie = Movie()
discover = Discover()
person = Person()
genres = Genre()



def readFile(fileName):
	movie_log = pd.read_csv(fileName, sep='|')
	pd.set_option('display.max_rows', len(movie_log))
	return movie_log

def searchByDirector(name):
	director_name = person.search(name, {'language': 'kr'})
	first_result = director_name[0]
	movies = discover.discover_movies({'with_crew': first_result.id})
	return movies


def findID(movie_log):
	for mv in movie_log['Title']:
		result = movie.search(mv, {'language': 'kr'})
		for i in range(len(result)):
			credits = movie.credits(result[i].id)
			director=''
			for credit in credits.crew:
				if credit['job'] == 'Director':
					director = credit.name
			print(result[i].title, result[i].id, director)
		print()
		print()

def searchByDirector(name):
	director_name = person.search(name)
	first_result = director_name[0]
	movies = discover.discover_movies({'with_crew': first_result.id})
	for m in movies:
		print(m.title, m.id)

def findDirector(movie_log):
	director_log = []
	for movie_id in movie_log['ID']:
		credits = movie.credits(movie_id)
		director = ''
		for credit in credits.crew:
			if credit['job'] == 'Director':
				if director == '':
					director = credit.name
				else:
					director = director + ', ' + credit.name
		director_log.append(director)
	movie_log['Director'] = director_log

def findGenre(movie_log):
	genre_log = []
	for movie_id in movie_log['ID']:
		detail = movie.details(movie_id)
		movie_genre = ''
		for genre in detail.genres:
			if movie_genre == '':
				movie_genre = genre.name
			else:
				movie_genre = movie_genre + ', ' + genre.name
		genre_log.append(movie_genre)
	movie_log["Genre"] = genre_log

def findCountry(movie_log):
	country_log = []
	for movie_id in movie_log['ID']:
		detail = movie.details(movie_id)
		movie_country = ''
		for country in detail.production_countries:
			if movie_country == '':
				movie_country = country.name
			else:
				movie_country = movie_country + ', ' + country.name
		country_log.append(movie_country)
	movie_log['Country'] = country_log

def findYear(movie_log):
	year_log = []
	for movie_id in movie_log['ID']:
		detail = movie.details(movie_id)
		date = detail.release_date
		yearMonthDate = date.split('-')
		year = yearMonthDate[0]
		year_log.append(year)
	movie_log['Year'] = year_log

def histogram(movie_log, data):
	fig = px.histogram(pd.Series(movie_log[data].str.split(', ').sum())).update_xaxes(categoryorder='total descending')
	fig.show()

def count(movie_log, data):
	return pd.Series(movie_log[data].str.split(', ').sum()).value_counts()


#def findID(movie_log):
	#for mv in movie_log['제목']:
		#result = movie.search(mv, {'language': 'kr'})
		#for i in range(len(result)):
			#print(result[i].title, result[i].id, result[i].overview)

#def findID(movie_log):
	#for mv, d in movie_log.itertuples(index=False):
		#movie_result = movie.search(mv, {'language': 'kr'})
		#director = d
		#for dm in searchByDirector(director):
			#for mr in movie_result:
				#if mr.title == dm.title:
					#print(mr.title, mr.id)
		#print()
		


def main():
	movie_log = readFile('log.csv')
	findDirector(movie_log)
	findGenre(movie_log)
	findCountry(movie_log)
	findYear(movie_log)
	histogram(movie_log, 'Director')
	histogram(movie_log, 'Genre')
	histogram(movie_log, 'Country')
	#print(count(movie_log, 'Director'))
	#print(count(movie_log, 'Genre'))
	#print(count(movie_log, 'Country'))


	




if __name__ == '__main__':
	main()
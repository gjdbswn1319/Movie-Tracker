
from tmdbv3api import *

tmdb = TMDb()
tmdb.api_key = 'fcdb87b8e3a4e9fd5a5686f6bcceba17'

movie = Movie()
discover = Discover()
person = Person()
genres = Genre()


##########################################################################################################
##  SEARCH FUNCTIONS																					##
##  1. BY TITLE - TAKES THE FIRST RESULT AND SHOWS GENRE, DIRECTOR, CAST, AND OVERVIEW OF THE MOVIE     ##
##  2. BY DIRECTOR - SHOWS THE TITLE OF THE DIRECTOR'S MOVIES IN THE ORDER OF POPULARITY                ##
##  3. BY CAST - SHOWS THE TITLE OF THE CAST'S MOVIES IN THE ORDER OF POPULARITY                        ##
##  4. BY RELEASE YEAR - SHOWS THE TITLE OF MOVIES RELEASED IN THE YEAR IN THE ORDER OF POPULARITY      ##
##  5. BY GENRE - SHOWS THE TITLE OF MOVIES OF THE GENRE IN THE ORDER OF POPULARITY                     ##
##########################################################################################################

def searchByTitle(title):
	movie_title = movie.search(title)
	first_result = movie_title[0]

	# PRINTS MOVIE TITLE
	print('MOVIE TITLE: ', first_result.title)

	# PRINTS MOVIE GENRE
	detail = movie.details(first_result.id)
	print('GENRE: ', end='')
	for genre in detail.genres:
		print(genre.name, end=', ')
	print()

	# PRINTS MOVIE DIRECTOR
	print('DIRECTOR: ', end='')	
	credits = movie.credits(first_result.id)
	for credit in credits.crew:
		if credit['job'] == 'Director':
			print(credit.name)

	# PRINTS MOVIE CASTS
	print('CAST: ', end='')
	for i in range(5): # Prints up to 5 casts
		if i < len(credits.cast):
			print(credits.cast[i].name, end=', ')
	print()

	# PRINTS MOVIE OVERVIEW
	print("OVERVIEW: ", detail.overview)


def searchByDirector(name):
	director_name = person.search(name)
	first_result = director_name[0]
	movies = discover.discover_movies({'with_crew': first_result.id})
	for m in movies:
		print(m.title)


def searchByCast(name):
	cast_name = person.search(name)
	first_result = cast_name[0]
	movies = discover.discover_movies({'with_cast': first_result.id})
	for m in movies:
		print(m.title)


def searchByYear(year):
	movies = discover.discover_movies({'year': year})
	for m in movies:
		print(m.title)


def searchByGenre():

	# PRINTS ALL AVAILABLE MOVIE GENRE OPTIONS
	print("AVAILABLE MOVIE GENRES: ")
	movie_genres = genres.movie_list()
	for mg in movie_genres:
		print(mg.name)
	print()

	genre_id = '0'

	# FINDS THE GENRE ID THE USER ENTERED
	value = input("ENTER GENRE: ")
	for mg in movie_genres:
		if value.lower() == mg.name.lower():
			genre_id = mg.id

	# PRINTS MOVIES OF THE GENRE
	movies = discover.discover_movies({'with_genres': genre_id})
	for m in movies:
		print(m.title)




#############################################################################################
##  1. POPULAR(): SHOWS POPULAR MOVIES OF THE WEEK	 						               ##
##  2. RECOMMEND(): RECOMMENDS MOVIES BASED ON THE MOVIE USER ENTERS 		               ##
##  3. SIMILAR(): SHOWS SIMILAR MOVIES BASED ON THE MOVIE USER ENTERS                      ##
##  4. RATEABOVE(): SHOWS MOVIES ABOVE THE RATE USER ENTERS IN THE ORDER OF REVENUE        ##
#############################################################################################

def popular():
	popular = movie.popular()
	for p in popular:
		print(p.title)

def recommend(title):
	movie_title = movie.search(title)
	first_result = movie_title[0] # There may be more than one result with the same movie title
	recommendations = movie.recommendations(first_result.id)
	for recommendation in recommendations:
		print(recommendation.title)

def similar(title):
	movie_title = movie.search(title)
	first_result = movie_title[0]
	similar = movie.similar(first_result.id)
	for result in similar:
		print(result.title)

def rateAbove(rate):
	print()
	movies = discover.discover_movies({'vote_average.gte': rate, 'sort_by': 'revenue.desc'})
	for m in movies:
		print(m.title, '| RATE:', m.vote_average)




#########################
##  1. MENU()          ##
##  2. SEARCHMENU()    ##
#########################


def menu():
	print('****************************************')
	print('* MOVIE SEARCH - 0')
	print('* MOVIES OF THE WEEK - 1')
	print('* MOVIE RECOMMENDATIONS - 2')
	print('* FIND SIMILAR MOVIES - 3')
	print('* FIND MOVIES BY MINIMUM RATE - 4')
	print('****************************************')

	value = input()

	if value == '0':
		searchMenu()
	if value == '1':
		popular()
	if value == '2':
		recommend(input('ENTER MOVIE TITLE: '))
	if value == '3':
		similar(input('ENTER MOVIE TITLE: '))
	if value == '4':
		print('MOVIES WILL SHOW IN THE ORDER OF DECREASING REVENUE')
		rateAbove(input('ENTER RATE (MIN: 0, MAX: 10): '))

def searchMenu():
	print('****************************************')
	print('THE RESULT WILL SHOW IN THE ORDER OF POPULARITY')
	print('* SEARCH BY TITLE - 0') 
	print('* SEARCH BY DIRECTOR - 1')
	print('* SEARCH BY CAST - 2')
	print('* SEARCH BY RELEASE YEAR - 3')
	print('* SEARCH BY GENRE - 4')
	print('****************************************')

	value = input()

	if value == '0':
		searchByTitle(input('ENTER MOVIE TITLE: '))
	if value == '1':
		searchByDirector(input('ENTER DIRECTOR NAME: '))
	if value == '2':
		searchByCast(input('ENTER CAST NAME: '))
	if value == '3':
		searchByYear(input('ENTER YEAR: '))
	if value == '4':
		searchByGenre()


def main():
	menu()

if __name__ == '__main__':
	main()




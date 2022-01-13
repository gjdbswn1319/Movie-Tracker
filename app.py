from flask import Flask, render_template, url_for, request
from tmdbv3api import *
import pandas as pd

tmdb = TMDb()
tmdb.api_key = 'fcdb87b8e3a4e9fd5a5686f6bcceba17'

movie = Movie()

movie_log = pd.read_csv('/Users/EllyHur/Desktop/interview/log.csv', sep='|')

app = Flask(__name__)

@app.route('/')
@app.route('/home')


def home():
	#return "hello"
	#return <h1>Hello world</h1>
	return render_template('index2.html')

@app.route('/result', methods = ['POST', 'GET'])
def result():
	director = ''
	output = request.form.to_dict()
	print('output: ', output['name'])
	movie_title = movie.search(output['name'])
	first_result = movie_title[0]
	credits = movie.credits(first_result.id)
	for credit in credits.crew:
		if credit['job'] == 'Director':
			director = credit.name

	return render_template('index2.html', name = director)


if __name__ == "__main__":
	app.run(debug=True)





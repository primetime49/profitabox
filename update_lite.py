from base import *
from bs4 import BeautifulSoup
import urllib
import requests
import re
import csv
import time
import glob
import json

files = [f for f in glob.glob('*.csv')]
filenames = []

filenum = 0
for f in files:
    filenum += 1
    print(str(filenum)+'. '+f)
    filenames.append(f)

filename = int(input('Choose data source (1/2/3/...): '))
filename = filenames[filename-1]
with open(filename, 'r', encoding='ISO-8859-1') as f:
    reader = csv.reader(f)
    your_list = list(reader)

movie_list = build_list(your_list)

start_time = time.time()
year = int(input('From year: '))
until = int(input('Until year: '))
while year <= until:
    count = 0
    year_time = time.time()
    page = ''
    soup = ''
    movies = ''
    try:
        page = requests.get("https://www.boxofficemojo.com/year/" +
                            str(year)+'/?grossesOption=totalGrosses')
        soup = BeautifulSoup(page.content, 'html.parser')
        movies = soup.find_all(href=re.compile("/release"))
    except Exception as e:
        print(e)
        print('Failed to load movies from '+str(year))
        year += 1
        continue
    movies_year = find_movies_year(movie_list, year)
    new_movies = []
    for moviee in movies:
        try:
            movie_time = time.time()

            # DOMESTIC BO
            dom = BO_number(
                moviee.find_parent().find_next_siblings()[3].string)
            if dom < 1000000:
                print(str(year)+' movie has reached sub-1M')
                break
            if moviee.find_next_sibling() != None:
                print(moviee.string+' is re-release\n')
                continue
            movie = find_movie(moviee.string, year, movie_list)
            if movie.name == '':
                print(moviee.string+' is new movie')
                movie = Movie(moviee.string, '', year)
                movie_list.append(movie)
                new_movies.append(movie)

            href = movie.href

            # IMDB API
            imdb_url = imdb+href.split('/')[2]
            payload = {}
            headers = {}
            clean = json.loads(requests.request(
                "GET", imdb_url, headers=headers, data=payload).text)

            # BUDGET
            try:
                movie.budget = int(
                    BO_number(clean['boxOffice']['budget'].split(' (')[0]))
            except:
                print('No budget reported for '+movie.name)

            # DIRECTOR
            try:
                movie.director = clean['directors']
            except:
                print('No director found for '+movie.name)

            # CAST
            try:
                cast_list = []
                for a in clean['actorList']:
                    cast_list.append(a['name'])
                movie.cast = ', '.join(cast_list)
            except Exception as e:
                print(e)
                print('Failed to get casts for '+movie.name)

            # PRODUCTION CO.
            try:
                movie.prod = clean['companies']
            except Exception as e:
                print(e)
                print('Failed to get production co. for '+movie.name)

            # IMDB SCORE
            try:
                movie.score = float(clean['imDbRating'])
            except:
                print('Failed to get imdb score of '+movie.name)

            # IMDB REVIEW COUNT
            try:
                movie.reviews = int(clean['imDbRatingVotes'])
            except:
                print('Failed to get number of reviews for '+movie.name)

            # MPAA RATING
            try:
                movie.rating = clean['contentRating']
            except:
                print('No MPAA Rating for '+movie.name)

            # RUNTIME
            try:
                movie.runtime = clean['runtimeMins']
            except:
                print('No runtime found for '+movie.name)

            # GENRES
            try:
                movie.genres = clean['genres']
            except:
                print('No genres found for '+movie.name)

            movie.runtime = runtiming(movie.runtime)

            print(movie.name+" --- %s seconds ---\n" %
                  (time.time() - movie_time))
            count += 1
            try:
                movies_year.remove(movie)
            except:
                pass
        except Exception as e:
            print(e)
            print('Undefined error for '+moviee.string)
            try:
                if movie in new_movies:
                    new_movies.remove(movie)
                    movies_year.append(movie)
            except:
                pass
            print('\n')
    print('Successfully updated '+str(count)+' movies for year '+str(year))
    print('--- Removing '+str(len(movies_year))+' movies from dataset ---')
    for md in movies_year:
        print(md.name)
        movie_list.remove(md)
    print('------')
    print('--- Got '+str(len(new_movies)) +
          ' new movies for year '+str(year)+' ---')
    for md in new_movies:
        print(md.name)
    print('------')
    print(str(year)+" --- %s seconds ---\n" % (time.time() - year_time))
    year += 1
print("Total time --- %s seconds ---" % (time.time() - start_time))

with open(filename, 'w', newline='', encoding='ISO-8859-1') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(csv_header())

for movie in movie_list:
    with open(filename, 'a', newline='', encoding='ISO-8859-1') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerows(csv_movie(movie))

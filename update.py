from base import *
from bs4 import BeautifulSoup
import urllib
import requests
import re
import csv
import time
import glob
import calendar
import json

files = [f for f in glob.glob('*.csv')]
filenames = []

filenum = 0
for f in files:
    filenum += 1
    print(str(filenum)+'. '+f)
    filenames.append(f)

filename = 0
if len(filenames) > 1:
    filename = int(input('Choose data source (1/2/3/...): '))
filename = filenames[filename-1]
with open(filename, 'r', encoding = 'ISO-8859-1') as f:
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
        page = requests.get("https://www.boxofficemojo.com/year/"+str(year)+'/?grossesOption=totalGrosses')
        soup = BeautifulSoup(page.content, 'html.parser')
        movies = soup.find_all(href=re.compile("/release"))
    except Exception as e:
        print(e)
        print('Failed to load movies from '+str(year))
        year += 1
        continue
    movies_year = find_movies_year(movie_list,year)
    new_movies = []
    for moviee in movies:
        try:
            movie_time = time.time()

            # DOMESTIC BO
            dom = BO_number(moviee.find_parent().find_next_siblings()[3].string)
            if dom < 1000000:
                print(str(year)+' movie has reached sub-1M')
                break
            if moviee.find_next_sibling() != None:
                print(moviee.string+' is re-release\n')
                continue
            movie = find_movie(moviee.string,year,movie_list)
            if movie.name == '':
                print(moviee.string+' is new movie')
                movie = Movie(moviee.string, '',year)
                movie_list.append(movie)
                new_movies.append(movie)
            elif dom == movie.dom:
                print(moviee.string+' has no revenue update\n')
                movies_year.remove(movie)
                continue

            # MAX THEATER COUNT
            try:
                movie.theater = int(moviee.find_parent().find_next_siblings()[4].string.replace(',',''))
            except:
                print('No theater count for '+movie.name)
            
            # RELEASE MONTH
            try:
                movie.month = list(calendar.month_abbr).index(moviee.find_parent().find_next_siblings()[8].string.split(' ')[0])
            except:
                print('No release month for '+movie.name)
            
            # RELEASE DATE
            try:
                movie.date = int(moviee.find_parent().find_next_siblings()[8].string.split(' ')[1])
            except:
                print('Failed to get release date for '+movie.name)
            
            detail = requests.get(base+moviee.get('href'))
            details = BeautifulSoup(detail.content, 'html.parser')
            href = details.find(class_='a-link-normal mojo-title-link refiner-display-highlight').get('href')
            movie.href = re.search('\/[^\/]+\/[^\/]+',href).group()
            titsum = requests.get(base+href)
            titsums = BeautifulSoup(titsum.content, 'html.parser')
            earnings = titsums.find_all('span', class_='a-size-medium a-text-bold')
            movie.dom = BO_number(earnings[0].findChildren()[0].string)

            # INTERNATIONAL BO
            try:
                movie.inter = BO_number(earnings[1].findChildren()[0].string)
            except:
                print('No international earnings for '+movie.name)
            
            # DISTRIBUTOR
            try:
                movie.studio = titsums.find('span', string = 'Domestic Distributor').find_next_sibling().get_text().split('See')[0]
            except:
                print('No Distributing studio for '+movie.name)
            
            # OPENING BO
            try:
                movie.opening = int(BO_number(titsums.find('span', string = 'Domestic Opening').find_next_sibling().string))
            except:
                print('No opening numbers for '+movie.name)
            
            # IMDB API (1)
            imdb_url = imdb_1
            querystring = {"r":"json","i":href.split('/')[2]}
            payload = {}
            headers = mda_headers
            clean = json.loads(requests.request("GET", imdb_url, headers=headers, params=querystring).text)
            
            # DIRECTOR
            try:
                movie.director = clean['Director']
            except:
                print('No director found for '+movie.name)
                
            # IMDB SCORE
            try:
                movie.score = float(clean['imdbRating'])
            except:
                print('Failed to get imdb score of '+movie.name)
            
            # IMDB REVIEW COUNT
            try:
                movie.reviews = int(clean['imdbVotes'].replace(',',''))
            except:
                print('Failed to get number of reviews for '+movie.name)
            
            # MPAA RATING
            try:
                movie.rating = clean['Rated']
            except:
                print('No MPAA Rating for '+movie.name)
                
            # RUNTIME
            try:
                movie.runtime = clean['Runtime'].split(' ')[0]
            except:
                print('No runtime found for '+movie.name)
            
            # GENRES
            try:
                movie.genres = clean['Genre']
            except:
                print('No genres found for '+movie.name)

            # IMDB API (2)
            # BUDGET
            try:
                if movie.budget == 0:
                    imdb_url = imdb_2
                    querystring = {"tconst":href.split('/')[2]}
                    payload = {}
                    headers = imdb_headers
                    clean = json.loads(requests.request("GET", imdb_url, headers=headers, params=querystring).text)
                    
                    movie.budget = int(clean['titleBoxOffice']['budget']['amount'])
                else:
                    print('Budget already exists')
            except:
                print('No budget reported for '+movie.name)

            # IMDB API (3)
            # CAST
            try:
                if movie.cast == '':
                    imdb_url = imdb_3
                    querystring = {"tconst":href.split('/')[2]}
                    payload = {}
                    headers = imdb_headers
                    clean = json.loads(requests.request("GET", imdb_url, headers=headers, params=querystring).text)

                    movie.cast = ', '.join([c['name'] for c in clean['cast'][:20]])
                else:
                    print('Cast already exists')
            except Exception as e:
                print(e)
                print('Failed to get casts for '+movie.name)
            
            # IMDB API (4)
            # PRODUCTION CO.
            try:
                if movie.prod == '':
                    imdb_url = imdb_4
                    querystring = {"tconst":href.split('/')[2]}
                    payload = {}
                    headers = imdb_headers
                    clean = json.loads(requests.request("GET", imdb_url, headers=headers, params=querystring).text)

                    movie.prod = ', '.join([c['rowTitle'] for c in clean['categories'][0]['section']['items']])
                else:
                    print('Prod compaines already exist')
            except Exception as e:
                print(e)
                print('Failed to get production co. for '+movie.name)
            
            release = titsums.find(string = 'Original Release').find_parent().get('value')
            releasee = requests.get(base+release)
            releases = BeautifulSoup(releasee.content, 'html.parser')

            # CHINA BO
            try:
                movie.setChina(int(BO_number(releases.find('a', string='China').find_parent().find_next_siblings()[2].string)))
            except:
                print('No china release for '+movie.name)
            
            # INDONESIA BO
            try:
                movie.indo = int(BO_number(releases.find('a', string='Indonesia').find_parent().find_next_siblings()[2].string))
            except:
                print('No indonesia release for '+movie.name)

            movie.runtime = runtiming(movie.runtime)

            print(movie.name+" --- %s seconds ---\n" % (time.time() - movie_time))
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
    print('--- Got '+str(len(new_movies))+' new movies for year '+str(year)+' ---')
    for md in new_movies:
        print(md.name)
    print('------')
    print(str(year)+" --- %s seconds ---\n" % (time.time() - year_time))
    year += 1
print("Total time --- %s seconds ---" % (time.time() - start_time))

with open(filename, 'w' , newline='', encoding = 'ISO-8859-1') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(csv_header())

for movie in movie_list:
    with open(filename, 'a' , newline='', encoding = 'ISO-8859-1') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerows(csv_movie(movie))
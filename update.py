from base import *
from bs4 import BeautifulSoup
import urllib
import requests
import re
import csv
import time
import glob

files = [f for f in glob.glob('*.csv')]
filenames = []

filenum = 0
for f in files:
    filenum += 1
    print(str(filenum)+'. '+f)
    filenames.append(f)

filename = int(input('Choose data source (1/2/3/...): '))
filename = filenames[filename-1]
with open(filename, 'r') as f:
    reader = csv.reader(f)
    your_list = list(reader)

movie_list = []
for m in your_list[1:]:
    movie = Movie(m[0],m[1],int(m[2]))
    movie.month = m[3]
    movie.studio = m[4]
    movie.rating = m[5]
    movie.runtime = int(m[6])
    movie.genres = m[7]
    movie.theater = int(m[8])
    movie.opening = int(m[9])
    movie.dom = int(m[10])
    movie.inter = int(m[11])
    movie.china = int(m[12])
    movie.indo = int(m[13])
    movie.budget = int(m[15])
    movie_list.append(movie)

print(len(movie_list))

with open(filename, 'w' , newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows([['title','href','year','month','studio','rating','runtime','genres','theater_count','opening','domestic','foreign (ex. china)','china','indonesia','total','budget','profit']])
start_time = time.time()
year = int(input('From year: '))
until = int(input('Until year: '))
while year <= until:
    count = 0
    year_time = time.time()
    page = requests.get("https://www.boxofficemojo.com/year/"+str(year)+'/?grossesOption=totalGrosses')
    soup = BeautifulSoup(page.content, 'html.parser')
    movies = soup.find_all(href=re.compile("/release"))
    for moviee in movies:
        try:
            movie_time = time.time()
            if BO_number(moviee.find_parent().find_next_siblings()[4].string) < 1000000:
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
            try:
                movie.theater = int(moviee.find_parent().find_next_siblings()[5].string.replace(',',''))
            except:
                print('No theater count for '+movie.name)
            detail = requests.get(base+moviee.get('href'))
            details = BeautifulSoup(detail.content, 'html.parser')
            href = details.find(class_='a-link-normal mojo-title-link refiner-display-highlight').get('href')
            movie.href = re.search('\/[^\/]+\/[^\/]+',href).group()
            titsum = requests.get(base+href)
            titsums = BeautifulSoup(titsum.content, 'html.parser')
            earnings = titsums.find_all('td', class_='a-text-right a-align-center')
            movie.dom = BO_number(earnings[0].string)
            try:
                movie.inter = BO_number(earnings[1].string)
            except:
                print('No international earnings for '+movie.name)
            try:
                movie.studio = titsums.find('span', text = 'Domestic Distributor').find_next_sibling().get_text().split('See')[0]
            except:
                print('No Distributing studio for '+movie.name)
            try:
                movie.opening = int(BO_number(titsums.find('span', text = 'Domestic Opening').find_next_sibling().string))
            except:
                print('No opening numbers for '+movie.name)
            try:
                movie.budget = int(BO_number(titsums.find('span', text = 'Budget').find_next_sibling().string))
            except:
                summary = requests.get(imdb+href)
                summarys = BeautifulSoup(summary.content, 'html.parser')
                try:
                    movie.budget = int(BO_number(re.search('[0-9,]+',summarys.find('h4', text = 'Budget:').find_parent().get_text()).group()))
                except:
                    print('No budget reported for '+movie.name)
            try:
                movie.month = titsums.find('span', text = 'Earliest Release Date').find_next_sibling().string.split(' ')[0]
            except:
                print('No release month for '+movie.name)
            try:
                movie.rating = titsums.find('span', text = 'MPAA').find_next_sibling().string
            except:
                print('No MPAA Rating for '+movie.name)
            try:
                movie.runtime = titsums.find('span', text = 'Running Time').find_next_sibling().string
            except:
                print('No runtime found for '+movie.name)
            try:
                movie.genres = re.sub(r'\s+',' ',titsums.find('span', text = 'Genres').find_next_sibling().string.replace('\n',''))
            except:
                print('No genres found for '+movie.name)
            release = titsums.find(text = 'Original Release').find_parent().get('value')
            releasee = requests.get(base+release)
            releases = BeautifulSoup(releasee.content, 'html.parser')
            try:
                movie.setChina(int(BO_number(releases.find('a', text='China').find_parent().find_next_siblings()[2].string)))
            except:
                print('No china release for '+movie.name)
            try:
                movie.indo = int(BO_number(releases.find('a', text='Indonesia').find_parent().find_next_siblings()[2].string))
            except:
                print('No indonesia release for '+movie.name)
            movie.runtime = runtiming(movie.runtime)
            print(movie.name+" --- %s seconds ---\n" % (time.time() - movie_time))
            count += 1
        except Exception as e:
            print(e)
            print('Undefined error for '+moviee.string+'\n')
    print('Got '+str(count)+' movies for year '+str(year))
    print(str(year)+" --- %s seconds ---\n" % (time.time() - year_time))
    year += 1
print("Total time --- %s seconds ---" % (time.time() - start_time))
print(len(movie_list))
for movie in movie_list:
    with open(filename, 'a' , newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerows([[movie.name,movie.href,movie.year,movie.month,movie.studio,movie.rating,movie.runtime,movie.genres,movie.theater,movie.opening,movie.dom,movie.inter,movie.china,movie.indo,movie.getTotal(),movie.budget,movie.getProfit()]])
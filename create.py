from base import *
from bs4 import BeautifulSoup
import urllib
import requests
import re
import csv
import time
import calendar

filename = input('Filename (without .csv): ')
with open(filename+'.csv', 'w' , newline='', encoding = 'ISO-8859-1') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows([['title','href','year','month','date','studio','prod_co','director','rating','runtime','genres','theater_count','opening','domestic','foreign (ex. china)','china','indonesia','total','budget','profit']])
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
            movie = Movie(moviee.string,'',year)
            try:
                movie.theater = int(moviee.find_parent().find_next_siblings()[5].string.replace(',',''))
            except:
                print('No theater count for '+movie.name)
            try:
                movie.month = list(calendar.month_abbr).index(moviee.find_parent().find_next_siblings()[9].string.split(' ')[0])
            except:
                print('No release month for '+movie.name)
            try:
                movie.date = int(moviee.find_parent().find_next_siblings()[9].string.split(' ')[1])
            except:
                print('Failed to get release date for '+movie.name)
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
            summary = requests.get(imdb+href)
            summarys = BeautifulSoup(summary.content, 'html.parser')
            try:
                movie.budget = int(BO_number(titsums.find('span', text = 'Budget').find_next_sibling().string))
            except:
                try:
                    movie.budget = int(BO_number(re.search('[0-9,]+',summarys.find('h4', text = 'Budget:').find_parent().get_text()).group()))
                except:
                    print('No budget reported for '+movie.name)
            try:
                dirs = summarys.find('h4', text = re.compile("Director")).find_next_siblings()
                dirs = list(map(lambda d: d.string, dirs))
                movie.director = clean_director(', '.join(dirs))
            except:
                print('No director found for '+movie.name)
            try:
                casts = summarys.find('td', class_='castlist_label').find_parent().find_next_siblings()
                cast_list = []
                fail_cast = 0
                for cast in casts:
                    try:
                        cast_list.append(cast.find('img').get('alt'))
                    except:
                        fail_cast += 1
                movie.cast = ', '.join(cast_list)
                if fail_cast > 0:
                    print('Failed to get '+str(fail_cast)+' cast for '+movie.name)
            except Exception as e:
                print(e)
                print('Failed to get casts for '+movie.name)
            try:
                prods = summarys.find('h4', text = 'Production Co:').find_next_siblings()
                prod_co = []
                for prod in prods:
                    if prod.string != None:
                        prod_co.append(re.sub(r'^ ', '', prod.string))
                movie.prod = ', '.join(prod_co)
            except Exception as e:
                print(e)
                print('Failed to get production co. for '+movie.name)
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
            movie_list.append(movie)
            movie.runtime = runtiming(movie.runtime)
            print(movie.name+" --- %s seconds ---\n" % (time.time() - movie_time))
            count += 1
            with open(filename+'.csv', 'a' , newline='', encoding = 'ISO-8859-1') as myfile:
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                wr.writerows([[movie.name,movie.href,movie.year,get_month(movie.month),movie.date,movie.studio,movie.prod,movie.director,movie.rating,movie.runtime,movie.genres,movie.theater,movie.opening,movie.dom,movie.inter,movie.china,movie.indo,movie.getTotal(),movie.budget,movie.getProfit()]])
        except Exception as e:
            print(e)
            print('Undefined error for '+moviee.string+'\n')
    print('Got '+str(count)+' movies for year '+str(year))
    print(str(year)+" --- %s seconds ---\n" % (time.time() - year_time))
    year += 1
print("Total time --- %s seconds ---" % (time.time() - start_time))
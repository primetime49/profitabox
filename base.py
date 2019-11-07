from bs4 import BeautifulSoup
import urllib
import requests
import re
import csv
import calendar
import time
base = "https://www.boxofficemojo.com"
imdb = "https://www.imdb.com"
movie_list = []

def BO_number(bo):
    return int(bo.replace('$','').replace(',','').replace('\xa0',''))

def runtiming(runtime):
    num = re.findall('[0-9]+',runtime)
    if 'hr' in runtime:
        if 'min' in runtime:
            return 60*int(num[0])+int(num[1])
        else:
            return 60*int(num[0])
    else:
        if 'min' in runtime:
            return int(num[0])
    return 0

def find_movie(name,year, movies):
    for movie in movies:
        if movie.name == name and movie.year == year:
            return movie
    return Movie('','',0)

class Movie:
    def __init__(self, name, href, year):
        self.name = name
        self.href = href
        self.year = year
        self.month = ''
        self.opening = 0
        self.theater = 0
        self.dom = 0
        self.inter = 0
        self.china = 0
        self.indo = 0
        self.studio = ''
        self.rating = ''
        self.runtime = ''
        self.genres = ''
        self.budget = 0
    
    def setChina(self,china):
        self.china = china
        self.inter -= china
    
    def getProfit(self):
        if self.budget != 0:
            rev = 0.5*self.dom
            rev += 0.4*self.inter
            rev += 0.25*self.china
            return rev-self.budget
        else:
            return 0
    def getTotal(self):
        return self.dom+self.inter+self.china
        
    def __str__(self):
        tbp = ''
        tbp += '['+self.month+' '+str(self.year)+'] '+(self.name)+'\n'
        tbp += 'Studio: '+self.studio+'\n'
        tbp += 'Rating: '+self.rating+'\n'
        tbp += 'Runtime: '+str(self.runtime)+' minutes\n'
        tbp += 'Genres: '+self.genres+'\n'
        tbp += 'Opening: ${:0,.2f}'.format(self.opening)+'\n'
        tbp += 'Theater: '+str(self.theater)+'\n'
        tbp += 'Domestic: ${:0,.2f}'.format(self.dom)+'\n'
        tbp += 'Foregin (ex. China): ${:0,.2f}'.format(self.inter)+'\n'
        tbp += 'China: ${:0,.2f}'.format(self.china)+'\n'
        tbp += 'Total: ${:0,.2f}'.format(self.dom+self.inter+self.china)+'\n'
        tbp += 'Budget: ${:0,.2f}'.format(self.budget)+'\n'
        tbp += 'Profit: ${:0,.2f}'.format(self.getProfit())+'\n'
        tbp += '------'
        return tbp
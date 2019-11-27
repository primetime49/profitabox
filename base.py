from bs4 import BeautifulSoup
import re
import calendar
base = "https://www.boxofficemojo.com"
imdb = "https://www.imdb.com"
movie_list = []

def get_month(month):
    try:
        try:
            return calendar.month_name[month]
        except:
            return list(calendar.month_name).index(month)
    except:
        return ''

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

def find_all_movie(query,ml):
    movies = []
    try:
        for m in ml:
            if query.lower() in m.name.lower():
                movies.append(m)
            elif len(query.split(' ')) >= 2:
                if query.lower() in m.director.lower() or query.lower() in m.studio.lower() or query.lower() in m.cast.lower() or query.lower() in m.prod.lower():
                    movies.append(m)
            else:
                if query.lower() in list(map(lambda d: d.lower(), m.director.replace(',','').split(' '))):
                    movies.append(m)
                elif query.lower() in list(map(lambda d: d.lower(), m.cast.replace(',','').split(' '))):
                    movies.append(m)
                elif query.lower() in list(map(lambda d: d.lower(), m.prod.replace(',','').split(' '))):
                    movies.append(m)
                elif query.lower() in list(map(lambda s: s.lower(), m.studio.split(' '))):
                    movies.append(m)
                elif query.lower() in list(map(lambda g: g.lower(), m.genres.split(' '))):
                    movies.append(m)
            
        return movies
    except:
        return movies

def clean_director(director):
    found = re.findall(', \|, [0-9]+ more credit',director)
    if len(found) > 0:
        return director.replace(found[0],'')
    else:
        return director

def local_movies(movie_list):
    return sorted(movie_list,key=lambda m: (m.indo), reverse=True)

def build_list(your_list):
    movie_list = []
    for m in your_list[1:]:
        movie = Movie(m[0],m[1],int(m[2]))
        movie.month = get_month(m[3])
        movie.date = int(m[4])
        movie.studio = m[5]
        movie.prod = m[6]
        movie.director = m[7]
        movie.cast = m[8]
        movie.rating = m[9]
        movie.runtime = int(m[10])
        movie.genres = m[11]
        movie.theater = int(m[12])
        movie.opening = int(m[13])
        movie.dom = int(m[14])
        movie.inter = int(m[15])
        movie.china = int(m[16])
        movie.indo = int(m[17])
        movie.budget = int(m[19])
        movie_list.append(movie)
    return movie_list

class Movie:
    def __init__(self, name, href, year):
        self.name = name
        self.href = href
        self.year = year
        self.month = ''
        self.date = 0
        self.opening = 0
        self.theater = 0
        self.dom = 0
        self.inter = 0
        self.china = 0
        self.indo = 0
        self.studio = ''
        self.rating = ''
        self.runtime = 0
        self.genres = ''
        self.budget = 0
        self.director = ''
        self.cast = ''
        self.prod = ''
    
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
        tbp += '['+str(self.date)+' '+get_month(self.month)+' '+str(self.year)+'] '+(self.name)+'\n'
        tbp += 'Studio: '+self.studio+'\n'
        tbp += 'Production co.: '+self.prod+'\n'
        tbp += 'Director: '+self.director+'\n'
        tbp += 'Casts: '+self.cast+'\n'
        tbp += 'Rating: '+self.rating+'\n'
        tbp += 'Runtime: '+str(self.runtime)+' minutes\n'
        tbp += 'Genres: '+self.genres+'\n'
        tbp += 'Opening: ${:0,.2f}'.format(self.opening)+'\n'
        tbp += 'Theater: '+str(self.theater)+'\n'
        tbp += 'Domestic: ${:0,.2f}'.format(self.dom)+'\n'
        tbp += 'Foregin (ex. China): ${:0,.2f}'.format(self.inter)+'\n'
        tbp += 'China: ${:0,.2f}'.format(self.china)+'\n'
        tbp += 'Indonesia: ${:0,.2f}'.format(self.indo)+'\n'
        tbp += 'Total: ${:0,.2f}'.format(self.dom+self.inter+self.china)+'\n'
        tbp += 'Budget: ${:0,.2f}'.format(self.budget)+'\n'
        tbp += 'Profit: ${:0,.2f}'.format(self.getProfit())+'\n'
        tbp += '------'
        return tbp
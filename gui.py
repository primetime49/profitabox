from base import *
import csv
from tkinter import *
import glob

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

root = Tk()

# set window title
root.title('Profitabox')

# set window icon
img = PhotoImage(file='icon_v5.png')
root.wm_iconphoto(True, img)

# Make default fullscreen with toolbar
width= root.winfo_screenwidth()
height= root.winfo_screenheight()
root.geometry("%dx%d" % (width, height))

buttons = []
fields = []
showed = 0
sortBy = 'Year'
minTC = 0
maxTC = 10000
desc = True
minYear = 0
maxYear = 10000
monthVal = 'All'

def sortMovies(searchRaw):
    #searchRaw = clean_list(searchRaw)
    if sortBy == 'Year':
        return sorted(searchRaw,key=lambda m: (m.year,m.month,m.date,m.dom), reverse=desc)
    elif sortBy == 'Opening':
        return sorted(searchRaw,key=lambda m: (m.opening,m.dom), reverse=desc)
    elif sortBy == 'Domestic':
        return sorted(searchRaw,key=lambda m: (m.dom,m.year), reverse=desc)
    elif sortBy == 'Worldwide':
        return sorted(searchRaw,key=lambda m: (m.getTotal(),m.year), reverse=desc)
    elif sortBy == 'Budget':
        temp = sorted(searchRaw,key=lambda m: (m.dom), reverse=True)
        return sorted(temp,key=lambda m: (m.budget), reverse=desc)
    elif sortBy == 'Profit':
        return sorted(searchRaw,key=lambda m: (m.getProfit(),m.year), reverse=desc)
    elif sortBy == 'IMDb Rating':
        return sorted(searchRaw,key=lambda m: (m.score,m.reviews), reverse=desc)
    elif sortBy == 'Total Reviews':
        temp = sorted(searchRaw,key=lambda m: (m.dom), reverse=True)
        return sorted(temp,key=lambda m: (m.reviews), reverse=desc)

def filterMovies(searchRaw):
    newResult = []
    for sr in searchRaw:
        if sr.theater >= minTC and sr.theater <= maxTC:
            if sr.year >= minYear and sr.year <= maxYear:
                 if monthVal == 'All' or monthVal == get_month(sr.month):
                      newResult.append(sr)
    return newResult

def showMovie(movie):
    title.config(text=movie.name.upper())
    release.config(text='Released on '+str(movie.date)+' '+get_month(movie.month)+' '+str(movie.year)+' by '+movie.studio)
    review.config(text='IMDb Score: '+str(movie.score)+' by '+str(movie.reviews)+' users ')
    prod.config(text='Made by {}'.format(movie.prod))
    director.config(text='Directed by {}'.format(movie.director))
    cast.config(text='Casts: {}'.format(movie.cast))
    genre.config(text='Genres: {}'.format(movie.genres))
    rating.config(text='MPAA Rating: {}'.format(movie.rating))
    runtime.config(text='Runtime: {} minutes'.format(movie.runtime))
    theater.config(text='Max theaters count: {}'.format(movie.theater))
    opening.config(text='Opening: ${:0,.2f}'.format(movie.opening))
    dom.config(text='Domestic: ${:0,.2f}'.format(movie.dom))
    inter.config(text='Foregin (ex. China): ${:0,.2f}'.format(movie.inter))
    china.config(text='China: ${:0,.2f}'.format(movie.china))
    indo.config(text='Indonesia: ${:0,.2f}'.format(movie.indo))
    total.config(text='Total: ${:0,.2f}'.format(movie.dom+movie.inter+movie.china))
    budget.config(text='Budget: ${:0,.2f}'.format(movie.budget))
    profit.config(text='Profit: ${:0,.2f}'.format(movie.getProfit()))
    if movie.getProfit() < 0:
        profit.config(fg="red")
    elif movie.getProfit() > 0:
        profit.config(fg="green")
    else:
        profit.config(fg="black")
    
def emptyPage():
    for field in fields:
        field.config(text = '')

searchLabel = Label(root, text='Enter the movie:')
searchLabel.pack()
searchFrame = Frame(root)
searchFrame.pack()
searchEntry = Entry(searchFrame, width =50)
searchEntry.pack(side=LEFT)

sortFrame = Frame(root)

sortVar = StringVar(sortFrame)
choices = ['Year','Opening','Domestic','Worldwide','Budget','Profit','IMDb Rating','Total Reviews']
sortVar.set('Year')
sortMenu = OptionMenu(sortFrame, sortVar, *choices)
sortMenu.pack(side=LEFT)

dirVar = StringVar(sortFrame)
choices = ['UP', 'DOWN']
dirVar.set('DOWN')
dirMenu = OptionMenu(sortFrame, dirVar, *choices)
dirMenu.pack(side=LEFT)

searchButt = Button(searchFrame, text='SEARCH', command=lambda:getMovies(showed))
searchButt.pack(side=LEFT)

sortLabel = Label(root, text='Sort by:')
sortLabel.pack()
sortFrame.pack()

filterFrame = Frame(root)
filterFrame.pack()
minLabel = Label(filterFrame, text='Theaters count:', anchor='w')
minLabel.pack(side=LEFT)
minEntry = Entry(filterFrame, width = 5)
minEntry.pack(side=LEFT)
stripLabel = Label(filterFrame, text=' - ', anchor='w')
stripLabel.pack(side=LEFT)
maxEntry = Entry(filterFrame, width = 5)
maxEntry.pack(side=LEFT)

yearFrame = Frame(root)
yearFrame.pack()
yearLabel = Label(yearFrame, text='Release year:', anchor='w')
yearLabel.pack(side=LEFT)
mnyEntry = Entry(yearFrame, width = 5)
mnyEntry.pack(side=LEFT)
syLabel = Label(yearFrame, text=' - ', anchor='w')
syLabel.pack(side=LEFT)
mxyEntry = Entry(yearFrame, width = 5)
mxyEntry.pack(side=LEFT)

monthFrame = Frame(root)
monthFrame.pack()
monthLabel = Label(monthFrame, text='Release month:', anchor='w')
monthLabel.pack(side=LEFT)
monthVar = StringVar(monthFrame)
choices = ['All', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
monthVar.set('All')
monthMenu = OptionMenu(monthFrame, monthVar, *choices)
monthMenu.pack()

filterButton = Button(root, text='Filter', command=lambda:getMovies(showed))
filterButton.pack()

title = Label(root, text='', anchor='w')
title.pack(fill='both')
fields.append(title)
release = Label(root, text='', anchor='w')
release.pack(fill='both')
fields.append(release)
review = Label(root, text='', anchor='w')
review.pack(fill='both')
fields.append(review)
prod = Label(root, text='', anchor='w')
prod.pack(fill='both')
fields.append(prod)
director = Label(root, text='', anchor='w')
director.pack(fill='both')
fields.append(director)
cast = Label(root, text='', anchor='w')
cast.pack(fill='both')
fields.append(cast)
genre = Label(root, text='', anchor='w')
genre.pack(fill='both')
fields.append(genre)
rating = Label(root, text='', anchor='w')
rating.pack(fill='both')
fields.append(rating)
runtime = Label(root, text='', anchor='w')
runtime.pack(fill='both')
fields.append(runtime)
theater = Label(root, text='', anchor='w')
theater.pack(fill='both')
fields.append(theater)
opening = Label(root, text='', anchor='w')
opening.pack(fill='both')
fields.append(opening)
dom = Label(root, text='', anchor='w')
dom.pack(fill='both')
fields.append(dom)
inter = Label(root, text='', anchor='w')
inter.pack(fill='both')
fields.append(inter)
china = Label(root, text='', anchor='w')
china.pack(fill='both')
fields.append(china)
indo = Label(root, text='', anchor='w')
indo.pack(fill='both')
fields.append(indo)
total = Label(root, text='', anchor='w')
total.pack(fill='both')
fields.append(total)
budget = Label(root, text='', anchor='w')
budget.pack(fill='both')
fields.append(budget)
profit = Label(root, text='', anchor='w')
profit.pack(fill='both')
fields.append(profit)

def change_dropdown(*args):
    global sortBy, desc
    sortBy = sortVar.get()
    if dirVar.get() == 'DOWN':
        desc = True
    else:
       desc = False
    getMovies(showed)

def filterTC():
    global minTC, maxTC, minYear, maxYear, monthVal

    if minEntry.get().isdigit():
        minTC = int(minEntry.get())
    else:
        minTC = 0
    if maxEntry.get().isdigit():
        maxTC = int(maxEntry.get())
    else:
        maxTC = 10000
    
    if mnyEntry.get().isdigit():
        minYear = int(mnyEntry.get())
    else:
        minYear = 0
    if mxyEntry.get().isdigit():
        maxYear = int(mxyEntry.get())
    else:
        maxYear = 10000

    monthVal = monthVar.get()
    
# link function to change dropdown
sortVar.trace('w', change_dropdown)
dirVar.trace('w', change_dropdown)

def getMovies(showed):
    emptyPage()
    for button in buttons:
        button.destroy()
    search = searchEntry.get()
    searchRaw = find_all_movie(search, movie_list)
    searchResult = sortMovies(searchRaw)
    filterTC()
    searchResult = filterMovies(searchResult)
    maxShow = 10+showed
    while showed < maxShow and showed < len(searchResult):
        movie = searchResult[showed]
        movieButton = Button(root, text=movie.name, command=lambda movie=movie:showMovie(movie), )
        movieButton.pack()
        buttons.append(movieButton)
        showed += 1
    if len(searchResult) > showed:
        nextPage = Button(root, text='Next page', command=lambda showed=showed:getMovies(showed), )
        nextPage.pack(side=RIGHT)
        buttons.append(nextPage)
    if showed > 10:
        prevPage = Button(root, text='Previous page', command=lambda showed=maxShow-20:getMovies(showed), )
        prevPage.pack(side=LEFT)
        buttons.append(prevPage)

searchEntry.bind('<Return>', lambda event: getMovies(showed))
root.mainloop()
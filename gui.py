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

filename = int(input('Choose data source (1/2/3/...): '))
filename = filenames[filename-1]
with open(filename, 'r', encoding = 'ISO-8859-1') as f:
    reader = csv.reader(f)
    your_list = list(reader)

movie_list = build_list(your_list)

root = Tk()
buttons = []
fields = []
showed = 0
sortBy = 'Year'

def sortMovies(searchRaw):
    if sortBy == 'Year':
        return sorted(searchRaw,key=lambda m: (m.year,m.month,m.dom), reverse=True)
    elif sortBy == 'Domestic':
        return sorted(searchRaw,key=lambda m: (m.dom,m.year), reverse=True)
    elif sortBy == 'Worldwide':
        return sorted(searchRaw,key=lambda m: (m.getTotal(),m.year), reverse=True)
    elif sortBy == 'Profit':
        return sorted(searchRaw,key=lambda m: (m.getProfit(),m.year), reverse=True)

def showMovie(movie):
    title.config(text=movie.name.upper())
    release.config(text='Released on '+get_month(movie.month)+' '+str(movie.year)+' by Studio '+movie.studio)
    director.config(text='Directed by {}'.format(movie.director))
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
sortVar = StringVar(root)
choices = {'Year','Domestic','Worldwide','Profit'}
sortVar.set('Year')
sortMenu = OptionMenu(root, sortVar, *choices)
searchButt = Button(searchFrame, text='SEARCH', command=lambda:getMovies(showed))
searchButt.pack(side=LEFT)
sortLabel = Label(root, text='Sort by:')
sortLabel.pack()
sortMenu.pack()
title = Label(root, text='', anchor='w')
title.pack(fill='both')
fields.append(title)
release = Label(root, text='', anchor='w')
release.pack(fill='both')
fields.append(release)
director = Label(root, text='', anchor='w')
director.pack(fill='both')
fields.append(director)
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
    global sortBy
    sortBy = sortVar.get()
    getMovies(showed)

# link function to change dropdown
sortVar.trace('w', change_dropdown)

def getMovies(showed):
    emptyPage()
    for button in buttons:
        button.destroy()
    search = searchEntry.get()
    searchRaw = find_all_movie(search, movie_list)
    searchResult = sortMovies(searchRaw)
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
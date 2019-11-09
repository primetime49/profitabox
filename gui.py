from base import *
import csv
from tkinter import *

filename = input('Data source (without .csv): ')
with open(filename+'.csv', 'r',encoding = "ISO-8859-1") as f:
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

root = Tk()
buttons = []
fields = []
showed = 0

def showMovie(movie):
    title.config(text=movie.name.upper())
    release.config(text='Released on '+movie.month+' '+str(movie.year)+' by Studio '+movie.studio)
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
searchEntry = Entry(root, width =50)
searchEntry.pack()
searchButt = Button(root, text='SEARCH', command=lambda:getMovies(showed))
searchButt.pack()
title = Label(root, text='', anchor='w')
title.pack(fill='both')
fields.append(title)
release = Label(root, text='', anchor='w')
release.pack(fill='both')
fields.append(release)
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

def getMovies(showed):
    emptyPage()
    for button in buttons:
        button.destroy()
    search = searchEntry.get()
    searchResult = find_all_movie(search, movie_list)
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
        prevPage = Button(root, text='Previous page', command=lambda showed=int((showed-10)/10):getMovies(showed), )
        prevPage.pack(side=LEFT)
        buttons.append(prevPage)

searchEntry.bind('<Return>', lambda event: getMovies(showed))
root.mainloop()
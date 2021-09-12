import base

def pagination(request, response, movie_list):
    page = request.args.get('page')
    page_size =  request.args.get('pageSize')
    if page is None or page == "":
        page = 0
    else:
        page = int(page)
    if page_size is None or page_size == "":
        page_size = 25
    else:
        page_size = int(page_size)    
    for i in range(0, page+1):
        for j in range(i*page_size, i*page_size+page_size):
            response['data'].append(movie_list[j])
    return response

def search(request, response, movie_list):
    name = request.args.get('name')
    if name is None:
        name = ""
    movie_list = base.find_all_movie(name, movie_list)
    max = len(movie_list)
    if max > 25:
        max = 25
    for i in range(0, max):
        response['data'].append(movie_list[i])
    return response
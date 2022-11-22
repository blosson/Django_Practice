# 회원가입 시 랜덤영화 보여주기
@api_view(['GET'])
# @permission_classes([IsAuthenticated]) # 왜 이거 설정하면 에러뜰까
def random_movies(request):
    top_movies_json = open('movies/fixtures/all_movies.json', encoding='utf-8')    # topratedmovies DB 10000개
    top_movies = json.load(top_movies_json)                                 # 리스트 안에 있는 딕셔너리 형태

    genres_json = open('movies/fixtures/genres.json', encoding='utf-8')            # 장르 DB
    genres = json.load(genres_json)      


    original_genres = []                                        # 전체 장르 id를 담을 리스트
    for genre in genres:
        original_genres.append(genre['fields']['genre_id'])     # for문 돌려서 장르 id를 리스트에 담아줌
    original_genres.remove(99)                                  # 원래 장르 19개에서 99번 장르인 '다큐멘터리'는 제외했음. (DB에 장르 99번 영화가 없기 때문)
    original_genres.sort()                                      # 오름차순으로 정렬
    # print(original_genres)

    selected_top_movies = []
    for top_movie in top_movies:
        if top_movie['fields']['popularity'] >= 100:
            selected_top_movies.append(top_movie)

    print(len(selected_top_movies))
            



    random_top_movies = random.sample(selected_top_movies, 42)           # 일단 랜덤으로 42개의 영화를 가져옴
    selected_genres = []                                        # 랜덤으로 가져온 42개의 영화의 장르를 넣어줄 리스트
    for random_top_movie in random_top_movies:
        genre_ids = random_top_movie['fields']['genre_ids']
        for genre_id in genre_ids:
            selected_genres.append(genre_id)                    # 영화들의 장르 아이디들을 리스트에 담아줌

    selected_genres = sorted(list(set(selected_genres)))        # set로 중복 제거하고 오름차순 정렬
    # print(selected_genres)

    if selected_genres != original_genres:                      
        not_contained_genres = original_genres                  # 현재 없는 장르
        for selected_genre in selected_genres:
            not_contained_genres.remove(selected_genre)     
        print(not_contained_genres)

        for not_contained_genre in not_contained_genres:
            genre_movies = []
            for top_movie in top_movies:
                if not_contained_genre in top_movie['fields']['genre_ids']:
                    genre_movies.append(top_movie)

            # print(genre_movies)
            while True:
                random_genre_movie = random.sample(genre_movies, 1)[0]
                if random_genre_movie not in random_top_movies:
                    random_top_movies.append(random_genre_movie)
                    # print(len(random_top_movies))
                    break
                
        print(len(random_top_movies))
        while len(random_top_movies) < 48:
            while True:
                random_top_movie = random.sample(top_movies, 1)[0]
                if random_top_movie not in random_top_movies:
                    random_top_movies.append(random_top_movie)
                    break
                
        # print(len(random_top_movies), 'end!!')
        # pprint(random_top_movies)


    else:
        # print('oh')
        while len(random_top_movies) < 48:
            while True:
                random_top_movie = random.sample(top_movies, 1)[0]
                if random_top_movie not in random_top_movies:
                    random_top_movies.append(random_top_movie)
                    break

        # print(len(random_top_movies), 'end!!')
    #     pprint(random_top_movies[0])
    print(len(random_top_movies))
    context = {
        'random_top_movies': random_top_movies,
    }
    return Response(context)



# 영화 DB API로 받아오는 함수 (11.19 민혁 추가)
@api_view(['GET'])
def get_db(request):
    for i in range(1, 527):
        URL = 'https://api.themoviedb.org/3/movie/top_rated?api_key=a10047aa70542f33ac2138abb4e13bb7&language=ko-kr&page=' + str(i)

        print(i)  # 그냥 출력 확인용
        response = requests.get(URL).json()
        movies = response['results']

        for movie in movies:
            added_movie = Movie(       
                adult = movie['adult'],
                movie_id = movie['id'],   
                title = movie['title'],
                genre_ids = movie['genre_ids'],  
                overview = movie['overview'],
                release_date = movie['release_date'],
                popularity = movie['popularity'],
                vote_average = movie['vote_average'],
                poster_path = movie['poster_path'],
                backdrop_path = movie['backdrop_path'],
            )
            added_movie.save()

            context = {
                 added_movie,
             }

    return Response(context) 

# 영화 추천 함수
@api_view(['GET'])
def recommend(request, username):
    person = get_object_or_404(get_user_model(), username=username)

    liked_movies_id_list = []
    for like_movies in person.like_movies.all():                # 요게 핵심..
        liked_movies_id_list.append(like_movies.movie_id)
        # print(like_movies.movie_id)
    print(liked_movies_id_list)

    recommended_movies = []
    how_many = []                       # 추천된 영화 id 목록
    for liked_movies_id in liked_movies_id_list:
        for i in range(1, 3):
            URL = 'https://api.themoviedb.org/3/movie/' + str(liked_movies_id) + '/recommendations?api_key=a10047aa70542f33ac2138abb4e13bb7&language=ko-KR&page=' + str(i)
            response = requests.get(URL).json()
            movies = response['results']

            # pprint(movies)
    
            for movie in movies:
                recommended_movies.append(movie)
                how_many.append([movie['id'], movie['popularity']])
                # print(how_many) 


    how_many2 = {}  # 미쳤다..       영화 추천된 cnt랑 popularity 동시에 넣어줌
    for el in how_many:
        if el[0] in how_many2:
            how_many2[el[0]] = [how_many2[el[0]][0] + 1, el[1]]    
            pass
        else:
            how_many2[el[0]] = [1, el[1]]
        # print(how_many2)

    # print(how_many2)



    # <병진햄의 알고리즘 조언!!!> - 감사합니다~
    # how_many2 = []
    # for idx, id in enumerate(how_many):
    #     for otheridx, cnt, otherid, info in enumerate(how_many2):
    #         if id == otherid:
    #             how_many2[otheridx][0] += 1
    #             break
    #     else:
    #         how_many2.append([1, id, info])

    # how_many2.sort()
    # # [cnt, id, {영화정보}]


    how_many2 = list(how_many2.items())
    how_many2.sort(key=lambda x: x[1], reverse=True)
    # print(how_many2)
    how_many2 = how_many2[0:20]


    how_many2 = random.sample(how_many2, 12)
    how_many2.sort(key=lambda x: x[1], reverse=True)
    # print(how_many2)


    recommended_ids = []
    for id in how_many2:
        recommended_ids.append(id[0])

    # print(len(recommended_movies))

    # 리스트 안에 있는 중복된 딕셔너리 제거하는 방법
    not_redundant_movies = list({recommended_movie['id']: recommended_movie for recommended_movie in recommended_movies}.values())
    # print(len(not_redundant_movies))

    # # recommended_movies = list(set(recommended_movies))
    final_movies = []
    for id in recommended_ids:
        for not_redundant_movie in not_redundant_movies:
            if not_redundant_movie['id'] == id:
                final_movies.append(not_redundant_movie)

    # print(len(final_movies))
            

    context = {
        'final_movies': final_movies
    }
    return Response(context)



# 최신영화 추천 및 DB 저장 알고리즘
@api_view(['GET'])
def latest_movies(request):

    top_movies_json = open('movies/fixtures/all_movies.json', encoding='utf-8')    # topratedmovies DB 10000개
    top_movies = json.load(top_movies_json)  
    
    # movies = Movie.objects.raw('select movie_id from ')
    latest_movies = []
    for i in range(1, 4):
        URL = 'https://api.themoviedb.org/3/movie/now_playing?api_key=a10047aa70542f33ac2138abb4e13bb7&language=ko-KR&page=' + str(i)

        # print(i)  # 그냥 출력 확인용
        response = requests.get(URL).json()

        # print(response)
        movies = response['results']

        # DB에 저장하는 과정
        # top_movie_ids = []
        # for idx, top_movie in enumerate(top_movies):
        #     top_movie_ids.append(top_movie['fields']['movie_id'])
        #     print(idx)

        for movie in movies:
            latest_movies.append(movie)
        
        random_latest_movies = random.sample(latest_movies, 12)   

        for random_latest_movie in random_latest_movies:
            # if random_latest_movie['id'] not in top_movie_ids:
            added_movie = Movie(       
                adult = random_latest_movie['adult'],
                movie_id = random_latest_movie['id'],   
                title = random_latest_movie['title'],
                genre_ids = random_latest_movie['genre_ids'],  
                overview = random_latest_movie['overview'],
                release_date = random_latest_movie['release_date'],
                popularity = random_latest_movie['popularity'],   
                vote_average = random_latest_movie['vote_average'],
                poster_path = random_latest_movie['poster_path'],
                backdrop_path = random_latest_movie['backdrop_path'],
            )
            added_movie.save()
            print(added_movie)
            # print(idx, '아래')

        # axios에 보내주는 과정

    context = {
        'random_latest_movies': random_latest_movies
    }

    return Response(context) 
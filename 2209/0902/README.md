1. 앱의 urls.py에서 <int:pk>가 들어가는 url들이 조금 헷갈렸다. (path들은 모두 특정 게시물에 적용되는 것임을 떠올리면 좋을 것 같다.)
```python
app_name = 'movies'
urlpatterns = [
    path('', views.index, name="index"),
    path('new/', views.new, name="new"),
    path('create/', views.create, name="create"),
    path('<int:pk>/', views.detail, name="detail"),
    path('<int:pk>/edit/', views.edit, name="edit"),
    path('<int:pk>/update/', views.update, name="update"),
    path('<int:pk>/delete/', views.delete, name="delete"),
]
```

2. 
-  POST 방식으로 받아온 데이터를 변수에 저장하고 이를 다시 화면에 출력하는 일련의 과정의 연습이 더 필요할 것 같다.
- 그리고 입력 html에서 name 값이 데이터를 받아올 때 쓰이는 것도 다시 한 번 상기시켜야겠다.
-  return 시 movie.pk를 입력해야 해당 번호의 게시글의 상세 정보를 볼 수 있음에 주의!
```python
def create(request):
    # 사용자의 데이터를 받아서
    title = request.POST.get('title')
    audience = request.POST.get('audience')
    ...

    # 2 (저장하기)
    movie = Movie(
        title=title,
        audience=audience,
        release_date=release_date,
        genre=genre,
        score=score,
        poster_url=poster_url,
        description=description,
        )
    movie.save()

    # movie.pk를 입력해야 해당 번호의 게시글의 상세 정보를 볼 수 있음에 주의!
    return redirect('movies:detail', movie.pk)
```

3. 
- 글을 수정할 때 이전에 있던 값을 보여주어야 하는데, 그 과정을 정확히 이해해야할 것 같다. form 태그 안에서 value 값이 일반적으로 그 역할을 하는데 예외적으로 textarea, select, date 타입의 태그는 따로 신경써서 초기화 해주어야 한다. 그 예는 아래 코드와 같음
- 그리고 form에서 action url 입력할 때 반드시 'url 경로' 옆에 해당 pk값을 입력해주어야 해당 게시물이 업데이트 된다!! appname.pk를 잊지 말자!
```python
{% block content %}
  <h1>EDIT</h1>
  <hr>
  
  <form action=" {% url 'movies:update' movie.pk %}" method="POST">
    {% csrf_token %}
    <label for="title">Title:</label>
    <input type="text" name="title" id="title" value="{{movie.title}}"><br>
    <label for="audience">Audience:</label>
    <input type="text" name="audience" id="audience" value="{{movie.audience}}"><br>
    <label for="release_date">Release_Date:</label>
    <input type="date" name="release_date" id="release_date" value="{{release_date}}"><br>
    <label for="audience">Genre:</label>
    <select name="genre" id="genre">
      <option value="{{ movie.genre }}" selected hidden>{{ movie.genre }}</option>
      <option value="comedy">코미디</option>
      <option value="action">액션</option>
      <option value="romance">로맨스</option>
      <option value="horror">공포</option>
    </select><br>
    <label for="score">Score:</label>
    <input type="text" name="score" id="score" value="{{movie.score}}"><br>
    <label for="poster_url">Poster_URL:</label>
    <input type="text" name="poster_url" id="poster_url" value="poster_url"><br>
    <label for="description">Description:</label>
    <textarea name="description" id="description" cols="30" rows="10">{{movie.description}}</textarea><br>
    <input type="submit" value="Submit">
  </form>
    <hr>
    <a href=" {% url 'movies:index' %}">[BACK]</a>

{% endblock content %}
```

1. Admin에 model을 추가하고, pk 번호만 출력되는 것이 아닌 제목, 생성일자 같은 필드값을 노출시키려면 app의 admin.py에서 따로 설정을 해주어야 한다!
```python
from django.contrib import admin
from .models import Movie

# Register your models here.
class MovieAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'audience', 'release_date', 'genre', 'score', 'poster_url', 'description')
admin.site.register(Movie, MovieAdmin)
```

5. 장고 오류 뜰 때마다 스트레스 받긴 한데 기초문법, web, 알고리즘보다 훨씬 재밌습니다! 장고왕이 되어서 돌아오겠습니다.. Adios...
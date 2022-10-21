# 1
  - T
  - F / DELETE와 PUT도 있음
  - F / 계층관계인지 아닌지 어떻게 앎.. (내 생각)


# 2
  - 200: 성공, 서버가 요청을 제대로 처리했다는 뜻
  - 400: 잘못된 요청, 서버가 요청의 구문을 인식하지 못함
  - 401: 권한 없음, 로그인 안 했을 때
  - 403: 서버가 요청을 거부함, csrf 토큰 안 썼을 때
  - 404: 찾을 수 없음, DELETE 했을 때 
  - 500: 서버에 오류가 발생하여 요청을 수행할 수 없음


# 3
from articles.serializers import ArticleListSerializer

class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = '__all__'


# 4
복붙 아니고 타이핑해서 이해해보겠습니다..
Serializer allows complex data such as querysets and model instances to be converted to native Python datatypes that can then be easily rendered into `JSON``XML` or other content types. Serializers also provide deserialization, allowing parsed data to be converted back into complex types, after first validating the incoming data.

The serializers in REST framework vbery similary to Django's `Form` and `ModelForm` classes. We provide a `Serializer` class which gives you a powerful, genereic way to control the output of your responses, as well as a `ModelSerializer` class which providees a useful shortcut for creating serializers that deal with model instances and querysets.
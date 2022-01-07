"""
- MTV의 model역할
- django는 이 모델을 이용해 DB의 종류에 상관 없이, SQL을 잘 모르더라도 DB를 편하게 이용 할 수 있도록 ORM을 사용

class MyModelName(models.model):

    # Fields
    # 필드 이름은 쿼리 및 템플릿에서 참조하는데 쓰임
    # 필드는 또한 인수로 지정된 라벨을 가지고 있거나 필드 변수 이름의 첫자를 대문자, 밑줄을 공백으로 바꿔 기본 라벨을 추정함
    # my_field_name = My field name을 기본 라벨로 가지고 있음
    my_field_name = models.CharField(max_length=20, help_text='Enter field documentation') # 최대 길이 20자, 텍스트 라벨

    # Metadata
    class Meta: # 모델에 대한 모델-레벨 Metadata 설정 가능, 모델 타입을 쿼리할 때 반환되는 기본 레코드 순서를 제어함
        ordering = ['-my_filed_name']

        #ordering = ['title', '-pubdate'] <- 책들은 A-Z까지 알파벳 순 정렬되고 발행일 별로 가장 최근 것부터 가장 오래된 것순으로 정렬
        # -를 붙이면 반대로 정렬임.

    # Methods
    # 웹사이트의 개별적인 모델 레코드를 보여주기 위핸 URL 반환 메소드, 관리자 사이트 안의 모델 레코드 수정화면에 View on Site를 자동 추가함
    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self): ## 각각 object가 사람이 읽을 수 있는 문자열을 반환하도록 함(권장)
        return self.field_name

기본키: 레코드를 구분할 수 있는 고유의 키임, 값이 꼭 존재해야함(NULL값 X), 중복되는 값을 가지면 안됨
ex) 사람으로 따지면 주민등록번호, 사번을 이용할 수 있음, 이름은 동일 이름이 있을 수 있어 기본키가 아님

주민등록번호, 사번은 candidate key(후보 키)라고 함. 이 중 가장 잘 대표하는 것을 기본키(primary key, PK)로 정함

외래키: 각 관계를 이어주는 키임, 새롭게 생성되는 행에서 외래키에 해당하는 값이 외래키가 참조하는 테이블에 존재하는 지 체크함
ex) 사용자 정보 테이블에서 사용자 id(기본키) 구하고 그 사용자 정보에 주문 테이블을 참조한다고하면 주문 테이블에 사용자 id가 있어야함.
그 id가 주문 테이블에 있어서는 외래키라고함(FK)

참고: https://brunch.co.kr/@dan-kim/26
"""

from django.db import models


# Create your models here.

from django.db import models
from django.urls import reverse

class Genre(models.Model):
    """Model representing a book genre"""
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        """String for representing the Model object"""
        return self.name


class Language(models.Model):
    """Model representing a language."""
    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)
    # on_delete=models.SET_NULL: 관련된 저자 레코드가 삭제되었을 때 저자의 값을 Null로 설정함
    # author를 따로 class로 선언할수도 있음 어떻게 짜냐에 따라 다름
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True) # 각각 책은 하나의 저자만 가능, 저자는 여러개의 책을 가질 수 있음

    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')


    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['title', 'author']

    def display_genre(self):
        """Creates a string for the Genre. This is required to display genre in Admin."""
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])

"""
  null vs blank 차이
  
  null: DB와 관련된 것으로 데이터베이스 컬럼이 null이 될수 있는지 여부
  blank: 유효성과 관련됨. application 레벨에서 정의, 비어 있음임 즉 문자열로 따지면 '' <- 이거
  
  blank=True, null=True -> 값을 아예 비워둘 수가 있음
  
  다만!!! CharField, TextField와 같은 문자열 기반 필드에 null=True를 정의하는 것은 문제임
  
  blank=True, null=True면 null값과 '' <-빈 문자열이 저장됨.
  데이터 없음 이라는 정의에 빈 문자열과 null값이 같이 들어가므로 큰 문제임. 그래서 왠만하면
  
  데이터 없음을 표현하기위해 장고에서는 빈 문자열로 표현하는 것을 선호함!!!
  즉 charField, TextField에 대해선 blank=True만 선언해주면 좋음
"""
import uuid # Required for unique book instances
from django.contrib.auth.models import User  # Required to assign User as a borrower
from datetime import date

class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    # UUIDField: id 필드가 이 모델의 primary_key 로 설정되는 데 사용
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)


    def __str__(self):
        """String for representing the Model object."""
        return '{0} ({1})'.format(self.id, self.book.title)


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100) # 이름
    last_name = models.CharField(max_length=100) #성
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object. 성-이름 순서로 출력 """
        return f'{self.last_name}, {self.first_name}'











"""locallibrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views일 경우
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views일 경우
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
다른 참조할 URL FILE 들을 포함시켜야 하는 경우
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))


    : 사이트의 URL과 뷰의 연결을 지정, 모든 URL 매핑 코드가 포함될 수 있음. 다만 특정한 어플리케이션에 매핑의 일부를 할당하는 것이
    일반적임, 주소 관리 및 client 요청을 가장 먼저 받음


"""
from django.contrib import admin
from django.urls import path


"""
path(연결시킬 주소, 어떤 view(application.함수명)를 연결시킬 것인가)

앱 이름은 복수형이 좋음
"""
urlpatterns = [
    path('admin/', admin.site.urls),
]

from django.urls import include
urlpatterns += [
    path('catalog/', include('catalog.urls')), # www.xxxx.com/catalog로 시작되는 요청이 들어오면 catalog/urls.py를 참조하여 매핑
]

from django.views.generic import RedirectView

urlpatterns += [
    path('', RedirectView.as_view(url='/catalog/', permanent=True)),
    # 루트 URL(127.0.0.1:8000) -> 127.0.0.1:8000/catalog/로 리다이렉트 함
    # 첫번째 인자를 비워놓으면 '/'을 의미함. '/'라고 작성하면 개발 서버 시작 시 경고를 보여줌
    # 경고: Your URL pattern '/' has a route beginning with a '/'
]

from django.conf import settings
from django.conf.urls.static import static

#  URL 매퍼에 추가할 것은 개발 중에 정적 파일들을 제공하는 것을 가능케 함
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
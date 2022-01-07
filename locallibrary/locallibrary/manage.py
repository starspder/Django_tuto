#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.


 : 어플리케이션을 생성하고 데이터베이스와 작업하고 개발 웹 서버를 시작하기 위해 사용됨

 urls.py: 장고 서버로 요청(request)가 들어오면 그 요청이 어디로 가야하는지 인식하고 관련된 함수(view)로 넘겨줌
 views.py: HTTP 요청을 수신하고 HTTP 응답을 반환하는 함수 작성, Model을 통해 요청에 맞는 필요 데이터에 접근, tempalte에게 HTTP 응답 서식을 맡김
 Templates**: view.py에서 지정한 index.html 만듬. html 파일들은 기본적으로 app 폴더안의 templates 폴더 안에 위치함

 MTV(model template view)
 데이터베이스 관리: Model : 응용프로그램의 데이터 구조를 정의하고 기록을 관리함(추가, 수정, 삭제)
 레이아웃(화면): Template: 파일의 구조와 레이아웃을 정의함, 실제 내용을 보여줌
 중심 컨트롤러(심장): View: HTPP 요청을 수신하고 HTTP 응답을 반환함, Model을 통해 요청을 충족시키는데 필요한 데이터 접근, 템플릿에게 응답의 서식을 맡김


실행하기전에 꼭 migration을 하는 게 좋음.

py manage.py makemigrations #  어플리케이션에 변경 사항을 추적해 DB에 적용 할 내용을 정리합니다. 앱 안의 모델에 변경 사항이 존재할 때 사용
py manage.py migrate: 실제 변경 사항을 DB에 반영함
"""
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'locallibrary.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

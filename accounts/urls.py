from django.urls import path
from . import views

# app_name은 왜 쓸까요?
# 우리는 기본적으로 URL을 모두 변수화해서 쓰고 있음
# Template, View에서 직접 '/accounts/' X
# app_name 과 path 이름으로

app_name = 'accounts'

urlpatterns = [
    # 회원 목록 조회
    path('', views.index, name='index'),
    # 회원 세부 정보 조회
    path('<int:pk>/', views.detail, name='detail'),
    # 회원가입
    path('signup/', views.signup, name='signup'),
    # 로그인
    path('login/', views.login, name='login'),
    # 로그아웃
    path('logout/', views.logout, name='logout'),
    # 회원 정보 수정
    path('update/', views.update, name='update'),
    # 비밀번호 변경
    path('password/', views.change_password, name='change_password'),
]
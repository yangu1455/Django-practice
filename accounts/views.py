from multiprocessing import context
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
# 현재 요청과 새 세션 데이터가 파생될 업데이트 된 사용자 객체를 가져오고, 세션 데이터를 적절하게 업데이트해줌
# 암호가 변경되어도 로그아웃 되지 않도록 새로운 비밀번호의 세션 데이터로 세션을 업데이트
from django.contrib.auth import update_session_auth_hash



# Create your views here.

# 회원 목록 조회
@login_required
def index(request):
    users = get_user_model().objects.order_by('pk')
    context = {
        'users' : users,
    }
    return render(request, 'accounts/index.html', context)

# 회원 세부 정보 조회
@login_required
def detail(request, pk):
    user = get_user_model().objects.get(pk=pk)
    context = {
        'user' : user,
    }
    return render(request, 'accounts/detail.html', context)

# 회원 가입 폼
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # 바로 로그인 시켜주는 경우
            # user = form.save()  # ModelForm의 save 메서드의 리턴값은 해당 모델의 인스턴스다!
            # auth_login(request, user)  # 로그인
        
            # 로그인 시켜주지 않고 로그인 창으로 보내는 경우
            form.save()
            messages.success(request, '가입이 완료 되었습니다.')
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    context = {
        'form' : form,
    }
    return render(request, 'accounts/signup.html', context)

# 로그인
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # 세션에 저장
            # login 함수는 request, user 객체를 인자로 받음
            # user 객체는 어디있어요? 바로 form에서 인증된 유저 정보를 받을 수 있음
            auth_login(request, form.get_user())
            # local~/accounts/login/?next=/articles/1/update/
            # request.GET.get('next') : /articles/1/update/

            # if request.GET.get('next'):
            #     return redirect(request.GET.get('next'))
            # else:
            #     return redirect('accounts:index')
            messages.success(request, '로그인 되었습니다.')
            return redirect(request.GET.get('next') or 'articles:index')
    else:
        form = AuthenticationForm()

    context = {
        'form' : form
    }
    return render(request, 'accounts/login.html', context)


# 로그아웃
def logout(request):
    auth_logout(request)
    messages.warning(request, '로그아웃 하였습니다.')
    return redirect('articles:index')


# 회원 정보 수정
@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # return redirect('accounts:detail', request.user.pk)
            return redirect('accounts:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form' : form,
    }
    return render(request, 'accounts/update.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        # form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # 암호 변경 시 세션 무효화 방지하기
            update_session_auth_hash(request, form.user)
            return redirect('accounts:detail', request.user.pk)
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form' : form,
    }
    return render(request, 'accounts/change_password.html', context)


# 탈퇴하면서 해당 유저의 세션 정보도 같이 지우고 싶은 경우
# def delete(request):
#     request.user.delete()
#     auth_logout(request)
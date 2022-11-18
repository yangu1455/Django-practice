from django.shortcuts import render, redirect
from django.contrib import messages
from articles.forms import ReviewForm, CommentForm
from .models import Review
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    reviews = Review.objects.all()
    context = {
        'reviews' : reviews,
    }
    return render(request, 'articles/index.html', context)

def detail(request, pk):
    review = Review.objects.get(pk=pk)
    comment_form = CommentForm()
    context = {
        'review' : review,
        'comments' : review.comment_set.all(),
        'comment_form' : comment_form,
    }
    return render(request, 'articles/detail.html', context)

@login_required
def create(request):
    # if request.user.is_authenticated:
    # 유효성 검사
    if request.method == 'POST':
        # DB에 저장하는 로직
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            # 로그인한 유저 => 작성자네!
            review.user = request.user
            review.save()
            messages.success(request, '글 작성이 완료되었습니다.')
            return redirect('articles:index')
    else:
        review_form = ReviewForm()
    
    context = {
        'review_form' : review_form,
    }
    return render(request, 'articles/form.html', context=context)    
    # else:
    #     # 여러가지 방법이 있음
    #     # return render(....)
    #     return redirect('accounts:login')


@login_required
def update(request, pk):
    review = Review.objects.get(pk=pk)
    if request.method == "POST":
        # POST : input 값 가져와서 검증하고, DB에 저장
        review_form = ReviewForm(request.POST, request.FILES, instance=review)
        # 유효성 검사
        if review_form.is_valid():
            # 유효하면 세이브
            review_form.save()
            messages.success(request, '글이 수정되었습니다.')
            # 유효성 검사 통과하면 상세보기 페이지로
            return redirect("articles:detail", review.pk)
            
    # 유효성검사 통과하지 않으면 => context부터해서 오류메시지 담긴 article_form을 랜더링
    else:
        # GET : Form을 제공
        review_form = ReviewForm(instance=review)

    context = {
        "review_form": review_form,
        'review' : review, # 이걸 안넣어주면 커스텀한 폼에 데이터도 안들어가고 돌아가기 버튼도 안되는데 왜그런지는 모르겠음 위에서 지정해주잖아
    }
    return render(request, "articles/form.html", context)

@login_required
def delete(request, pk):
    Review.objects.get(pk=pk).delete()
    return redirect('articles:index')

def comment_create(request, pk):
    review = Review.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        # 멈춰! 사용자가 입력한 값 뿐만이 아니라 다른 값들을 받아서 쓸 수 있게
        comment = comment_form.save(commit=False)
        comment.review = review
        # 작성자 정보도 저장
        comment.user = request.user
        comment.save()
    return redirect('articles:detail', review.pk)
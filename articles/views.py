from django.shortcuts import render, redirect
from articles.forms import ReviewForm
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
    context = {
        'review' : review,
    }
    return render(request, 'articles/detail.html', context)

@login_required
def create(request):
    # if request.user.is_authenticated:
    # 유효성 검사
    if request.method == 'POST':
        # DB에 저장하는 로직
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review_form.save()
            return redirect('articles:index')
    else:
        review_form = ReviewForm()
    
    context = {
        'review_form' : review_form,
    }
    return render(request, 'articles/new.html', context=context)    
    # else:
    #     # 여러가지 방법이 있음
    #     # return render(....)
    #     return redirect('accounts:login')


@login_required
def update(request, pk):
    review = Review.objects.get(pk=pk)
    if request.method == "POST":
        # POST : input 값 가져와서 검증하고, DB에 저장
        review_form = ReviewForm(request.POST, instance=review)
        # 유효성 검사
        if review_form.is_valid():
            # 유효하면 세이브
            review_form.save()
            # 유효성 검사 통과하면 상세보기 페이지로
            return redirect("articles:detail", review.pk)
            
    # 유효성검사 통과하지 않으면 => context부터해서 오류메시지 담긴 article_form을 랜더링
    else:
        # GET : Form을 제공
        review_form = ReviewForm(instance=review)

    context = {
        "review_form": review_form,
    }
    return render(request, "articles/update.html", context)

@login_required
def delete(request, pk):
    Review.objects.get(pk=pk).delete()
    return redirect('articles:index')

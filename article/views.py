from django.shortcuts import render, redirect
from .models import Article, Author
from django.contrib.auth.models import User
from .forms import *

def homepage(request):
    articles = Article.objects.filter(active=True)
    # articles = Article.objects.raw("SELECT * FROM article_article")

    return render(
        request,
        "article/homepage.html",
        {"articles": articles}
    )


def article(request, id):
    if request.method == "POST":
        article = Article.objects.get(id=id)
        article.active = False
        article.save()
        return redirect(homepage)

    article = Article.objects.get(id=id)
    return render(
        request,
        "article/article.html",
        {"article": article}
    )


def add_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "success.html")

    form = ArticleForm()
    return render(request, "article/add_article.html", {"form": form})


def edit_article(request, id):
    article = Article.objects.get(id=id)

    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return render(request, "success.html")

    form = ArticleForm(instance=article)
    return render(request, "article/add_article.html", {"form": form})

def authors(request):
    authors = Author.objects.all()
    return render(request, "article/authors.html", {"authors": authors})


def profile(request, pk):
    author = Author.objects.get(id=pk)
    return render(request, "article/profile.html", {"author": author})


def add_author(request):
    if request.method == "GET":
        form = AuthorForm()
        context = {}
        context["form"] = form
        return render(request, "article/add_author.html", context)
    
    elif request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "success.html")


def users(request):
    context = {}
    context["users_all"] = User.objects.all()
    return render(request, "article/users.html", context)

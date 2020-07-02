from django.shortcuts import render, \
    redirect
from .models import Article, Author
from django.contrib.auth.models import User
from .forms import *
from django.db.models import Q


def homepage(request):
    if "key_word" in request.GET:
        key = request.GET.get("key_word")  
        articles = Article.objects.filter(Q(active=True), 
            Q(title__contains=key) | Q(text__contains=key) | Q(comments__text__contains=key) \
                | Q(author__name__contains=key) | Q(author__user__username=key)
        )
        articles = articles.distinct()

    else:
        articles = Article.objects.filter(active=True)

    return render(
        request,
        "article/homepage.html",
        {"articles": articles}
    )


def articles(request, tag):
    context = {}
    tag = Tag.objects.get(name=tag)
    context["articles"] = Article.objects.filter(tag=tag)
    return render(request, "article/articles.html", context)


def article(request, id):
    article = Article.objects.get(id=id)
    article.views += 1
    user = request.user
    if not user.is_anonymous:
        article.readers.add(user)
    article.save()
    if request.method == "POST":
        if "delete_btn" in request.POST:
            article.active = False
            article.save()
            return redirect(homepage)
        elif "comment_btn" in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = Comment()
                comment.user = request.user
                comment.article = article
                comment.text = form.cleaned_data["text"]
                comment.save()        

    context = {}
    context["article"] = article
    context["form"] = CommentForm()
    
    return render(
        request,
        "article/article.html",
        context
    )


def add_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            # Запрашиваемый пользователь становится автором
            if not Author.objects.filter(user=request.user):
                author = Author(
                    user=request.user,
                    name=request.user.username
                )
                author.save()
            else:
                author = Author.objects.get(user=request.user)

            # Добавляем статью
            article = Article()
            article.author = author
            article.title = form.cleaned_data["title"]
            article.text = form.cleaned_data["text"]
            article.picture = form.cleaned_data["picture"]
            article.save()
            
            # Настриваем теги
            tags = form.cleaned_data["tags"]
            for tag in tags.split(","):
                obj, created = Tag.objects.get_or_create(name=tag)
                article.tag.add(obj)

            article.save()
            return render(request, "success.html")

    form = ArticleForm()
    return render(request, "article/add_article.html", {"form": form})


def edit_article(request, id):
    article = Article.objects.get(id=id)

    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            # Добавляем статью
            article.title = form.cleaned_data["title"]
            article.text = form.cleaned_data["text"]
            article.picture = form.cleaned_data["picture"]
            article.save()
            
            # Настриваем теги
            tags = form.cleaned_data["tags"]
            for tag in tags.split(","):
                obj, created = Tag.objects.get_or_create(name=tag)
                article.tag.add(obj)

            article.save()
            context = {}
            context["article"] = article
            context["form"] = CommentForm()
            context["message"] = "Статья была изменена успешно!"
            
            return render(
                request,
                "article/article.html",
                context
            )

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

def edit_comment(request, id):
    comment = Comment.objects.get(id=id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return render(request, "success.html")

    form = CommentForm(instance=comment)
    return render(request, "article/comment_form.html", {"form": form})


def delete_comment(request, id):
    Comment.objects.get(id=id).delete()
    return render(request, "success.html")

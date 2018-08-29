from django.forms import formset_factory
from django.shortcuts import get_object_or_404
from .forms import *
#from django.contrib.auth.forms import UserCreationForm
from .forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.utils import timezone
import random
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect





def listArticle(request):
    articles_list = Article.objects.filter(status='publish').exclude(author=None)
    paginator = Paginator(articles_list, 50)
    page = request.GET.get('page')

    if page == None:
        page = 1

    articles = paginator.page(page)

    return render(request, 'article/list.html', {
        'articles': articles,
    })


def listArticleFromUser(request, id):
    user = get_object_or_404(User, id=id)
    articles_list = Article.objects.filter(status='publish', author=user)
    paginator = Paginator(articles_list, 50)
    page = request.GET.get('page')

    if page == None:
        page = 1

    articles = paginator.page(page)
    return render(request, 'article/listArticleFromUser.html', {
        'articles': articles,
        'userAuthor': user
    })



def previewArticle(request):
    articles = Article.objects.filter(decision=1).order_by('-id')[:10]
    return render(request, 'article/preview.html', {
        'articles': articles
    })


@login_required(login_url='/login')
def editArticle(request, id):

    article = get_object_or_404(Article, id=id)
    FactFormSet = formset_factory(FactForm, extra=1, max_num=4)

    article = get_object_or_404(Article, id=id)
    component = Component.objects.get(article=article)
    facts = Fact.objects.filter(article=article)

    if article.status == 'on_correct' or article.status == 'copy' or article.status == 'ready':
        if article.author != request.user and request.user.parameter.isCorrector == '0':
            return redirect('article_list')

    if request.method == "POST":

        component_form = ComponentForm(request.POST)
        formset = FactFormSet(request.POST)
        article_form = ArticleForm(request.POST)

        if article_form.is_valid() and component_form.is_valid() and formset.is_valid:

            if article.author != request.user:
                new = article_form.save(commit=False)
                new.author = request.user
                new.date = timezone.now()
                new.idArticle = article.id
                new.status = 'copy'
                new.save()

                component = component_form.save(commit=False)
                component.article = new
                component.save()

                for form in formset:
                    fact = form.save(commit=False)
                    fact.article = new
                    fact.save()

                correctArticle = ArticleToCorrect.objects.filter(article=article)
                correctArticle.delete()

                messages.success(request, "This article has been sended to author as a correction")

            else:
                articleB = article_form.save()
                article.title = articleB.title
                article.hang = articleB.hang
                article.category = articleB.category
                article.time = articleB.time
                article.decision = articleB.decision
                article.author = request.user
                article.youtube = articleB.youtube
                article.save()

                componentB = component_form.save(commit=False)
                component.article = article
                component.component = componentB.component
                component.save()

                for fact in facts:
                    fact.delete()

                for form in formset:
                    fact = form.save(commit=False)
                    fact.article = article
                    fact.save()

                messages.success(request, "Your article has been edited")

            return redirect('article_select', id=article.id)
    else:
        article_form = ArticleForm(instance=article)
        component_form = ComponentForm(instance=component)

        array=[]
        for fact in facts:
            dict = {}
            dict['text'] = str(fact.text)
            array.append(dict)

        formset = FactFormSet(initial=array)

    return render(request, 'article/edit.html', {
        'article_form': article_form,
        'component_form': component_form,
        'formset': formset,
    })


@login_required(login_url='/login')
def addArticle(request):

    FactFormSet = formset_factory(FactForm, extra=1, max_num=6)
    error = 0

    if request.method == "POST":

        article_form = ArticleForm(request.POST)
        component_form = ComponentForm(request.POST)
        formset = FactFormSet(request.POST)

        if article_form.is_valid() and component_form.is_valid() and formset.is_valid():

            color = [
                ['317989', 'd22f4c'],
                ['2e30c2', 'c29923'],
                ['afc22e', '5c5131'],
                ['710071', 'ff7e00'],
                ['f80', '720ea5'],
                ['24444b', '5aa86c'],
                ['782020', 'db3600'],
                ['2b7ea5', 'a54cbc'],
                ['84c9ea', '535743'],
            ]

            rand = random.randint(0, 8)
            article = article_form.save(commit=False)
            article.status = "ready"
            article.author = request.user
            article.date = timezone.now()
            article.save()

            component = component_form.save(commit=False)
            component.article = article
            component.save()

            for form in formset:
                fact = form.save(commit=False)
                fact.article = article
                fact.save()

            messages.success(request, "Your article has been created")

            return redirect('article_select', id=article.id)

    else:
        article_form = ArticleForm()
        component_form = ComponentForm()
        formset = FactFormSet()

    return render(request, 'article/add.html', {
        'article_form': article_form,
        'component_form': component_form,
        'formset': formset,
        'error': error
    })


def selectArticle(request, id):

    if not request.user.is_authenticated():
        request.user = None

    article = get_object_or_404(Article, id=id)
    component = Component.objects.get(article=article)
    facts = Fact.objects.filter(article=article)
    articleLike = ArticleLike.objects.filter(article=article, user=request.user)
    articleRead = ArticleReadAfter.objects.filter(article=article, user=request.user)
    follow = Follow.objects.filter(user=request.user, target=article.author)
    interrest = ArticleInterrest.objects.filter(user=request.user, article=article)
    articleCopys = Article.objects.filter(idArticle=article.id, status='copy')
    commentaries = Commentary.objects.filter(article=article)
    articleAllLike = ArticleLike.objects.filter(article=article)
    haveImageArticle = HaveImageArticle.objects.filter(user=request.user, article=article)
    authorReco = AuthorRecognize.objects.filter(user=request.user, author=article.author)

    if article.status == 'on_correct' or article.status == 'ready':

        if not request.user:
            return redirect('article_list')

        if article.author != request.user:
            if request.user.parameter.isCorrector == '0':
                return redirect('article_list')

    if request.method == 'POST':
        form = CommentaryForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()

            article.interest = article.interest + 1
            article.save()

            messages.success(request, "Your comment has been added")

            return redirect('article_select', id=article.id)
    else:
        form = CommentaryForm()

    up = article.goodPoint
    down = article.badPoint
    x = 0
    max = article.goodPoint + article.badPoint

    if max != 0:
        x = float(up) / max
        x = int(x * 100)

    return render(request, "article/select.html", {
        'article': article,
        'component': component,
        'facts': facts,
        'articleLike': articleLike,
        'articleRead': articleRead,
        'follow': follow,
        'articleCopys': articleCopys,
        'interrest': interrest,
        'form': form,
        'commentaries': commentaries,
        'articleAllLike': articleAllLike,
        'haveImageArticle': haveImageArticle,
        'authorRecognize': authorReco,
        'up': up,
        'down': down,
        'max': max,
        'x': x
    })


@login_required(login_url='/login')
def publishArticle(request, id):
    article = get_object_or_404(Article, id=id)
    facts = Fact.objects.filter(article=article)

    if article.author != request.user:
        return redirect('article_list')

    for fact in facts:
        fact.isPublish = 1
        fact.save()

    article.status = 'publish'
    article.save()

    param1 = Parameter.objects.get(user=article.author)
    param1.goodPoint = param1.goodPoint + 1
    param1.save()

    messages.success(request, "Your article has been published")

    return redirect('article_select', id=article.id)


def selectFact(request, idA, idF):
    article = get_object_or_404(Article, id=idA)
    fact = get_object_or_404(Fact, id=idF)

    if fact.isPublish == 0:
        return redirect('article_list')

    justifications_list = Justification.objects.filter(fact=fact)
    paginator = Paginator(justifications_list, 10)
    page = request.GET.get('page')
    if page == None:
        page = 1

    justifications = paginator.page(page)

    takeDecisionJustification = []
    for j in justifications:
        if request.user.is_authenticated:
            point = Point.objects.filter(user=request.user, justification=j)
            decision = len(point)
            takeDecisionJustification.append([j, decision])
        else:
            point = Point.objects.filter(justification=j)
            decision = 1
            takeDecisionJustification.append([j, decision])

    if request.method == "POST":
        form = JustificationForm(request.POST, request.FILES)
        if form.is_valid():
            justification = form.save(commit=False)

            if justification.decision == '0':
                fact.badPoint = fact.badPoint + 1
                article.badPoint = article.badPoint + 1
            elif justification.decision == '1':
                fact.goodPoint = fact.goodPoint + 1
                article.goodPoint = article.goodPoint + 1

            justification.fact = fact
            justification.user = request.user
            justification.save()
            fact.save()
            article.save()

            request.user.parameter.goodPoint = request.user.parameter.goodPoint + 1
            request.user.parameter.save()

            messages.success(request, "Your justification has been added")

            return redirect('article_select_fact', idA=article.id, idF=fact.id)

    else:
        form = JustificationForm()

    return render(request, 'fact/select.html', {
        'article': article,
        'fact': fact,
        'takeDecisionJustification': takeDecisionJustification,
        'form': form,
        'justifications': justifications
    })


@login_required(login_url='/login')
def justificationDisagree(request, idA, idF, idJ):
    article = get_object_or_404(Article, id=idA)
    fact = get_object_or_404(Fact, id=idF)
    justification = get_object_or_404(Justification, id=idJ)
    point = Point()

    if justification.decision == '1':
        fact.badPoint = fact.badPoint + 1
        article.badPoint = article.badPoint + 1
    elif justification.decision == '0':
        fact.goodPoint = fact.goodPoint + 1
        article.goodPoint = article.goodPoint + 1

    point.user = request.user
    point.justification = justification
    point.save()
    article.save()

    request.user.parameter.goodPoint = request.user.parameter.goodPoint + 1
    request.user.parameter.save()

    messages.success(request, "You are not agree with a justification")

    fact.save()

    return redirect('article_select_fact', idA=article.id, idF=fact.id)


@login_required(login_url='/login')
def justificationAgree(request, idA, idF, idJ):
    article = get_object_or_404(Article, id=idA)
    fact = get_object_or_404(Fact, id=idF)
    justification = get_object_or_404(Justification, id=idJ)
    point = Point()

    if justification.decision == '1':
        fact.goodPoint = fact.goodPoint + 1
        article.goodPoint = article.goodPoint + 1
    elif justification.decision == '0':
        fact.badPoint = fact.badPoint + 1
        article.badPoint = article.badPoint + 1

    point.user = request.user
    point.justification = justification
    point.save()
    fact.save()
    article.save()

    request.user.parameter.goodPoint = request.user.parameter.goodPoint + 1
    request.user.parameter.save()

    messages.success(request, "You are agree with a justification")

    return redirect('article_select_fact', idA=article.id, idF=fact.id)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():

            post = request.POST
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            new_user = User.objects.create_user(username=username,email=None, password=password)
            new_user.is_active = True
            new_user.first_name = post.get('firstname')
            new_user.last_name = post.get('lastname')
            new_user.save()

            param = Parameter()
            param.user = new_user
            param.isCorrector = 0
            param.save()

            new_user = authenticate(username=username, password=password)

            login(request, new_user)
            return redirect('choose_question_secret')
    else:
        form = UserCreationForm()
    return render(request, 'authentification/signup.html', {'form': form})


def chooseSecretQuestion(request):

    if request.method == 'POST':
        form = ParameterForm(request.POST)

        if form.is_valid():

            request.user.parameter.secretQuestion = request.POST.get('secretQuestion')
            request.user.parameter.secretResponse = request.POST.get('secretResponse')
            request.user.parameter.save()
            request.user.is_active = True
            request.user.save()

            return redirect('article_list')

    else:
        form = ParameterForm()

    return render(request, 'authentification/question.html', {
        'form': form
    })


@login_required(login_url='/login')
def logoutAction(request):
    logout(request)

    messages.success(request, "You are disconnect")

    return redirect('article_list')


@login_required(login_url='/login')
def profileAction(request):
    user = request.user

    if user.parameter.goodPoint >= 100 and user.parameter.isCorrector == '0':
        param = Parameter.objects.get(user=user)
        param.isCorrector = 1
        param.save()

    return render(request, 'authentification/profile.html', {
        'user': user
    })


@login_required(login_url='/login')
@user_have_secret_question
def listArticleUser(request):

    articleReady = Article.objects.filter(author=request.user.id, status='ready')
    articlePublish = Article.objects.filter(author=request.user.id, status='publish')
    articleToCorrect = Article.objects.filter(author=request.user.id, status='on_correct')

    articlesC = []
    allArticles = []

    for aR in articleToCorrect:

        a = Article.objects.filter(idArticle=aR.id).first()
        articlesC.append([
            aR, a
        ])

    for aReady in articleReady:
        allArticles.append(aReady)

    for aP in articlePublish:
        allArticles.append(aP)

    paginator = Paginator(allArticles, 25)
    page = request.GET.get('page')

    if page == None:
        page = 1

    allArticles = paginator.page(page)

    return render(request, 'article/user.html', {
        'articles': allArticles,
        'articleToCorrect': articlesC
    })


@login_required(login_url='/login')
def likeArticle(request, id):
    article = get_object_or_404(Article, id=id)
    articleLike = ArticleLike()
    articleLike.article = article
    articleLike.user = request.user
    articleLike.save()

    article.interest = article.interest + 1
    article.save()

    param1 = Parameter.objects.get(user=article.author)
    param1.goodPoint = param1.goodPoint + 1
    param1.save()

    param2 = Parameter.objects.get(user=request.user)
    param2.goodPoint = param2.goodPoint + 1
    param2.save()

    messages.success(request, "You add an article to like")

    return redirect('article_list_like')


@login_required(login_url='/login')
def dislikeArticle(request, id):
    article = get_object_or_404(Article, id=id)
    articleLike = ArticleLike.objects.filter(article=article, user=request.user)
    articleLike.delete()

    article.interest = article.interest - 1
    article.save()

    messages.success(request, "You remove an article to like")

    return redirect('article_list_like')


@login_required(login_url='/login')
def listLikeArticle(request):
    articles_list = ArticleLike.objects.filter(user=request.user)
    paginator = Paginator(articles_list, 25)
    page = request.GET.get('page')

    if page == None:
        page = 1

    articles = paginator.page(page)
    return render(request, 'article/like.html', {
        'articles': articles
    })


@login_required(login_url='/login')
def readArticle(request, id):
    article = get_object_or_404(Article, id=id)
    articleRead = ArticleReadAfter()
    articleRead.article = article
    articleRead.user = request.user
    articleRead.save()

    messages.success(request, "You add an article to read")

    return redirect('article_read_list')


@login_required(login_url='/login')
def unreadArticle(request, id):
    article = get_object_or_404(Article, id=id)
    articleRead = ArticleReadAfter.objects.filter(article=article, user=request.user)
    articleRead.delete()

    messages.success(request, "You remove an article to read")

    return redirect('article_read_list')


@login_required(login_url='/login')
def listReadArticle(request):
    articles_list = ArticleReadAfter.objects.filter(user=request.user)
    paginator = Paginator(articles_list, 25)
    page = request.GET.get('page')

    if page == None:
        page = 1

    articles = paginator.page(page)

    return render(request, 'article/read.html', {
        'articles': articles
    })


@login_required(login_url='/login')
def readAfterArticle(request, id):
    article = get_object_or_404(Article, id=id)


@login_required(login_url='/login')
def follow(request, id):
    user = get_object_or_404(User, id=id)
    follow = Follow()
    follow.user = request.user
    follow.target = user
    follow.save()

    messages.success(request, "You follow " + follow.target.username)

    return redirect('follow_list')


@login_required(login_url='/login')
def unfollow(request, id):
    current = request.user
    user = get_object_or_404(User, id=id)
    follow = Follow.objects.filter(user=current, target=user)
    follow.delete()

    messages.success(request, "You unfollow " + user.username)

    return redirect('follow_list')


@login_required(login_url='/login')
def chooseFollowForCorrection(request, id):
    article = get_object_or_404(Article, id=id)

    if article.author != request.user:
        return redirect('article_list')

    articleCorrect = ArticleToCorrect()
    articleCorrect.article = article
    articleCorrect.save()

    messages.success(request, "Your article is ready to be correct")

    article.status = 'on_correct'
    article.save()

    return redirect('article_list_user')


@login_required(login_url='/login')
def acceptCorrection(request, id, id2):
    article = get_object_or_404(Article, id=id)

    if article.author != request.user:
        return redirect('article_list')

    copyArticle = get_object_or_404(Article, id=id2)

    copyArticle.corrector = copyArticle.author
    copyArticle.author = article.author
    copyArticle.status = 'ready'
    copyArticle.idArticle = 0
    copyArticle.save()

    article.delete()

    messages.success(request, "You accept the correction")

    return redirect('article_list_user')


@login_required(login_url='/login')
def refuseCorrection(request, id, id2):
    articleUser = get_object_or_404(Article, id=id)
    article = get_object_or_404(Article, id=id2)
    article.delete()

    articleUser.status = 'ready'
    articleUser.save()

    messages.success(request, "You refuse the correction")

    return redirect('article_list_user')


@login_required(login_url='/login')
def interrestArticle(request, id):
    article = get_object_or_404(Article, id=id)
    article.interest = article.interest + 1
    article.save()

    interrestArticle = ArticleInterrest()
    interrestArticle.user = request.user
    interrestArticle.article = article
    interrestArticle.save()

    param1 = Parameter.objects.get(user=article.author)
    param1.goodPoint = param1.goodPoint + 1
    param1.save()

    param2 = Parameter.objects.get(user=request.user)
    param2.goodPoint = param2.goodPoint + 1
    param2.save()

    messages.success(request, "You mark your interrest for this article")

    return redirect('article_select', id=article.id)


@login_required(login_url='/login')
def imageAcceptArticle(request, id):
    article = get_object_or_404(Article, id=id)
    haveImageArticle = HaveImageArticle()
    haveImageArticle.user = request.user
    haveImageArticle.article = article
    haveImageArticle.save()

    article.goodPoint = article.goodPoint + 1
    article.save()

    messages.success(request, "The images are true")

    return redirect('article_select', id=article.id)


@login_required(login_url='/login')
def imageRefuseArticle(request, id):
    article = get_object_or_404(Article, id=id)
    haveImageArticle = HaveImageArticle()
    haveImageArticle.user = request.user
    haveImageArticle.article = article
    haveImageArticle.save()

    article.badPoint = article.badPoint + 1
    article.save()

    messages.success(request, "The images are false")

    return redirect('article_select', id=article.id)


@login_required(login_url='/login')
def listCorrectArticle(request):

    articles_list = ArticleToCorrect.objects.all()

    new = []
    for a in articles_list:
        if a.article.author != request.user:
            new.append(a)

    paginator = Paginator(new, 50)
    page = request.GET.get('page')

    if page == None:
        page = 1

    articles = paginator.page(page)

    return render(request, 'corrector/list.html', {
        'articles': articles
    })


def forgetPassword(request):

    form = None
    back = ""

    if request.method == 'POST':
        post = request.POST
        user = User.objects.filter(username=post.get('username'))

        if len(user) != 0:
            param = Parameter.objects.filter(user=user)
            back = "This username was not found"

            if len(param) != 0:
                param = param.first()
                return redirect('response_secret_question', id=param.id)

        else:
            back = "This username was not found"

    return render(request, 'registration/password_forget.html', {
        'form': form,
        'back': back
    })


def responseSecretQuestion(request, id):

    back = ""
    param = Parameter.objects.filter(id=id).first()

    if request.method == 'POST':
        post = request.POST
        response = post.get('response')

        if response != param.secretResponse:
            back = "This is not your response !"
        else:
            request.session['secret'] = response
            return redirect('password_change', id=param.id)

    return render(request, 'registration/password_response.html', {
        'param': param,
        'back': back
    })


def changePassword(request, id):

    param = Parameter.objects.filter(id=id).first()
    back = ""

    if request.session.get('secret'):
        if request.session.get('secret') != param.secretResponse:
            return redirect('article_list')
    else:
        return redirect('article_list')

    if request.method == 'POST':
        post = request.POST
        password = post.get('password')
        reset_password = post.get('reset_password')

        if password != reset_password:
            back = "different password"
        elif len(password) <= 6:
            back = "your password need to have mort than 6 caracter"
        else:
            u = User.objects.get(id=param.user.id)
            u.set_password(password)
            u.save()

            request.session['secret'] = None

            return redirect('article_list')

    return render(request, 'registration/password_change.html', {
        'back': back
    })


@login_required(login_url='/login')

def listFollow(request):
    follows_list = Follow.objects.filter(user=request.user)
    paginator = Paginator(follows_list, 50)
    page = request.GET.get('page')

    if page == None:
        page = 1

    follows = paginator.page(page)

    return render(request, 'follow/list.html', {
        'follows': follows
    })


@login_required(login_url='/login')
@login_required(login_url='/login')
def acceptAuthorRecognize(request, idA, id):
    author = get_object_or_404(User, id=id)
    article = get_object_or_404(Article, id=idA)
    authorReco = AuthorRecognize(user=request.user, author=author)
    authorReco.save()

    return redirect('article_select', id=article.id)

@user_have_secret_question
@login_required(login_url='/login')
def refuseAuthorRecognize(request, idA, id):
    author = get_object_or_404(User, id=id)
    article = get_object_or_404(Article, id=idA)
    authorReco = AuthorRecognize(user=request.user, author=author)
    authorReco.save()

    return redirect('article_select', id=article.id)


def search(request):

    if request.method == 'GET':
        get = request.GET
        if get.get('title'):
            title = get.get('title')
            list_articles = Article.objects.filter(title__contains=title).exclude(author=None)

            paginator = Paginator(list_articles, 50)
            page = request.GET.get('page')

            if page == None:
                page = 1

            articles = paginator.page(page)
        else:
            return redirect('article_list')

    return render(request, 'search/list.html', {
        'articles': articles
    })


def listArticleCategory(request):

    if request.method == 'GET':
        get = request.GET

        if get.get('category'):

            category = get.get('category')
            list_articles = Article.objects.filter(category=category, status='publish')

            paginator = Paginator(list_articles, 50)
            page = request.GET.get('page')

            if page == None:
                page = 1

            articles = paginator.page(page)
        else:
            return redirect('article_list')

    return render(request, 'article/category.html', {
        'articles': articles,
        'category': category
    })

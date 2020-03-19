from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.views import View
from .models import Film, Actor,Filmmaker, Genre, Comment
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from django.http import JsonResponse, HttpResponse
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth.forms import PasswordChangeForm
from .forms import  CommentForm
from django.core.paginator import Paginator



from django.shortcuts import redirect
from .models import Message
from datetime import datetime

app_url = "/popcorn/"

# наше представление для входа
class LoginFormView(FormView):

    form_class = AuthenticationForm
    template_name = "reg/login.html"
    success_url = app_url
    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = app_url + "login/"
    template_name = "reg/register.html"
    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(app_url)

class PasswordChangeView(FormView):
    # будем строить на основе
    # встроенной в django формы смены пароля
    form_class = PasswordChangeForm
    template_name = 'reg/password_change_form.html'
    # после смены пароля нужно снова входить
    success_url = app_url + 'login/'
    def get_form_kwargs(self):
        kwargs = super(PasswordChangeView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        if self.request.method == 'POST':
            kwargs['data'] = self.request.POST
        return kwargs
    def form_valid(self, form):
        form.save()
        return super(PasswordChangeView, self).form_valid(form)

def catalog(request):
    film = Film.objects.all()
    actor = Actor.objects.all()
    filmmaker = Filmmaker.objects.all()
    context = {
        'films': film,
    }
    return render(request, 'index.html', context)

class FilmsDetail(View):

    def get(self, request, slug):
        film = Film.objects.get(url=slug)
        comment = Comment.objects.filter(film__url=slug)
        paginator = Paginator(comment, 5)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)

        is_paginated = page.has_other_pages()

        if page.has_previous():
            prev_url = '?page={}'.format(page.previous_page_number())
        else:
            prev_url = ''

        if page.has_next():
            next_url = '?page={}'.format(page.next_page_number())
        else:
            next_url = ''

        context={
            'film': film,
            'comment': page,
            'form': CommentForm(),
            'is_paginated' : is_paginated,
            'next_url' : next_url,
            'prev_url' : prev_url
        }
        return render(request, "film_detail.html", context)
    def post(self,request,*args,**kwargs):
        comment = CommentForm(request.POST)
        if comment.is_valid():
            comment = comment.cleaned_data
            film = Film.objects.get(url=kwargs['slug'])
            c = Comment(user=request.user,film=film,text=comment['text'])
            c.save()
        return render(request, "film_detail.html", {'film': film,'form':CommentForm()})

def Films(request):
    films = Film.objects.all()
    genres = Genre.objects.all()
    context = {
        'films': films,
        'genres':genres
    }
    return render(request, 'films.html', context)

def Actors(request):
    actors = Actor.objects.all()
    return  render(request, "actors.html", {'actors': actors})

def Filmmakers(request):
    filmmakers = Filmmaker.objects.all()
    return  render(request, "filmmaker.html", {'filmmakers': filmmakers})

class ActorView(View):
    """Вывод информации о актере"""
    def get(self, request, slug):
        actor = Actor.objects.get(url = slug)
        return  render(request, "actor-page.html", {'actor' : actor})

class FilmmakerView(View):
    """Вывод информации о актере"""
    def get(self, request, slug):
        filmmaker = Filmmaker.objects.get(url = slug)
        return  render(request, "filmmaker-page.html", {'filmmaker' : filmmaker})

class FilmFilter(View):
    def get(self, request):
        genres = Genre.objects.all()
        query = Film.objects.filter(genres__in=request.GET.get("genre"))
        return render(request, "films.html", {'films': query, 'genres' : genres})

class SearchFilm(View):
    def get(self, request):
        genres = Genre.objects.all()
        query = Film.objects.filter(name__icontains=request.GET.get("findFilm"))
        return render(request, "films.html", {'films': query, 'genres': genres})



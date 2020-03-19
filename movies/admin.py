from django.contrib import admin
from .models import Actor, Filmmaker, Film, Genre, Reviews, Rating, RatingStar, Message, Comment
#логин admin
#пароль diana

admin.site.register(Actor)
admin.site.register(Genre)
admin.site.register(Reviews)
admin.site.register(Rating)
admin.site.register(RatingStar)
admin.site.register(Film)
admin.site.register(Filmmaker)
admin.site.register(Message)
admin.site.register(Comment)
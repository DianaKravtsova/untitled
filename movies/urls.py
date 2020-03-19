from django.urls import path



from . import views

urlpatterns = [
    path("", views.catalog, name="index"),
    path("register/", views.RegisterFormView.as_view(), name='register'),
    path("login/", views.LoginFormView.as_view(), name='login'),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("films/", views.Films, name="films"),
    path("filter/", views.FilmFilter.as_view(), name='filter'),
    path("search/", views.SearchFilm.as_view(), name='search'),
    path("films/<slug:slug>/", views.FilmsDetail.as_view(), name="film_detail"),
    path("actors/", views.Actors, name="actors"),
    path("actors/<slug:slug>/", views.ActorView.as_view(), name="actor-page"),
    path("filmmakers/", views.Filmmakers, name="filmmakers"),
    path("filmmakers/<slug:slug>/", views.FilmmakerView.as_view(), name="filmmaker-page"),
]

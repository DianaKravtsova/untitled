from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from transliterate import translit


def upload_location(instance,filename):
    return "%s/%s" %('video',translit(filename,'ru',reversed=True))

class Filmmaker(models.Model):
    name = models.CharField("Имя", max_length=100)
    photography = models.ImageField("Фото",upload_to="filmmakers/")
    biography = models.CharField(max_length=600, null = True)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    url = models.SlugField(max_length=130, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Режиссер"
        verbose_name_plural = "Режиссеры"

    def get_absolute_url(self):
        return reverse('filmmaker-page', kwargs={"slug": self.url})

class Actor(models.Model):
    name = models.CharField("Имя", max_length=100)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    biography = models.TextField(max_length=600, null = True)
    photography = models.ImageField("Изображение", upload_to="actors/")
    url = models.SlugField(max_length=130, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor-page', kwargs={"slug": self.url})

    class Meta:
        verbose_name = "Актер"
        verbose_name_plural = "Актеры"


class Genre(models.Model):
    """Жанры"""
    name = models.CharField("Имя", max_length=100)
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Film(models.Model):
    """Фильм"""
    name = models.CharField("Название", max_length=100, null=False)
    article = models.CharField(max_length=600)
    title_page = models.ImageField("Постер", upload_to="films/")
    year = models.PositiveSmallIntegerField("Дата выхода", default=2019)
    country = models.CharField("Страна", max_length=30)
    filmmaker = models.ForeignKey(Filmmaker, verbose_name="режиссер", related_name="filmmaker", on_delete=models.CASCADE)
    actors = models.ManyToManyField(Actor, verbose_name="актеры", related_name="film_actor")
    genres = models.ManyToManyField(Genre, verbose_name="жанры")
    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField("Черновик", default=False)
    trailer = models.FileField(upload_to=upload_location, blank=True, null=True, )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("film_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-value"]


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="звезда")
    film = models.ForeignKey(Film, on_delete=models.CASCADE, verbose_name="фильм")

    def __str__(self):
        return f"{self.star} - {self.film}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Reviews(models.Model):
    """Отзывы"""
    name = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )
    film = models.ForeignKey(Film, verbose_name="фильм", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.film}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

class Message(models.Model):
    chat = models.ForeignKey(
        Film,
        verbose_name='Чат под загадкой',
        on_delete=models.CASCADE, null=False)
    name = models.ForeignKey(
        User,
        verbose_name='Пользователь', on_delete=models.CASCADE)
    message = models.TextField('Сообщение')
    pub_date = models.DateTimeField(
        'Дата сообщения',
        default=timezone.now)

    def __str__(self):
        return f"{self.name} - {self.chat}"

class Comment(models.Model):
    film = models.ForeignKey(Film,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.film}"

    class Meta:
        ordering = ['-date']
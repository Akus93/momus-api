from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name='Użytkownik', on_delete=models.CASCADE)
    photo = models.ImageField(verbose_name='Zdjęcie', upload_to='user_photos', max_length=255, blank=True, null=True)
    city = models.CharField(verbose_name='Miejscowość', max_length=128, blank=True, null=True)
    description = models.TextField(verbose_name='Opis', max_length=2048, blank=True, null=True)
    birth_date = models.DateField(verbose_name='Data urodzenia', null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    class Meta:
        verbose_name = 'Profil użytkownika'
        verbose_name_plural = 'Profile użytkowników'


class Post(models.Model):
    author = models.ForeignKey(UserProfile, verbose_name='Autor')
    title = models.CharField(verbose_name='Tytuł', max_length=64)
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Obrazek', upload_to='images', max_length=255)
    rate = models.SmallIntegerField(verbose_name='Ocena', default=0)
    tags = ArrayField(models.CharField(max_length=20, blank=True), 5, verbose_name='Tagi')
    is_pending = models.BooleanField(verbose_name='Czy oczekujący', default=1)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posty'


class Favorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='Użytkownik')
    post = models.ForeignKey(Post, verbose_name='Post')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')

    class Meta:
        verbose_name = 'Ulubiony'
        verbose_name_plural = 'Ulubione'
        ordering = ['-create_date']


class Comment(models.Model):
    author = models.ForeignKey(UserProfile, verbose_name='Autor', related_name='author')
    post = models.ForeignKey(Post, verbose_name='Post')
    text = models.CharField(verbose_name='Tekst', max_length=255)
    is_active = models.BooleanField(verbose_name='Czy aktywny', default=True)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')

    def __str__(self):
        return 'Komentarz {} o {}'.format(self.author, self.teacher)

    class Meta:
        verbose_name = 'Komentarz'
        verbose_name_plural = 'Komentarze'


class Message(models.Model):
    sender = models.ForeignKey(UserProfile, verbose_name='Nadawca', related_name='sender')
    reciver = models.ForeignKey(UserProfile, verbose_name='Odbiorca', related_name='reciver')
    title = models.CharField(verbose_name='Tytuł', max_length=64)
    text = models.TextField(verbose_name='Tekst', max_length=1024)
    is_read = models.BooleanField(verbose_name='Czy odczytane', default=False)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')

    def __str__(self):
        return 'Wiadomość od {} do {}'.format(self.sender.user.username, self.reciver.user.username)

    class Meta:
        verbose_name = 'Wiadomość'
        verbose_name_plural = 'Wiadomości'
        ordering = ['-create_date']


class Notification(models.Model):
    MESSAGE = 'MESSAGE'
    COMMENT = 'COMMENT'
    REMOVE = 'REMOVE'
    TO_MAIN = 'TO_MAIN'
    NOTIFICATION_TYPES = (
        (MESSAGE, 'MESSAGE'),
        (COMMENT, 'COMMENT'),
        (REMOVE, 'REMOVE'),
        (TO_MAIN, 'TO_MAIN')
    )
    user = models.ForeignKey(UserProfile, verbose_name='Odbiorca')
    title = models.CharField(verbose_name='Tytuł', max_length=128)
    text = models.CharField(verbose_name='Tekst', max_length=255)
    type = models.CharField(verbose_name='Typ', choices=NOTIFICATION_TYPES, max_length=16)
    data = models.CharField(verbose_name='Dane', max_length=64, blank=True, null=True)
    is_read = models.BooleanField(verbose_name='Czy odczytane', default=False)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')

    def __str__(self):
        return 'Powiadomienie dla {}'.format(self.user.user.username)

    class Meta:
        verbose_name = 'Powiadomienie'
        verbose_name_plural = 'Powiadomienia'
        ordering = ['-create_date']


class ReportedPost(models.Model):
    author = models.ForeignKey(UserProfile, verbose_name='Autor zgłoszenia')
    post = models.ForeignKey(Post, verbose_name='Post')
    text = models.CharField(verbose_name='Tekst zgłoszenia', max_length=255)
    is_pending = models.BooleanField(verbose_name='Czy oczekujący', default=True)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')

    def __str__(self):
        return 'Zgłoszenie posta {}'.format(self.comment)

    class Meta:
        verbose_name = 'zgłoszenie posta'
        verbose_name_plural = 'Zgłoszone posta'


class ReportedComment(models.Model):
    author = models.ForeignKey(UserProfile, verbose_name='Autor zgłoszenia')
    comment = models.ForeignKey(Comment, verbose_name='Komentarz')
    text = models.CharField(verbose_name='Tekst zgłoszenia', max_length=255)
    is_pending = models.BooleanField(verbose_name='Czy oczekujący', default=True)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')

    def __str__(self):
        return 'Zgłoszenie komentarza {}'.format(self.comment)

    class Meta:
        verbose_name = 'zgłoszenie komentarza'
        verbose_name_plural = 'Zgłoszone komentarze'

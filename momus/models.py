from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name='Użytkownik', on_delete=models.CASCADE)
    photo = models.ImageField(verbose_name='Zdjęcie', upload_to='photos', max_length=255, blank=True, null=True)
    city = models.CharField(verbose_name='Miejscowość', max_length=128, blank=True, null=True)
    description = models.TextField(verbose_name='Opis', max_length=2048, blank=True, null=True)
    birth_date = models.DateField(verbose_name='Data urodzenia', null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    class Meta:
        verbose_name = 'Profil użytkownika'
        verbose_name_plural = 'Profile użytkowników'

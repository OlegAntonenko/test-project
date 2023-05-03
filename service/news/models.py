import datetime
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile

from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    """
    Модель 'Автор'
    """
    user = models.OneToOneField(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class News(models.Model):
    """
    Модель 'Новости'
    """
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    image = models.ImageField(upload_to='images', verbose_name='Главное изображение')
    preview = models.ImageField(upload_to='images_resize', verbose_name='Превью', blank=True)
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    date = models.DateTimeField(default=datetime.datetime.now, verbose_name='Дата')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)

            # Присвоить параметр size=200 наименьшей стороне
            size = 200
            width, height = img.size
            if width < height:
                width = size
            else:
                height = size
            new_image = img.resize((width, height))

            # Сохранить изображение
            new_image_io = BytesIO()
            new_image.save(new_image_io, format='PNG')
            temp_name = self.image.name
            print(temp_name)
            self.preview.save(
                temp_name,
                content=ContentFile(new_image_io.getvalue()),
                save=False
            )

        super(News, self).save(*args, **kwargs)

    class Meta:
        ordering = ['date']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

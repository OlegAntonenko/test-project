from django.contrib import admin

from news.models import News, Author

admin.site.register(News)
admin.site.register(Author)

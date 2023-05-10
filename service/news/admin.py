from django_summernote.admin import SummernoteModelAdmin
from django.contrib import admin
from news.models import News, Author


class NewsAdmin(SummernoteModelAdmin):
    exclude = ('preview', 'date',)
    summernote_fields = ('text',)


admin.site.register(News, NewsAdmin)
admin.site.register(Author)

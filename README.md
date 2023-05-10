# test-project

Развертывание: 

1) docker-compose build
2) docker-compose up 
3) Добавить .env файл для настроек рассылки (Указать в нем: EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, 
RECIPIENT_ADDRESS)
4) docker-compose exec web-app python manage.py migrate 
5) docker-compose exec web-app python manage.py makemigrations
6) docker-compose exec web-app python manage.py createsuperuser

URLs:

1) CRUD новостей: http://127.0.0.1:8000/news/ 
2) Загрузка *.xlsx файла с координатами: http://127.0.0.1:8000/upload/
3) admin: http://127.0.0.1:8000/admin/

Примечания:

1) Не получилось вызвать constance_updated из news.signals для изменения времени выполнения таски. 
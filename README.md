### Установка
```
pip install -r requirements.txt
```
##### Запуск сервера
Удалить базу данных sqlite3.db, потом создать миграции.
```
python manage.py runserver
```
##### Подготовка базы данных
```
python manage.py makemigrations post
python manage.py migrate
```
##### Создание супервользователя (Хотяяя, возможно там уже создан)
```
python manage.py createsuperuser
```
##### Запуск сервера
```
python manage.py runserver
```

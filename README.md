### Установка
```
pip install -r requirements.txt
```
##### Подготовка базы данных
Удалить базу данных sqlite3.db, потом создать миграции.
```
python manage.py makemigrations post
python manage.py migrate
```
##### Запуск сервера
```
python manage.py runserver
```
##### Создание супервользователя (Хотяяя, возможно там уже создан)
```
python manage.py createsuperuser
```
##### Запуск сервера
```
python manage.py runserver
```

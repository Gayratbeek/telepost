### Установка
```
pip install -r requirements.txt
python manage.py collectstatic """Только надо поменять настройки глобальной статических настроек в settings.py"""
sudo apt-get install gdal-bin """Установка отображений утилит в убунту"""
```
##### Подготовка базы данных
```
python manage.py migrate
```

##### При добавлении главной категории комментировать models.category 
```
def save(self. *args, **kwargs) """Комментировать при первой категории нижние 4 строки"""
# super(Category, self).save()
#       if self.parent.mptt_level is not None:
#            if self.parent.mptt_level == 3:
#                raise ValueError(u'Достигнута максимальная вложенность!')
```
##### Создание супервользователя (Хотяяя, возможно там уже создан)
```
python manage.py createsuperuser
```

##### Запуск сервера
```
python manage.py runserver
```

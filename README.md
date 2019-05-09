# СЭД МТУСИ

> Vue.js/Django проект

## Построение

### Фронтенд, Vue.js

Не забудьте установить npm!

``` bash
# перейти в папку с фронтендом
cd frontend

# установить зависимости
npm install

# запустить с горячей перезагрузкой localhost:8080
npm run dev

# построить для продакшена с минификацией
npm run build

# построить для продакшена и посмотреть bundle analyzer report
npm run build --report
```

### Бекенд, Django

Не забудьте установить python!

``` bash
# установить зависимости
pip3 install -r requirements.txt

# В командной строке указать password smtp сервера (вместо 
# password подставить пароль, он есть у разработчика приложения).
# Вроде бы это не перманентно делается, я не поняла, но иначе не
# работает
set edms-mtuci-password=password

# запустить
python manage.py runserver
```

## Другие штуки

[Документация](edms-mtuci.herokuapp.ru/docs "edms-mtuci.herokuapp.ru/docs")

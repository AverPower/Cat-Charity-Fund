<a name="readme-top"></a>

<br />
<div align="center">
  <a href="https://github.com/AverPower/QRKot">
    <img src="static/img/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">YaCut - это приложение для Благотворительного фонда поддержки котиков. 

Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции</h3>

  <p align="center">
    Данный проект был написан в рамках 23 спринта обучения на курсе Python-разработчик от Яндекс.Практикума
    <br />
    <a href="https://github.com/AverPower/QRKot"><strong>Открыть код проекта »</strong></a>
    <br />
    <br />
  </p>
</div>

### Стек

* ![Static Badge](https://img.shields.io/badge/Python-3.10-yellow?logo=python)
* ![Static Badge](https://img.shields.io/badge/fastapi-0.111.0-brightgreen?logo=fastapi)
* ![Static Badge](https://img.shields.io/badge/sqlalchemy-6.0-purple?logo=sqlalchemy)
* ![Static Badge](https://img.shields.io/badge/pydantic-2.7-blue?logo=pydantic)


### Установка

Клонировать репозиторий и перейти в него в командной строке:

```
git clone 
```

```
cd qrkot
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/MacOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Запустить миграции

```
alembic migrate
```


Запустить сервер

```
uvicorn app.main:app --reload
```

Открыть документацию приложения в браузере по адресу

```
http://localhost/docs
```
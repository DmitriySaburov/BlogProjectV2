# BlogProjectV2

# сделать дамп БД
python -Xutf8 manage.py dumpdata --indent=2 --output=dump.json
# загрузить дамп БД
python -Xutf8 manage.py loaddata dump.json
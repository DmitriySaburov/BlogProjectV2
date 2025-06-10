# BlogProjectV2

# сделать дамп БД
python -Xutf8 manage.py dumpdata --indent=2 --output=dump.json
# загрузить дамп БД
провести миграции
python -Xutf8 manage.py loaddata dump.json
если не сразабывает, то перед load сделать это:
python manage.py shell
from django.contrib.contenttypes.models import ContentType
ContentType.objects.all().delete()

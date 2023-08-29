import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from recipes.models import Ingredient, Tag

DATA_FOLDER = settings.BASE_DIR.parent / 'data'


class Command(BaseCommand):
    help = 'Import ingredients and tags from csv data.'
    requires_migrations_checks = True

    @staticmethod
    def import_data_from_csv(file_name, model, obj_keys):
        """Импортирует данные из CSV в базу данных для указанной модели."""
        with open(DATA_FOLDER / file_name, "rt") as file:
            file.readline()
            objects = []
            names = set()
            for row in csv.reader(file, dialect="excel"):
                name = row[0]
                if row[0] in names:
                    continue
                names.add(name)
                obj_kwargs = {k: v for k, v in zip(obj_keys, row)}
                objects.append(model(**obj_kwargs))
            model.objects.bulk_create(objects)

    def handle(self, *args, **options):
        """Начинает импортировать и записывать данные в базу данных."""
        try:
            self.import_data_from_csv(
                'ingredients.csv', Ingredient, ['name', 'measurement_unit']
            )
            self.import_data_from_csv(
                'tags.csv', Tag, ['name', 'color', 'slug']
            )
        except Exception as error:
            self.stdout.write(self.style.ERROR(error))
            raise error
        self.stdout.write(
            self.style.SUCCESS('Successful csv data import!')
        )

import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from pathlib import Path

from recipes.models import Ingredient, Tag


class Command(BaseCommand):
    help = 'Import ingredients and tags from csv data.'
    requires_migrations_checks = True

    @staticmethod
    def import_data_from_csv(file_name, model, obj_keys):
        """Импортирует данные из CSV в базу данных для указанной модели."""
        with open(Path(settings.CSV_FILES_DIR) / file_name, "rt") as file:
            file.readline()
            names = set()
            for row in csv.reader(file, dialect="excel"):
                name = next(iter(row))
                if name in names:
                    continue
                names.add(name)
                obj_kwargs = {key: value for key, value in zip(obj_keys, row)}
                model.objects.get_or_create(**obj_kwargs)

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

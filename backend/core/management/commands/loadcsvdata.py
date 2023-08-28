import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from recipes.models import Ingredient, Tag

DATA_FOLDER = settings.BASE_DIR.parent / 'data'

class Command(BaseCommand):
    help = 'Import ingredients and tags from csv data.'
    requires_migrations_checks = True

    @staticmethod
    def import_ingredients_from_csv(file_name, model):
        """Импортирует ингредиенты из CSV в базу данных для указанной модели."""
        with open(DATA_FOLDER / file_name, "rt") as file:
            file.readline()
            objects = []
            names = set()
            for row in csv.reader(file, dialect="excel"):
                name, measurement_unit = row
                if name in names:
                    continue
                names.add(name)
                obj_kwargs = {
                    'name': name,
                    'measurement_unit': measurement_unit
                }
                objects.append(model(**obj_kwargs))
            model.objects.bulk_create(objects)

    @staticmethod
    def import_tags_from_csv(file_name, model):
        """Импортирует ингредиенты из CSV в базу данных для указанной модели."""
        with open(DATA_FOLDER / file_name, "rt") as file:
            file.readline()
            objects = []
            names = set()
            for row in csv.reader(file, dialect="excel"):
                name, color, slug = row
                if name in names:
                    continue
                names.add(name)
                obj_kwargs = {
                    'name': name,
                    'color': color,
                    'slug': slug
                }
                objects.append(model(**obj_kwargs))
            model.objects.bulk_create(objects)

    def handle(self, *args, **options):
        """Начинает импортировать и записывать данные в базу данных."""
        try:
            self.import_ingredients_from_csv('ingredients.csv', Ingredient)
            self.import_tags_from_csv('tags.csv', Tag)
        except Exception as error:
            self.stdout.write(self.style.ERROR(error))
            raise error
        self.stdout.write(
            self.style.SUCCESS('Successful csv data import!')
        )

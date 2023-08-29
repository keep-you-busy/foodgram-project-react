# coding: utf8
import os
from collections import defaultdict

from django.db.models import Sum
from fpdf import FPDF
from recipes.models import IngredientRecipe

SYSTEM_TTFONTS = os.path.join(os.path.dirname(__file__), 'fonts')
FONT_PATH = os.path.join(SYSTEM_TTFONTS, 'NotoSans-Regular.ttf')
INGREDIENT_WIDTH = 100
MEASUREMENT_WIDTH = 30
AMOUNT_WIDTH = 30


class PDFWithHeaderFooter(FPDF):
    """Класс с готовыми значениями загаловка и нижнего колонтитула."""

    def header(self):
        self.add_font('NotoSans', style='', fname=FONT_PATH, uni=True)
        self.set_font('NotoSans', size=12)
        self.cell(0, 10, 'Список покупок', 10, 1, 'C')

    def footer(self):
        self.add_font('NotoSans', style='', fname=FONT_PATH, uni=True)
        self.set_y(-15)
        self.set_font('NotoSans', size=8)
        self.cell(0, 10, 'Страница ' + str(self.page_no()), 0, 0, 'C')


def data_prepare(user):
    """Метод для забора и  подготовки данных для PDF."""
    ingredients_data = defaultdict(lambda: ('', 0))
    ingredients_values = IngredientRecipe.objects.filter(
        recipe__in_carts__user=user
    ).values(
        'ingredient__name',
        'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
    for item in ingredients_values:
        name = item.get('ingredient__name')
        unit = item.get('ingredient__measurement_unit')
        amount = str(item.get('amount'))

        ingredients_data[name] = (unit, amount)

    return ingredients_data


def make_shopping_cart(user, temp_filename):
    """Создание списка покупок в PDF."""
    pdf = PDFWithHeaderFooter()
    font_path = os.path.join(SYSTEM_TTFONTS, 'NotoSans-Regular.ttf')
    pdf.add_font('NotoSans', style='', fname=font_path, uni=True)
    pdf.add_page()
    pdf.set_font('NotoSans', size=12)

    pdf.cell(INGREDIENT_WIDTH, 10, 'Ингредиент', border=1)
    pdf.cell(MEASUREMENT_WIDTH, 10, 'Е. И.', border=1)
    pdf.cell(AMOUNT_WIDTH, 10, 'Количество', border=1)
    pdf.ln()

    ingredients_data = data_prepare(user)

    for name, (unit, amount) in ingredients_data.items():
        pdf.cell(INGREDIENT_WIDTH, 10, name, border=1)
        pdf.cell(MEASUREMENT_WIDTH, 10, unit, border=1)
        pdf.cell(AMOUNT_WIDTH, 10, amount, border=1)
        pdf.ln()

    pdf.output(temp_filename)

import os
from collections import defaultdict

from django.db.models import Sum
from fpdf import FPDF
from recipes.models import IngredientRecipe


INGREDIENT_WIDTH = 100
MEASUREMENT_WIDTH = 30
AMOUNT_WIDTH = 30
FONT_PATH = '/app/core/fonts/NotoSans-Regular.ttf'


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
        amount = item.get('amount')
        current_unit, current_amount = ingredients_data[name]
        if not current_unit:
            current_unit = unit
        current_amount += amount
        ingredients_data[name] = (current_unit, current_amount)

    return ingredients_data


def make_shopping_cart(user, temp_filename):
    """Создание списка покупок в PDF."""
    pdf = PDFWithHeaderFooter()
    pdf.add_font('NotoSans', style='', fname=FONT_PATH, uni=True)
    pdf.add_page()
    pdf.set_font('NotoSans', size=12)

    pdf.cell(INGREDIENT_WIDTH, 10, 'Ингредиент', border=1)
    pdf.cell(MEASUREMENT_WIDTH, 10, 'Е. И.', border=1)
    pdf.cell(AMOUNT_WIDTH, 10, 'Количество', border=1)
    pdf.ln()

    ingredients_data = data_prepare(user)

    for name, (unit, amount) in ingredients_data.items():
        amount = str(amount)
        pdf.cell(INGREDIENT_WIDTH, 10, name, border=1)
        pdf.cell(MEASUREMENT_WIDTH, 10, unit, border=1)
        pdf.cell(AMOUNT_WIDTH, 10, amount, border=1)
        pdf.ln()

    pdf.output(temp_filename)

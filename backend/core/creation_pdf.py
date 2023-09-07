from collections import defaultdict

from django.db.models import Sum
from fpdf import FPDF
from recipes.models import IngredientRecipe


INGREDIENT_WIDTH = 100
MEASUREMENT_WIDTH = 30
AMOUNT_WIDTH = 30
TRANSLATION = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e',
               'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k',
               'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
               'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts',
               'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '',
               'э': 'e', 'ю': 'yu', 'я': 'ya'}


class PDFWithHeaderFooter(FPDF):
    """Класс с готовыми значениями загаловка и нижнего колонтитула."""

    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'List', 10, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')


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


def russian_to_latin(input_string):
    """Перевод с кириллицы на латиницу для кодировки latin-1."""
    input_string.lower()
    translated_string = input_string.translate(str.maketrans(TRANSLATION))
    return translated_string


def make_shopping_cart(user, temp_filename):
    """Создание списка покупок в PDF."""
    pdf = PDFWithHeaderFooter()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font('Arial', size=12)

    pdf.cell(INGREDIENT_WIDTH, 10, 'Ingredient', border=1)
    pdf.cell(MEASUREMENT_WIDTH, 10, 'Unit', border=1)
    pdf.cell(AMOUNT_WIDTH, 10, 'Amount', border=1)
    pdf.ln()

    ingredients_data = data_prepare(user)

    for name, (unit, amount) in ingredients_data.items():
        name = russian_to_latin(name)
        unit = russian_to_latin(unit)
        amount = str(amount)
        pdf.cell(INGREDIENT_WIDTH, 10, name, border=1)
        pdf.cell(MEASUREMENT_WIDTH, 10, unit, border=1)
        pdf.cell(AMOUNT_WIDTH, 10, amount, border=1)
        pdf.ln()

    pdf.output(temp_filename)

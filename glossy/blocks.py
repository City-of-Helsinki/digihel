from django.forms import Select
from wagtail.wagtailcore import blocks

from glossy.models import Category


class _TermCategoryChoiceBlock(blocks.ChooserBlock):
    target_model = Category
    widget = Select

    def value_for_form(self, value):
        if hasattr(value, 'pk'):
            return value.pk
        return value

    def value_from_form(self, value):
        return super(_TermCategoryChoiceBlock, self).value_from_form(value or None)


class TermCategoryBlock(blocks.StructBlock):
    category = _TermCategoryChoiceBlock(required=True, label='Category')

    class Meta:
        template = 'glossy/term-category.html'
        label = 'Term Category'

    def get_context(self, value):
        context = super(TermCategoryBlock, self).get_context(value)
        context['terms'] = value['category'].terms.filter(list_visible=True).order_by('name')
        return context

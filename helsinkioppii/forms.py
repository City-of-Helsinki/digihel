from django import forms
from django.utils.translation import ugettext_lazy as _
from taggit.models import Tag

from helsinkioppii.models.cases import Case, SchoolGrade, SchoolSubject, CaseTheme


def get_live_case_keywords():
    """
    Returns keywords (tags) for published Case objects.

    :return: Keywords
    :rtype: Queryset
    """
    return Tag.objects.filter(
        pk__in=Case.objects.live().values_list('keywords__pk')
    )


class CaseFilterForm(forms.Form):
    free_text = forms.CharField(
        label=_('Free text'),
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Search'),
        }),
    )
    themes = forms.ModelMultipleChoiceField(
        CaseTheme.objects.all(),
        label=_('Themes'),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'filter-keywordlist list-unstyled checkbox'
        }),
        required=False,
    )
    grades = forms.ModelMultipleChoiceField(
        SchoolGrade.objects.all(),
        label=_('School grades'),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'filter-keywordlist list-unstyled checkbox'
        }),
        required=False,
    )
    subjects = forms.ModelMultipleChoiceField(
        SchoolSubject.objects.all(),
        label=_('School subjects'),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'filter-keywordlist list-unstyled checkbox'
        }),
        required=False,
    )

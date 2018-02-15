from django import forms
from django.utils.translation import ugettext_lazy as _
from taggit.models import Tag

from helsinkioppii.utils import strip_dangerous_html
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


def html_content_field(label):
    return forms.CharField(
        label=label,
        widget=forms.Textarea(attrs={
            'rows': '8'
        }),
        required=False,
        strip=True,
    )


class CaseForm(forms.Form):
    title = forms.CharField(
        label=_('Title:'),
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        required=True,
        strip=True,
    )

    # Image
    image = forms.ImageField(
        label=_('Image:'),
        required=False
    )
    image_title = forms.CharField(
        label=_('Image title:'),
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        required=False,
        strip=True,
    )

    # Meta fields
    school = forms.CharField(
        label=_('School:'),
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        required=False,
        strip=True,
    )
    student_count = forms.IntegerField(
        label=_('Student count:'),
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        }),
        required=False,
        min_value=0
    )
    themes = forms.ModelMultipleChoiceField(
        CaseTheme.objects.all(),
        label=_('Themes:'),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'list-unstyled checkbox'
        }),
        required=False,
        help_text=_('Select any fitting existing themes.'),
    )
    new_themes = forms.CharField(
        label=_('Other themes:'),
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        required=False,
        strip=True,
        help_text=_('Add any themes that aren\'t listed above. Separate multiple entries with ";".'),
    )
    grades = forms.ModelMultipleChoiceField(
        SchoolGrade.objects.all(),
        label=_('School grades:'),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'list-unstyled checkbox'
        }),
        required=False,
        help_text=_('Select any fitting existing school grades.'),
    )
    new_grades = forms.CharField(
        label=_('Other school grades:'),
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        required=False,
        strip=True,
        help_text=_('Add any school grades that aren\'t listed above. Separate multiple entries with ";".'),
    )
    subjects = forms.ModelMultipleChoiceField(
        SchoolSubject.objects.all(),
        label=_('School subjects:'),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'list-unstyled checkbox'
        }),
        required=False,
        help_text=_('Select any fitting existing school subjects.'),
    )
    new_subjects = forms.CharField(
        label=_('Other school subjects:'),
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        required=False,
        strip=True,
        help_text=_('Add any school subjects that aren\'t listed above. Separate multiple entries with ";".'),
    )
    keywords = forms.CharField(
        label=_('Keywords:'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        required=False,
        strip=True,
        help_text=_('Separate multiple keywords with ";".'),
    )

    # Content fields
    abstract = forms.CharField(
        label=_('Abstract:'),
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': '4'
        }),
        required=True,
        strip=True,
    )

    # HTML fields
    content_objectives = html_content_field(_('Objectives:'))
    content_what = html_content_field(_('What was done:'))
    content_how = html_content_field(_('How it was done:'))
    content_who = html_content_field(_('Who participated:'))
    content_evaluation = html_content_field(_('How the learning was evaluated:'))
    content_materials = html_content_field(_('What materials were used:'))
    content_pros = html_content_field(_('Pros:'))
    content_cons = html_content_field(_('Cons:'))

    # Legal
    cc_license = forms.BooleanField(
        label=_('I am licensing this content under Creative Commons license.'),
        required=True,
    )
    photo_permission = forms.BooleanField(
        label=_(
            'I have the permission to publish the images associated to this case. I have the permission to use the '
            'images or I have the copyright to the images. People have given permission to publish the images they '
            'appear in.'
        ),
        required=True,
    )

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data['image'] and not cleaned_data['image_title']:
            # image and image_title are not required. If image does
            # exist image_title will be required.
            self.add_error('image_title', _('Image title is required if image exists.'))

        for field in self.cleaned_data:
            if 'content_' in field:
                cleaned_data[field] = strip_dangerous_html(cleaned_data[field])

        return cleaned_data

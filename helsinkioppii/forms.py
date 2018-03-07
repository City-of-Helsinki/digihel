from django import forms
from django.utils.translation import ugettext_lazy as _
from taggit.models import Tag

from helsinkioppii.utils import strip_dangerous_html
from helsinkioppii.fields import (
    get_case_form_gallery_image_fields, get_case_form_attachment_fields,
    get_case_form_link_fields, get_case_form_html_content_field
)
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


class CaseForm(forms.Form):
    GALLERY_IMAGE_COUNT = 8
    ATTACHMENT_COUNT = 5
    LINK_COUNT = 5

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
    content_objectives = get_case_form_html_content_field(_('Objectives:'))
    content_what = get_case_form_html_content_field(_('What was done:'))
    content_how = get_case_form_html_content_field(_('How it was done:'))
    content_who = get_case_form_html_content_field(_('Who participated:'))
    content_evaluation = get_case_form_html_content_field(_('How the learning was evaluated:'))
    content_materials = get_case_form_html_content_field(_('What materials were used:'))
    content_pros = get_case_form_html_content_field(_('Pros:'))
    content_cons = get_case_form_html_content_field(_('Cons:'))

    # Image gallery fields
    gallery_image_1, gallery_image_title_1 = get_case_form_gallery_image_fields(_('1.'))
    gallery_image_2, gallery_image_title_2 = get_case_form_gallery_image_fields(_('2.'))
    gallery_image_3, gallery_image_title_3 = get_case_form_gallery_image_fields(_('3.'))
    gallery_image_4, gallery_image_title_4 = get_case_form_gallery_image_fields(_('4.'))
    gallery_image_5, gallery_image_title_5 = get_case_form_gallery_image_fields(_('5.'))
    gallery_image_6, gallery_image_title_6 = get_case_form_gallery_image_fields(_('6.'))
    gallery_image_7, gallery_image_title_7 = get_case_form_gallery_image_fields(_('7.'))
    gallery_image_8, gallery_image_title_8 = get_case_form_gallery_image_fields(_('8.'))

    # Attachment fields
    attachment_file_1, attachment_title_1 = get_case_form_attachment_fields(_('1.'))
    attachment_file_2, attachment_title_2 = get_case_form_attachment_fields(_('2.'))
    attachment_file_3, attachment_title_3 = get_case_form_attachment_fields(_('3.'))
    attachment_file_4, attachment_title_4 = get_case_form_attachment_fields(_('4.'))
    attachment_file_5, attachment_title_5 = get_case_form_attachment_fields(_('5.'))

    # Sidebar link fields
    link_url_1, link_text_1, delete_link_1 = get_case_form_link_fields(_('1.'))
    link_url_2, link_text_2, delete_link_2 = get_case_form_link_fields(_('2.'))
    link_url_3, link_text_3, delete_link_3 = get_case_form_link_fields(_('3.'))
    link_url_4, link_text_4, delete_link_4 = get_case_form_link_fields(_('4.'))
    link_url_5, link_text_5, delete_link_5 = get_case_form_link_fields(_('5.'))

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

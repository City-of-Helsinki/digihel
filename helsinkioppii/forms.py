from django import forms
from django.utils.translation import ugettext_lazy as _
from taggit.models import Tag

from helsinkioppii.fields import (
    get_case_form_gallery_image_fields, get_case_form_attachment_fields,
    get_case_form_link_fields, get_case_form_html_content_field
)
from helsinkioppii.models.cases import Case, SchoolGrade, SchoolSubject, CaseTheme
from helsinkioppii.utils import humanized_range, strip_dangerous_html
from helsinkioppii.widgets import HelClearableImageInput


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
        label=_('Free search'),
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Search'),
        }),
    )
    themes = forms.ModelMultipleChoiceField(
        CaseTheme.objects.none(),  # Set in __init__
        label=_('Themes'),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'filter-keywordlist list-unstyled checkbox'
        }),
        required=False,
    )
    grades = forms.ModelMultipleChoiceField(
        SchoolGrade.objects.none(),  # Set in __init__
        label=_('Levels of education'),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'filter-keywordlist list-unstyled checkbox'
        }),
        required=False,
    )
    subjects = forms.ModelMultipleChoiceField(
        SchoolSubject.objects.none(),  # Set in __init__
        label=_('School subjects'),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'filter-keywordlist list-unstyled checkbox'
        }),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        self.language_code = kwargs.pop('language_code', 'fi')
        super().__init__(*args, **kwargs)

        # Override ModelMultipleChoiceField querysets for current locale
        self.fields['themes'].queryset = CaseTheme.objects.filter(language_code=self.language_code)
        self.fields['grades'].queryset = SchoolGrade.objects.filter(language_code=self.language_code)
        self.fields['subjects'].queryset = SchoolSubject.objects.filter(language_code=self.language_code)


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
        widget=HelClearableImageInput(),
        required=False
    )
    image_title = forms.CharField(
        label=_('Image title:'),
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        required=True,
        strip=True,
    )

    # Meta fields
    school = forms.CharField(
        label=_('Educational institution:'),
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        required=True,
        strip=True,
    )
    themes = forms.ModelMultipleChoiceField(
        CaseTheme.objects.none(),  # Set in __init__
        label=_('Themes:'),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'list-unstyled checkbox'
        }),
        required=True,
        help_text=_('Select any fitting themes.'),
    )
    grades = forms.ModelMultipleChoiceField(
        SchoolGrade.objects.none(),  # Set in __init__
        label=_('Levels of education:'),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'list-unstyled checkbox'
        }),
        required=True,
        help_text=_('Select any fitting levels of education.'),
    )
    subjects = forms.ModelMultipleChoiceField(
        SchoolSubject.objects.none(),  # Set in __init__
        label=_('School subjects:'),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'list-unstyled checkbox'
        }),
        required=False,
        help_text=_('Select any fitting school subjects.'),
    )
    keywords = forms.CharField(
        label=_('Keywords:'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        required=True,
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
    content_objectives = get_case_form_html_content_field(_('Objectives:'), help_text=_('Please format your text using bullet points.'))
    content_what = get_case_form_html_content_field(_('What was done:'))
    content_how = get_case_form_html_content_field(_('How it was done:'))
    content_who = get_case_form_html_content_field(_('Participants:'))
    content_evaluation = get_case_form_html_content_field(_('Evaluation:'), help_text=_('Please format your text using bullet points.'))
    content_materials = get_case_form_html_content_field(_('Materials:'), help_text=_('Please format your text using bullet points.'))
    content_pros = get_case_form_html_content_field(_('Pros:'), help_text=_('Please format your text using bullet points.'))
    content_cons = get_case_form_html_content_field(_('Cons:'), help_text=_('Please format your text using bullet points.'))

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

    def __init__(self, *args, **kwargs):
        self.language_code = kwargs.pop('language_code', 'fi')
        super().__init__(*args, **kwargs)

        # Override ModelMultipleChoiceField querysets for current locale
        self.fields['themes'].queryset = CaseTheme.objects.filter(language_code=self.language_code)
        self.fields['grades'].queryset = SchoolGrade.objects.filter(language_code=self.language_code)
        self.fields['subjects'].queryset = SchoolSubject.objects.filter(language_code=self.language_code)

    def clean(self):
        cleaned_data = super().clean()

        file_index = url_index = 0
        title_index = text_index = 1
        image_fields = [('image', 'image_title')]
        attachment_fields = []
        link_fields = []

        # Populate `image_fields` with all gallery image fields
        for i in humanized_range(1, self.GALLERY_IMAGE_COUNT):
            image_fields.append(
                ('gallery_image_{i}'.format(i=i), 'gallery_image_title_{i}'.format(i=i))
            )

        # Populate `attachment_fields` with all attachment fields on the form
        for i in humanized_range(1, self.ATTACHMENT_COUNT):
            attachment_fields.append(
                ('attachment_file_{i}'.format(i=i), 'attachment_title_{i}'.format(i=i))
            )

        for i in humanized_range(1, self.LINK_COUNT):
            link_fields.append(
                ('link_url_{i}'.format(i=i), 'link_text_{i}'.format(i=i))
            )

        for fields in image_fields:
            if cleaned_data.get(fields[file_index]) and not cleaned_data.get(fields[title_index]):
                # image and image_title are not required. If image does
                # exist image_title will be required.
                self.add_error(fields[title_index], _('Title is required if image exists.'))

        for fields in attachment_fields:
            if cleaned_data.get(fields[file_index]) and not cleaned_data.get(fields[title_index]):
                # attachments and attachment titles are not required. If
                # attachment does exist attachment_title will be required.
                self.add_error(fields[title_index], _('Title is required if attachment exists.'))

        for fields in link_fields:
            if cleaned_data.get(fields[url_index]) and not cleaned_data.get(fields[text_index]):
                # link_url and link_text are not required. If link url does
                # exist link_text will be required.
                self.add_error(fields[text_index], _('Link text is required if link exists.'))

        for field in cleaned_data:
            if 'content_' in field:
                cleaned_data[field] = strip_dangerous_html(cleaned_data[field])

        return cleaned_data

from django import forms
from django.utils.translation import ugettext_lazy as _

from helsinkioppii.widgets import HelClearableFileInput, HelClearableImageInput


def get_case_form_html_content_field(label, help_text=''):
    """
    Return field for html content.
    """
    return forms.CharField(
        label=label,
        widget=forms.Textarea(attrs={
            'rows': '8'
        }),
        required=False,
        strip=True,
        help_text=help_text,
    )


def get_case_form_gallery_image_fields(label_ordinal):
    """
    Return field for image and image title.
    """
    image_field = forms.ImageField(
        label=_('%s gallery image:') % label_ordinal,
        widget=HelClearableImageInput(),
        required=False,
    )
    title_field = forms.CharField(
        label=_('%s gallery image title:') % label_ordinal,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        required=False,
        strip=True,
    )
    return image_field, title_field


def get_case_form_attachment_fields(label_ordinal):
    """
    Return field for file and file title.
    """
    file_field = forms.FileField(
        label=_('%s attachment:') % label_ordinal,
        widget=HelClearableFileInput(),
        required=False,
    )
    title_field = forms.CharField(
        label=_('%s attachment title:') % label_ordinal,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        required=False,
        strip=True,
    )
    return file_field, title_field


def get_case_form_link_fields(label_ordinal):
    """
    Return field for link url, link text, and delete selection.
    """
    url_field = forms.URLField(
        label=_('%s sidebar link url:') % label_ordinal,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        required=False,
    )
    text_field = forms.CharField(
        label=_('%s sidebar link text:') % label_ordinal,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        required=False,
        strip=True,
    )
    delete_field = forms.BooleanField(
        label=_('Delete'),
        required=False,
    )
    return url_field, text_field, delete_field

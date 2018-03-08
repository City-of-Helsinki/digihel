from django.forms import ClearableFileInput


class HelClearableFileInput(ClearableFileInput):
    template_name = 'helsinkioppii/widgets/clearable_file_input.html'


class HelClearableImageInput(ClearableFileInput):
    template_name = 'helsinkioppii/widgets/clearable_image_input.html'

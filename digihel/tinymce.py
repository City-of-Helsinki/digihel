import json

from wagtailtinymce.rich_text import TinyMCERichTextArea


class DigiHelTinyMCERichTextArea(TinyMCERichTextArea):
    plugins = [
        'advlist',
        'anchor',
        'autolink',
        'charmap',
        'code',
        'codesample',
        'contextmenu',
        'directionality',
        'emoticons',
        'fullscreen',
        'hr',
        'image',
        'imagetools',
        'insertdatetime',
        'link',
        'lists',
        'media',
        'nonbreaking',
        'pagebreak',
        'paste',
        'preview',
        'print',
        'searchreplace',
        'table',
        'template',
        'textpattern',
        'visualblocks',
        'visualchars',
        'wordcount',
    ]
    default_buttons = [
        [
            ['undo', 'redo'],
            ['styleselect'],
            ['bold', 'italic', 'termspan'],
            ['bullist', 'numlist', 'outdent', 'indent'],
            ['table'],
            ['link', 'unlink'],
            ['wagtaildoclink', 'wagtailimage', 'wagtailembed'],
            ['pastetext', 'fullscreen'],
            ['termspan'],
        ],
    ]
    default_options = {
        'image_advtab': True,
        'browser_spellcheck': True,
        'noneditable_leave_contenteditable': True,
        'language': 'en',
        'language_load': True,
        'content_css': [
            # add static URLs here?
        ]
    }

    def build_js_init_arguments(self):
        args = super(DigiHelTinyMCERichTextArea, self).build_js_init_arguments()
        args.update(
            plugins=self.plugins,
        )
        args.pop('menubar', None)  # Always enable the menubar
        return args

import json

from django.templatetags.static import static

from wagtailtinymce.rich_text import TinyMCERichTextArea


class DigiHelTinyMCERichTextArea(TinyMCERichTextArea):
    plugins = [
        'anchor',
        'autolink',
        'charmap',
        'code',
        'codesample',
        'contextmenu',
        'definitionlist',
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
    style_formats = [
        {
            'title': 'Additional info',
            'block': 'div',
            'classes': 'more-info'
        }
    ]
    default_buttons = [
        [
            ['undo', 'redo'],
            ['styleselect'],
            ['bold', 'italic'],
            ['bullist', 'numlist', 'ToggleDefinitionList', 'ToggleDefinitionItem', 'outdent', 'indent'],
            ['table'],
            ['link', 'unlink'],
            ['wagtaildoclink', 'wagtailimage', 'wagtailembed'],
            ['pastetext', 'fullscreen'],
            ['termlink'],
        ],
    ]
    default_options = {
        'image_advtab': True,
        'browser_spellcheck': True,
        'noneditable_leave_contenteditable': True,
        'language': 'en',
        'language_load': True,
        'content_css': []
    }

    def build_js_init_arguments(self):
        args = super(DigiHelTinyMCERichTextArea, self).build_js_init_arguments()
        args.update(
            plugins=self.plugins,
        )
        args.pop('menubar', None)  # Always enable the menubar
        args['content_css'].append(static('css/tinymce-content.css'))
        args['skin'] = 'wagtail'
        args['height'] = 600
        args['style_formats'] = [
            {'title': 'Additional info','block': 'section','classes': 'more-info', 'wrapper': 'true'},
            {'title': 'Document link','inline': 'span','classes': 'document-link'},
        ]
        args['style_formats_merge'] = True
        args['extended_valid_elements'] = 'div[class]'
        return args

    @classmethod
    def getDefaultArgs(cls):
        args = super(DigiHelTinyMCERichTextArea, cls).getDefaultArgs()
        args['options'] = cls.default_options
        args['height'] = 600
        args['style_formats'] = [
            {'title': 'Additional info', 'block': 'section', 'classes': 'more-info', 'wrapper': 'true'},
            {'title': 'Document link', 'inline': 'span', 'classes': 'document-link'},
        ]
        args['style_formats_merge'] = True
        args['extended_valid_elements'] = 'div[class]'
        args['plugins'] = cls.plugins
        return args

    def render_js_init(self, id_, name, value):
        kwargs = self.kwargs.copy()

        if 'buttons' in self.kwargs:
            if self.kwargs['buttons'] is False:
                kwargs['toolbar'] = False
            else:
                kwargs['toolbar'] = [
                    ' | '.join([' '.join(groups) for groups in rows])
                    for rows in self.kwargs['buttons']
                ]

        if 'menus' in self.kwargs:
            if self.kwargs['menus'] is False:
                kwargs['menubar'] = False
            else:
                kwargs['menubar'] = ' '.join(self.kwargs['menus'])

        if 'passthru_init_keys' in self.kwargs:
            kwargs.update(self.kwargs['passthru_init_keys'])

        if 'table' in self.kwargs:
            for key, values in self.kwargs['table'].items():
                kwargs[f'table_{key}'] = values

        kwargs.pop('menubar', None)

        return "makeTinyMCEEditable({0}, {1});".format(json.dumps(id_), json.dumps(kwargs))
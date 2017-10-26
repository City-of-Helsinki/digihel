from wagtail.wagtailcore import blocks

ICONS = (
    ('icon-signpost', 'signpost'),
    ('icon-lifering', 'lifering'),
    ('icon-info', 'info'),
)


class BannerLiftBlock(blocks.StructBlock):
    TEMPLATE_VAR = 'block'

    icon = blocks.ChoiceBlock(choices=ICONS)
    abstract = blocks.TextBlock(max_length=225)
    page = blocks.PageChooserBlock()

    class Meta:
        template = 'helsinkioppii/blocks/banner_lift.html'
        icon = 'openquote'

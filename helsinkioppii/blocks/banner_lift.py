from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock

class BannerLiftBlock(blocks.StructBlock):
    TEMPLATE_VAR = 'block'
    icon = ImageChooserBlock(required=False)
    title = blocks.CharBlock(max_length=120)
    abstract = blocks.TextBlock(max_length=225)
    page = blocks.PageChooserBlock()

    class Meta:
        template = 'helsinkioppii/blocks/banner_lift.html'
        icon = 'openquote'

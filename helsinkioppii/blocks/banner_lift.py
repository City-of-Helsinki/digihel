from django.utils.translation import ugettext_lazy as _
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock

class BannerLiftBlock(blocks.StructBlock):
    TEMPLATE_VAR = 'block'
    icon = ImageChooserBlock(required=False)
    title = blocks.CharBlock(max_length=120)
    abstract = blocks.TextBlock(max_length=225)
    page_link = blocks.PageChooserBlock(required=False)
    external_link = blocks.URLBlock(help_text=_('Overrides page link if set.'), required=False)

    class Meta:
        template = 'helsinkioppii/blocks/banner_lift.html'
        icon = 'openquote'

    def get_context(self, value, parent_context=None):
        context = super(BannerLiftBlock, self).get_context(value, parent_context)
        context['block_link_url'] = self.get_link_url(value)
        return context

    def get_link_url(self, instance):
        url = ''
        if instance['external_link']:
            url = instance['external_link']
        elif instance['page_link']:
            url = instance['page_link'].url
        return url

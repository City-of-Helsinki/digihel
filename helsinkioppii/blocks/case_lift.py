from wagtail.wagtailcore import blocks

from helsinkioppii.models.cases import Case


class CaseLiftBlock(blocks.StructBlock):
    TEMPLATE_VAR = 'block'

    case = blocks.PageChooserBlock(target_model=Case)

    class Meta:
        template = 'helsinkioppii/blocks/case_lift.html'
        icon = 'openquote'

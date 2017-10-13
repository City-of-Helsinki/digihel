from wagtail.wagtailcore import blocks

from helsinkioppii.models.cases import Case

ICONS = (
    ('icon-signpost', 'signpost'),
    ('icon-lifering', 'lifering'),
    ('icon-info', 'info'),
)


class CaseLiftBlock(blocks.StructBlock):
    TEMPLATE_VAR = 'block'

    icon = blocks.ChoiceBlock(choices=ICONS)
    case = blocks.PageChooserBlock(target_model=Case)

    class Meta:
        template = 'helsinkioppii/blocks/case_lift.html'
        icon = 'openquote'

from wagtail.wagtailcore import blocks


class TrainingLiftBlock(blocks.StructBlock):
    TEMPLATE_VAR = 'block'

    title = blocks.CharBlock(max_length=120, required=True)
    time = blocks.DateTimeBlock(required=False)
    description = blocks.TextBlock(required=False)
    link = blocks.URLBlock(required=True)

    class Meta:
        template = 'helsinkioppii/blocks/training_lift.html'
        icon = 'openquote'

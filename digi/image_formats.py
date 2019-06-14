from wagtail.images.formats import FORMATS

# Monkey patch the default formats to always use the
# original image instead of a width-constrained version.
for f in FORMATS:
    if f.name == 'fullwidth':
        f.filter_spec = 'original'

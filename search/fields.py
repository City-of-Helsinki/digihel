from wagtail.wagtailsearch import index

tag_search_field = index.RelatedFields('tags', [
    index.SearchField('name'),
])

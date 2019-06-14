from wagtail.search import index

tag_search_field = index.RelatedFields('tags', [
    index.SearchField('name'),
])

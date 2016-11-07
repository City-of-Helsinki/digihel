from search.fields import tag_search_field


def patch_blog_page_search():
    from blog.models import BlogPage
    BlogPage.search_fields = list(BlogPage.search_fields) + [
        tag_search_field,
    ]

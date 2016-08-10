from django.shortcuts import render


def list_children(page):
    html = '<ul><li><a href="{url}">{title}</a></li>'.format(url=page.url, title=page.title)
    children = page.get_children().live().public().order_by('path')
    for child in children:
        html += list_children(child)
    html += '</ul>'
    return html


def sitemap_view(request):
    root_page = request.site.root_page

    html = list_children(root_page)

    return render(request, 'sitemap.html', {'sitemap_html': html})

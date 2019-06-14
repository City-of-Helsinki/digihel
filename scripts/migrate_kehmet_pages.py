from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction
from wagtail.core.models import Page

from content.models import ContentPage
from kehmet.models import KehmetContentPage, KehmetFrontPage

cp_type = ContentType.objects.get_for_model(ContentPage)

k_root = Page.objects.get(url_path='/digietu/kehmet/')
pages = k_root.get_descendants().type(ContentPage)

dummy_page = Page(title="dummy", path="1234", slug="dummy-slug", depth=1)


def convert_page(page, target_model):
    try:
        page.kehmetcontentpage
        return
    except:
        pass

    kcp_type = ContentType.objects.get_for_model(target_model)
    cp_page = page.specific
    kcp_page = target_model(body=cp_page.body, page_ptr=page)
    for f in kcp_page._meta.fields:
        setattr(kcp_page, f.name, getattr(cp_page, f.name))
    super(Page, kcp_page).save()

    for f in dummy_page._meta.fields:
        setattr(cp_page, f.name, getattr(dummy_page, f.name))
    cp_page.page_ptr_id = dummy_page.id
    cp_page.save()
    print(page)
    models.Model.delete(cp_page, keep_parents=True)

    page.content_type = kcp_type
    page.save(update_fields=['content_type'])


with transaction.atomic():
    dummy_page.save()
    if not isinstance(k_root, KehmetFrontPage):
        convert_page(k_root, KehmetFrontPage)
    for page in pages:
        convert_page(page, KehmetContentPage)
    p = Page.objects.get(id=dummy_page.id)
    p.delete()

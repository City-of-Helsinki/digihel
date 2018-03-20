from django.db import models
from django.http import HttpResponseRedirect
from django.utils import translation
from wagtail.wagtailadmin.edit_handlers import PageChooserPanel
from wagtail.wagtailcore.models import Page


class LanguageRedirectionPage(Page):

    def serve(self, request):
        language = translation.get_language_from_request(request)

        # Index pages are located at depth 3 with slug being one of the
        # available language codes.
        if not Page.objects.live().filter(slug=language, depth=3).exists():
            language = 'fi'  # Default to finnish

        url = '{url}{language}/'.format(
            url=self.url,
            language=language,
        )

        return HttpResponseRedirect(url)


class TranslatablePageMixin(models.Model):
    swedish_link = models.ForeignKey(
        Page,
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
        related_name='+'
    )
    english_link = models.ForeignKey(
        Page,
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
        related_name='+'
    )

    panels = [
        PageChooserPanel('swedish_link'),
        PageChooserPanel('english_link'),
    ]

    def get_language(self):
        """
        Returns the language code for this page.
        """
        # Look through ancestors of this page for its language homepage
        # The language homepage is located at depth 3
        language_homepage = self.get_ancestors(inclusive=True).get(depth=3)

        # The slug of language homepages are enforced to be set to the language code
        return language_homepage.slug

    def get_linked_page_for_language_code(self, lang_code):
        if lang_code == 'fi':
            return self.finnish_page()
        elif lang_code == 'en':
            return self.english_page()
        elif lang_code == 'sv':
            return self.swedish_page()

    def finnish_page(self):
        """
        Return the finnish version of this page
        """
        language = self.get_language()

        if language == 'fi':
            return self
        elif language == 'sv':
            return type(self).objects.filter(swedish_link=self).first().specific
        elif language == 'en':
            return type(self).objects.filter(english_link=self).first().specific

    def english_page(self):
        """
        Return the english version of this page
        """
        finnish_page = self.finnish_page()

        if finnish_page and finnish_page.english_link:
            return finnish_page.english_link.specific

    def swedish_page(self):
        """
        Return the swedish version of this page
        """
        finnish_page = self.finnish_page()

        if finnish_page and finnish_page.swedish_link:
            return finnish_page.swedish_link.specific

    class Meta:
        abstract = True

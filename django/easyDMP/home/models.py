from django.db import models


from wagtail.models import Page
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
)
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    register_setting,
)

@register_setting
class NavigationSettings(BaseGenericSetting):
    twitter_url = models.URLField(verbose_name="Twitter URL", blank=True) # TODO: Change this!
    github_url = models.URLField(verbose_name="GitHub URL", blank=True)
    github_icon = models.ImageField(upload_to='icons', blank=True)
    panels = [
        MultiFieldPanel(
            [
                FieldPanel("twitter_url"),
                FieldPanel("github_url"),
                FieldPanel("github_icon"),
            ],
            "Social settings",
        )
    ]


class HomePage(Page):
    pass

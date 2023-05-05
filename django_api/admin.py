from django.contrib import admin
from django_api import models


class AdAdmin(admin.ModelAdmin):
    """
    Настройки отображения, фильтрации и поиска модели:'Ad' на панели администратора
    """

    list_display = (
        "seller",
        "title",
        "description",
        "price",
        "image",

        'flag_good',
        'updated',
        "created",
    )
    list_display_links = (
        "title",
    )
    list_editable = (
        'flag_good',
    )
    list_filter = (
        "seller",
        "title",
        "description",
        "price",
        "image",

        'flag_good',
        'updated',
        "created",
    )
    # filter_horizontal = (
    #     'users',
    # )
    fieldsets = (
        (
            "Основное",
            {
                "fields": (
                    "seller",
                    "title",
                    "description",
                    "price",
                    "image",
                )
            },
        ),
        (
            "Техническое",
            {
                "fields": (
                    'flag_good',
                    'updated',
                    "created",
                )
            },
        ),
    )
    search_fields = [
        "seller",
        "title",
        "description",
    ]


admin.site.register(models.Ad, AdAdmin)

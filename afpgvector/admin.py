from datetime import datetime

from django.contrib import admin
from django.utils.html import format_html

from afpgvector.models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    using = "vector"
    search_fields = ("metadata__title", "content")
    list_display = ("get_title", "get_url", "hash_id", "get_pd")
    readonly_fields = ("content", "metadata", "embedding", "hash_id", "created_at")

    def get_title(self, obj):
        return obj.metadata.get("title")

    def get_url(self, obj):
        url = obj.metadata.get("url")
        if url:
            return format_html(f"<a href='{url}' target=_blank>{url}</a>")

    def get_pd(self, obj):
        pd = obj.metadata.get("pd")
        if pd:
            return datetime.strptime(pd, "%Y-%m-%dT%H:%M:%S%z")

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(
            db_field, request, using=self.using, **kwargs
        )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(
            db_field, request, using=self.using, **kwargs
        )

    get_title.short_description = "Title"
    get_url.short_description = "URL"
    get_pd.short_description = "Publication date"

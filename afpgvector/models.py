from django.conf import settings
from django.db import models
from pgvector.django import CosineDistance, VectorField


class Document(models.Model):
    class Meta:
        managed = False
        app_label = "afpgvector"
        db_table = "documents"
        ordering = ("-created_at",)

    id = models.IntegerField(primary_key=True)
    content = models.TextField()
    metadata = models.JSONField()
    embedding = VectorField(dimensions=1536)
    hash_id = models.CharField(max_length=32)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.metadata.get("title")

    @classmethod
    def query(cls, embedding, n_results, score_threshold):
        print("Querying Postgres Vector DB...")
        return cls.objects.using("vector").annotate(
            distance=CosineDistance("embedding", embedding)
        ).defer("embedding", "hash_id", "created_at").filter(
            distance__lte=score_threshold
        ).order_by("distance")[:n_results]

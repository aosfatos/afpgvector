from hashlib import md5

from django.db import models
from django.utils import timezone
from pgvector.django import CosineDistance, VectorField


class Document(models.Model):
    class Meta:
        managed = False
        app_label = "afpgvector"
        db_table = "documents"
        ordering = ("-created_at",)

    id = models.BigAutoField(primary_key=True, editable=False)
    content = models.TextField()
    metadata = models.JSONField()
    embedding = VectorField(dimensions=1536)
    hash_id = models.CharField(max_length=32)
    created_at = models.DateTimeField(default=timezone.now())

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

    @classmethod
    def insert(cls, embedding, content, metadata):
        print("Inserting data on Postgres Vector DB...")
        hash_id = md5(content.encode()).hexdigest()
        return cls.objects.using("vector").create(
            content=content,
            embedding=embedding,
            metadata=metadata,
            hash_id=hash_id,
        )

    @classmethod
    def delete_from_url(cls, url):
        documents = cls.objects.using("vector").filter(metadata__url=url)
        print(f"Deleting {documents.count()} embedding vectors...")
        documents.delete()
        print("Done!")

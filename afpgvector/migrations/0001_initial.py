from django.db import migrations, models
import pgvector


class Migration(migrations.Migration):
    operations = [
        pgvector.django.VectorExtension(),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('metadata', models.JSONField()),
                ('embedding', pgvector.django.VectorField(dimensions=1536)),
                ('hash_id', models.CharField(max_length=32)),
                ('created_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'documents',
                'ordering': ('-created_at',),
                'managed': False,
            },
        ),
    ]

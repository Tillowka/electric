from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("works", "0002_remove_work_is_published")]

    operations = [
        migrations.CreateModel(
            name="SiteVisitor",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("visitor_key", models.CharField(max_length=64, unique=True, verbose_name="Идентификатор посетителя")),
                ("first_seen", models.DateTimeField(auto_now_add=True, verbose_name="Первое посещение")),
                ("last_seen", models.DateTimeField(db_index=True, verbose_name="Последняя активность")),
            ],
            options={"verbose_name": "Посетитель сайта", "verbose_name_plural": "Посетители сайта"},
        ),
    ]

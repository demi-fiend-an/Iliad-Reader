from django.db import migrations, models
import django.db.models.deletion


def attach_old_annotations_to_english(apps, schema_editor):
    QuizSong = apps.get_model("main", "QuizSong")
    Annotation = apps.get_model("main", "Annotation")

    english_song = QuizSong.objects.filter(number=1, language="en").first()
    if english_song is None:
        english_song = QuizSong.objects.create(
            number=1,
            language="en",
            title="Book I",
            text_html="",
        )

    # The original project had one global Annotation table and one English
    # reader. Those existing annotations therefore belong to English Book I.
    Annotation.objects.filter(song__isnull=True).update(song=english_song)


def reverse_annotations(apps, schema_editor):
    Annotation = apps.get_model("main", "Annotation")
    Annotation.objects.update(song=None)


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0002_quiz"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quizsong",
            name="number",
            field=models.PositiveIntegerField(verbose_name="Номер песни"),
        ),
        migrations.AddField(
            model_name="quizsong",
            name="language",
            field=models.CharField(
                choices=[
                    ("en", "English"),
                    ("ru", "Русский"),
                    ("kk", "Қазақша"),
                ],
                default="en",
                max_length=2,
                verbose_name="Язык версии",
            ),
        ),
        migrations.AddField(
            model_name="quizsong",
            name="text_html",
            field=models.TextField(
                blank=True,
                help_text=(
                    "Для английской версии можно оставить пустым, чтобы использовать "
                    "сохранённый текст Book I. Для русского и казахского вставьте сюда "
                    "текст в HTML, используя span class=\"clickable\" data-target=\"ID\" "
                    "для слов с аннотациями."
                ),
                verbose_name="Текст песни (HTML)",
            ),
        ),
        migrations.AddField(
            model_name="annotation",
            name="song",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="annotations",
                to="main.quizsong",
                verbose_name="Версия песни",
            ),
        ),
        migrations.AlterField(
            model_name="annotation",
            name="html_id",
            field=models.CharField(max_length=100, verbose_name="ID элемента в HTML"),
        ),
        migrations.RunPython(
            attach_old_annotations_to_english,
            reverse_annotations,
        ),
        migrations.AlterField(
            model_name="annotation",
            name="song",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="annotations",
                to="main.quizsong",
                verbose_name="Версия песни",
            ),
        ),
        migrations.AlterModelOptions(
            name="quizsong",
            options={
                "ordering": ["number", "language"],
                "verbose_name": "Версия песни",
                "verbose_name_plural": "Версии песен",
            },
        ),
        migrations.AlterModelOptions(
            name="quizquestion",
            options={
                "ordering": ["order"],
                "verbose_name": "Вопрос теста",
                "verbose_name_plural": "Вопросы теста",
            },
        ),
        migrations.AlterModelOptions(
            name="annotation",
            options={
                "verbose_name": "Аннотация",
                "verbose_name_plural": "Аннотации",
            },
        ),
        migrations.AddConstraint(
            model_name="quizsong",
            constraint=models.UniqueConstraint(
                fields=("number", "language"),
                name="unique_song_version_language",
            ),
        ),
        migrations.AddConstraint(
            model_name="annotation",
            constraint=models.UniqueConstraint(
                fields=("song", "html_id"),
                name="unique_annotation_id_per_song",
            ),
        ),
    ]

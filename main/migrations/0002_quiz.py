from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="QuizSong",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "number",
                    models.PositiveIntegerField(
                        unique=True,
                        verbose_name="Номер песни",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        max_length=200,
                        verbose_name="Название песни",
                    ),
                ),
            ],
            options={
                "verbose_name": "Песня теста",
                "verbose_name_plural": "Песни теста",
                "ordering": ["number"],
            },
        ),
        migrations.CreateModel(
            name="QuizQuestion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "order",
                    models.PositiveIntegerField(
                        verbose_name="Номер вопроса",
                    ),
                ),
                (
                    "question",
                    models.TextField(verbose_name="Текст вопроса"),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="quiz/",
                        verbose_name="Картинка",
                    ),
                ),
                (
                    "option_a",
                    models.CharField(
                        max_length=500,
                        verbose_name="Вариант A",
                    ),
                ),
                (
                    "option_b",
                    models.CharField(
                        max_length=500,
                        verbose_name="Вариант B",
                    ),
                ),
                (
                    "option_c",
                    models.CharField(
                        max_length=500,
                        verbose_name="Вариант C",
                    ),
                ),
                (
                    "option_d",
                    models.CharField(
                        max_length=500,
                        verbose_name="Вариант D",
                    ),
                ),
                (
                    "correct_option",
                    models.CharField(
                        choices=[
                            ("a", "Вариант A"),
                            ("b", "Вариант B"),
                            ("c", "Вариант C"),
                            ("d", "Вариант D"),
                        ],
                        max_length=1,
                        verbose_name="Правильный вариант",
                    ),
                ),
                (
                    "song",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="questions",
                        to="main.quizsong",
                        verbose_name="Песня",
                    ),
                ),
            ],
            options={
                "verbose_name": "Вопрос теста",
                "verbose_name_plural": "Вопросы теста",
                "ordering": ["song__number", "order"],
            },
        ),
        migrations.AddConstraint(
            model_name="quizquestion",
            constraint=models.UniqueConstraint(
                fields=("song", "order"),
                name="unique_question_order_in_song",
            ),
        ),
    ]

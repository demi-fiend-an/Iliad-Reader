from django.db import models


class QuizSong(models.Model):
    LANGUAGE_CHOICES = [
        ("en", "English"),
        ("ru", "Русский"),
        ("kk", "Қазақша"),
    ]

    number = models.PositiveIntegerField(verbose_name="Номер песни")
    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default="en",
        verbose_name="Язык версии",
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Название песни",
    )
    text_html = models.TextField(
        blank=True,
        verbose_name="Текст песни (HTML)",
        help_text=(
            "Для английской версии можно оставить пустым, чтобы использовать "
            "сохранённый текст Book I. Для русского и казахского вставьте сюда "
            "текст в HTML, используя span class=\"clickable\" data-target=\"ID\" "
            "для слов с аннотациями."
        ),
    )

    class Meta:
        ordering = ["number", "language"]
        constraints = [
            models.UniqueConstraint(
                fields=["number", "language"],
                name="unique_song_version_language",
            )
        ]
        verbose_name = "Версия песни"
        verbose_name_plural = "Версии песен"

    def __str__(self):
        return f"Песнь {self.number} — {self.get_language_display()}: {self.title}"


class Annotation(models.Model):
    song = models.ForeignKey(
        QuizSong,
        on_delete=models.CASCADE,
        related_name="annotations",
        null=True,
        blank=True,
        verbose_name="Версия песни",
    )
    html_id = models.CharField(
        max_length=100,
        verbose_name="ID элемента в HTML",
    )
    title = models.CharField(max_length=200, verbose_name="Заголовок аннотации")
    commentary = models.TextField(verbose_name="Текст комментария")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["song", "html_id"],
                name="unique_annotation_id_per_song",
            )
        ]
        verbose_name = "Аннотация"
        verbose_name_plural = "Аннотации"

    def __str__(self):
        language = self.song.get_language_display() if self.song else "без версии"
        return f"{self.html_id} — {language} — {self.title}"


class QuizQuestion(models.Model):
    OPTION_CHOICES = [
        ("a", "Вариант A"),
        ("b", "Вариант B"),
        ("c", "Вариант C"),
        ("d", "Вариант D"),
    ]

    song = models.ForeignKey(
        QuizSong,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name="Версия песни",
    )
    order = models.PositiveIntegerField(verbose_name="Номер вопроса")
    question = models.TextField(verbose_name="Текст вопроса")
    image = models.ImageField(
        upload_to="quiz/",
        blank=True,
        null=True,
        verbose_name="Картинка",
    )

    option_a = models.CharField(max_length=500, verbose_name="Вариант A")
    option_b = models.CharField(max_length=500, verbose_name="Вариант B")
    option_c = models.CharField(max_length=500, verbose_name="Вариант C")
    option_d = models.CharField(max_length=500, verbose_name="Вариант D")

    correct_option = models.CharField(
        max_length=1,
        choices=OPTION_CHOICES,
        verbose_name="Правильный вариант",
    )

    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(
                fields=["song", "order"],
                name="unique_question_order_in_song_version",
            )
        ]
        verbose_name = "Вопрос теста"
        verbose_name_plural = "Вопросы теста"

    def __str__(self):
        return (
            f"Песнь {self.song.number} — "
            f"{self.song.get_language_display()} — вопрос {self.order}"
        )

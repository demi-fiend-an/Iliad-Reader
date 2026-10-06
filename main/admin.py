from django.contrib import admin

from .models import Annotation, QuizQuestion, QuizSong


class AnnotationInline(admin.TabularInline):
    model = Annotation
    extra = 1
    fields = ("html_id", "title", "commentary")


class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestion
    extra = 1
    fields = (
        "order",
        "question",
        "image",
        "option_a",
        "option_b",
        "option_c",
        "option_d",
        "correct_option",
    )


@admin.register(QuizSong)
class QuizSongAdmin(admin.ModelAdmin):
    list_display = ("number", "language", "title")
    list_filter = ("language", "number")
    ordering = ("number", "language")
    inlines = [AnnotationInline, QuizQuestionInline]
    fieldsets = (
        (
            "Версия песни",
            {
                "fields": ("number", "language", "title", "text_html"),
            },
        ),
    )


@admin.register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    list_display = ("song", "html_id", "title")
    list_filter = ("song__language", "song__number")
    search_fields = ("html_id", "title", "commentary")


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ("song", "order", "question", "correct_option")
    list_filter = ("song__language", "song__number")
    ordering = ("song__number", "song__language", "order")

"""URL configuration for iliad project."""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from main import views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Reader: English remains the default URL, while Russian and Kazakh
    # have their own language-specific pages.
    path("", views.iliad_page, {"language": "en"}, name="home"),
    path("reader/<str:language>/", views.iliad_page, {"song_number": 1}, name="reader_language"),
    path(
        "reader/<str:language>/<int:song_number>/",
        views.iliad_page,
        name="reader_song",
    ),

    # Quiz for each independent language version.
    path("quiz/", views.quiz_home, {"language": "en"}, name="quiz_home"),
    path("quiz/<str:language>/", views.quiz_home, name="quiz_home_language"),
    path(
        "quiz/<str:language>/<int:song_number>/",
        views.quiz_song,
        name="quiz_song",
    ),
    path(
        "quiz/<str:language>/<int:song_number>/reset/",
        views.quiz_reset,
        name="quiz_reset",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

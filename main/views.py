from django.shortcuts import get_object_or_404, redirect, render

from .models import QuizQuestion, QuizSong


PASS_PERCENT = 85
SUPPORTED_LANGUAGES = {"en", "ru", "kk"}

LANGUAGE_NAMES = {
    "en": "English",
    "ru": "Русский",
    "kk": "Қазақша",
}

INTERFACE_TEXT = {
    "en": {
        "iliad": "The Iliad",
        "book": "Book",
        "song": "Song",
        "read_song": "Read Song",
        "take_quiz": "Take the quiz",
        "back": "Back",
        "back_to_iliad": "Back to the Iliad",
        "back_to_quiz": "Back to quiz",
        "all_songs": "All songs",
        "language": "Language",
        "annotations": "Annotation panel",
        "select_annotation": "Select an annotated word or phrase to read its note.",
        "text_missing": "The text for this language has not been added yet. Add it in Django Admin → Song Versions.",
        "quiz": "The Iliad — Quiz",
        "quiz_subtitle": "Answer each question immediately. Your score is calculated after every answer. You need more than {pass_percent}% to unlock the next song.",
        "start": "Start",
        "no_quiz_questions": "No quiz questions have been added yet.",
        "score": "Score",
        "questions": "Questions",
        "answer": "Answer",
        "correct": "Correct ✓",
        "correct_text": "You got this question right.",
        "incorrect": "Incorrect ✕",
        "correct_answer": "The correct answer was:",
        "already_answered": "Already answered",
        "already_answered_text": "This question has already been counted in your score.",
        "previous": "Previous",
        "next_question": "Next question",
        "next_song": "Next song",
        "need_more": "You need more than {pass_percent}% to unlock the next song.",
        "song_complete": "Song complete",
        "final_score": "Your final score:",
        "passed": "You passed. The next song is unlocked.",
        "failed": "You did not get more than {pass_percent}%. You can retry the song.",
        "retry": "Retry this song",
        "song_locked": "Song locked",
        "locked_message": "You must score more than {required_percent}% on the previous song before you can continue.",
        "no_questions": "No questions have been added to this song yet.",
    },
    "ru": {
        "iliad": "Илиада",
        "book": "Книга",
        "song": "Песнь",
        "read_song": "Читать Песнь",
        "take_quiz": "Пройти викторину",
        "back": "Назад",
        "back_to_iliad": "Вернуться к Илиаде",
        "back_to_quiz": "Вернуться к викторине",
        "all_songs": "Все песни",
        "language": "Язык",
        "annotations": "Панель аннотаций",
        "select_annotation": "Выберите выделенное слово или выражение, чтобы прочитать примечание.",
        "text_missing": "Текст на этом языке ещё не добавлен. Добавьте его в Django Admin → Версии песен.",
        "quiz": "Илиада — Викторина",
        "quiz_subtitle": "Отвечайте на каждый вопрос сразу. Результат подсчитывается после каждого ответа. Для разблокировки следующей песни нужно набрать больше {pass_percent}%.",
        "start": "Начать",
        "no_quiz_questions": "Вопросы для викторины ещё не добавлены.",
        "score": "Результат",
        "questions": "Вопросы",
        "answer": "Ответить",
        "correct": "Правильно ✓",
        "correct_text": "Вы правильно ответили на этот вопрос.",
        "incorrect": "Неправильно ✕",
        "correct_answer": "Правильный ответ:",
        "already_answered": "Уже отвечено",
        "already_answered_text": "Этот вопрос уже учтён в вашем результате.",
        "previous": "Предыдущий",
        "next_question": "Следующий вопрос",
        "next_song": "Следующая песнь",
        "need_more": "Для разблокировки следующей песни нужно набрать больше {pass_percent}%.",
        "song_complete": "Песнь завершена",
        "final_score": "Ваш итоговый результат:",
        "passed": "Вы прошли викторину. Следующая песнь разблокирована.",
        "failed": "Вы не набрали больше {pass_percent}%. Вы можете пройти песнь ещё раз.",
        "retry": "Пройти песнь ещё раз",
        "song_locked": "Песнь заблокирована",
        "locked_message": "Чтобы продолжить, нужно набрать больше {required_percent}% в предыдущей песне.",
        "no_questions": "Вопросы для этой песни ещё не добавлены.",
    },
    "kk": {
        "iliad": "Илиада",
        "book": "Кітап",
        "song": "Жыр",
        "read_song": "Жырды оқу",
        "take_quiz": "Викторинадан өту",
        "back": "Артқа",
        "back_to_iliad": "Илиадаға оралу",
        "back_to_quiz": "Викторинаға оралу",
        "all_songs": "Барлық жырлар",
        "language": "Тіл",
        "annotations": "Аннотациялар панелі",
        "select_annotation": "Түсіндірмесін оқу үшін белгіленген сөзді немесе тіркесті таңдаңыз.",
        "text_missing": "Бұл тілдегі мәтін әлі қосылмаған. Оны Django Admin → Жыр нұсқалары бөлімінде қосыңыз.",
        "quiz": "Илиада — Викторина",
        "quiz_subtitle": "Әр сұраққа бірден жауап беріңіз. Нәтиже әр жауаптан кейін есептеледі. Келесі жырды ашу үшін {pass_percent}%-дан жоғары нәтиже қажет.",
        "start": "Бастау",
        "no_quiz_questions": "Викторина сұрақтары әлі қосылмаған.",
        "score": "Нәтиже",
        "questions": "Сұрақтар",
        "answer": "Жауап беру",
        "correct": "Дұрыс ✓",
        "correct_text": "Бұл сұраққа дұрыс жауап бердіңіз.",
        "incorrect": "Қате ✕",
        "correct_answer": "Дұрыс жауап:",
        "already_answered": "Жауап берілген",
        "already_answered_text": "Бұл сұрақ сіздің нәтижеңізде бұрыннан есептелген.",
        "previous": "Алдыңғы",
        "next_question": "Келесі сұрақ",
        "next_song": "Келесі жыр",
        "need_more": "Келесі жырды ашу үшін {pass_percent}%-дан жоғары нәтиже қажет.",
        "song_complete": "Жыр аяқталды",
        "final_score": "Қорытынды нәтиже:",
        "passed": "Викторинадан өттіңіз. Келесі жыр ашылды.",
        "failed": "Сіз {pass_percent}%-дан жоғары нәтиже жинамадыңыз. Жырды қайта тапсыра аласыз.",
        "retry": "Жырды қайта өту",
        "song_locked": "Жыр бұғатталған",
        "locked_message": "Жалғастыру үшін алдыңғы жырдан {required_percent}%-дан жоғары нәтиже жинауыңыз керек.",
        "no_questions": "Бұл жырға сұрақтар әлі қосылмаған.",
    },
}


def _ui(language):
    return {
        key: value.format(pass_percent=PASS_PERCENT, required_percent=PASS_PERCENT)
        for key, value in INTERFACE_TEXT[language].items()
    }


def _language_or_404(language):
    language = language.lower()
    if language not in SUPPORTED_LANGUAGES:
        from django.http import Http404
        raise Http404("Unsupported language")
    return language


def _get_song(language, song_number): # первая или вторая песня? он выбирает и вытаскивает из ДБ? склайт3
    return get_object_or_404(
        QuizSong,
        language=language,
        number=song_number,
    )


def iliad_page(request, language="en", song_number=1):
    language = _language_or_404(language)
    song = QuizSong.objects.filter(language=language, number=song_number).first()

    if song is None:
        # Keep the default reader URL friendly if a requested song does not
        # exist for this language.
        if song_number != 1:
            from django.http import Http404
            raise Http404("This song is not available for the selected language")

    annotations = song.annotations.all() if song else []
    songs = QuizSong.objects.filter(language=language).order_by("number")
    previous_song = (
        songs.filter(number=song.number - 1).first() if song else None
    )
    next_song = (
        songs.filter(number=song.number + 1).first() if song else None
    )

    # When switching language, stay on the same song if that translation
    # exists; otherwise fall back to Book I.
    language_song_links = {}
    current_number = song.number if song else 1
    for code in SUPPORTED_LANGUAGES:
        target = QuizSong.objects.filter(
            language=code, number=current_number
        ).first()
        if target is None:
            target = QuizSong.objects.filter(language=code, number=1).first()
        language_song_links[code] = target  # работает так; если я на второй песне и переключаю язык на втторую песне останусь да

    return render(
        request,
        "index.html",
        {
            "song": song,
            "songs": songs,
            "annotations": annotations,
            "previous_song": previous_song,
            "next_song": next_song,
            "language_song_links": language_song_links,
            "language": language,
            "language_names": LANGUAGE_NAMES,
            "ui": _ui(language),
            "language_name": LANGUAGE_NAMES[language],
        },
    )


def quiz_home(request, language="en"):
    language = _language_or_404(language)
    songs = QuizSong.objects.filter(language=language)

    return render(
        request,
        "quiz_home.html",
        {
            "songs": songs,
            "language": language,
            "language_names": LANGUAGE_NAMES,
            "ui": _ui(language),
            "pass_percent": PASS_PERCENT,
        },
    )


def _quiz_key(song):
    # Every language is a separate QuizSong, so scores are automatically
    # independent between English, Russian and Kazakh.
    return f"quiz_song_{song.id}"   # щас, форс мажор, 1 минуту 
    # форс мажор решен, как он работает; квиз кей является нечто вроде как идентификатором для теста: если переходишь на русский тест, результат казахского не перемешивается и не влияет. Дальше?


def _song_result(request, song):
    data = request.session.get(_quiz_key(song), {})
    answered = set(data.get("answered", []))
    correct = int(data.get("correct", 0))
    total = song.questions.count()

    percent = round((correct / total) * 100, 1) if total else 0

    return {
        "answered": answered,
        "correct": correct,
        "total": total,
        "percent": percent,
        "passed": bool(
            total
            and percent > PASS_PERCENT
            and len(answered) >= total
        ),
    }


def _song_is_unlocked(request, song):
    if song.number <= 1:
        return True

    previous_song = QuizSong.objects.filter(
        language=song.language,
        number=song.number - 1,
    ).first()

    if previous_song is None:
        return True

    return _song_result(request, previous_song)["passed"]


def quiz_song(request, language, song_number):
    language = _language_or_404(language)
    song = _get_song(language, song_number)
    songs = QuizSong.objects.filter(language=language)

    if not _song_is_unlocked(request, song):
        return render(
            request,
            "quiz_locked.html",
            {
                "song": song,
                "required_percent": PASS_PERCENT,
                "songs": songs,
                "language": language,
                "language_names": LANGUAGE_NAMES,
            "ui": _ui(language),
            },
        )

    questions = list(song.questions.all())
    result = _song_result(request, song)

    if not questions:
        return render(
            request,
            "quiz_empty.html",
            {
                "song": song,
                "songs": songs,
                "language": language,
                "language_names": LANGUAGE_NAMES,
            "ui": _ui(language),
            },
        )

    try:
        question_number = int(request.GET.get("question", 1))
    except (TypeError, ValueError):
        question_number = 1

    question_number = max(1, min(question_number, len(questions)))
    question = questions[question_number - 1]
    already_answered = question.id in result["answered"]
    selected_option = None
    is_correct = None

    if request.method == "POST" and not already_answered:
        selected_option = request.POST.get("answer")

        if selected_option not in {"a", "b", "c", "d"}:
            return redirect(
                f"{request.path}?question={question_number}"
            )

        is_correct = selected_option == question.correct_option
        data = request.session.get(
            _quiz_key(song),
            {"answered": [], "correct": 0, "answers": {}},
        )
        answered = set(data.get("answered", []))

        if question.id not in answered:
            answered.add(question.id)
            data["answered"] = list(answered)
            data["answers"] = data.get("answers", {})
            data["answers"][str(question.id)] = selected_option

            if is_correct:
                data["correct"] = int(data.get("correct", 0)) + 1

            request.session[_quiz_key(song)] = data
            request.session.modified = True

        result = _song_result(request, song)
        already_answered = True

    elif already_answered:
        data = request.session.get(_quiz_key(song), {})
        selected_answers = data.get("answers", {})
        selected_option = selected_answers.get(str(question.id))
        if selected_option:
            is_correct = selected_option == question.correct_option

    next_question = (
        question_number + 1
        if question_number < len(questions)
        else None
    )

    next_song = QuizSong.objects.filter(
        language=language,
        number=song.number + 1,
    ).first()

    previous_question = question_number - 1 if question_number > 1 else None

    return render(
        request,
        "quiz.html",
        {
            "song": song,
            "songs": songs,
            "questions": questions,
            "question": question,
            "question_number": question_number,
            "already_answered": already_answered,
            "answered_ids": result["answered"],
            "selected_option": selected_option,
            "is_correct": is_correct,
            "next_question": next_question,
            "next_song": next_song,
            "previous_question": previous_question,
            "correct": result["correct"],
            "total": result["total"],
            "percent": result["percent"],
            "passed": result["passed"],
            "pass_percent": PASS_PERCENT,
            "language": language,
            "language_names": LANGUAGE_NAMES,
            "ui": _ui(language),
            "language_name": LANGUAGE_NAMES[language],
        },
    )


def quiz_reset(request, language, song_number):
    language = _language_or_404(language)
    song = _get_song(language, song_number)

    if request.method == "POST":
        request.session.pop(_quiz_key(song), None)
        request.session.modified = True

    return redirect(
        "quiz_song",
        language=language,
        song_number=song.number,
    )

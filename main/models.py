from django.db import models

class Annotation(models.Model):
    html_id = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="ID элемента в HTML"
    )
    title = models.CharField(max_length=200, verbose_name="Заголовок аннотации")
    commentary = models.TextField(verbose_name="Текст комментария")

    def __str__(self):
        return f"{self.html_id} - {self.title}"
      

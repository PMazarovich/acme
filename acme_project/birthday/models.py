from django.db import models
# birthday/models.py
from django.db import models

from birthday.validators import real_age


class Birthday(models.Model):
    first_name = models.CharField('Имя', max_length=20)
    last_name = models.CharField(
        'Фамилия', max_length=20, help_text='Необязательное поле', blank=True
    )
    # Валидатор указывается в описании поля.
    birthday = models.DateField('Дата рождения', validators=(real_age,))
    image = models.ImageField('Фото', blank=True, upload_to="birthdays_images")
    class Meta:
        # совокупность значений полей «Имя», «Фамилия» и «Дата рождения» не должна повторяться в БД.
        constraints = (
            models.UniqueConstraint(
                fields=('first_name', 'last_name', 'birthday'),
                name='Unique person constraint',
            ),
        )

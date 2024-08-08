# birthday/forms.py
from django import forms
from django.core.exceptions import ValidationError

from .validators import real_age

#
#
# class BirthdayForm(forms.Form):
#     first_name = forms.CharField(label='Имя', max_length=20)
#     last_name = forms.CharField(
#         label='Фамилия', required=False, help_text='Необязательное поле'
#     )
#     birthday = forms.DateField(
#         label='Дата рождения',
#         widget=forms.DateInput(attrs={'type': 'date'}),
#         # В аргументе validators указываем список или кортеж
#         # валидаторов этого поля (валидаторов может быть несколько).
#         validators=(real_age,),
#     )

# birthday/forms.py
from django import forms

# Импортируем класс модели Birthday.
from .models import Birthday

BEATLES = {'Джон Леннон', 'Пол Маккартни', 'Джордж Харрисон', 'Ринго Старр'}
# # Для использования формы с моделями меняем класс на forms.ModelForm.
class BirthdayForm(forms.ModelForm):
    # Удаляем все описания полей.

    # Все настройки задаём в подклассе Meta.
    class Meta:
        # Указываем модель, на основе которой должна строиться форма.
        model = Birthday
        # Указываем, что надо отобразить все поля.
        fields = '__all__'

        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'})
        }

    def clean(self):
        # Вызов родительского метода clean. (см Birthday.constraints)
        super().clean()
        # Получаем имя и фамилию из очищенных полей формы.
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        # Проверяем вхождение сочетания имени и фамилии во множество имён.
        if f'{first_name} {last_name}' in BEATLES:
            raise ValidationError(
                'Мы тоже любим Битлз, но введите, пожалуйста, настоящее имя!'
            )

    # def clean_first_name(self):
    #     # Получаем значение имени из словаря очищенных данных.
    #     first_name = self.cleaned_data['first_name']
    #     # Разбиваем полученную строку по пробелам
    #     # и возвращаем только первое имя.
    #     return first_name.split()[0]

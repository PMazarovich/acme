# birthday/views.py
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from .forms import BirthdayForm
from .models import Birthday
# Импортируем из utils.py функцию для подсчёта дней.
from .utils import calculate_birthday_countdown


def birthday_list(request):
    # Получаем все объекты модели Birthday из БД. В отсортированном виде!!
    birthdays = Birthday.objects.all().order_by('id')
    # Передаём их в контекст шаблона.
    paginator = Paginator(birthdays, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'birthday/birthday_list.html', context)

#
# def edit_birthday(request, pk):
#     # Находим запрошенный объект для редактирования по первичному ключу
#     # или возвращаем 404 ошибку, если такого объекта нет.
#     instance = get_object_or_404(Birthday, pk=pk)
#     # Связываем форму с найденным объектом: передаём его в аргумент instance.
#     form = BirthdayForm(request.POST or None, instance=instance)
#     # Всё остальное без изменений.
#     context = {'form': form}
#     # Сохраняем данные, полученные из формы, и отправляем ответ:
#     if form.is_valid():
#         form.save()
#         birthday_countdown = calculate_birthday_countdown(
#             form.cleaned_data['birthday']
#         )
#         context.update({'birthday_countdown': birthday_countdown})
#     return render(request, 'birthday/birthday.html', context)


def delete_birthday(request, pk):
    # Получаем объект модели или выбрасываем 404 ошибку.
    instance = get_object_or_404(Birthday, pk=pk)
    # В форму передаём только объект модели;
    # передавать в форму параметры запроса не нужно.
    form = BirthdayForm(instance=instance)
    context = {'form': form}
    # Если был получен POST-запрос...
    if request.method == 'POST':
        # ...удаляем объект:
        instance.delete()
        # ...и переадресовываем пользователя на страницу со списком записей.
        return redirect('birthday:list')
    # Если был получен GET-запрос — отображаем форму.
    return render(request, 'birthday/birthday.html', context)


def birthday(request, pk=None):
    # Если в запросе указан pk (если получен запрос на редактирование объекта):
    if pk is not None:
        # Получаем объект модели или выбрасываем 404 ошибку.
        instance = get_object_or_404(Birthday, pk=pk)
    else:
        # Связывать форму с объектом не нужно, установим значение None.
        instance = None
    # сначала при вызове /birthday/, если в post нет никаких данных,
    # создаем экземпляр Form и отдаем пустую клиенту.
    # Если же данные есть, обновить контекст и вернуть форму уже с данными.
    # То есть, генерируется 2!! html страницы. Сначала пустая, потом с данными (если они приходят)
    form = BirthdayForm(request.POST or None, files=request.FILES or None, instance=instance)
    # Создаём словарь контекста сразу после инициализации формы.
    context = {'form': form}
    # Если форма валидна...
    if form.is_valid():
        form.save()  # сохраняем данные в БД
        print("saved")
        # ...вызовем функцию подсчёта дней:
        birthday_countdown = calculate_birthday_countdown(
            # ...и передаём в неё дату из словаря cleaned_data.
            form.cleaned_data['birthday']
        )
        # Обновляем словарь контекста: добавляем в него новый элемент.
        context.update({'birthday_countdown': birthday_countdown})
    return render(request, 'birthday/birthday.html', context)

# birthday/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView

from .forms import BirthdayForm
from .models import Birthday
# Импортируем из utils.py функцию для подсчёта дней.
from .utils import calculate_birthday_countdown


#
# def birthday_list(request):
#     # Получаем все объекты модели Birthday из БД. В отсортированном виде!!
#     birthdays = Birthday.objects.all().order_by('id')
#     # Передаём их в контекст шаблона.
#     paginator = Paginator(birthdays, 10)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     context = {'page_obj': page_obj}
#     return render(request, 'birthday/birthday_list.html', context)

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


# def delete_birthday(request, pk):
#     # Получаем объект модели или выбрасываем 404 ошибку.
#     instance = get_object_or_404(Birthday, pk=pk)
#     # В форму передаём только объект модели;
#     # передавать в форму параметры запроса не нужно.
#     form = BirthdayForm(instance=instance)
#     context = {'form': form}
#     # Если был получен POST-запрос...
#     if request.method == 'POST':
#         # ...удаляем объект:
#         instance.delete()
#         # ...и переадресовываем пользователя на страницу со списком записей.
#         return redirect('birthday:list')
#     # Если был получен GET-запрос — отображаем форму.
#     return render(request, 'birthday/birthday.html', context)


# def birthday(request, pk=None):
#     # Если в запросе указан pk (если получен запрос на редактирование объекта):
#     if pk is not None:
#         # Получаем объект модели или выбрасываем 404 ошибку.
#         instance = get_object_or_404(Birthday, pk=pk)
#     else:
#         # Связывать форму с объектом не нужно, установим значение None.
#         instance = None
#     # сначала при вызове /birthday/, если в post нет никаких данных,
#     # создаем экземпляр Form и отдаем пустую клиенту.
#     # Если же данные есть, обновить контекст и вернуть форму уже с данными.
#     # То есть, генерируется 2!! html страницы. Сначала пустая, потом с данными (если они приходят)
#     form = BirthdayForm(request.POST or None, files=request.FILES or None, instance=instance)
#     # Создаём словарь контекста сразу после инициализации формы.
#     context = {'form': form}
#     # Если форма валидна...
#     if form.is_valid():
#         form.save()  # сохраняем данные в БД
#         print("saved")
#         # ...вызовем функцию подсчёта дней:
#         birthday_countdown = calculate_birthday_countdown(
#             # ...и передаём в неё дату из словаря cleaned_data.
#             form.cleaned_data['birthday']
#         )
#         # Обновляем словарь контекста: добавляем в него новый элемент.
#         context.update({'birthday_countdown': birthday_countdown})
#     return render(request, 'birthday/birthday.html', context)


class BirthdayListView(LoginRequiredMixin, ListView):
    model = Birthday
    ordering = 'id'
    paginate_by = 10


class BirthdayMixin:
    model = Birthday
    success_url = reverse_lazy('birthday:list')


class BirthdayFormMixin:
    form_class = BirthdayForm
    template_name = 'birthday/birthday.html'

# Класс UserPassesTestMixin унаследован от AccessMixin,
# который по умолчанию переадресует анонимных пользователей на страницу логина.
# Поэтому при использовании UserPassesTestMixin миксин LoginRequiredMixin можно не использовать
class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class BirthdayCreateView(LoginRequiredMixin, BirthdayMixin, BirthdayFormMixin, CreateView):
    def form_valid(self, form):  # If the form is valid, save the associated model.
        form.instance.author = self.request.user
        # Продолжить валидацию, описанную в форме.
        return super().form_valid(form)
        # # Указываем модель, с которой работает CBV...
    # model = Birthday
    # # Указываем имя формы:
    # form_class = BirthdayForm
    # # Этот класс сам может создать форму на основе модели!
    # # Нет необходимости отдельно создавать форму через ModelForm.
    # # Указываем поля, которые должны быть в форме:
    # fields = '__all__'
    # # Явным образом указываем шаблон:
    # template_name = 'birthday/birthday.html'
    # # Указываем namespace:name страницы, куда будет перенаправлен пользователь
    # # после создания объекта:
    # success_url = reverse_lazy('birthday:list')


class BirthdayUpdateView(OnlyAuthorMixin, UpdateView):
    model = Birthday
    form_class = BirthdayForm
    template_name = 'birthday/birthday.html'

    # Определяем метод test_func() для миксина UserPassesTestMixin:
    def test_func(self):  # этот self пришел из UserPassesTestMixin, т.к. test_func переопределяется оттуда
        # Получаем текущий объект.
        object = self.get_object()
        # Метод вернёт True или False.
        # Если пользователь - автор объекта, то тест будет пройден.
        # Если нет, то будет вызвана ошибка 403.
        return object.author == self.request.user


class BirthdayDeleteView(OnlyAuthorMixin, BirthdayMixin, DeleteView):
    template_name = 'birthday/birthday_confirm_delete.html'
    pass
    # model = Birthday
    # success_url = reverse_lazy('birthday:list')


# birthday/views.py
class BirthdayDetailView(LoginRequiredMixin, DetailView):
    model = Birthday
    template_name_suffix = '_detail'

    # Модифицируем контекстные данные для html формы
    def get_context_data(self, **kwargs):
        # Получаем словарь контекста:
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь новый ключ:
        context['birthday_countdown'] = calculate_birthday_countdown(
            # Дату рождения берём из объекта в словаре context:
            self.object.birthday
        )
        # Возвращаем словарь контекста.
        return context

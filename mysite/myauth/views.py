from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _, ngettext
from django.views import View
from django.views.generic import TemplateView, CreateView
from django.views.decorators.cache import cache_page
from .models import Profile


class HelloView(View):
    welcome_message = _('Welcome, Hello, World!')  # переменная с текстом, который хотим перевести

    def get(self, request: HttpRequest) -> HttpResponse:
        items_str = request.GET.get('items') or 0
        items = int(items_str)
        products_line = ngettext(
            'one product',
            '{count} products',
            items,
        )
        products_line = products_line.format(count=items)
        return HttpResponse(
            f'<h1>{self.welcome_message}</h1>'
            f'\n<h2>{products_line}</h2>'

        )
        # return render(request,'', context='')
        # команда python manage.py makemessages -l en - выбирает язык, на который необходимо перевести сообщение
        # после того, как в файле джанго.по ввели перевод, нужно скомпилировать изменения с помощью команды
        # python manage.py compilemessages. При каждом обновлении джанго.по, нужно вводить команду compilemessages


class AboutMeView(TemplateView):
    template_name = 'myauth/about_me.html'


# создание новой сущности пользователя (регистрация)
class RegistrationView(CreateView):
    form_class = UserCreationForm  # форма для создания пользователя
    template_name = 'myauth/registration.html'
    success_url = reverse_lazy('myauth:about_me')

    # чтобы сразу пройти аутентификацию, дорабатывается функция form_valid
    def form_valid(self, form):
        response = super().form_valid(form)  # подготовка ответа с уже созданным пользователем
        Profile.objects.create(user=self.object)  # создание профиля пользователю. Такая реализация отделяет создание
        # профиля от аутентификации, если есть необходимость не сразу аутентифицироваться

        # вытаскиваем чистые данные для аутентификации
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')  # можно использовать password1 или password2 так как при
        # регистрации заполняются поля с паролями под этими конкретными именами
        user = authenticate(
            self.request,
            username=username,
            password=password)

        login(request=self.request, user=user)
        return response


def login_view(request: HttpRequest):
    if request.method == 'GET':
        if request.user.is_authenticated:  # проверка пользователя, выполнил ли он аутентификацию
            return redirect('/admin/')

        return render(request, 'myauth/login.html')  # перенаправление на страницу логина

    username = request.POST['username']
    password = request.POST['password']

    # вернет пользователя при правильных данных, или None, если нет
    user = authenticate(request, username=username, password=password)

    if user is not None:  # если все данные верны, переходим на нужную страницу
        login(request, user)
        return redirect('/admin/')

    # в другом случае вернется шаблон, но с ошибкой
    return render(request, 'myauth/login.html', {'error': 'Invalid login credentials'})


# def logout_view(request: HttpRequest) -> HttpResponse:
#     logout(request)
#     return redirect(reverse('myauth:login'))


class MyLogoutView(LogoutView):
    next_page = reverse_lazy('myauth:login')  # перенаправление на страницу после разлогирования


# Cookie текстовые файлы, предназначенные для хранения информации пользователя: его предпочтения, какие выборы он сделал
# а также для отслеживания действий пользователя и контекстной рекламы. Cookie сгорают по истечению времени, заданным
# в настройках
# создание функции для установки cookie
@user_passes_test(lambda u: u.is_superuser)  # декоратор, который проверяет пользователя на суперюзера. Избежать
def set_cookie_view(request: HttpRequest) -> HttpResponse:  # бесконечного перенаправления можно, если прописать условие в самой функции
    response = HttpResponse('Cookie set!')  # Создание объекта
    response.set_cookie('fizz', 'buzz', max_age=3600)  # Создание ключа, его значения и срока жизни cookie в max_ages в сек
    return response


# создание функции для чтения cookie
@cache_page(timeout=60 * 2)  # кэширование на определенное время
def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get('fizz', 'default_value')
    return HttpResponse(f'Cookie value: {value!r}')


# Session это хранение информации пользователя в то время как он обращается в приложению: какие сайты посещал или какие
# товары были помещены в корзину на сайте. Данные хранятся на backend, а у пользователя есть только токен в cookie,
# который связывает его с сессией в приложении. Токен также используется для идентификации пользователя. Срок жизни
# сессии устанавливается автоматически, но можно установить срок жизни в своем проекте.
# создание функции для установки сессии
@permission_required('myauth.view_profile', raise_exception=True)  # декоратор для проверки отдельного разрешения у пользователя.
def set_session_view(request: HttpRequest) -> HttpResponse:  # raise_exception используется, чтобы не было бесконечного
    request.session['foobar'] = 'spameggs'                   # цикла с перенаправлениями
    return HttpResponse('Session set!')


# создание функции для чтения сессии
@login_required  # декоратор, который проверяет аутентифицирован ли пользователь. Если нет, то доступ на страницу закрыт
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get('foobar', 'default value')
    return HttpResponse(f'Session value: {value!r}')


class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({'foo': 'bar', 'spam': 'eggs'})
from django.contrib.auth.views import LoginView
from django.urls import path
from .views import (
    login_view,
    set_cookie_view,
    get_cookie_view,
    set_session_view,
    get_session_view,
    MyLogoutView,
    AboutMeView,
    RegistrationView,
    FooBarView,
    HelloView,
)

app_name = 'myauth'

# LoginView избавляет от необходимости писать функцию аутентификации, так как в классе уже реализована логика
# При этом, в шаблоне достаточно указать форму form.as_p и не расписывать поля
# В settings проекта в самом конце необходимо указать адрес перенаправления по умолчанию (LOGIN_REDIRECT_URL)
# Если уже выполнен вход и чтобы не заходить на страницу login, прописываем redirect_authenticated_user=True
urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='myauth/login_form.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    # path('login/', login_view, name='login'),
    # path('logout/', logout_view, name='logout'),
    path('cookie/set/', set_cookie_view, name='set_cookie'),
    path('cookie/get/', get_cookie_view, name='get_cookie'),
    path('session/set/', set_session_view, name='set_cookie'),
    path('session/get/', get_session_view, name='get_cookie'),
    path('about_me/', AboutMeView.as_view(), name='about_me'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('foo_bar/', FooBarView.as_view(), name='foo_bar'),
    path('hello/', HelloView.as_view(), name='hello'),
]

from django.test import TestCase
from django.urls import reverse
import json


class GetCookieViewTestCase(TestCase):
    def test_get_cookie_view(self):
        response = self.client.get(reverse('myauth:get_cookie'), HTTP_USER_AGENT='Mozilla/5.0')  #self.client предоставляется родительским классом TestCase
        self.assertContains(response, 'Cookie value') #self.assertContains позволяет проверить ответ на содержимость значения


class FooBarViewTestCase(TestCase):
    def test_foo_bar_view(self):
        response = self.client.get(reverse('myauth:foo_bar'), HTTP_USER_AGENT='Mozilla/5.0')
        self.assertEqual(response.status_code, 200) #проверка, действительно ли статус код ответа - 200
        self.assertEqual(
            response.headers['content-type'], 'application/json',
        ) #проверка, содердит ли ответ 'application/json' в заголовке 'content-type'

        expected_data = {'foo': 'bar', 'spam': 'eggs'}
        # received_data = json.loads(response.content) #конвертируем ответ в json, так как изначально приходит в байтах
        # self.assertEqual(
        #     received_data, expected_data,
        # ) #проверка, равно ли содержимое ответа с ожидаемым ответом

        self.assertJSONEqual(response.content, expected_data) #упрощенный вариант проверки ответа контента и ожидаемого
        #контента без конвертации с помощью json модуля, но с помощью self.assertJSONEqual
import allure
import pytest
import requests

import data
import urls
import helpers


class TestCreateUser:
    @allure.title('Создание пользователя')
    @allure.description('Успешное создание нового пользователя')
    def test_create_new_user_success(self):
        payload = helpers.generate_user_data()
        response = requests.post(urls.URL_BASE + urls.URL_REGISTRATION, data=payload)
        token = response.json()['success']
        assert response.status_code == 200 and token == True

    @allure.description('Нельзя создать двух одинаковых курьеров')
    def test_create_similar_user_false(self):
        payload = helpers.generate_user_data()
        requests.post(urls.URL_BASE + urls.URL_REGISTRATION, data=payload)
        response = requests.post(urls.URL_BASE + urls.URL_REGISTRATION, data=payload)
        assert (response.status_code == 403 and response.json()['message'] == data.TestBodyText.text_similar_user_403)

    @allure.description('Нельзя создать пользователя без обязательного поля email')
    def test_create_user_without_email_false(self):
        response = requests.post(urls.URL_BASE + urls.URL_REGISTRATION, data=data.TestBodyData.body_data_without_email)
        assert (response.status_code == 403
                and response.json()['message'] == data.TestBodyText.text_user_without_fields_403)

    @allure.description('Нельзя создать пользователя без обязательного поля password')
    def test_create_user_without_password_false(self):
        response = requests.post(urls.URL_BASE + urls.URL_REGISTRATION, data=data.TestBodyData.body_data_without_password)
        assert (response.status_code == 403
                and response.json()['message'] == data.TestBodyText.text_user_without_fields_403)

    @allure.description('Нельзя создать пользователя без обязательного поля name')
    def test_create_user_without_name_false(self):
        response = requests.post(urls.URL_BASE + urls.URL_REGISTRATION, data=data.TestBodyData.body_data_without_name)
        assert (response.status_code == 403
                and response.json()['message'] == data.TestBodyText.text_user_without_fields_403)


class TestLoginUser:
    @allure.title('Логин пользователя')
    @allure.description('Успешная авторизация существующего пользователя')
    def test_user_authorisation_success(self):
        user = helpers.create_new_user()
        authorisation = {
            'email': user['email'],
            'password': user['password'],
            'name': user['name']
        }
        response = requests.post(urls.URL_BASE + urls.URL_LOGIN, data=authorisation)
        helpers.delete_user(user['token'])
        assert response.status_code == 200 and response.json()['user']['email'] == user['email']

    @allure.description('Нельзя авторизироваться с неверным логином и паролем')
    def test_user_authorisation_without_login_password_false(self):
        payload = helpers.generate_user_data()
        response = requests.post(urls.URL_BASE + urls.URL_LOGIN, data=payload)
        assert response.status_code == 401 and response.json()['message'] == data.TestBodyText.text_authorisation_incorrect_401


class TestChangeUserData:
    @allure.title('Изменение данных пользователя')
    @allure.description('Изменение данных пользователя с авторизацией')
    @pytest.mark.parametrize('change_field', ['email', 'password', 'name'])
    def test_user_change_email_with_authorisation_success(self, change_field):
        payload = helpers.authorisation_new_user()
        change_payload = helpers.generate_user_data()
        response = requests.patch(urls.URL_BASE + urls.URL_USER,
                                  data=change_payload,
                                  headers={'Authorization': payload['token']})
        assert response.status_code == 200 and response.json()['success'] == True

    @allure.description('Изменение данных пользователя без авторизации')
    @pytest.mark.parametrize('change_field', ['email', 'password', 'name'])
    def test_user_change_email_without_authorisation_failed(self, change_field):
        payload = helpers.create_new_user()
        change_payload = helpers.generate_user_data()
        response = requests.patch(urls.URL_BASE + urls.URL_USER,
                                  data=change_payload)
        assert (response.status_code == 401
                and response.json()['message'] == data.TestBodyText.text_user_without_authorization_401)
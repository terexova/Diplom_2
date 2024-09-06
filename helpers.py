import allure
import requests
from faker import Faker

import urls


@allure.step('Данные для нового пользователя')
def generate_user_data():
    fake = Faker()
    payload = {
        "email": fake.email(),
        "password": fake.password(8),
        "name": fake.name()
    }
    return payload

@allure.step('Регистрация нового пользователя')
def create_new_user():
    payload = generate_user_data()
    response = requests.post(urls.URL_BASE + urls.URL_REGISTRATION, data=payload)
    payload['code'] = response.status_code
    payload['token'] = response.json()['accessToken']
    payload['retoken'] = response.json()['refreshToken']
    return payload

@allure.step('Авторизация нового пользователя')
def authorisation_new_user():
    payload = create_new_user()
    response = requests.post(urls.URL_BASE + urls.URL_LOGIN, data=payload)
    payload['token'] = response.json()['accessToken']
    payload['retoken'] = response.json()['refreshToken']
    return payload


@allure.step('Удаление пользователя')
def delete_user(token):
    requests.delete(urls.URL_BASE + urls.URL_USER, headers={'Authorisation': token})



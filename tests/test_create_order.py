import allure
import requests

import data
import urls
import helpers



class TestCreateOrder:
    @allure.title('Создание заказа')
    @allure.description('Успешное создание заказа с авторизированным пользователем')
    def test_create_new_order_with_authorisation_success(self):
        payload = helpers.authorisation_new_user()
        response = requests.post(urls.URL_BASE + urls.URL_ORDER,
                                 data=data.ingredients_data,
                                 headers={'Authorization': payload['token']})
        assert response.status_code == 200 and response.json()['success'] == True

    @allure.description('Успешное создание заказа пользователем без авторизации')
    def test_create_new_order_without_authorisation_success(self):
        response = requests.post(urls.URL_BASE + urls.URL_ORDER,
                                 data=data.ingredients_data)
        assert response.status_code == 200 and response.json()['success'] == True

    @allure.description('Нельзя создать заказ без ингредиентов')
    def test_create_new_order_without_ingredients_failed(self):
        response = requests.post(urls.URL_BASE + urls.URL_ORDER)
        assert (response.status_code == 400
                and response.json()['message'] == data.TestBodyText.text_order_without_ingredients_400)

    @allure.description('Нельзя создать заказ с неверным хешем ингредиентов')
    def test_create_new_order_with_wrong_hash_ingredients_failed(self):
        response = requests.post(urls.URL_BASE + urls.URL_ORDER,
                                 data=data.ingredients_wrong_data)
        assert response.status_code == 500


class TestGetUsersOrder:
    @allure.title('Получение заказов пользователя')
    @allure.description('Получение заказов пользователя с авторизацией')
    def test_get_order_user_with_authorisation_success(self):
        payload = helpers.authorisation_new_user()
        create_order = requests.post(urls.URL_BASE + urls.URL_ORDER,
                                     data=data.ingredients_data,
                                     headers={'Authorization': payload['token']})
        response = requests.get(urls.URL_BASE + urls.URL_ORDER,
                                headers={'Authorization': payload['token']})

        assert response.status_code == 200 and response.json()['success'] == True

    @allure.description('Нельзя получить заказ пользователю без авторизации')
    def test_get_order_user_without_authorisation_failed(self):
        response = requests.get(urls.URL_BASE + urls.URL_ORDER)
        assert (response.status_code == 401
                and response.json()['message'] == data.TestBodyText.text_user_without_authorization_401)

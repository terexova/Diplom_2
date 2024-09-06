
ingredients_data = {'ingredients': ['61c0c5a71d1f82001bdaaa6d', '61c0c5a71d1f82001bdaaa6f']}
ingredients_wrong_data = {'ingredients': ['61c0c5a71', '61c0c5a71']}

class TestBodyText:
    text_similar_user_403 = 'User already exists'
    text_user_without_fields_403 = 'Email, password and name are required fields'
    text_authorisation_incorrect_401 = 'email or password are incorrect'
    text_user_without_authorization_401 = 'You should be authorised'
    text_order_without_ingredients_400 = 'Ingredient ids must be provided'



class TestBodyData:
    body_data_without_email = {'email': '',
                               'password': '123',
                               'name': 'Olga'
                               }

    body_data_without_password = {'email': 'terexova@mail.ru',
                                  'password': '',
                                  'name': 'Olga'
                                  }

    body_data_without_name = {'email': 'terexova@mail.ru',
                              'password': '123',
                              'name': ''
                              }

    body_data_change_email = {'email': 'terexova7@mail.ru',
                              'password': '12345',
                              'name': 'Olgaaa'
                             }

    body_data_change_password = {'email': 'terexova@mail.ru',
                                 'password': '1234',
                                 'name': 'Olga'
                                }
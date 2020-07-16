from model_bakery import baker
from munch import Munch
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from users.models import User

email = 'email@test.com'
password = '1234'


class UserRegisterTestCase(APITestCase):
    url = '/users'

    def test_without_email(self):
        response = self.client.post(self.url, {'email': '', 'password': password})
        self.assertEqual(400, response.status_code)

    def test_email_format(self):
        # wrong format
        wrong_email = 'wrong@format'
        response = self.client.post(self.url, {'email': wrong_email, 'password': password})
        self.assertEqual(400, response.status_code)

        # correct format
        response = self.client.post(self.url, {'email': email, 'password': password})
        print(response.data, email)
        # self.assertEqual(response.data['email'], email)
        self.assertEqual(201, response.status_code)

    def test_without_password(self):
        response = self.client.post(self.url, {'email': email, 'password': ''})
        self.assertEqual(400, response.status_code, {'msg': 'please input email.'})

    def test_too_long_password(self):
        # max_length over 128
        long_password = 'aaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjkkkkkkkkkkllllllllll'
        response = self.client.post(self.url, {'email': email, 'password': long_password})
        self.assertEqual(400, response.status_code, {'msg': 'password is too long.'})


class UserLoginTestCase(APITestCase):
    url = '/users/login'

    def setUp(self) -> None:
        self.user = User.objects.create(email=email)
        self.user.set_password(password)
        self.user.save()

    def test_without_password(self):
        response = self.client.post(self.url, {'email': email})
        self.assertEqual(400, response.status_code, {'msg': 'please input your password.'})

    def test_with_wrong_password(self):
        response = self.client.post(self.url, {'email': email, 'password': '1111'})
        self.assertEqual(400, response.status_code, {'msg': 'please input correct password.'})

    def test_without_email(self):
        response = self.client.post(self.url, {'email': '', 'password': password})
        self.assertEqual(400, response.status_code, {'msg': 'please input your email.'})

    def test_with_wrong_format_email(self):
        wrong_format = 'wrong@mail'
        response = self.client.post(self.url, {'email': wrong_format, 'password': password})
        self.assertEqual(400, response.status_code, {'msg': 'please input correct email format.'})

    def test_with_correct_info(self):
        response = self.client.post(self.url, {'email': email, 'password': password})
        self.assertEqual(200, response.status_code)

    def test_is_token_created(self):
        response = self.client.post(self.url, {'email': email, 'password': password})
        print(response.data)
        self.assertTrue(response.data['token'])
        self.assertTrue(Token.objects.filter(user_id=self.user.id))

        self.fail()


class UserLogOutTestCase(APITestCase):
    url = '/users/logout'

    def setUp(self) -> None:
        self.user = User.objects.create(email=email)
        self.user.set_password(password)
        self.user.save()

        baker.make(Token, user=self.user)
        token = Token.objects.get(user_id=self.user.id)
        self.client.force_authenticate(user=self.user, token=token)

    def test_is_token_deleted(self):
        response = self.client.delete(self.url)
        self.assertEqual(200, response.status_code)
        self.assertFalse(Token.objects.filter(user_id=self.user.id).exists())


class UserDeactivateTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email=email)
        self.user.set_password(password)
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.url = f'/users/{self.user.id}'

    def test_user_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(204, response.status_code)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())
        self.assertFalse(Token.objects.filter(user_id=self.user.id).exists())


class UserRetrieveUpdateTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email=email)
        self.user.set_password(password)
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.url = f'/users/{self.user.id}'

    def test_user_retrieve(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

        res = Munch(response.data)
        # self.assertTrue(res.id)
        # self.assertEqual(res.id, self.user.id)
        self.assertEqual(res.email, email)

    def test_user_update(self):
        data = {
            'email': 'anothermail@mail.com',
            'password': '1234',
        }
        response = self.client.put(self.url, data=data)

        self.assertEqual(200, response.status_code)

        res = Munch(response.data)
        print(res)
        self.assertEqual(res.email, data['email'])
        self.assertEqual(res.password, data['password'])

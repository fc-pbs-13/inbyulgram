from rest_framework import status
from rest_framework.test import APITestCase

from photos.models import Photo, Comment
from users.models import User


class PhotosTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test@example.com',
            password='1111'
        )
        self.photo = Photo.objects.create(
            image='img',
            caption='text',
            user=self.user
        )

    def test_photo_create(self):
        data = {
            'image': 'img',
            'caption': 'text',
        }
        self.client.force_authenticate(self.user)   # foreign Key NOT NULL constraint failed issue
        response = self.client.post(f'/users/{self.user.id}/photos', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_photo_retrieve(self):
        response = self.client.get(f'/users/{self.user.id}/photos/{self.photo.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.photo.id, response.data.get('id'))

    def test_photo_update(self):
        data = {
            'image': 'img',
            'caption': 'text patch'
        }
        response = self.client.patch(f'/users/{self.user.id}/photos/{self.photo.id}', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['caption'], response.data.get('caption'))

    def test_photo_delete(self):
        response = self.client.delete(f'/users/{self.user.id}/photos/{self.photo.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Photo.objects.filter(id=self.photo.id))


class CommentTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email='commenttest@example.com',
            password='1111'
        )
        self.photo = Photo.objects.create(
            image='img',
            caption='text',
            user=self.user
        )
        self.comment = Comment.objects.create(
            photo=self.photo,
            user=self.user,
            description='comment test',
        )

    def test_comment_create(self):
        data = {
            'photo': self.photo,
            'description': 'comment test'
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(f'/users/{self.user.id}/photos/{self.photo.id}/comments', data=data)
        self.assertEqual(response.status_code, 201)

    def test_comment_retrieve(self):
        response = self.client.get(f'/users/{self.user.id}/photos/{self.photo.id}/comments/{self.comment.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('id'), self.comment.id)

    def test_comment_update(self):
        data = {
            'description': 'test comment update',
        }
        response = self.client.patch(f'/users/{self.user.id}/photos/{self.photo.id}/comments/{self.comment.id}',
                                     data=data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(data['description'], response.data.get('description'))

    def test_comment_delete(self):
        response = self.client.delete(f'/users/{self.user.id}/photos/{self.photo.id}/comments/{self.comment.id}')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Comment.objects.filter(id=self.comment.id))

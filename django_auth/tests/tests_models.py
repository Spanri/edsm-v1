from django.test import TestCase
from django.test import Client
from users.models import User, Notif, UserProfile
from docs.models import Doc
c = Client()

class UserTestCase(TestCase):
    def setUp(self):
        u = User.objects.create(
            email="lol@mail.ru", 
            password="gag123456"
        )
        # Я не знаю, как это тестировать, 
        # ибо u.id=1, а надо то новый создавать
        # UserProfile.objects.create(
        #     user_id=u.id,
        #     first_name="First name"
        # )

    def test_user(self):
        pass

class NotifTestCase(TestCase):
    # def test_docs_owner(self):
    #     response = c.get('/api/users/1/docs/')
    #     self.assertEqual(response.status_code, 200)
    
    # def test_docs_owner_one(self):
    #     response = c.get('/api/users/docs/67/')
    #     self.assertEqual(response.status_code, 200)
    
    # def test_all_docs(self):
    #     response = c.get('/api/users/all_docs')
    #     self.assertEqual(response.status_code, 200)
    
    # def test_common(self):
    #     response = c.get('/api/users/notif/common')
    #     self.assertEqual(response.status_code, 200)
    
    def test_all_docs(self):
        response = c.get('/api/users/1/notif/')
        self.assertEqual(response.status_code, 200)
    
    # def test_add_signature(self):
    #     u = User.objects.create(
    #         email="lol@mail.ru",
    #         password="gag123456"
    #     )
    #     response = c.post('/api/docs', {
    #         "title": "test.doc",
    #         "user_id": u.id
    #     })
    #     c.post('/api/users/notif', {
    #         "is_owner": False,
    #         "is_signature_request": True,
    #         "is_queue": True,
    #         # "message": 'Вас просят подписать документ.',
    #         "user_id": u.id,
    #         "doc_id": 1
    #     })
    #     response = c.post('/api/users/notif/add_signature/', {
    #         "id": 1
    #     })
    #     self.assertEqual(response.status_code, 200)

class DocTestCase(TestCase):
    def setUp(self):
        """
        Создание документа (для этого надо создать пользователя)
        """
        u = User.objects.create(
            email="lol@mail.ru",
            password="gag123456"
        )
        response = c.post('/api/docs', {
            "title": "test.doc",
            "user_id": u.id
        })
        self.assertEqual(response.status_code, 200)
    
    def test_doc(self):
        pass

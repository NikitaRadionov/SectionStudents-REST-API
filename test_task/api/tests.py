from django.test import TestCase
from django.test import Client
from .models import ApiUser, Section, UserSection

# /api/sections

class TestCreateSections(TestCase):

    def setUp(self):

        users_data = (('test_nikita', '1234' ,'STUDENT'),
                      ('test_radion', '1234', 'TEACHER'),
                      ('test_dmitry', '1234', 'MODERATOR'))

        for username, password, role in users_data:
            ApiUser.objects.create_user(username=username, password=password, role=role)


    def tearDown(self):

        usernames = ('test_nikita', 'test_radion', 'test_dmitry')

        for username in usernames:
            ApiUser.objects.get(username=username).delete()


    def test_RoleCreateRequest(self):
        nikita, radion, dmitry = Client(), Client(), Client()
        nikita.login(username='test_nikita', password='1234')
        radion.login(username='test_radion', password='1234')
        dmitry.login(username='test_dmitry', password='1234')

        uri = "/api/sections"

        nikita_response = nikita.post(uri, {"title": "section1"}, content_type="application/json")
        radion_response = radion.post(uri, {"title": "section2"}, content_type="application/json")
        dmitry_response = dmitry.post(uri, {"title": "section3"}, content_type="application/json")

        Section.objects.get(title="section2").delete()
        Section.objects.get(title="section3").delete()

        self.assertEqual(nikita_response.status_code, 403)
        self.assertEqual(radion_response.status_code, 201)
        self.assertEqual(dmitry_response.status_code, 201)


    def test_DoubleCreateSection(self):
        radion, dmitry = Client(), Client()
        radion.login(username='test_radion', password='1234')
        dmitry.login(username='test_dmitry', password='1234')

        uri = "/api/sections"

        radion_response = radion.post(uri, {"title": "section"}, content_type="application/json")
        dmitry_response = dmitry.post(uri, {"title": "section"}, content_type="application/json")

        Section.objects.get(title="section").delete()

        self.assertEqual(radion_response.status_code, 201)
        self.assertEqual(dmitry_response.status_code, 400)


class TestDeleteSection(TestCase):


    def setUp(self):

        users_data = (('test_nikita', '1234' ,'STUDENT'),
                      ('test_radion', '1234', 'TEACHER'),
                      ('test_dmitry', '1234', 'MODERATOR'))

        for username, password, role in users_data:
            ApiUser.objects.create_user(username=username, password=password, role=role)

        for i in range(1, 4):
            Section.objects.create(title=f"section{i}")


    def tearDown(self):

        usernames = ('test_nikita', 'test_radion', 'test_dmitry')

        for username in usernames:
            ApiUser.objects.get(username=username).delete()

        for i in range(1, 4):
            try:
                Section.objects.get(title=f"section{i}").delete()
            except Section.DoesNotExist:
                pass


    def test_RoleRequest(self):
        nikita, radion, dmitry = Client(), Client(), Client()
        nikita.login(username='test_nikita', password='1234')
        radion.login(username='test_radion', password='1234')
        dmitry.login(username='test_dmitry', password='1234')

        uri_pattern = "/api/sections/"

        uri = {
            "section1": uri_pattern + "section1",
            "section2": uri_pattern + "section2",
            "section3": uri_pattern + "section3"
        }

        nikita_response = nikita.delete(uri["section1"])
        radion_response = radion.delete(uri["section2"])
        dmitry_response = dmitry.delete(uri["section3"])

        self.assertEqual(nikita_response.status_code, 403)
        self.assertEqual(radion_response.status_code, 403)
        self.assertEqual(dmitry_response.status_code, 204)


    def test_DoubleDeleteSection(self):
        dmitry = Client()
        dmitry.login(username='test_dmitry', password='1234')

        uri = "/api/sections/section1"

        dmitry_firstResponse = dmitry.delete(uri)
        dmitry_secondResponse = dmitry.delete(uri)

        self.assertEqual(dmitry_firstResponse.status_code, 204)
        self.assertEqual(dmitry_secondResponse.status_code, 404)


class TestUpdateSection(TestCase):

    def setUp(self):

        users_data = (('test_nikita', '1234' ,'STUDENT'),
                      ('test_radion', '1234', 'TEACHER'),
                      ('test_dmitry', '1234', 'MODERATOR'))

        for username, password, role in users_data:
            ApiUser.objects.create_user(username=username, password=password, role=role)

        for i in range(1, 4):
            Section.objects.create(title=f"section{i}")
    

    def tearDown(self):

        usernames = ('test_nikita', 'test_radion', 'test_dmitry')

        for username in usernames:
            ApiUser.objects.get(username=username).delete()

        for i in range(1, 4):
            try:
                Section.objects.get(title=f"section{i}").delete()
            except Section.DoesNotExist:
                pass
    

    def test_RoleRequest(self):
        nikita, radion, dmitry = Client(), Client(), Client()
        nikita.login(username='test_nikita', password='1234')
        radion.login(username='test_radion', password='1234')
        dmitry.login(username='test_dmitry', password='1234')

        uri_pattern = "/api/sections/"

        uri = {
            "section1": uri_pattern + "section1",
            "section2": uri_pattern + "section2",
            "section3": uri_pattern + "section3"
        }

        nikita_response = nikita.patch(uri["section1"], {"teacher": "test_radion"}, content_type="application/json")
        radion_response = radion.patch(uri["section2"], {"teacher": "test_radion"}, content_type="application/json")
        dmitry_response = dmitry.patch(uri["section3"], {"teacher": "test_radion"}, content_type="application/json")

        self.assertEqual(nikita_response.status_code, 403)
        self.assertEqual(radion_response.status_code, 403)
        self.assertEqual(dmitry_response.status_code, 200)

        nikita_response = nikita.patch(uri["section1"], {"title": "new_section1", "teacher": "test_radion"}, content_type="application/json")
        radion_response = radion.patch(uri["section2"], {"title": "new_section2", "teacher": "test_radion"}, content_type="application/json")
        dmitry_response = dmitry.patch(uri["section3"], {"title": "new_section3", "teacher": "test_radion"}, content_type="application/json")

        self.assertEqual(nikita_response.status_code, 403)
        self.assertEqual(radion_response.status_code, 403)
        self.assertEqual(dmitry_response.status_code, 200)


    def test_RequestWithBadSection(self):
        dmitry = Client()
        dmitry.login(username='test_dmitry', password='1234')

        uri = "/api/sections/nonExistenSection"

        dmitry_response = dmitry.patch(uri, {"teacher": "test_radion"}, content_type="application/json")

        self.assertEqual(dmitry_response.status_code, 404)
    

    def test_RequestWithBadData(self):
        dmitry = Client()
        dmitry.login(username='test_dmitry', password='1234')

        uri = "/api/sections/section1"

        dmitry_response = dmitry.patch(uri, {"teacher": "test_nikita"}, content_type="application/json")

        self.assertEqual(dmitry_response.status_code, 400)

        dmitry_response = dmitry.patch(uri, {"title": "section2"}, content_type="application/json")

        self.assertEqual(dmitry_response.status_code, 400)



# /api/student/sections

class TestJoinSection(TestCase):

    def setUp(self):

        users_data = (('test_nikita', '1234' ,'STUDENT'),
                      ('test_radion', '1234', 'TEACHER'),
                      ('test_dmitry', '1234', 'MODERATOR'))

        for username, password, role in users_data:
            ApiUser.objects.create_user(username=username, password=password, role=role)

        for i in range(1, 4):
            Section.objects.create(title=f"section{i}")


    def tearDown(self):

        usernames = ('test_nikita', 'test_radion', 'test_dmitry')

        for username in usernames:
            ApiUser.objects.get(username=username).delete()

        for i in range(1, 4):
            Section.objects.get(title=f"section{i}").delete()


    def test_RoleRequest(self):
        nikita, radion, dmitry = Client(), Client(), Client()
        nikita.login(username='test_nikita', password='1234')
        radion.login(username='test_radion', password='1234')
        dmitry.login(username='test_dmitry', password='1234')

        uri = "/api/student/sections"

        nikita_response = nikita.post(uri, {"section": "section1"}, content_type="application/json")
        radion_response = radion.post(uri, {"section": "section2"}, content_type="application/json")
        dmitry_response = dmitry.post(uri, {"section": "section3"}, content_type="application/json")

        UserSection.objects.get(section=Section.objects.get(title="section1")).delete()

        self.assertEqual(nikita_response.status_code, 201)
        self.assertEqual(radion_response.status_code, 403)
        self.assertEqual(dmitry_response.status_code, 403)


    def test_DoubleJoinSection(self):
        nikita = Client()
        nikita.login(username='test_nikita', password='1234')

        uri = "/api/student/sections"

        nikita_firstResponse = nikita.post(uri, {"section": "section1"}, content_type="application/json")
        nikita_secondResponse = nikita.post(uri, {"section": "section1"}, content_type="application/json")

        UserSection.objects.get(section=Section.objects.get(title="section1")).delete()

        self.assertEqual(nikita_firstResponse.status_code, 201)
        self.assertEqual(nikita_secondResponse.status_code, 400)


    def test_JoinNonExistentSection(self):
        nikita = Client()
        nikita.login(username='test_nikita', password='1234')

        uri = "/api/student/sections"

        nikita_response = nikita.post(uri, {"section": "nonExistentSection"}, content_type="application/json")

        self.assertEqual(nikita_response.status_code, 400)


class TestLeaveSection(TestCase):


    def setUp(self):

        users_data = (('test_nikita', '1234' ,'STUDENT'),
                      ('test_radion', '1234', 'TEACHER'),
                      ('test_dmitry', '1234', 'MODERATOR'))

        for username, password, role in users_data:
            ApiUser.objects.create_user(username=username, password=password, role=role)

        for i in range(1, 4):
            Section.objects.create(title=f"section{i}")

        UserSection.objects.create(student = ApiUser.objects.get(username="test_nikita"),
                                   section = Section.objects.get(title="section1"))


    def tearDown(self):

        try:
            UserSection.objects.get(student = ApiUser.objects.get(username="test_nikita"),
                                    section= Section.objects.get(title="section1"))
        except UserSection.DoesNotExist:
            pass

        usernames = ('test_nikita', 'test_radion', 'test_dmitry')

        for username in usernames:
            ApiUser.objects.get(username=username).delete()

        for i in range(1, 4):
            Section.objects.get(title=f"section{i}").delete()


    def test_RoleRequest(self):
        nikita, radion, dmitry = Client(), Client(), Client()
        nikita.login(username='test_nikita', password='1234')
        radion.login(username='test_radion', password='1234')
        dmitry.login(username='test_dmitry', password='1234')

        uri_pattern = "/api/student/sections/"

        uri = {
            "section1": uri_pattern + "section1",
            "section2": uri_pattern + "section2",
            "section3": uri_pattern + "section3"
        }

        nikita_response = nikita.delete(uri["section1"])
        radion_response = radion.delete(uri["section2"])
        dmitry_response = dmitry.delete(uri["section3"])

        self.assertEqual(nikita_response.status_code, 204)
        self.assertEqual(radion_response.status_code, 403)
        self.assertEqual(dmitry_response.status_code, 403)


    def test_DoubleLeaveSection(self):
        nikita = Client()
        nikita.login(username='test_nikita', password='1234')

        uri = "/api/student/sections/section1"

        nikita_firstResponse = nikita.delete(uri)
        nikita_secondResponse = nikita.delete(uri)

        self.assertEqual(nikita_firstResponse.status_code, 204)
        self.assertEqual(nikita_secondResponse.status_code, 404)


    def test_LeaveNonExistentSection(self):
        nikita = Client()
        nikita.login(username='test_nikita', password='1234')

        uri = "/api/student/sections/nonExistentSection"

        nikita_response = nikita.delete(uri)

        self.assertEqual(nikita_response.status_code, 404)


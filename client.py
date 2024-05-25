import requests
import json

tokens = {

}


endpoints = [
    "http://localhost:8000/auth/token/login", # получить токен для аутентификации
    "http://localhost:8000/auth/users/", # Зарегистрировать нового пользователя
    "http://localhost:8000/api/sections", # секции
    "http://localhost:8000/api/student/sections", # секции студента
]

def set_up():

    def register_users(users):

        for user in users:
            register_new_user(**user, inform=False)


    def get_tokens(users):
        message_strings = []
        message = "Put this into global dictionary tokens:\n"
        check = {}

        tokens = []
        another_message = "All available users tokens:\n"
        for user in users:
            token = get_user_token(**user, info=False, return_data=True)
            user['token'] = 'Token ' + token
            string = ''

            if not check.get('STUDENT') and user['role'] == "STUDENT":
                string = "\'" + user['role'] + "\': \'Token " + token + "\',"
                check[user['role']] = string

            if not check.get('TEACHER') and user['role'] == "TEACHER":
                string = "\'" + user['role'] + "\': \'Token " + token + "\',"
                check[user['role']] = string

            if not check.get('MODERATOR') and user['role'] == "MODERATOR":
                string = "\'" + user['role'] + "\': \'Token " + token + "\',"
                check[user['role']] = string
            
            if string != '':
                message_strings.append(string)
            
            string = "\'" + user['username'] + "\': \'Token " + token + "\',"
            tokens.append(string)

        message = message + "\n".join(message_strings)
        print(message)
        print()
        another_message = another_message + "\n".join(tokens)
        print(another_message)
        return 'Token ' + token


    def create_sections(moderator, sections):

        for section in sections:
            test_PostListCreateSectionsAPIView(moderator, **section, inform=False)


    def join_sections(users, sections):

        for section in sections:
            for user in users:
                if user['role'] == 'STUDENT':
                    test_PostListCreateUserSectionAPIView(token=user['token'], section=section['title'], inform=False)


    def update_sections(moderator, sections):
        i = 0
        for section in sections:
            teacher = "Tieru" if i % 2 == 0 else "Tim"
            test_PatchRUDSectionsAPIView(token=moderator, lookup_title=section['title'], teacher=teacher, hands=False, inform=False)
            i += 1
        


    users = [
        {"username": "Nikita", "password": "vkusno_i_tochka1999", "role": "STUDENT"},
        {"username": "Tieru", "password": "vkusno_i_tochka1999", "role": "TEACHER"},
        {"username": "Maxim", "password": "vkusno_i_tochka1999", "role": "MODERATOR"},
        {"username": "Sally", "password": "vkusno_i_tochka1999", "role": "STUDENT"},
        {"username": "Tim", "password": "vkusno_i_tochka1999", "role": "TEACHER"},
        {"username": "Morty", "password": "vkusno_i_tochka1999", "role": "MODERATOR"},
    ]
    
    sections = [
        {"title": "math"},
        {"title": "programm"},
        {"title": "biology"},
        {"title": "chemistry"},
        {"title": "english"},
        {"title": "music"},
    ]

    register_users(users)
    moderator = get_tokens(users)
    create_sections(moderator, sections)
    join_sections(users, sections)
    update_sections(moderator, sections)


def print_ResponseInfo(response, headers=False, nice=False):

    have_data = False

    print(f"response status code = {response.status_code}")
    
    try:
        if nice:
            print(json.dumps(response.json(), indent=4))
        else:
            print(response.json())
        have_data = True
    except:
        print("There are no json")

    if headers:
        print(response.headers)
    
    return have_data


def get_user_token(username=None, password=None, info=True, return_data=False, **kwargs):
    username = input("username: ") if username is None else username
    password = input("password: ") if password is None else password
    data = {"username": username, "password": password}
    endpoint = endpoints[0]

    response = requests.post(endpoint, data=data)
    if info:
        print_ResponseInfo(response)
    
    if return_data:
        data = response.json()
        return data['auth_token']


def register_new_user(username=None, password=None, role=None, inform=True):
    username = input("username: ") if username is None else username
    password = input("password: ") if password is None else password

    if role is None:
        message = """Please chose role for user:
1. MODERATOR
2. STUDENT
3. TEACHER
"""
        i = int(input(message))
        roles = {1: "MODERATOR", 2: "STUDENT", 3: "TEACHER"}
        role = roles[i]

    data = {"username": username, "password": password, "role": role}
    endpoint = endpoints[1]

    response = requests.post(endpoint, data=data)
    if inform:
        print_ResponseInfo(response)


def choose_token(inform_message = None):
    if inform_message is not None:
        print(inform_message)
    message = """Choose who should make request:
1. STUDENT
2. TEACHER
3. MODERATOR
"""
    user_key = input(message)
    mapping = {"1": "STUDENT", "2": "TEACHER", "3": "MODERATOR"}
    token = tokens[mapping[user_key]]
    return token


# For Section views

def test_GetListCreateSectionsAPIView():

    endpoint = endpoints[2]

    response = requests.get(endpoint)

    print_ResponseInfo(response, nice=True)


def test_PostListCreateSectionsAPIView(token=None, title=None, inform=True):

    token = choose_token() if token is None else token
    title = input('title: ') if title is None else title
    endpoint = endpoints[2]

    headers = {"Authorization": token}

    data = {'title': title}

    response = requests.post(endpoint, data=data, headers=headers)

    if inform:
        print_ResponseInfo(response)


def test_DeleteRUDSectionsAPIView():

    token = choose_token()
    title = input('title: ')
    endpoint = endpoints[2] + f"/{title}"

    headers = {"Authorization": token}

    response = requests.delete(endpoint, headers=headers)

    print_ResponseInfo(response)


def test_PatchRUDSectionsAPIView(token=None, lookup_title=None, teacher=None, hands=True, inform=True):
    token = choose_token(inform_message="This action with endpoint only for users with role MODERATOR") if token is None else token
    lookup_title = input("lookup title: ") if lookup_title is None else lookup_title
    endpoint = endpoints[2] + f"/{lookup_title}"

    data = {}

    if hands:
        have_teacher = input("do u want add teacher ? y/n ") == 'y'
        if have_teacher:
            teacher_isNone = input("do u want teacher be None ? y/n ") == 'n'
            teacher = input("teacher_username: ") if teacher_isNone else None
            data['teacher'] = teacher
        have_title = input("do u want add title ? y/n ") == 'y'
        if have_title:
            title = input("title: ")
            data['title'] = title

        print(f"Sended data: {data}")
    else:
        data['teacher'] = teacher

    headers = {"Authorization": token}

    response = requests.patch(endpoint, data=data, headers=headers)

    if inform:
        print_ResponseInfo(response)


def test_PutRUDSectionsAPIView():
    token = choose_token(inform_message="This action with endpoint only for users with role MODERATOR")
    lookup_title = input("lookup title: ")
    endpoint = endpoints[2] + f"/{lookup_title}"

    data = {}

    teacher_isNone = input("do u want teacher be None ? y/n ") == 'n'
    teacher = input("teacher_username: ") if teacher_isNone else None
    data['teacher'] = teacher


    title = input("title: ")
    data['title'] = title


    print(f"Sended data: {data}")

    headers = {"Authorization": token}

    response = requests.put(endpoint, data=data, headers=headers)

    print_ResponseInfo(response)



# For UserSection views

def test_GetListCreateUserSectionAPIView():
    token = choose_token(inform_message="This endpoint for users with role STUDENT")
    endpoint = endpoints[3]

    headers = {"Authorization": token}

    response = requests.get(endpoint, headers=headers)

    print_ResponseInfo(response)


def test_PostListCreateUserSectionAPIView(token=None, section=None, inform=True):
    token = choose_token(inform_message="This endpoint for users with role STUDENT") if token is None else token
    section = input('section: ') if section is None else section
    endpoint = endpoints[3]

    data = {"section": section}
    headers = {"Authorization": token}
    response = requests.post(endpoint, data=data, headers=headers)

    if inform:
        print_ResponseInfo(response, headers=True)


def test_GetRetrieveDestroyUserSectionAPIView():
    token = choose_token(inform_message="This endpoint for users with role STUDENT")
    section = input("section: ")
    endpoint = endpoints[3] + f"/{section}"

    headers = {"Authorization": token}

    response = requests.get(endpoint, headers=headers)

    print_ResponseInfo(response)


def test_DeleteRetrieveDestroyUserSectionAPIView():
    token = choose_token(inform_message="This endpoint for users with role STUDENT")
    section = input("section: ")
    endpoint = endpoints[3] + f"/{section}"

    headers = {"Authorization": token}

    response = requests.delete(endpoint, headers=headers)

    print_ResponseInfo(response)


if __name__ == "__main__":
    set_up()

import os
from hashlib import sha1

def checkUser(username,password):
    # get file add
    django_root = os.path.dirname(get_project_root())
    folder_path = os.path.join(django_root, 'dj_data')
    file_path = folder_path + '/secret.kk'
    # get pass
    content = read_file(file_path)
    password = get_hash(password, 'dua')
    print("passss:",password)
    print("contentnnn:",content)
    if content == password and username == 'root':
        print("login success")
        return True
    else:
        print("login fail")
        return False


#get pass with salt
def get_hash(str, salt=None): # salt 盐

    str = 'kai@'+str+'@iak'
    if salt:
        str = str + salt

    sh = sha1()
    sh.update(str.encode('utf-8'))
    return sh.hexdigest()



#read file content
def read_file(filename):

    filename = str(filename)

    with open(filename) as file:
        content = file.read()

        return content

# get root-add
def get_project_root():

    current_path = os.path.abspath(__file__)

    while not os.path.exists(os.path.join(current_path, 'manage.py')):

        current_path = os.path.dirname(current_path)

        if current_path == '' or current_path == '/':

            break
    return current_path

#create data file
def init_datas(filePath):
    os.makedirs(filePath+'/datas')
    pass

def create_file(filePath,password):

    file_path = filePath

    try:
        with open(file_path, 'w') as file:
            content = password
            file.write(content)
            return True
    except IOError as e:
        return False



# Initialize account root root
def init_admin(filepath,password,salt):

    password = get_hash(password, salt)
    create_file(filepath, password)


# create dj-data core folder
def create_folder_in_root():


    django_root =get_project_root()

    django_root = os.path.dirname(get_project_root())

    folder_path = os.path.join(django_root, 'dj_data')


    if not os.path.exists(folder_path):


        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")


        file_path = folder_path + '/secret.kk'
        init_admin(file_path,'root','dua')
        init_datas(folder_path)
    else:

        print(f"Folder '{folder_path}' already exists.")

        if not os.path.exists(os.path.join(folder_path, 'secret.kk')):

             init_admin(folder_path + '/secret.kk', 'root', 'dua')

        else:

             if read_and_validate_file(folder_path + '/secret.kk','root', 'dua'):
                 password = get_hash('root', 'dua')
                 create_file(folder_path + '/secret.kk', password)

        if not os.path.exists(os.path.join(folder_path, 'datas')):

             init_datas(folder_path)


from django.core.exceptions import ValidationError

def read_and_validate_file(file_path,password,salt):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            password = get_hash(password, salt)
            if not content.strip():
                print('content empty')
                return True
            if password != content:
                return True

    except FileNotFoundError:
        raise print('no found')
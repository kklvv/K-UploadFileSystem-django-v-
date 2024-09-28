import pickle
import os
from apps.up01.Tools import AuthLogin
from django.core.serializers import serialize
from django.forms.models import model_to_dict
from apps.up01.Tools.Datas import Mine
from django.core.paginator import Paginator
import shutil
import random
from datetime import datetime


def FindOne(name):

    folder_path = dj_data_datas()
    myobj = load_object(folder_path + '/' + name + '/' + name + '.kk')
    myobj = {'baseName': myobj.baseName,'yuanName': myobj.baseName, 'rootName': myobj.rootName, 'password': myobj.password,
             'time': os.path.getctime(folder_path + '/' + name + '/' + name + '.kk')}

    return myobj

def GetFileNames(BaseName):

    folder_path = dj_data_datas()+"/"+BaseName+"/"+BaseName+".kk"
    myobj=load_object(folder_path)
    file_list=[]
    try:

            file_list= myobj.file_list

    except Exception as e:

        file_list= []

    return file_list

#mb / kb / gb
def filesize_to_str(filesize):
    if filesize >= 1024 ** 3:
        size_str = str(round(filesize / (1024 ** 3), 2)) + ' GB'
    elif filesize >= 1024 ** 2:
        size_str = str(round(filesize / (1024 ** 2), 2)) + ' MB'
    elif filesize >= 1024:
        size_str = str(round(filesize / 1024, 2)) + ' KB'
    else:
        size_str = str(filesize) + ' bytes'
    return size_str



#mb / kb
def filesizeformat(bytes):
    if bytes:
        bytes = float(bytes)
        kb = bytes / 1024
        if kb >= 1024:
            mb = kb / 1024
            return '{0:.2f} MB'.format(mb)
        else:
            return '{0:.2f} KB'.format(kb)
    else:
        return '0 Bytes'



def FindAll02(currentPage,itemsPerPage,BaseName):

    formala = (currentPage - 1) * itemsPerPage
    file_names = GetFileNames(BaseName)
    objs=[]
    from datetime import datetime

    for fstr in file_names:

        folder_path = dj_data_datas() + "/" + BaseName + "/" +fstr
        file_stats = os.stat(folder_path)

        creation_time = file_stats.st_ctime

        timestamp = int(creation_time)

        date_time = datetime.fromtimestamp(timestamp)


        file_size = file_stats.st_size
        myobj= {'fileName': fstr, 'date': date_time.strftime('%Y-%m-%d %H:%M:%S'), 'size': filesize_to_str(file_size)}
        objs.append(myobj)

    objs = list(reversed(objs))

    print("file_names:",file_names)


    paginator = Paginator(objs, itemsPerPage)


    page_obj = paginator.get_page(currentPage)

    print('page_obj', page_obj.object_list)

    return {'success': 'true', 'message': 'ok', 'total': len(objs), 'data': page_obj.object_list}


def FindAll(currentPage,itemsPerPage):

    formala = (currentPage - 1) * itemsPerPage
    folder_names = GetDataDirPath()
    folder_path = dj_data_datas()
    objects = []
    print("folder_names",folder_names)
    for f in folder_names:

        myobj = load_object(folder_path + '/' + f + '/' + f + '.kk')

        myobj = {'baseName':myobj.baseName,'rootName':myobj.rootName,'password':myobj.password,'time':os.path.getctime(folder_path + '/' + f + '/' + f + '.kk')}

        objects.append(myobj)



    array = []
    sortedData = []
    for ml in objects:
        array.append(ml['time'])


    sorted_array = sorted(set(array), reverse=True)


    for sl in sorted_array:

        for s2 in objects:

            if sl == s2['time']:
                sortedData.append(s2)


    paginator = Paginator(sortedData, itemsPerPage)

    page_obj = paginator.get_page(currentPage)

    print('page_obj',page_obj.object_list)

    return {'success': 'true', 'message': 'ok', 'total': len(objects), 'data': page_obj.object_list}


def dj_data_datas():
    django_root = os.path.dirname(AuthLogin.get_project_root())
    folder_path = os.path.join(django_root, 'dj_data/datas')
    return folder_path


def GetDataDirPath():

    folder_path = dj_data_datas()
    folder_names = get_folder_names(folder_path)
    return folder_names


def store_object(obj):

    folder_path = dj_data_datas()
    folder_names = GetDataDirPath()

    if(len(folder_names)>0):
        for f in folder_names:
            if(f==obj.baseName):
                return False

            else:

                return mkD(folder_path, obj)

    else:

        return mkD(folder_path, obj)


def update_object(obj):

    folder_path = dj_data_datas()
    folder_names = GetDataDirPath()
    flag= False
    if (obj.yuanName == obj.baseName):

        folder_path = folder_path + '/' + obj.baseName + '/' + obj.baseName + '.kk'
        myobj = load_object(folder_path)

        datass={'baseName': myobj.baseName,'rootName': obj.rootName,'password': obj.password}
        data = Mine(datass);
        data.file_list=myobj.file_list

        with open(folder_path, 'wb') as file:
            pickle.dump(data, file)

        return True

    else:

        for f in folder_names:

            if (obj.baseName == f):

                return False

            if (obj.baseName != f):

                folder_path = folder_path + '/' + obj.baseName + '/' + obj.baseName + '.kk'
                yuan_folder_path = dj_data_datas() + '/' + obj.yuanName + '/' + obj.yuanName + '.kk'
                print("path1:",folder_path)
                print("path2:",yuan_folder_path)
                myobj = load_object(yuan_folder_path)

                datass = {'baseName': obj.baseName, 'rootName': obj.rootName, 'password': obj.password}
                data = Mine(datass);
                data.file_list = myobj.file_list

                with open(yuan_folder_path, 'wb') as file:
                    pickle.dump(data, file)


                os.renames(dj_data_datas() + '/' + obj.yuanName+ '/' + obj.yuanName + '.kk', dj_data_datas() + '/' +obj.yuanName+ '/' + obj.baseName + '.kk')


                os.renames(dj_data_datas() + '/' + obj.yuanName, dj_data_datas() + '/' +obj.baseName)
                return True




def load_object(folder_path):

    with open(folder_path, 'rb') as file:
        return pickle.load(file)


def mkD(folder_path,obj):

    os.makedirs(folder_path + '/' + obj.baseName)
    print(f"Folder '{folder_path + '/' + obj.baseName}' created successfully.")
    folder_path = folder_path + '/' + obj.baseName+'/'+obj.baseName+'.kk'

    with open(folder_path, 'wb') as file:
        pickle.dump(obj, file)



    return True

def get_folder_names(directory):
    return [folder for folder in os.listdir(directory) if os.path.isdir(os.path.join(directory, folder))]


def DelData(lists):

    folder_path = dj_data_datas()

    for obj in lists:

        shutil.rmtree(folder_path+"/"+obj)



def saveFile(fileInuput,BaseName):
    nN=''
    folder_path = dj_data_datas()
    folder_path = folder_path+"/"+BaseName+"/"
    for item in fileInuput:
        obj = fileInuput.get(item)
        filename = obj.name
        new_string = truncate_from_end(filename, '.')
        nN= str(random.randint(1000000000, 9999999999))
        nN=nN+"."+new_string
        folder_path = folder_path+nN
        f = open(folder_path, 'wb')
        for line in obj.chunks():
            f.write(line)
        f.close()

    folder_path = dj_data_datas()
    file_list=[]
    file_list.append(nN)
    myobj = load_object(folder_path + '/' + BaseName + '/' + BaseName + '.kk')

    try:


            myobj.file_list.append(nN)



    except Exception as e:

        myobj.file_list = file_list


    folder_path = folder_path + '/' + myobj.baseName + '/' + myobj.baseName + '.kk'

    with open(folder_path, 'wb') as file:
        pickle.dump(myobj, file)


def cut_string_from_end(s):
    try:
        index = s.rindex('.')
        return s[:index]
    except ValueError:
        return s




def truncate_from_end(s, stop_char):

    if stop_char not in s:
        return s

    index = s.rindex(stop_char)

    return s[index + 1:]

def file_name_update(file_name,yuan_name,all_name,base_name):
    file_names = GetFileNames(base_name)
    flag= False

    for fstr in file_names:

        if file_name == cut_string_from_end(fstr):

            flag = True

    if flag:

        print("SAME")

    else:

        folder_path = dj_data_datas() + '/' + base_name + '/' + base_name + '.kk'
        myobj=load_object(folder_path)
        yuandian=''
        fileLists= myobj.file_list
        for index, value in enumerate(fileLists):
            if value == all_name:
                yuandian= value
                fileLists[index] =file_name+"."+truncate_from_end(all_name,'.')

        older_path = dj_data_datas()+ '/' + base_name + '/' + base_name + '.kk'

        with open(older_path, 'wb') as file:
            pickle.dump(myobj, file)

        path1 = dj_data_datas() + '/' + base_name + '/' +yuandian
        path2 = dj_data_datas() + '/' + base_name + '/' +file_name+"."+truncate_from_end(all_name,'.')
        os.renames(path1, path2)


def DelFiles(files,name):
    folder_path01 = dj_data_datas() + '/' + name + '/' + name + '.kk'
    folder_path02 = dj_data_datas() + '/' + name+"/"
    myobj = load_object(folder_path01)

    fileLists = myobj.file_list
    for val02 in files:


        for index, value in enumerate(fileLists):
            if value == val02:
                os.remove(folder_path02 + val02)
                fileLists.remove(fileLists[index])

    with open(folder_path01, 'wb') as file:
        pickle.dump(myobj, file)


def get_first_char_index(s, char):
        return s.index(char) if char in s else -1


def check_admin(username,password,basename):
    flag= False
    try:

        folder_path = dj_data_datas() + '/' + basename + '/' + basename + '.kk'
        myobj = load_object(folder_path)
        if myobj.password == password and myobj.rootName == username:
            flag= True
            return flag

    except Exception as e:

        return flag

def get_user(basename):

    folder_path = dj_data_datas() + '/' + basename + '/' + basename + '.kk'
    myobj = load_object(folder_path)

    return myobj.rootName+myobj.password+myobj.baseName





from django.shortcuts import render,HttpResponse,redirect
import os
from django.http import HttpResponse, Http404

from apps.up01.Tools import AuthLogin
from apps.up01.Tools.Datas import Mine  # 正确导入类
from apps.up01.Tools import mkDatas  # 正确导入类
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core import serializers
import json

@require_GET
def login_kk(request,username,password,baseName):

    flag = mkDatas.check_admin(username,password,baseName)
    if flag:

        print('a', flag)
        data = {'state': flag}
        request.session[baseName] = username+password+baseName
        return JsonResponse(data)

    else:
        print('b', flag)
        return render(request, 'up01/pages/login_kk.html')


@require_GET
def login(request,username,password):

    flag = AuthLogin.checkUser(username,password)
    if flag:

        print('a', flag)
        data = {'state': flag}
        request.session['kk_admin'] = "kawsar"
        return JsonResponse(data)

    else:
        print('b', flag)
        return render(request, 'up01/pages/login.html')

def logout(request):
    if request.session.items():
        del request.session["kk_admin"]
    return render(request, 'up01/pages/login.html')


def home(request):

    return render(request, 'up01/pages/index.html')

def admin(request,name):

    data = {'DataName': name}
    if request.session.items():
        try:
            session_name = request.session[name]
            userA = mkDatas.get_user(name)
            if session_name == userA:


                return render(request, 'up01/pages/mkTable.html', data)

            else:
                return render(request, 'up01/pages/login_kk.html', data)

        except Exception as e:

            return render(request, 'up01/pages/login_kk.html', data)
    else:

        return render(request, 'up01/pages/mkTable.html',data)

def MakeDataP(request):

    return render(request,'up01/pages/mkDataBase.html')

def findAllDataBases(request):
    pass

@csrf_exempt
@require_http_methods(["POST"])
def MkDataBaseupdate(request):

    if request.method == 'POST':
        try:
            data01 = json.loads(request.body)  # 解析请求体中的JSON数据
            data =Mine(data01);
            data.yuanName =data01.get('yuanName')


            print('data',str(data))

            flag = mkDatas.update_object(data)


            if flag:

                return JsonResponse({'msg': 'success.'})

            else:

                return JsonResponse({'msg': 'fail.'})

        except json.JSONDecodeError:
            return JsonResponse({'Msg': 'Invalid JSON in request body.'}, status=400)



@csrf_exempt
@require_http_methods(["POST"])
def MkDataBasesave(request):

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            data=Mine(data);

            flag = mkDatas.store_object(data)

            if flag:

                return JsonResponse({'msg': 'success.'})

            else:

                return JsonResponse({'msg': 'fail.'})

        except json.JSONDecodeError:
            return JsonResponse({'Msg': 'Invalid JSON in request body.'}, status=400)



def findAllDataBases02(request,currentPage,itemsPerPage,BaseName):
    print(currentPage)
    print(itemsPerPage)
    print(BaseName)
    list_data= mkDatas.FindAll02(currentPage,itemsPerPage,BaseName)

    return JsonResponse(list_data)


def findAllDataBases(request,currentPage,itemsPerPage):

    list_data = mkDatas.FindAll(currentPage,itemsPerPage)
    print('findAllDataBases',currentPage,itemsPerPage)
    print('list_data',list_data)

    return JsonResponse(list_data)

@require_GET
def delData(request,ids):

   list_output = ids.split(',')
   mkDatas.DelData(list_output)

   return JsonResponse({'msg': list_output})

def finOne01(request,name1,name2):

    name11=mkDatas.cut_string_from_end(name1)


    return JsonResponse({'filename':name11,'filename2':name1})

@require_GET
def file_name_update(request,file_name,yuan_name,all_name,base_name):


    if file_name == yuan_name:
        return JsonResponse({'msg': "NO"})
    else:
        mkDatas.file_name_update(file_name,yuan_name,all_name,base_name)
        return JsonResponse({'msg': "ok"})

@require_GET
def Findone(request,name):

    print('name',name)
    myobj = mkDatas.FindOne(name)
    return JsonResponse(myobj)



def index(request):


    return render(request,'up01/pages/login.html')



@require_GET
def get_client_ip(request,name):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]+"/"+name
    else:
        ip = request.META.get('REMOTE_ADDR')+"/"+name

    domain_name = request.get_host()+"/"+"kk_"+name

    return JsonResponse({'myip': ip,'mydomain':domain_name})

def FindAllData(request,DataName):

    print("DataName"+DataName)
    data = {'DataName':DataName}

    return render(request,'up01/pages/mkTable.html',data)

@csrf_exempt
@require_http_methods(["POST"])
def DownloadFile(request):
    data = json.loads(request.body)
    file_name = data.get('name')
    base_name = data.get('dataName')


    folder_path = mkDatas.dj_data_datas() + '/' + base_name + '/' + file_name

    # with open(folder_path, 'rb') as f:
    #     try:
    #         response = HttpResponse(f)
    #         response['content_type'] = "application/octet-stream"
    #         response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(folder_path)
    #         return response
    #     except Exception:
    #         raise Http404

    try:
        response = HttpResponse(read_file(folder_path))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename' + os.path.basename(folder_path)
        return response
    except Exception:
        raise Http404



def read_file(url, chunk_size=1024):
    with open(url, "rb") as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


@csrf_exempt
@require_http_methods(["POST"])
def UploadFile(request):

    print('file:', request.FILES)
    dataName= request.POST['dataName']
    mkDatas.saveFile(request.FILES,dataName)
    return JsonResponse({'msg': 'ok'})

def del02(request,file_names,baseName):

    list_output = file_names.split(',')
    mkDatas.DelFiles(list_output,baseName)

    return JsonResponse({'msg': "ok"})


def ToAdmin(request,param):

    if "kk_" in param:

        return JsonResponse({'Msg': 'success'})
    else:
        return JsonResponse({'Msg': 'not found'}, status=404)


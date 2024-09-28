"""UpSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from apps.up01 import views


urlpatterns = [


    # path("kai/", include( ([
    #
    #                path('index/', views.index, name="index"),
    #                path('login/?P<username>/?P<password>', views.login, name="login"),
    #
    #                        ], 'up01'
    # ))),



                              path('index/', views.index),
                              path('get_client_ip/<str:name>', views.get_client_ip),
                              path('login/<str:username>/<str:password>', views.login),
                              path('login_kk/<str:username>/<str:password>/<str:baseName>', views.login_kk),

                              path('home/', views.home),
                              path('admin/<str:name>', views.admin),
                              path('logout/', views.logout),
                              path('MakeDataP/', views.MakeDataP),
                              path('findAllDataBases/', views.findAllDataBases),
                              path('MkDataBasesave/', views.MkDataBasesave),
                              path('upload/', views.UploadFile, name='upload_file'),
                              path('download/', views.DownloadFile, name='download_file'),
                              path('findAllDataBases/<int:currentPage>/<int:itemsPerPage>', views.findAllDataBases),
                              path('finOne01/<str:name1>/<str:name2>', views.finOne01),
                              path('findAllDataBases02/<int:currentPage>/<int:itemsPerPage>/<str:BaseName>', views.findAllDataBases02),
                              path('file_name_update/<str:file_name>/<str:yuan_name>/<str:all_name>/<str:base_name>', views.file_name_update),
                              path('del02/<str:file_names>/<str:baseName>', views.del02),
                              path('FindOne/<str:name>', views.Findone),
                              path('delData/<str:ids>', views.delData),
                              path('FindAllData/<str:DataName>', views.FindAllData),
                              path('MkDataBaseupdate/', views.MkDataBaseupdate),
                              path('<str:param>', views.ToAdmin),


]

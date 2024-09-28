from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse,render,redirect
from apps.up01.Tools import AuthLogin
from apps.up01.Tools import mkDatas


class Md1(MiddlewareMixin):

    def process_request(self, request):

        AuthLogin.create_folder_in_root()

        print("req")

    def process_response(self, request, response):

        request_path = request.path
        print("request_path:",request_path)

        if "kk_" in request_path:

            index = mkDatas.get_first_char_index(request_path,'_')
            sub_s = request_path[index+1:]
            data = {'DataName': sub_s}
            print(data)
            if request.session.items():

                try:
                    session_name = request.session[sub_s]
                    userA=mkDatas.get_user(sub_s)
                    if session_name == userA:


                        return render(request, 'up01/pages/mkTable.html',data)

                    else:

                        return render(request, 'up01/pages/login_kk.html',data)

                except Exception as e:

                    return render(request, 'up01/pages/login_kk.html',data)

            else:

                return render(request, 'up01/pages/login_kk.html',data)


        if request.session.items():

            try:

                session_name = request.session["kk_admin"]

            except Exception as e:
                return render(request, 'up01/pages/login.html')

            if request_path == "/" and session_name == 'kawsar':


                return render(request, 'up01/pages/index.html')



            if session_name == 'kawsar':

                return response
            else:

                return render(request, 'up01/pages/login.html')
        else:

            if request_path == "/login/" or request_path == '/login':
                print("login")
                return response
            else:
                return render(request, 'up01/pages/login.html')


    def process_view(self, request, callback, callback_args, callback_kwargs):

        print("md1 process_view...")


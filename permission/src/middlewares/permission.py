from django.contrib.auth.models import User
from permission.models import GroupPermission, Permission, Log, Group, UserGroup

from django.shortcuts import HttpResponse, redirect

class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        print('estou aqui',request.method,request.path)


        if request.path in ['/admin/login/','/admin/logout/']:
            return response

        if request.user.is_anonymous:
            return redirect('/admin/login/')

        #Pegar o log aqui
        print('estou aqui - pt2',request.method,request.path,request.body)

        l = Log()
        l.user = request.user
        l.url = request.path
        l.text = request.body
        l.save()

        if request.user.is_superuser:
            print('is superuser')
            return response

        permissionExists = Permission.objects.filter(method=request.method,url=request.path)
        if not permissionExists:
            return HttpResponse('Ola permissao não encontrada')

        groupExists = GroupPermission.objects.filter(permission=permissionExists[0].id)
        if not groupExists:
            return HttpResponse('grupo de permissões não encontrado')

        userPermissionExists = UserGroup.objects.filter(user=request.user.id,group=groupExists[0].id)
        if not userPermissionExists:
            return HttpResponse('Você não tem acesso a esse recurso')


        return response
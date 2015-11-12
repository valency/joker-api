from datetime import datetime

from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

from serializers import *


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


@api_view(['POST'])
def register(request):
    if "username" in request.POST and "password" in request.POST:
        try:
            User.objects.get(username=request.POST["username"])
            return Response(status=status.HTTP_409_CONFLICT)
        except ObjectDoesNotExist:
            user = User.objects.create_user(username=request.POST["username"], password=request.POST["password"])
            user.save()
            account = Account(user=user)
            account.save()
            return Response({"id": account.user.id})
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    if "username" in request.POST and "password" in request.POST:
        try:
            User.objects.get(username=request.POST["username"])
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if user is not None:
            if user.is_active:
                token = Token.objects.get_or_create(user=user)
                return Response({
                    "id": Account.objects.get(user=user).id,
                    "ticket": token[0].key
                })
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def change_password(request):
    if "id" in request.POST and "old" in request.POST and "new" in request.POST:
        try:
            account = Account.objects.get(id=int(request.POST["id"]))
            print account
            user = authenticate(username=account.user.username, password=request.POST["old"])
            if user is not None:
                if account.previous_password is not None and request.POST["new"] == account.previous_password:
                    return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
                else:
                    user.set_password(request.POST["new"])
                    user.save()
                    account.previous_password = request.POST["old"]
                    account.last_change_of_password = datetime.now()
                    account.save()
                    return Response(status=status.HTTP_202_ACCEPTED)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def verify(request):
    if "id" in request.GET and "ticket" in request.GET:
        try:
            account = Account.objects.get(id=int(request.GET["id"]))
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.GET["ticket"] == str(Token.objects.get(user=account.user)):
            return Response({
                "id": account.id,
                "last_change_of_password": account.last_change_of_password
            })
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def trust(request):
    html = "<html><body style='margin:10px;'><p>Success!</p><p>You can close this page now.</p></body></html>"
    return HttpResponse(html)

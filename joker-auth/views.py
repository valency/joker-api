import uuid

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate

from serializers import *


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


@api_view(['POST'])
def register(request):
    if "username" in request.POST and "password" in request.POST:
        user = User.objects.create_user(username=request.POST["username"], password=request.POST["password"])
        user.save()
        account = Account(user=user)
        account.save()
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def change_password(request):
    if "id" in request.POST and "old" in request.POST and "new" in request.POST:
        try:
            account = Account.objects.get(id=request.POST["id"])
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if account.auth(request.POST["old"]):
            account.user.set_password(request.POST["new"])
            account.save()
            return Response(AccountSerializer(account).data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    if "username" in request.POST and "password" in request.POST:
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if user is not None and user.is_active:
            account = Account.objects.get(user=user)
            account.ticket = str(uuid.uuid4())
            account.save()
            return Response({
                "id": account.user.id,
                "ticket": account.ticket
            })
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

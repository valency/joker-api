import csv
import gzip
from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist

from serializers import *

from common.common import *


@api_view(['GET'])
def csv_to_json(request):
    if "src" in request.GET:
        with open(DATA_PATH + request.GET["src"], "rb") as f:
            reader = csv.DictReader(f)
            content = [row for row in reader]
        return Response({
            "header": reader.fieldnames,
            "content": content
        })
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def env_get(request):
    if "key" in request.GET:
        try:
            return Response(EnvironmentVariableSerializer(EnviromentVariable.objects.get(key=request.GET["key"])).data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def env_set(request):
    if "key" in request.GET and "value" in request.GET:
        try:
            env_var = EnviromentVariable(key=request.GET["key"], value=request.GET["value"], last_update=datetime.now())
            env_var.save()
            return Response(EnvironmentVariableSerializer(env_var).data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def extract_gzip(request):
    if "src" in request.GET:
        src = DATA_PATH + request.GET["src"]
        dest = DATA_PATH + request.GET["src"][:-3]
        line_count = 0
        with gzip.open(src, 'rb') as infile:
            with open(dest, 'w') as outfile:
                for line in infile:
                    outfile.write(line)
                    line_count += 1
        return Response({
            "src": src,
            "dest": dest,
            "lines": line_count
        })
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

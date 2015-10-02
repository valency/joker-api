import csv

from rest_framework import viewsets
from rest_framework.decorators import api_view

from serializers import *
from common.common import *


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


MT = ModelTools(model=4)


@api_view(['GET'])
def get_cust_by_id(request):
    return MT.get_cust_by_id(request)


@api_view(['GET'])
def get_cust_rank(request):
    return MT.get_cust_rank(request)


@api_view(['GET'])
def get_cust_all(request):
    return MT.get_cust_all(request)


@api_view(['GET'])
def get_cust_field_range(request):
    return MT.get_cust_field_range(request)


@api_view(['GET'])
def get_cust_field_unique(request):
    return MT.get_cust_field_unique(request)


@api_view(['GET'])
def get_cust_sources(request):
    return MT.get_cust_sources(request)


@api_view(['GET'])
def remove_cust_all(request):
    return MT.remove_cust_all(request)


@api_view(['GET'])
def histogram(request):
    return MT.histogram(request)


@api_view(['GET'])
def cust_dist(request):
    return MT.cust_dist(request)


@api_view(['GET'])
def add_cust_from_csv(request):
    if "src" in request.GET:
        count = {
            "processed": 0,
            "success": 0,
            "fail": 0
        }
        try:
            f = open(DATA_PATH + request.GET["src"], "rb")
            reader = csv.DictReader(f)
            for row in reader:
                count["processed"] += 1
                try:
                    cust = Customer(id=int(row["CUST_ID"]), source=request.GET["src"])
                    cust.segment = row["SEGMENT"]
                    cust.age = int(row["AGE"])
                    cust.gender = row["GENDER"]
                    cust.yrs_w_club = int(row["YRS_W_CLUB"])
                    cust.is_member = int(row["IS_MEMBER"]) > 0
                    cust.is_hrs_owner = int(row["IS_HRS_OWNER"]) > 0
                    cust.major_channel = row["MAJOR_CHANNEL"]
                    cust.active_rate = float(row["ACTIVE_RATE"])
                    cust.inv = float(row["INV"])
                    cust.div = float(row["DIV"])
                    cust.rr = float(row["RR"])
                    cust.active_rate_exotic = float(row["ACTIVE_RATE_EXOTIC"])
                    cust.inv_exotic = float(row["INV_EXOTIC"])
                    cust.div_exotic = float(row["DIV_EXOTIC"])
                    cust.rr_exotic = float(row["RR_EXOTIC"])
                    cust.score = float(row["SCORE"])
                    cust.reason_code_1 = row["REASON_CODE_1"]
                    cust.reason_code_2 = row["REASON_CODE_2"]
                    cust.reason_code_3 = row["REASON_CODE_3"]
                    cust.reason_code_4 = row["REASON_CODE_4"]
                    inv_part = []
                    for i in range(0, CUST_INV_PART_COUNT, 1):
                        inv_part.append(float(row["INV" + str(i + 1)]))
                    cust.inv_part = inv_part
                    inv_exotic_part = []
                    for i in range(0, CUST_INV_EXOTIC_COUNT, 1):
                        inv_exotic_part.append(float(row["INV_EXOTIC" + str(i + 1)]))
                    cust.inv_exotic_part = inv_exotic_part
                    cust.save()
                    count["success"] += 1
                except TypeError:
                    count["fail"] += 1
                    continue
            f.close()
        except IOError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(count)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

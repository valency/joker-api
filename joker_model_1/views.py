import csv
import uuid

from rest_framework import viewsets

from rest_framework.decorators import api_view

from serializers import *
from common.common import *


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerSetViewSet(viewsets.ModelViewSet):
    queryset = CustomerSet.objects.all()
    serializer_class = CustomerSetSerializer


MT = ModelTools(model=1)


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
def kmeans(request):
    return MT.kmeans(request)


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
                    cust.mtg_num = int(row["MTG_NUM"])
                    cust.inv = float(row["INV"])
                    cust.div = float(row["DIV"])
                    cust.rr = float(row["RR"])
                    cust.end_bal = float(row["END_BAL"])
                    cust.recharge_times = int(row["RECHARGE_TIMES"])
                    cust.recharge_amount = float(row["RECHARGE_AMOUNT"])
                    cust.withdraw_times = int(row["WITHDRAW_TIMES"])
                    cust.withdraw_amount = float(row["WITHDRAW_AMOUNT"])
                    cust.grow_prop = float(row["GROW_PROPENSITY"])
                    cust.decline_prop = float(row["DECLINE_PROPENSITY"])
                    cust.reason_code_1 = row["REASON_CODE_1"]
                    cust.reason_code_2 = row["REASON_CODE_2"]
                    cust.reason_code_3 = row["REASON_CODE_3"]
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


@api_view(['GET'])
def get_set(request):
    if "id" in request.GET:
        try:
            return Response(CustomerSetSerializer(CustomerSet.objects.get(id=request.GET["id"])).data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def create_set(request):
    if "length" in request.GET and "source" in request.GET:
        try:
            size = int(request.GET["length"])
            cust_set = Customer.objects.filter(source=request.GET["source"])
            # Handle order
            if "order" in request.GET:
                cust_set = cust_set.order_by(request.GET["order"])
            # Handle filter
            if "filter" in request.GET and "filter_mode" in request.GET and request.GET["filter"] != "":
                # Condition: field, in/range, value(~):
                filter_mode = request.GET["filter_mode"]
                filter_set = None
                for c in str(request.GET["filter"]).split(":"):
                    c_part = c.split(",")
                    c_value = c_part[2].split("~")
                    condition = {c_part[0] + "__" + c_part[1]: c_value}
                    if filter_set is None:
                        filter_set = cust_set.filter(**condition)
                    else:
                        if filter_mode == "and":
                            filter_set = filter_set.filter(**condition)
                        elif filter_mode == "or":
                            filter_set = filter_set | cust_set.filter(**condition)
                        else:
                            return Response(status=status.HTTP_400_BAD_REQUEST)
                cust_set = filter_set
            # Handle size
            cust_set = cust_set[:size]
            # Save customer set
            dbset_id = str(uuid.uuid4())
            for cust in cust_set:
                dbset = CustomerSet(id=dbset_id, cust=cust)
                dbset.save()
            # Export
            return Response({
                "id": dbset_id,
                "cust": CustomerSerializer(cust_set, many=True).data
            })
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

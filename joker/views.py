import csv

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator

from serializers import *
from common import *


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


@api_view(['GET'])
def get_cust_by_id(request):
    if "id" in request.GET:
        try:
            cust = Customer.objects.get(id=request.GET["id"])
            return Response(CustomerSerializer(cust).data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_cust_all(request):
    if "start" in request.GET and "length" in request.GET:
        try:
            size = int(request.GET["length"])
            page = int(request.GET["start"]) / size + 1
            cust = Paginator(Customer.objects.all(), size).page(page)
            return Response({
                "recordsTotal": Customer.objects.count(),
                "recordsFiltered": Customer.objects.count(),
                "data": CustomerSerializer(cust, many=True).data
            })
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except TypeError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def remove_cust_by_id(request):
    if "id" in request.GET:
        try:
            cust = Customer.objects.get(id=request.GET["id"])
            cust.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def remove_cust_all(request):
    try:
        cust = Customer.objects.all()
        cust.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def add_cust(request):
    if "cust" in request.POST:
        serializer = CustomerSerializer(data=request.POST["cust"])
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def add_cust_from_csv(request):
    if "src" in request.GET:
        count = {
            "processed": 0,
            "success": 0,
            "fail": 0
        }
        try:
            f = open(Common.DATA_PATH + request.GET["src"], "rb")
            reader = csv.DictReader(f)
            for row in reader:
                count["processed"] += 1
                try:
                    cust = Customer()
                    cust.id = int(row["CUST_ID"])
                    if "AGE" in row.keys(): cust.age = int(row["AGE"])
                    if "GENDER" in row.keys(): cust.gender = row["GENDER"]
                    if "YRS_W_CLUB" in row.keys(): cust.yrs_w_club = int(row["YRS_W_CLUB"])
                    if "IS_MEMBER" in row.keys(): cust.is_member = int(row["IS_MEMBER"]) > 0
                    if "IS_HRS_OWNER" in row.keys(): cust.is_hrs_owner = int(row["IS_HRS_OWNER"]) > 0
                    if "MAJOR_CHANNEL" in row.keys(): cust.major_channel = row["MAJOR_CHANNEL"]
                    if "MTG_NUM" in row.keys(): cust.mtg_num = int(row["MTG_NUM"])
                    if "INV" in row.keys(): cust.inv = float(row["INV"])
                    if "INV_SEG1" in row.keys(): cust.inv_seg_1 = float(row["INV_SEG1"])
                    if "INV_SEG2" in row.keys(): cust.inv_seg_2 = float(row["INV_SEG2"])
                    if "INV_SEG3" in row.keys(): cust.inv_seg_3 = float(row["INV_SEG3"])
                    if "DIV" in row.keys(): cust.div = float(row["DIV"])
                    if "RR" in row.keys(): cust.rr = float(row["RR"])
                    if "END_BAL" in row.keys(): cust.end_bal = float(row["END_BAL"])
                    if "RECHARGE_TIMES" in row.keys(): cust.recharge_times = int(row["RECHARGE_TIMES"])
                    if "RECHARGE_AMOUNT" in row.keys(): cust.recharge_amount = float(row["RECHARGE_AMOUNT"])
                    if "WITHDRAW_TIMES" in row.keys(): cust.withdraw_times = int(row["WITHDRAW_TIMES"])
                    if "WITHDRAW_AMOUNT" in row.keys(): cust.withdraw_amount = float(row["WITHDRAW_AMOUNT"])
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
def assign_pred(request):
    if "id" in request.GET and "label_prob" in request.GET and "reason_code_1" in request.GET and "reason_code_2" in request.GET and "reason_code_3" in request.GET:
        try:
            cust = Customer.objects.get(id=request.GET["id"])
            r = cust.assign_pred(request.GET["label_prob"], request.GET["reason_code_1"], request.GET["reason_code_2"], request.GET["reason_code_3"])
            if r is None:
                return Response(CustomerSerializer(cust).data)
            else:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def assign_pred_from_csv(request):
    if "src" in request.GET:
        count = {
            "processed": 0,
            "success": 0,
            "fail": 0
        }
        try:
            f = open(request.GET["src"], "rb")
            reader = csv.DictReader(f)
            for row in reader:
                count["processed"] += 1
                try:
                    cust = Customer.objects.get(id=request.GET["id"])
                    r = cust.assign_pred(row["LABEL_PROB"], row["REASON_CODE_1"], row["REASON_CODE_2"], row["REASON_CODE_3"])
                    if r is None:
                        count["success"] += 1
                    else:
                        count["fail"] += 1
                except TypeError:
                    count["fail"] += 1
                    continue
                except ObjectDoesNotExist:
                    count["fail"] += 1
                    continue
            f.close()
            return Response(count)
        except IOError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

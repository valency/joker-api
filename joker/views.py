from collections import Counter
import csv
import StringIO

import xlsxwriter
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Count, Max, Min
from django.http import HttpResponse

from djqscsv import render_to_csv_response

from mathematics import *
from serializers import *
from common import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class Customer1ViewSet(viewsets.ModelViewSet):
    queryset = Customer1.objects.all()
    serializer_class = Customer1Serializer


class Customer2ViewSet(viewsets.ModelViewSet):
    queryset = Customer2.objects.all()
    serializer_class = Customer2Serializer


@api_view(['POST'])
def register(request):
    if "username" in request.POST and "password" in request.POST:
        user = User.objects.create_user(username=request.POST["username"], password=request.POST["password"])
        user.save()
        conf = Configuration(export_mode="csv")
        conf.save()
        account = Account(user=user, conf=conf)
        account.save()
        return Response(AccountSerializer(account).data)
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
            return Response(AccountSerializer(account).data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_cust_by_id(request):
    if "id" in request.GET and "model" in request.GET:
        try:
            model = int(request.GET["model"])
            if model == 1:
                return Response(Customer1Serializer(Customer1.objects.get(id=int(request.GET["id"]))).data)
            elif model == 2:
                return Response(Customer2Serializer(Customer2.objects.get(id=int(request.GET["id"]))).data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_cust_rank(request):
    if "id" in request.GET and "model" in request.GET and "column" in request.GET:
        try:
            model = int(request.GET["model"])
            if model == 1:
                cust_set = Customer1.objects
            elif model == 2:
                cust_set = Customer2.objects
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            cust = cust_set.get(id=int(request.GET["id"]))
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        rank = list(cust_set.order_by("-" + request.GET["column"]).values_list(request.GET["column"], flat=True)).index(getattr(cust, request.GET["column"]))
        return Response({"rank": rank, "total": cust_set.count()})
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_cust_all(request):
    if "draw" in request.GET and "start" in request.GET and "length" in request.GET and "model" in request.GET:
        try:
            model = int(request.GET["model"])
            size = int(request.GET["length"])
            page = int(request.GET["start"]) / size + 1
            # Handle model
            if model == 1:
                cust_set = Customer1.objects
            elif model == 2:
                cust_set = Customer2.objects
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # Handle order
            if "order[0][column]" in request.GET:
                order = "-" if "order[0][dir]" in request.GET and request.GET["order[0][dir]"] == "desc" else ""
                keyword = request.GET["columns[" + request.GET["order[0][column]"] + "][data]"]
                cust_set = cust_set.order_by(order + keyword)
            else:
                cust_set = cust_set.all()
            # Handle segment
            if "segment" in request.GET and request.GET["segment"] != "":
                cust_set = cust_set.filter(segment__in=str(request.GET["segment"]).split(","))
            # Export
            if "csv" in request.GET and request.GET["csv"] == "true":
                return render_to_csv_response(cust_set)
            elif "xlsx" in request.GET and request.GET["xlsx"] == "true":
                # if model == 1:
                #     workbook = queryset_to_workbook(cust_set, Customer1._meta.get_all_field_names())
                # elif model == 2:
                #     workbook = queryset_to_workbook(cust_set, Customer2._meta.get_all_field_names())
                # else:
                #     return Response(status=status.HTTP_400_BAD_REQUEST)
                # response = HttpResponse(mimetype='application/vnd.ms-excel')
                # response['Content-Disposition'] = 'attachment; filename="export.xls"'
                # workbook.save(response)
                # return response
                # if model == 1:
                #     data_set = Customer1Serializer(cust_set, many=True).data
                # elif model == 2:
                #     data_set = Customer2Serializer(cust_set, many=True).data
                # else:
                #     return Response(status=status.HTTP_400_BAD_REQUEST)
                # Construct xlsx
                output = StringIO.StringIO()
                book = xlsxwriter.Workbook(output)
                sheet = book.add_worksheet()
                if model == 1:
                    headers = Customer1._meta.get_all_field_names()
                elif model == 2:
                    headers = Customer2._meta.get_all_field_names()
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                sheet.write_row(0, 0, headers)
                row_id = 0
                for row in cust_set:
                    row_id += 1
                    sheet.write_row(row_id, 0, [getattr(row, field) for field in headers])
                book.close()
                # Construct response
                output.seek(0)
                response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                response['Content-Disposition'] = "attachment; filename=cust_export.xlsx"
                return response
            else:
                cust_page = Paginator(cust_set, size).page(page)
                if model == 1:
                    total = Customer1.objects.count()
                    data = Customer1Serializer(cust_page, many=True).data
                elif model == 2:
                    total = Customer2.objects.count()
                    data = Customer2Serializer(cust_page, many=True).data
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                return Response({
                    "draw": int(request.GET["draw"]),
                    "recordsTotal": total,
                    "recordsFiltered": cust_set.count(),
                    "data": data
                })
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def search_cust(request):
    if "model" in request.GET and "length" in request.GET:
        try:
            model = int(request.GET["model"])
            size = int(request.GET["length"])
            # Handle model
            if model == 1:
                cust_set = Customer1.objects
            elif model == 2:
                cust_set = Customer2.objects
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # Handle order
            if "order" in request.GET:
                cust_set = cust_set.order_by(request.GET["order"])
            else:
                cust_set = cust_set.all()
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
            # Export
            cust_set = cust_set[:size]
            if model == 1:
                data = Customer1Serializer(cust_set, many=True).data
            elif model == 2:
                data = Customer2Serializer(cust_set, many=True).data
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_cust_field_range(request):
    if "model" in request.GET and "field" in request.GET:
        try:
            model = int(request.GET["model"])
            field = request.GET["field"]
            if model == 1:
                cust_set = Customer1.objects.all()
            elif model == 2:
                cust_set = Customer2.objects.all()
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            field_max = cust_set.aggregate(Max(field))
            field_min = cust_set.aggregate(Min(field))
            return Response({
                "max": field_max[field + "__max"],
                "min": field_min[field + "__min"]
            })
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_cust_field_unique(request):
    if "model" in request.GET and "field" in request.GET:
        try:
            model = int(request.GET["model"])
            field = request.GET["field"]
            if model == 1:
                cust_set = Customer1.objects
            elif model == 2:
                cust_set = Customer2.objects
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            unique = cust_set.values(field).distinct()
            unique_array = [u[field] for u in unique]
            return Response(unique_array)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def remove_cust_all(request):
    try:
        Customer1.objects.all().delete()
        Customer2.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def add_cust_from_csv(request):
    if "src" in request.GET and "model" in request.GET:
        model = int(request.GET["model"])
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
                    if model == 1:
                        cust = Customer1(id=int(row["CUST_ID"]))
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
                    elif model == 2:
                        cust = Customer2(id=int(row["CUST_ID"]))
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
                        cust.regular_prop = float(row["REGULAR_PROPENSITY"])
                        cust.reason_code_1 = row["REASON_CODE_1"]
                        cust.reason_code_2 = row["REASON_CODE_2"]
                        cust.reason_code_3 = row["REASON_CODE_3"]
                    else:
                        return Response(status=status.HTTP_400_BAD_REQUEST)
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
def histogram(request):
    if "column" in request.GET and "categorical" in request.GET and "model" in request.GET:
        column = request.GET["column"]
        model = int(request.GET["model"])
        if model == 1:
            cust = Customer1.objects.values_list(column, flat=True)
        elif model == 2:
            cust = Customer2.objects.values_list(column, flat=True)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if request.GET["categorical"] == "true":
            hist = numpy.divide(Counter(cust).values(), [float(len(cust))])
            bin_edges = Counter(cust).keys()
        else:
            hist, bin_edges = numpy.histogram(cust, 10)
            hist = numpy.divide(hist, [float(len(cust))])
            bin_edges = bin_edges.tolist()
        return Response({
            "hist": hist,
            "bin_edges": bin_edges
        })
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def kmeans(request):
    if "header" in request.GET and "pred_label" in request.GET and "n_clusters" in request.GET and "n_records" in request.GET and "model" in request.GET:
        # weight = [float(w) for w in request.GET["weight"].split(",")]
        result = Mathematics.joker_kmeans(request.GET["header"].split(","), request.GET["pred_label"], int(request.GET["n_clusters"]), int(request.GET["n_records"]), int(request.GET["model"]))
        if result is not None:
            return Response(result)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def cust_dist(request):
    if "column" in request.GET and "model" in request.GET:
        model = int(request.GET["model"])
        if model == 1:
            cust = Customer1.objects.all()
        elif model == 2:
            cust = Customer2.objects.all()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(cust.values(request.GET["column"]).annotate(total=Count(request.GET["column"])).order_by('-total'))
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def csv_to_json(request):
    if "src" in request.GET:
        with open(Common.DATA_PATH + request.GET["src"], "rb") as f:
            reader = csv.DictReader(f)
            content = [row for row in reader]
        return Response({
            "header": reader.fieldnames,
            "content": content
        })
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

import StringIO
import importlib
from collections import Counter

import numpy
import xlsxwriter
from djqscsv import render_to_csv_response
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Count, Max, Min
from django.http import HttpResponse

DATA_PATH = "/var/www/html/joker/data/"
CATEGORICAL_COLUMNS = ["id", "segment", "age", "gender", "is_member", "is_hrs_owner", "major_channel"]


def scale_linear_by_column(rawpoints, high=1.0, low=0.0):
    mins = numpy.min(rawpoints, axis=0)
    maxs = numpy.max(rawpoints, axis=0)
    rng = maxs - mins
    return numpy.nan_to_num(high - (((high - low) * (maxs - rawpoints)) / rng))


class ModelTools:
    model = 0
    Customer = None
    CustomerSerializer = None

    def __init__(self, model):
        if model != 1 and model != 2:
            raise ValueError("model can only choose from 1 or 2")
        else:
            self.model = model
            self.Customer = importlib.import_module("joker_model_" + str(model) + ".models").Customer
            self.CustomerSerializer = importlib.import_module("joker_model_" + str(model) + ".serializers").CustomerSerializer

    def get_cust_by_id(self, request):
        if "id" in request.GET and "source" in request.GET:
            try:
                cust_set = self.Customer.objects.filter(source=request.GET["source"])
                return Response(self.CustomerSerializer(cust_set.get(id=int(request.GET["id"]))).data)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_cust_rank(self, request):
        if "id" in request.GET and "source" in request.GET and "field" in request.GET:
            try:
                cust_set = self.Customer.objects.filter(source=request.GET["source"])
                cust = cust_set.get(id=int(request.GET["id"]))
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            rank = list(cust_set.order_by("-" + request.GET["field"]).values_list(request.GET["field"], flat=True)).index(getattr(cust, request.GET["field"]))
            return Response({"rank": rank, "total": cust_set.count()})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_cust_all(self, request):
        if "source" in request.GET and "draw" in request.GET and "start" in request.GET and "length" in request.GET:
            try:
                size = int(request.GET["length"])
                page = int(request.GET["start"]) / size + 1
                filename = request.GET["source"].replace(".csv", "").replace("_", "-")
                cust_set = self.Customer.objects.filter(source=request.GET["source"])
                # Handle order
                if "order[0][column]" in request.GET:
                    order = "-" if "order[0][dir]" in request.GET and request.GET["order[0][dir]"] == "desc" else ""
                    keyword = request.GET["columns[" + request.GET["order[0][column]"] + "][data]"]
                    filename += "_" + order + keyword.replace("_", "-")
                    cust_set = cust_set.order_by(order + keyword)
                # Handle segment
                if "segment" in request.GET and request.GET["segment"] != "":
                    filename += "_seg-" + request.GET["segment"]
                    cust_set = cust_set.filter(segment__in=str(request.GET["segment"]).split(","))
                # Export
                if "csv" in request.GET and request.GET["csv"] == "true":
                    return render_to_csv_response(cust_set, filename=filename + ".csv")
                elif "xlsx" in request.GET and request.GET["xlsx"] == "true":
                    output = StringIO.StringIO()
                    book = xlsxwriter.Workbook(output)
                    sheet = book.add_worksheet()
                    headers = self.Customer._meta.get_all_field_names()
                    sheet.write_row(0, 0, headers)
                    row_id = 0
                    for row in cust_set:
                        row_id += 1
                        sheet.write_row(row_id, 0, [getattr(row, field) for field in headers])
                    book.close()
                    # Construct response
                    output.seek(0)
                    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                    response['Content-Disposition'] = "attachment; filename=" + filename + ".xlsx"
                    return response
                else:
                    cust_page = Paginator(cust_set, size).page(page)
                    total = self.Customer.objects.filter(source=request.GET["source"]).count()
                    data = self.CustomerSerializer(cust_page, many=True).data
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

    def get_cust_field_range(self, request):
        if "field" in request.GET and "source" in request.GET:
            try:
                field = request.GET["field"]
                cust_set = self.Customer.objects.filter(source=request.GET["source"])
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

    def get_cust_field_unique(self, request):
        if "field" in request.GET and "source" in request.GET:
            try:
                field = request.GET["field"]
                unique = self.Customer.objects.filter(source=request.GET["source"]).values(field).distinct()
                unique_array = [u[field] for u in unique]
                return Response(unique_array)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_cust_sources(self, request):
        try:
            unique = self.Customer.objects.all().values("source").distinct()
            unique_array = [u["source"] for u in unique]
            return Response(unique_array)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def remove_cust_all(self, request):
        if "source" in request.GET:
            try:
                self.Customer.objects.filter(source=request.GET["source"]).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def histogram(self, request):
        if "field" in request.GET and "categorical" in request.GET and "source" in request.GET:
            field = request.GET["field"]
            cust = self.Customer.objects.filter(source=request.GET["source"]).values_list(field, flat=True)
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

    def cust_dist(self, request):
        if "field" in request.GET and "source" in request.GET:
            return Response(self.Customer.objects.filter(source=request.GET["source"]).values(request.GET["field"]).annotate(total=Count(request.GET["field"])).order_by('-total'))
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

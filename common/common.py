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
from statsmodels.tools import categorical

from kmeans import *

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
                return Response(self.CustomerSerializer(cust_set.get(id=int(request.GET["id"])).data))
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
                cust_set = self.Customer.objects.filter(source=request.GET["source"])
                # Handle order
                if "order[0][column]" in request.GET:
                    order = "-" if "order[0][dir]" in request.GET and request.GET["order[0][dir]"] == "desc" else ""
                    keyword = request.GET["columns[" + request.GET["order[0][column]"] + "][data]"]
                    cust_set = cust_set.order_by(order + keyword)
                # Handle segment
                if "segment" in request.GET and request.GET["segment"] != "":
                    cust_set = cust_set.filter(segment__in=str(request.GET["segment"]).split(","))
                # Export
                if "csv" in request.GET and request.GET["csv"] == "true":
                    return render_to_csv_response(cust_set)
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
                    response['Content-Disposition'] = "attachment; filename=cust_export.xlsx"
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

    def search_cust(self, request):
        if "length" in request.GET and "source" in request.GET:
            try:
                size = int(request.GET["length"])
                cust_set = self.Customer.objects.filter(source=request.GET["source"])
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
                # Export
                cust_set = cust_set[:size]
                data = self.CustomerSerializer(cust_set, many=True).data
                return Response(data)
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

    def remove_cust_all(self, request):
        if "source" in request.GET:
            try:
                self.Customer.objects.filter(source=request.GET["source"]).delete()
                return {
                    "status": status.HTTP_204_NO_CONTENT,
                    "data": ""
                }
            except ObjectDoesNotExist:
                return {
                    "status": status.HTTP_404_NOT_FOUND,
                    "data": ""
                }

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

    def kmeans(self, request):
        if "header" in request.GET and "pred_label" in request.GET and "n_clusters" in request.GET and "n_records" in request.GET and "source" in request.GET:
            # weight = [float(w) for w in request.GET["weight"].split(",")]
            result = self.perform_kmeans(request.GET["header"].split(","), request.GET["pred_label"], int(request.GET["n_clusters"]), int(request.GET["n_records"]), request.GET["source"])
            if result is not None:
                return Response(result)
            else:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def perform_kmeans(self, header, pred_label, n_clusters, n_records, source):
        cust_set = self.Customer.objects.filter(source=source).order_by("-" + pred_label)[:n_records]
        cust_matrix = numpy.array([])
        id_list = numpy.array([cust.id for cust in cust_set])
        for h in header:
            # Choose header
            cust_column = numpy.array([getattr(cust, h) for cust in cust_set])
            if h in CATEGORICAL_COLUMNS:
                cust_column = categorical(cust_column, drop=True)
            # Stack to matrix
            if cust_matrix.size == 0:
                cust_matrix = cust_column
            else:
                cust_matrix = numpy.column_stack((cust_matrix, cust_column))
        # Normalize
        cust_matrix = scale_linear_by_column(cust_matrix)
        # Weight
        # cust_matrix = numpy.nan_to_num(numpy.multiply(cust_matrix, numpy.array([numpy.array(weight)] * cust_set.count())))
        # Clustering
        kmeans_centres, kmeans_xtoc, kmeans_dist = kmeans(cust_matrix, randomsample(cust_matrix, n_clusters), metric="cosine")
        # Output
        result = []
        for i in range(0, len(id_list)):
            entity = {
                "id": id_list[i],
                "cluster": kmeans_xtoc[i]
            }
            cust = self.Customer.objects.filter(source=source).get(id=id_list[i])
            for h in header:
                entity[h] = cust.__dict__[h]
            result.append(entity)
        return result

    def cust_dist(self, request):
        if "field" in request.GET and "source" in request.GET:
            return Response(self.Customer.objects.filter(source=request.GET["source"]).values(request.GET["field"]).annotate(total=Count(request.GET["field"])).order_by('-total'))
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

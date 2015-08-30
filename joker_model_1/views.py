import csv
import uuid
from datetime import datetime

from statsmodels.tools import categorical
from rest_framework import viewsets
from rest_framework.decorators import api_view

from serializers import *
from common.common import *
import common.kmeans as joker_kmeans


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
def cust_dist(request):
    return MT.cust_dist(request)


@api_view(['GET'])
def kmeans(request):
    if "header" in request.GET and "n_clusters" in request.GET and "set_id" in request.GET:
        # weight = [float(w) for w in request.GET["weight"].split(",")]
        header = request.GET["header"].split(",")
        n_clusters = int(request.GET["n_clusters"])
        cust_set = CustomerSet.objects.filter(id=request.GET["set_id"])
        cust_matrix = numpy.array([])
        dbpk_list = numpy.array([entity.cust.dbpk for entity in cust_set])
        for h in header:
            # Choose header
            cust_column = numpy.array([getattr(entity.cust, h) for entity in cust_set])
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
        kmeans_centres, kmeans_xtoc, kmeans_dist = joker_kmeans.kmeans(cust_matrix, joker_kmeans.randomsample(cust_matrix, n_clusters), metric="cosine")
        # Output
        result = []
        for i in range(0, len(dbpk_list)):
            # Update cust set configurations
            cust = Customer.objects.get(dbpk=dbpk_list[i])
            cust_set_entity = cust_set.get(cust=cust)
            cust_set_entity.cluster_time = datetime.now()
            cust_set_entity.cluster_features = header
            cust_set_entity.cluster = kmeans_xtoc[i]
            cust_set_entity.cluster_count = n_clusters
            cust_set_entity.save()
            # Construct response
            entity = {
                "id": cust.id,
                "cluster": kmeans_xtoc[i]
            }
            for h in header:
                entity[h] = cust.__dict__[h]
            result.append(entity)
        return Response(result)
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
                    cust.grow_reason_code_1 = row["GROW_REASON_CODE_1"]
                    cust.grow_reason_code_2 = row["GROW_REASON_CODE_2"]
                    cust.grow_reason_code_3 = row["GROW_REASON_CODE_3"]
                    cust.decline_reason_code_1 = row["DECLINE_REASON_CODE_1"]
                    cust.decline_reason_code_2 = row["DECLINE_REASON_CODE_2"]
                    cust.decline_reason_code_3 = row["DECLINE_REASON_CODE_3"]
                    inv_part = []
                    for i in range(0, CUST_INV_PART_COUNT, 1):
                        inv_part.append(float(row["INV" + str(i + 1)]))
                    cust.inv_part = inv_part
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
def delete_set(request):
    if "id" in request.GET:
        try:
            CustomerSet.objects.filter(id=request.GET["id"]).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_set(request):
    if "id" in request.GET:
        resp = {
            "id": None,
            "name": None,
            "create_time": None,
            "cluster_time": None,
            "cluster_features": None,
            "cust": []
        }
        try:
            cust_set = CustomerSetSerializer(CustomerSet.objects.filter(id=request.GET["id"]), many=True).data
            for cust_set_entity in cust_set:
                if resp["id"] is None:
                    resp["id"] = cust_set_entity["id"]
                    resp["name"] = cust_set_entity["name"]
                    resp["create_time"] = cust_set_entity["create_time"]
                    resp["cluster_time"] = cust_set_entity["cluster_time"]
                    resp["cluster_features"] = cust_set_entity["cluster_features"]
                resp["cust"].append({
                    "cust": cust_set_entity["cust"],
                    "cluster": cust_set_entity["cluster"]
                })
            return Response(resp)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_set_all(request):
    return Response([{"id": u["id"], "name": CustomerSet.objects.filter(id=u["id"])[0].name} for u in CustomerSet.objects.all().values("id").distinct()])


@api_view(['GET'])
def create_set(request):
    if "length" in request.GET and "source" in request.GET and "name" in request.GET:
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
            name = request.GET["name"]
            if len(name) == 0 or name is None:
                name = dbset_id
            for cust in cust_set:
                dbset = CustomerSet(id=dbset_id, name=name, create_time=datetime.now(), cust=cust)
                dbset.save()
            # Export
            return Response({
                "id": dbset_id,
                "name": name,
                "cust": CustomerSerializer(cust_set, many=True).data
            })
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

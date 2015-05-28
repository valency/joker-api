from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from rest_framework import viewsets
from django.core.exceptions import ObjectDoesNotExist

from serializers import *


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs["content_type"] = "application/json;charset=utf-8"
        super(JSONResponse, self).__init__(content, **kwargs)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


def resp(status, content):
    return JSONResponse({"status": status, "content": content})


def get_cust_by_id(request):
    if "id" in request.GET:
        try:
            cust = Customer.objects.get(id=request.GET["id"])
            return resp(200, CustomerSerializer(cust).data)
        except ObjectDoesNotExist:
            return resp(404, "cust not exist")
    else:
        return resp(500, "parameter not correct")


def assign_pred(request):
    if "id" in request.GET and "label_prob" in request.GET and "reason_code_1" in request.GET and "reason_code_2" in request.GET and "reason_code_3" in request.GET:
        try:
            cust = Customer.objects.get(id=request.GET["id"])
            r = cust.assign_pred(request.GET["label_prob"], request.GET["reason_code_1"], request.GET["reason_code_2"], request.GET["reason_code_3"])
            return resp(r["status"], r["content"])
        except ObjectDoesNotExist:
            return resp(404, "cust not exist")
    else:
        return resp(500, "parameter not correct")


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
                    if r["status"] == 200:
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
            return resp(200, count)
        except IOError as exp:
            return resp(500, exp.strerror)
    else:
        return resp(500, "parameter not correct")

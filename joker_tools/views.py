import csv
import gzip
import operator
import os
from datetime import datetime, timedelta

from rest_framework.decorators import api_view

from joker_common.views import *
from joker_model_1.models import Customer as Customer1
from joker_model_2.models import Customer as Customer2
from joker_model_4.models import Customer as Customer4
from serializers import *


def export_csv(data, filename):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + filename
    writer = csv.writer(response, csv.excel)
    writer.writerow(data[0].keys())
    for obj in data:
        writer.writerow(obj.values())
    return response


def get_latest_data_file_list():
    latest_file = dict()
    for f in os.listdir(DATA_PATH):
        if f.lower().endswith('.csv'):
            for model, prefix in DATA_NAME_PREFIX.iteritems():
                if prefix in f:
                    if model not in latest_file or int(f.replace(prefix, "")[:8]) > int(latest_file[model].replace(prefix, "")[:8]):
                        latest_file[model] = f
                    break
    return latest_file


def convert_data_file_meta():
    resp = dict()
    latest_file = get_latest_data_file_list()
    resp["grow_update"] = datetime.fromtimestamp(os.path.getmtime(DATA_PATH + latest_file["1"])).strftime("%Y-%m-%d %H:%M:%S")
    resp["grow_from"] = latest_file["1"].replace(DATA_NAME_PREFIX["1"], "")[:8]
    resp["grow_to"] = latest_file["1"].replace(DATA_NAME_PREFIX["1"], "")[9:17]
    resp["lapse_update"] = resp["grow_update"]
    resp["lapse_from"] = resp["grow_from"]
    resp["lapse_to"] = resp["grow_to"]
    resp["regular_update"] = datetime.fromtimestamp(os.path.getmtime(DATA_PATH + latest_file["2"])).strftime("%Y-%m-%d %H:%M:%S")
    resp["regular_from"] = latest_file["2"].replace(DATA_NAME_PREFIX["2"], "")[:8]
    resp["regular_to"] = latest_file["2"].replace(DATA_NAME_PREFIX["2"], "")[9:17]
    resp["preference_update"] = datetime.fromtimestamp(os.path.getmtime(DATA_PATH + latest_file["4"])).strftime("%Y-%m-%d %H:%M:%S")
    resp["preference_from"] = latest_file["4"].replace(DATA_NAME_PREFIX["4"], "")[:8]
    resp["preference_to"] = latest_file["4"].replace(DATA_NAME_PREFIX["4"], "")[9:17]
    resp["participation_update"] = resp["preference_update"]
    resp["participation_from"] = resp["preference_from"]
    resp["participation_to"] = resp["preference_to"]
    resp["date"] = (datetime.strptime(resp["preference_from"], "%Y%m%d").date() - timedelta(1)).strftime("%Y%m%d")
    return resp


def string_similarity(str1, str2):
    str1_seg = str1.split(" ")
    str2_seg = str2.split(" ")
    return len(set(str1_seg) & set(str2_seg))


def search_reason_code(rc):
    if rc == "NA":
        return 0
    reason_codes = [i["desc"] for i in REASON_CODES]
    p = [string_similarity(rc, i) for i in reason_codes]
    max_index, max_value = max(enumerate(p), key=operator.itemgetter(1))
    return [i["rcode_id"] for i in REASON_CODES if i["desc"] == reason_codes[max_index]][0]


def repr_reason_code(rc_id, rc_text):
    if rc_id == 0 or rc_text == "NA":
        return None
    rc = [i["desc"] for i in REASON_CODES if rc_id == i["rcode_id"]][0]
    if "[0]" in rc.split(" "):
        return rc_text.split(" ")[rc.split(" ").index("[0]")]
    else:
        return None


def create_empty_cust(date, cust_id):
    return {
        "date": date,
        "cust_id": cust_id,
        "grow_score": None,
        "grow_rcode_1": None,
        "grow_rcode_value_1": None,
        "grow_rcode_2": None,
        "grow_rcode_value_2": None,
        "grow_rcode_3": None,
        "grow_rcode_value_3": None,
        "grow_rcode_4": None,
        "grow_rcode_value_4": None,
        "decline_score": None,
        "decline_rcode_1": None,
        "decline_rcode_value_1": None,
        "decline_rcode_2": None,
        "decline_rcode_value_2": None,
        "decline_rcode_3": None,
        "decline_rcode_value_3": None,
        "decline_rcode_4": None,
        "decline_rcode_value_4": None,
        "regular_score": None,
        "regular_rcode_1": None,
        "regular_rcode_value_1": None,
        "regular_rcode_2": None,
        "regular_rcode_value_2": None,
        "regular_rcode_3": None,
        "regular_rcode_value_3": None,
        "regular_rcode_4": None,
        "regular_rcode_value_4": None,
        "preference_score": None,
        "participation_score": None
    }


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
            return Response(EnvironmentVariableSerializer(EnvironmentVariable.objects.get(key=request.GET["key"])).data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def env_set(request):
    if "key" in request.GET and "value" in request.GET:
        try:
            env_var = EnvironmentVariable(key=request.GET["key"], value=request.GET["value"], last_update=datetime.now())
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


@api_view(['GET'])
def reason_code(request):
    return export_csv(REASON_CODES, "reason_code.csv")


@api_view(['GET'])
def update_info(request):
    return export_csv([convert_data_file_meta()], "update_info.csv")


@api_view(['GET'])
def full_result(request):
    if "date" in request.GET:
        meta_date = request.GET["date"]
        file_date = (datetime.strptime(meta_date, "%Y%m%d").date() + timedelta(1)).strftime("%Y%m%d")
        target_file = dict()
        for f in os.listdir(DATA_PATH):
            if f.lower().endswith('.csv'):
                for model, prefix in DATA_NAME_PREFIX.iteritems():
                    if prefix + file_date in f:
                        target_file[model] = f
                        break
        if len(target_file.keys()) < 3:
            return Response(status=status.HTTP_404_NOT_FOUND, data="Cannot find appropriate files regrading to the requested date.")
    else:
        meta_date = convert_data_file_meta()["date"]
        target_file = get_latest_data_file_list()
    resp = list()
    for cust in Customer1.objects.filter(source=target_file["1"]):
        c = create_empty_cust(meta_date, cust.id)
        c["grow_score"] = cust.grow_prop
        c["grow_rcode_1"] = search_reason_code(cust.grow_reason_code_1)
        c["grow_rcode_value_1"] = repr_reason_code(c["grow_rcode_1"], cust.grow_reason_code_1)
        c["grow_rcode_2"] = search_reason_code(cust.grow_reason_code_2)
        c["grow_rcode_value_2"] = repr_reason_code(c["grow_rcode_2"], cust.grow_reason_code_2)
        c["grow_rcode_3"] = search_reason_code(cust.grow_reason_code_3)
        c["grow_rcode_value_3"] = repr_reason_code(c["grow_rcode_3"], cust.grow_reason_code_3)
        c["grow_rcode_4"] = search_reason_code(cust.grow_reason_code_4)
        c["grow_rcode_value_4"] = repr_reason_code(c["grow_rcode_4"], cust.grow_reason_code_4)
        c["decline_score"] = cust.decline_prop
        c["decline_rcode_1"] = search_reason_code(cust.decline_reason_code_1)
        c["decline_rcode_value_1"] = repr_reason_code(c["decline_rcode_1"], cust.decline_reason_code_1)
        c["decline_rcode_2"] = search_reason_code(cust.decline_reason_code_2)
        c["decline_rcode_value_2"] = repr_reason_code(c["decline_rcode_2"], cust.decline_reason_code_2)
        c["decline_rcode_3"] = search_reason_code(cust.decline_reason_code_3)
        c["decline_rcode_value_3"] = repr_reason_code(c["decline_rcode_3"], cust.decline_reason_code_3)
        c["decline_rcode_4"] = search_reason_code(cust.decline_reason_code_4)
        c["decline_rcode_value_4"] = repr_reason_code(c["decline_rcode_4"], cust.decline_reason_code_4)
        resp.append(c)
    for cust in Customer2.objects.filter(source=target_file["2"]):
        c = None
        for cc in resp:
            if cc["cust_id"] == cust.id:
                c = cc
                break
        if c is None:
            c = create_empty_cust(meta_date, cust.id)
            resp.append(c)
        c["regular_score"] = cust.chance_to_be_regular
        c["regular_rcode_1"] = search_reason_code(cust.reason_code_1)
        c["regular_rcode_value_1"] = repr_reason_code(c["regular_rcode_1"], cust.reason_code_1)
        c["regular_rcode_2"] = search_reason_code(cust.reason_code_2)
        c["regular_rcode_value_2"] = repr_reason_code(c["regular_rcode_2"], cust.reason_code_2)
        c["regular_rcode_3"] = search_reason_code(cust.reason_code_3)
        c["regular_rcode_value_3"] = repr_reason_code(c["regular_rcode_3"], cust.reason_code_3)
        c["regular_rcode_4"] = search_reason_code(cust.reason_code_4)
        c["regular_rcode_value_4"] = repr_reason_code(c["regular_rcode_4"], cust.reason_code_4)
    for cust in Customer4.objects.filter(source=target_file["4"]):
        c = None
        for cc in resp:
            if cc["cust_id"] == cust.id:
                c = cc
                break
        if c is None:
            c = create_empty_cust(meta_date, cust.id)
            resp.append(c)
        c["preference_score"] = cust.score_hp_preference
        c["participation_score"] = cust.score_hp_participation
    return export_csv(resp, "full_result_" + meta_date + ".csv")

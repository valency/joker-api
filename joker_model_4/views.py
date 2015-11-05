import csv

from rest_framework import viewsets
from rest_framework.decorators import api_view

from joker_common.views import *
from serializers import *


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
                    cust.ar = float(row["AR"])
                    cust.inv_standard = float(row["INV_STANDARD"])
                    cust.div_standard = float(row["DIV_STANDARD"])
                    cust.rr_standard = float(row["RR_STANDARD"])
                    cust.ar_exotic = float(row["AR_EXOTIC"])
                    cust.inv_exotic = float(row["INV_EXOTIC"])
                    cust.div_exotic = float(row["DIV_EXOTIC"])
                    cust.rr_exotic = float(row["RR_EXOTIC"])
                    cust.betline_standard = int(row["BETLINE_STANDARD"])
                    cust.betline_exotic = int(row["BETLINE_EXOTIC"])
                    cust.mtg_num = int(row["MTG_NUM"])
                    cust.mtg_num_exotic = int(row["MTG_NUM_EXOTIC"])
                    cust.end_bal = float(row["END_BAL"])
                    cust.recharge_times = int(row["RECHARGE_TIMES"])
                    cust.recharge_amount = float(row["RECHARGE_AMOUNT"])
                    cust.withdraw_times = int(row["WITHDRAW_TIMES"])
                    cust.withdraw_amount = float(row["WITHDRAW_AMOUNT"])
                    cust.betline_1_half = int(row["BETLINE_1_HALF"])
                    cust.betline_2_half = int(row["BETLINE_2_HALF"])
                    cust.betline_recent = int(row["BETLINE_RECENT"])
                    cust.betline_exotic_recent = int(row["BETLINE_EXOTIC_RECENT"])
                    cust.exotic_half_increase = int(row["EXOTIC_HALF_INCREASE"])
                    cust.exotic_half_increase_ratio = float(row["EXOTIC_HALF_INCREASE_RATIO"])
                    cust.exotic_percent_1_half = float(row["EXOTIC_PERCENT_1_HALF"])
                    cust.exotic_percent_2_half = float(row["EXOTIC_PERCENT_2_HALF"])
                    cust.exotic_percent_half_increase = float(row["EXOTIC_PERCENT_HALF_INCREASE"])
                    cust.exotic_betline_percent = float(row["EXOTIC_BETLINE_PERCENT"])
                    cust.score_hp_preference = float(row["SCORE_HP_PREFERENCE"])
                    cust.score_hp_participation = float(row["SCORE_HP_PARTICIPATION"])
                    cust.hp_preference_reason_code_1 = row["HP_PREFERENCE_REASON_CODE_1"]
                    cust.hp_preference_reason_code_2 = row["HP_PREFERENCE_REASON_CODE_2"]
                    cust.hp_preference_reason_code_3 = row["HP_PREFERENCE_REASON_CODE_3"]
                    cust.hp_preference_reason_code_4 = row["HP_PREFERENCE_REASON_CODE_4"]
                    cust.hp_participation_reason_code_1 = row["HP_PARTICIPATION_REASON_CODE_1"]
                    cust.hp_participation_reason_code_2 = row["HP_PARTICIPATION_REASON_CODE_2"]
                    cust.hp_participation_reason_code_3 = row["HP_PARTICIPATION_REASON_CODE_3"]
                    cust.hp_participation_reason_code_4 = row["HP_PARTICIPATION_REASON_CODE_4"]
                    betline_standard_part = []
                    for i in range(0, CUST_INV_PART_COUNT, 1):
                        betline_standard_part.append(row["BETLINE_STANDARD" + str(i + 1)])
                    cust.betline_standard_part = ";".join(betline_standard_part)
                    betline_exotic_part = []
                    for i in range(0, CUST_INV_EXOTIC_COUNT, 1):
                        betline_exotic_part.append(row["BETLINE_EXOTIC" + str(i + 1)])
                    cust.betline_exotic_part = ";".join(betline_exotic_part)
                    cust.save()
                    count["success"] += 1
                except TypeError, exp:
                    count["fail"] += 1
                    print "TypeError:", exp
                print "\rImporting Row: " + str(count["processed"]),
            f.close()
        except IOError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(count)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

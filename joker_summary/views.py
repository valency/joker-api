import time

from django.db.models import Avg, Sum
from django.db.models import Count
from django.utils.termcolors import colorize
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from joker_summary.serializers import *

SUMMARY = dict()


def get_summary_by_season(season):
    global SUMMARY
    if season not in SUMMARY:
        SUMMARY[season] = create_summary_dict(season)
    return SUMMARY[season]


def create_summary_dict(season):
    print(colorize("Creating summary cache for season " + str(season) + "...", fg="green"))
    summary_dict = dict()
    start = time.time()
    stat_result = Summary.objects.filter(global_mtg_seqno__season=season, global_mtg_seqno__mtg_status="N").values("global_mtg_seqno", "cust_id__segment_code").annotate(Avg("global_mtg_seqno__season_mtg_seqno"), Count("cust_id"), Sum("standard_turnover"), Sum("exotic_turnover"), Sum("standard_betline"), Sum("exotic_betline"), Sum("race_num"), Sum("active_rate_ytd"), Sum("active_mtg_ytd"), Sum("standard_turnover_ytd"), Sum("exotic_turnover_ytd"), Sum("standard_betline_ytd"), Sum("exotic_betline_ytd")).order_by("global_mtg_seqno")
    for value_list in stat_result:
        if value_list["cust_id__segment_code"] is None:
            value_list["cust_id__segment_code"] = "other"
        if not summary_dict.has_key(value_list["cust_id__segment_code"]):
            summary_dict[value_list["cust_id__segment_code"]] = dict()
        summary_dict[value_list["cust_id__segment_code"]][value_list["global_mtg_seqno"]] = value_list
    end = time.time()
    print(colorize("Creating summary cache takes " + str(end - start) + " seconds.", fg="green"))
    return summary_dict


@api_view(['GET'])
def retrieve_segment_values(request):
    segment_values = Customer.objects.filter().values("segment_code").distinct()
    return Response(segment_values)


@api_view(['GET'])
def year_on_year_growth(request):
    if "season" in request.GET and "field" in request.GET:
        start = time.time()
        season = int(request.GET["season"])
        summary = get_summary_by_season(season)
        summary_last = get_summary_by_season(season - 1)
        if "segment" in request.GET:
            segment = request.GET["segment"].split(",")
        else:
            segment = summary.keys()
        field = request.GET["field"]
        global_mtg_seqno = summary[summary.keys()[0]].keys()
        global_mtg_seqno.sort()
        global_mtg_seqno_last = summary_last[summary_last.keys()[0]].keys()
        global_mtg_seqno_last.sort()
        std_value = [0] * len(global_mtg_seqno)
        exo_value = [0] * len(global_mtg_seqno)
        std_value_last = [0] * len(global_mtg_seqno)
        exo_value_last = [0] * len(global_mtg_seqno)
        std_value_ytd = [0] * len(global_mtg_seqno)
        exo_value_ytd = [0] * len(global_mtg_seqno)
        std_value_pytd = [0] * len(global_mtg_seqno)
        exo_value_pytd = [0] * len(global_mtg_seqno)
        std_growth = []
        exo_growth = []
        for i in range(len(global_mtg_seqno)):
            for s in segment:
                if summary.has_key(s) and summary[s].has_key(global_mtg_seqno[i]):
                    std_value[i] += summary[s][global_mtg_seqno[i]]["standard_" + field + "__sum"]
                    exo_value[i] += summary[s][global_mtg_seqno[i]]["exotic_" + field + "__sum"]
                    std_value_ytd[i] += summary[s][global_mtg_seqno[i]]["standard_" + field + "_ytd__sum"]
                    exo_value_ytd[i] += summary[s][global_mtg_seqno[i]]["exotic_" + field + "_ytd__sum"]
                if summary_last.has_key(s) and summary_last[s].has_key(global_mtg_seqno_last[i]):
                    std_value_last[i] += summary_last[s][global_mtg_seqno_last[i]]["standard_" + field + "__sum"]
                    exo_value_last[i] += summary_last[s][global_mtg_seqno_last[i]]["exotic_" + field + "__sum"]
                    std_value_pytd[i] += summary_last[s][global_mtg_seqno_last[i]]["standard_" + field + "_ytd__sum"]
                    exo_value_pytd[i] += summary_last[s][global_mtg_seqno_last[i]]["exotic_" + field + "_ytd__sum"]
            std_growth.append(float(std_value_ytd[i] - std_value_pytd[i]) / float(std_value_pytd[i]))
            exo_growth.append(float(exo_value_ytd[i] - exo_value_pytd[i]) / float(exo_value_pytd[i]))
        end = time.time()
        print("Task time: " + str(end - start) + " seconds...")
        return Response({
            "standard_" + field: {
                "standard_" + field + "_previous_season": std_value_last,
                "standard_" + field + "_this_season": std_value,
                "total_standard_" + field + "_pytd": std_value_pytd,
                "total_standard_" + field + "_ytd": std_value_ytd,
                "cumulative_growth_rate_of_total_standard_" + field: std_growth
            },
            "exotic_" + field: {
                "exotic_" + field + "_previous_season": exo_value_last,
                "exotic_" + field + "_this_season": exo_value,
                "total_exotic_" + field + "_pytd": exo_value_pytd,
                "total_exotic_" + field + "_ytd": exo_value_ytd,
                "cumulative_growth_rate_of_total_exotic_" + field: exo_growth
            }
        })
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

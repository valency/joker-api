import time
import numpy
from collections import Counter

from django.db.models import Avg, Sum, Min, Max
from django.db.models import Count
from django.utils.termcolors import colorize
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from joker_summary.serializers import *

SUMMARY = dict()
CHANNEL = dict()
CUSTOMER = dict()
ACTIVE = dict()
CUST_ANALYSIS = dict()
# New cache
NEW_CUST_SUMMARY = dict()
BET_TYPE = dict()


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


def get_channel_by_season(season):
    global CHANNEL
    if season not in CHANNEL:
        CHANNEL[season] = create_channel_dict(season)
    return CHANNEL[season]


def create_channel_dict(season):
    print colorize("Creating channel cache for season " + str(season) + "...", fg="green")
    channel_dict = dict()
    start = time.time()
    channel_info = Summary.objects.filter(global_mtg_seqno__season=season, global_mtg_seqno__mtg_status="N").values("turnover_channel_details", "cust_id__segment_code")
    for info in channel_info:
        if info["cust_id__segment_code"] is None:
            info["cust_id__segment_code"] = "other"
        if not channel_dict.has_key(info["cust_id__segment_code"]):
            channel_dict[info["cust_id__segment_code"]] = dict()
        for channel in info["turnover_channel_details"]:
            if not channel_dict[info["cust_id__segment_code"]].has_key(channel):
                channel_dict[info["cust_id__segment_code"]][channel] = dict()
                channel_dict[info["cust_id__segment_code"]][channel]["standard_turnover"] = 0.0
                channel_dict[info["cust_id__segment_code"]][channel]["exotic_turnover"] = 0.0
            channel_dict[info["cust_id__segment_code"]][channel]["standard_turnover"] += info["turnover_channel_details"][channel][0]
            channel_dict[info["cust_id__segment_code"]][channel]["exotic_turnover"] += info["turnover_channel_details"][channel][1]
    end = time.time()
    print "Creating channel cache takes " + str(end - start) + " seconds..."
    return channel_dict


def get_num_cust(season):
    global CUSTOMER
    if season not in CUSTOMER:
        CUSTOMER[season] = create_customer_dict()
    return CUSTOMER[season]


def create_customer_dict():
    customer_dict = dict()
    num_cust = Customer.objects.all().values("segment_code").annotate(Count("cust_id"))
    for num in num_cust:
        if num["segment_code"] is None:
            num["segment_code"] = "other"
        customer_dict[num["segment_code"]] = num["cust_id__count"]
    return customer_dict


def get_active_by_season(season):
    global ACTIVE
    if season not in ACTIVE:
        ACTIVE[season] = create_active_dict(season)
    return ACTIVE[season]


def create_active_dict(season):
    print colorize("Creating active cache for season " + str(season) + "...", fg="green")
    active_dict = dict()
    start = time.time()
    active_info = Summary.objects.filter(global_mtg_seqno__season=season, global_mtg_seqno__mtg_status="N").values("cust_id", "cust_id__segment_code").annotate(Min("global_mtg_seqno"), Min("global_mtg_seqno__season_mtg_seqno"))
    for info in active_info:
        if info["cust_id__segment_code"] is None:
            info["cust_id__segment_code"] = "other"
        if not active_dict.has_key(info["cust_id__segment_code"]):
            active_dict[info["cust_id__segment_code"]] = dict()
        active_dict[info["cust_id__segment_code"]][info["cust_id"]] = info
    end = time.time()
    print "Creating active cache takes " + str(end - start) + " seconds..."
    return active_dict


def get_cust_analysis_by_season(season):
    global CUST_ANALYSIS
    if season not in CUST_ANALYSIS:
        CUST_ANALYSIS[season] = dict()
        early_wakeup_dict, reactive_dict, inactive_dict = create_cust_analysis_dict(season)
        CUST_ANALYSIS[season]["early_wakeup"] = early_wakeup_dict
        CUST_ANALYSIS[season]["reactive"] = reactive_dict
        CUST_ANALYSIS[season]["inactive"] = inactive_dict
    return CUST_ANALYSIS[season]


def create_cust_analysis_dict(season):
    print colorize("Creating customer analysis cache for season " + str(season) + "...", fg="green")
    early_wakeup_dict = dict()
    reactive_dict = dict()
    inactive_dict = dict()
    start = time.time()
    summary = get_summary_by_season(season)
    active = get_active_by_season(season)
    active_last = get_active_by_season(season - 1)
    segment = summary.keys()
    global_mtg_seqno = summary[summary.keys()[0]].keys()
    global_mtg_seqno.sort()
    for s in segment:
        early_wakeup_dict[s] = [0 for i in range(len(global_mtg_seqno))]
        reactive_dict[s] = [0 for i in range(len(global_mtg_seqno))]
        inactive_dict[s] = [0 for i in range(len(global_mtg_seqno))]
        if active.has_key(s):
            for cust_id in active[s]:
                wake = active[s][cust_id]["global_mtg_seqno__season_mtg_seqno__min"]
                if active_last.has_key(s) and active_last[s].has_key(cust_id):
                    wake_last = active_last[s][cust_id]["global_mtg_seqno__season_mtg_seqno__min"]
                    if wake_last > wake:
                        for i in range(wake - 1, min(wake_last - 1, len(global_mtg_seqno))):
                            early_wakeup_dict[s][i] += 1
                else:
                    for i in range(wake - 1, len(global_mtg_seqno)):
                        reactive_dict[s][i] += 1
        if active_last.has_key(s):
            for cust_id in active_last[s]:
                if active.has_key(s) and active[s].has_key(cust_id):
                    wake = active[s][cust_id]["global_mtg_seqno__season_mtg_seqno__min"]
                else:
                    wake = len(global_mtg_seqno) + 1
                for i in range(wake - 1):
                    inactive_dict[s][i] += 1
    end = time.time()
    print "Creating customer analysis cache takes " + str(end - start) + " seconds..."
    return early_wakeup_dict, reactive_dict, inactive_dict


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


@api_view(['GET'])
def active_rate(request):
    if "season" in request.GET and "type" in request.GET:
        start = time.time()
        season = int(request.GET["season"])
        summary = get_summary_by_season(season)
        summary_last = get_summary_by_season(season - 1)
        if "segment" in request.GET:
            segment = request.GET["segment"].split(",")
        else:
            segment = summary.keys()
        global_mtg_seqno = summary[summary.keys()[0]].keys()
        global_mtg_seqno.sort()
        global_mtg_seqno_last = summary_last[summary_last.keys()[0]].keys()
        global_mtg_seqno_last.sort()
        num_cust = [0 for i in range(len(global_mtg_seqno))]
        num_cust_last = [0 for i in range(len(global_mtg_seqno))]
        active_rate_sum = [0 for i in range(len(global_mtg_seqno))]
        active_rate_sum_last = [0 for i in range(len(global_mtg_seqno))]
        meeting_id = [-1 for i in range(len(global_mtg_seqno))]
        meeting_id_last = [-1 for i in range(len(global_mtg_seqno))]
        for i in range(len(global_mtg_seqno)):
            for s in segment:
                if summary.has_key(s) and summary[s].has_key(global_mtg_seqno[i]):
                    meeting_id[i] = int(summary[s][global_mtg_seqno[i]]["global_mtg_seqno__season_mtg_seqno__avg"])
                    num_cust[i] += summary[s][global_mtg_seqno[i]]["cust_id__count"]
                    active_rate_sum[i] += summary[s][global_mtg_seqno[i]]["active_rate_ytd__sum"]
                if request.GET["type"] == "year":
                    if summary_last.has_key(s) and summary_last[s].has_key(global_mtg_seqno_last[i]):
                        meeting_id_last[i] = int(summary_last[s][global_mtg_seqno_last[i]]["global_mtg_seqno__season_mtg_seqno__avg"])
                        num_cust_last[i] += summary_last[s][global_mtg_seqno_last[i]]["cust_id__count"]
                        active_rate_sum_last[i] += summary_last[s][global_mtg_seqno_last[i]]["active_rate_ytd__sum"]
                elif request.GET["type"] == "month":
                    if i < 16:
                        if summary_last.has_key(s) and summary_last[s].has_key(global_mtg_seqno[i] - 16):
                            meeting_id_last[i] = int(summary_last[s][global_mtg_seqno[i] - 16]["global_mtg_seqno__season_mtg_seqno__avg"])
                            num_cust_last[i] += summary_last[s][global_mtg_seqno[i] - 16]["cust_id__count"]
                            active_rate_sum_last[i] += summary_last[s][global_mtg_seqno[i] - 16]["active_rate_ytd__sum"]
                    else:
                        if summary.has_key(s) and summary[s].has_key(global_mtg_seqno[i] - 16):
                            meeting_id_last[i] = int(summary[s][global_mtg_seqno[i] - 16]["global_mtg_seqno__season_mtg_seqno__avg"])
                            num_cust_last[i] += summary[s][global_mtg_seqno[i] - 16]["cust_id__count"]
                            active_rate_sum_last[i] += summary[s][global_mtg_seqno[i] - 16]["active_rate_ytd__sum"]
        active_rate_current = [float(active_rate_sum[i]) / float(num_cust[i]) for i in range(len(active_rate_sum))]
        active_rate_last = [float(active_rate_sum_last[i]) / float(num_cust_last[i]) for i in range(len(active_rate_sum_last))]
        end = time.time()
        print "Task time: " + str(end - start) + " seconds..."
        return Response({
            "active_rate_last": active_rate_last,
            "active_rate": active_rate_current,
            "meeting_id_last": meeting_id_last,
            "meeting_id": meeting_id
        })
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def channel_shares(request):
    if "season" in request.GET:
        start = time.time()
        season = int(request.GET["season"])
        channel = get_channel_by_season(season)
        if "segment" in request.GET:
            segment = request.GET["segment"].split(",")
        else:
            segment = channel.keys()
        major_channel = channel[channel.keys()[0]].keys()
        std_turnover = [0.0 for i in range(len(major_channel))]
        exo_turnover = [0.0 for i in range(len(major_channel))]
        for i in range(len(major_channel)):
            for s in segment:
                if channel.has_key(s) and channel[s].has_key(major_channel[i]):
                    std_turnover[i] += channel[s][major_channel[i]]["standard_turnover"]
                    exo_turnover[i] += channel[s][major_channel[i]]["exotic_turnover"]
        std_ratio = [s / sum(std_turnover) for s in std_turnover]
        exo_ratio = [s / sum(exo_turnover) for s in exo_turnover]
        end = time.time()
        print "Task time: " + str(end - start) + " seconds..."
        return Response({
            "major_channel": major_channel,
            "standard_turnover_ytd": std_ratio,
            "exotic_turnover_ytd": exo_ratio
        })
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def wakeup_rate(request):
    if "season" in request.GET:
        start = time.time()
        season = int(request.GET["season"])
        num_cust = get_num_cust(season, )
        num_cust_last = get_num_cust(season - 1)
        summary = get_summary_by_season(season)
        summary_last = get_summary_by_season(season - 1)
        if "segment" in request.GET:
            segment = request.GET["segment"].split(",")
            total_num = 0
            total_num_last = 0
            for s in segment:
                total_num += (0 if not num_cust.has_key(s) else num_cust[s])
                total_num_last += (0 if not num_cust_last.has_key(s) else num_cust_last[s])
        else:
            segment = summary.keys()
            total_num = sum(num_cust.values())
            total_num_last = sum(num_cust_last.values())
        global_mtg_seqno = summary[summary.keys()[0]].keys()
        global_mtg_seqno.sort()
        global_mtg_seqno_last = summary_last[summary_last.keys()[0]].keys()
        global_mtg_seqno_last.sort()
        wakeup_num = [0 for i in range(len(global_mtg_seqno))]
        wakeup_num_last = [0 for i in range(len(global_mtg_seqno))]
        for i in range(len(global_mtg_seqno)):
            for s in segment:
                wakeup_num[i] += (0 if not summary.has_key(s) or not summary[s].has_key(global_mtg_seqno[i]) else summary[s][global_mtg_seqno[i]]["cust_id__count"])
                wakeup_num_last[i] += (0 if not summary_last.has_key(s) or not summary_last[s].has_key(global_mtg_seqno_last[i]) else summary_last[s][global_mtg_seqno_last[i]]["cust_id__count"])
        wakeup_rate = [float(num) / float(total_num) for num in wakeup_num]
        wakeup_rate_last = [float(num) / float(total_num_last) for num in wakeup_num_last]
        end = time.time()
        print "Task time: " + str(end - start) + " seconds..."
        return Response({
            "wakeup_rate_previous_season": wakeup_rate_last,
            "wakeup_rate_this_season": wakeup_rate
        })
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def growth_in_detail(request):
    if "season" in request.GET:
        start = time.time()
        season = int(request.GET["season"])
        summary = get_summary_by_season(season)
        summary_last = get_summary_by_season(season - 1)
        if "segment" in request.GET:
            segment = request.GET["segment"].split(",")
        else:
            segment = summary.keys()
        global_mtg_seqno = summary[summary.keys()[0]].keys()
        global_mtg_seqno.sort()
        global_mtg_seqno_last = summary_last[summary_last.keys()[0]].keys()
        global_mtg_seqno_last.sort()
        total_investment = 0.0
        total_investment_last = 0.0
        num_cust = 0
        num_cust_last = 0
        num_race = 0
        num_race_last = 0
        num_bet = 0
        num_bet_last = 0
        num_meeting = 0
        num_meeting_last = 0
        for i in range(len(global_mtg_seqno)):
            for s in segment:
                if summary.has_key(s) and summary[s].has_key(global_mtg_seqno[i]):
                    total_investment += summary[s][global_mtg_seqno[i]]["standard_turnover__sum"] + summary[s][global_mtg_seqno[i]]["exotic_turnover__sum"]
                    if summary[s][global_mtg_seqno[i]]["cust_id__count"] > num_cust:
                        num_cust = summary[s][global_mtg_seqno[i]]["cust_id__count"]
                    num_race += summary[s][global_mtg_seqno[i]]["race_num__sum"]
                    num_bet += summary[s][global_mtg_seqno[i]]["standard_betline__sum"] + summary[s][global_mtg_seqno[i]]["exotic_betline__sum"]
                    if summary[s][global_mtg_seqno[i]]["active_mtg_ytd__sum"] > num_meeting:
                        num_meeting = summary[s][global_mtg_seqno[i]]["active_mtg_ytd__sum"]
                if summary_last.has_key(s) and summary_last[s].has_key(global_mtg_seqno_last[i]):
                    total_investment_last += summary_last[s][global_mtg_seqno_last[i]]["standard_turnover__sum"] + summary_last[s][global_mtg_seqno_last[i]]["exotic_turnover__sum"]
                    if summary_last[s][global_mtg_seqno_last[i]]["cust_id__count"] > num_cust_last:
                        num_cust_last = summary_last[s][global_mtg_seqno_last[i]]["cust_id__count"]
                    num_race_last += summary_last[s][global_mtg_seqno_last[i]]["race_num__sum"]
                    num_bet_last += summary_last[s][global_mtg_seqno_last[i]]["standard_betline__sum"] + summary_last[s][global_mtg_seqno_last[i]]["exotic_betline__sum"]
                    if summary_last[s][global_mtg_seqno_last[i]]["active_mtg_ytd__sum"] > num_meeting_last:
                        num_meeting_last = summary_last[s][global_mtg_seqno_last[i]]["active_mtg_ytd__sum"]
        end = time.time()
        print "Task time: " + str(end - start) + " seconds..."
        return Response({
            "total_investment": [int(s * 100 / total_investment_last) for s in [total_investment_last, total_investment]],
            "number_of_customers": [int(float(s * 100) / float(num_cust_last)) for s in [num_cust_last, num_cust]],
            "investment_per_customer": [int(total_investment_last / num_cust_last), int(total_investment / num_cust)],
            "races_per_customer": [num_race_last / num_cust_last, num_race / num_cust],
            "investment_per_race": [int(total_investment_last / num_race_last), int(total_investment / num_race)],
            "bet_per_race": [float(num_bet_last) / float(num_race_last), float(num_bet) / float(num_race)],
            "investment_per_bet": [int(total_investment_last / num_bet_last), int(total_investment / num_bet)],
            "meetings_per_customer": [num_meeting_last / num_cust_last, num_meeting / num_cust]
        })
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def month_on_month_growth(request):
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
        std_value = [0 for i in range(len(global_mtg_seqno))]
        exo_value = [0 for i in range(len(global_mtg_seqno))]
        std_value_last = [0 for i in range(len(global_mtg_seqno))]
        exo_value_last = [0 for i in range(len(global_mtg_seqno))]
        meeting_id = [-1 for i in range(len(global_mtg_seqno))]
        meeting_id_last = [-1 for i in range(len(global_mtg_seqno))]
        std_growth = []
        exo_growth = []
        for i in range(len(global_mtg_seqno)):
            for s in segment:
                if summary.has_key(s) and summary[s].has_key(global_mtg_seqno[i]):
                    meeting_id[i] = int(summary[s][global_mtg_seqno[i]]["global_mtg_seqno__season_mtg_seqno__avg"])
                    std_value[i] += summary[s][global_mtg_seqno[i]]["standard_" + field + "__sum"]
                    exo_value[i] += summary[s][global_mtg_seqno[i]]["exotic_" + field + "__sum"]
                if i < 16:
                    if summary_last.has_key(s) and summary_last[s].has_key(global_mtg_seqno[i] - 16):
                        meeting_id_last[i] = int(summary_last[s][global_mtg_seqno[i] - 16]["global_mtg_seqno__season_mtg_seqno__avg"])
                        std_value_last[i] += summary_last[s][global_mtg_seqno[i] - 16]["standard_" + field + "__sum"]
                        exo_value_last[i] += summary_last[s][global_mtg_seqno[i] - 16]["exotic_" + field + "__sum"]
                else:
                    if summary.has_key(s) and summary[s].has_key(global_mtg_seqno[i] - 16):
                        meeting_id_last[i] = int(summary[s][global_mtg_seqno[i] - 16]["global_mtg_seqno__season_mtg_seqno__avg"])
                        std_value_last[i] += summary[s][global_mtg_seqno[i] - 16]["standard_" + field + "__sum"]
                        exo_value_last[i] += summary[s][global_mtg_seqno[i] - 16]["exotic_" + field + "__sum"]
            std_growth.append(float(std_value[i] - std_value_last[i]) / float(std_value_last[i]))
            exo_growth.append(float(exo_value[i] - exo_value_last[i]) / float(exo_value_last[i]))
        end = time.time()
        print "Task time: " + str(end - start) + " seconds..."
        return Response({
            "standard_" + field: {
                "standard_" + field + "_current": std_value,
                "standard_" + field + "_last": std_value_last,
                "meeting_id_current": meeting_id,
                "meeting_id_last": meeting_id_last,
                "std_growth": std_growth
            },
            "exotic_" + field: {
                "exotic_" + field + "_current": exo_value,
                "exotic_" + field + "_last": exo_value_last,
                "meeting_id_current": meeting_id,
                "meeting_id_last": meeting_id_last,
                "exo_growth": exo_growth
            }
        })
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def active_analysis(request):
    if "season" in request.GET and "type" in request.GET:
        start = time.time()
        season = int(request.GET["season"])
        cust_type = request.GET["type"]
        summary = get_summary_by_season(season)
        cust_analysis = get_cust_analysis_by_season(season)
        cust_analysis_last = get_cust_analysis_by_season(season - 1)
        if "segment" in request.GET:
            segment = request.GET["segment"].split(",")
        else:
            segment = summary.keys()
        global_mtg_seqno = summary[summary.keys()[0]].keys()
        global_mtg_seqno.sort()
        num_cust = [0 for i in range(len(global_mtg_seqno))]
        num_cust_last = [0 for i in range(len(global_mtg_seqno))]
        for i in range(len(global_mtg_seqno)):
            for s in segment:
                if cust_analysis[cust_type].has_key(s):
                    num_cust[i] += cust_analysis[cust_type][s][i]
                if cust_analysis_last[cust_type].has_key(s):
                    num_cust_last[i] += cust_analysis_last[cust_type][s][i]
        end = time.time()
        print "Task time: " + str(end - start) + " seconds..."
        return Response({
            "num_cust_previous_season": num_cust_last,
            "num_cust_this_season": num_cust
        })
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# Below is new APIs
def get_new_cust_summary_by_season(season):
    global NEW_CUST_SUMMARY
    if season not in NEW_CUST_SUMMARY:
        NEW_CUST_SUMMARY[season] = create_new_cust_summary_dict(season)
    return NEW_CUST_SUMMARY[season]


def create_new_cust_summary_dict(season):
    print(colorize("Creating new customer summary cache for season " + str(season) + "...", fg="green"))
    summary_dict = dict()
    start = time.time()
    stat_result = Summary.objects.filter(global_mtg_seqno__season=season, global_mtg_seqno__mtg_status="N", cust_id__is_new_cust=1).values("global_mtg_seqno", "cust_id__segment_code").annotate(Avg("global_mtg_seqno__season_mtg_seqno"), Count("cust_id"), Sum("standard_turnover"), Sum("exotic_turnover"), Sum("standard_betline"), Sum("exotic_betline"), Sum("race_num"), Sum("active_rate_ytd"), Sum("active_mtg_ytd"), Sum("standard_turnover_ytd"), Sum("exotic_turnover_ytd"), Sum("standard_betline_ytd"), Sum("exotic_betline_ytd")).order_by("global_mtg_seqno")
    for value_list in stat_result:
        if value_list["cust_id__segment_code"] is None:
            value_list["cust_id__segment_code"] = "other"
        if not summary_dict.has_key(value_list["cust_id__segment_code"]):
            summary_dict[value_list["cust_id__segment_code"]] = dict()
        summary_dict[value_list["cust_id__segment_code"]][value_list["global_mtg_seqno"]] = value_list
    end = time.time()
    print(colorize("Creating summary cache takes " + str(end - start) + " seconds.", fg="green"))
    return summary_dict


def get_bet_type_by_season(season):
    global BET_TYPE
    if season not in BET_TYPE:
        BET_TYPE[season] = create_bet_type_dict(season)
    return BET_TYPE[season]


def create_bet_type_dict(season):
    print colorize("Creating bet type cache for season " + str(season) + "...", fg="green")
    bettype_dict = dict()
    start = time.time()
    bettype_info = Summary.objects.filter(global_mtg_seqno__season=season, global_mtg_seqno__mtg_status="N").values("turnover_bettype_details", "cust_id__segment_code")
    for info in bettype_info:
        if info["cust_id__segment_code"] is None:
            info["cust_id__segment_code"] = "other"
        if not bettype_dict.has_key(info["cust_id__segment_code"]):
            bettype_dict[info["cust_id__segment_code"]] = dict()
        for bet in info["turnover_bettype_details"]:
            if not bettype_dict[info["cust_id__segment_code"]].has_key(bet):
                bettype_dict[info["cust_id__segment_code"]][bet] = dict()
                bettype_dict[info["cust_id__segment_code"]][bet]["turnover"] = 0.0
            bettype_dict[info["cust_id__segment_code"]][bet]["turnover"] += info["turnover_bettype_details"][bet][0]
    end = time.time()
    print "Creating bet type cache takes " + str(end - start) + " seconds..."
    return bettype_dict


@api_view(['GET'])
def active_rate_new_cust(request):
    if "season" in request.GET and "type" in request.GET:
        start = time.time()
        season = int(request.GET["season"])
        summary = get_new_cust_summary_by_season(season)
        summary_last = get_new_cust_summary_by_season(season - 1)
        if "segment" in request.GET:
            segment = request.GET["segment"].split(",")
        else:
            segment = summary.keys()
        global_mtg_seqno = summary[summary.keys()[0]].keys()
        global_mtg_seqno.sort()
        global_mtg_seqno_last = summary_last[summary_last.keys()[0]].keys()
        global_mtg_seqno_last.sort()
        num_cust = [0 for i in range(len(global_mtg_seqno))]
        num_cust_last = [0 for i in range(len(global_mtg_seqno))]
        active_rate_sum = [0 for i in range(len(global_mtg_seqno))]
        active_rate_sum_last = [0 for i in range(len(global_mtg_seqno))]
        meeting_id = [-1 for i in range(len(global_mtg_seqno))]
        meeting_id_last = [-1 for i in range(len(global_mtg_seqno))]
        for i in range(len(global_mtg_seqno)):
            for s in segment:
                if summary.has_key(s) and summary[s].has_key(global_mtg_seqno[i]):
                    meeting_id[i] = int(summary[s][global_mtg_seqno[i]]["global_mtg_seqno__season_mtg_seqno__avg"])
                    num_cust[i] += summary[s][global_mtg_seqno[i]]["cust_id__count"]
                    active_rate_sum[i] += summary[s][global_mtg_seqno[i]]["active_rate_ytd__sum"]
                if request.GET["type"] == "year":
                    if summary_last.has_key(s) and summary_last[s].has_key(global_mtg_seqno_last[i]):
                        meeting_id_last[i] = int(summary_last[s][global_mtg_seqno_last[i]]["global_mtg_seqno__season_mtg_seqno__avg"])
                        num_cust_last[i] += summary_last[s][global_mtg_seqno_last[i]]["cust_id__count"]
                        active_rate_sum_last[i] += summary_last[s][global_mtg_seqno_last[i]]["active_rate_ytd__sum"]
                elif request.GET["type"] == "month":
                    if i < 16:
                        if summary_last.has_key(s) and summary_last[s].has_key(global_mtg_seqno[i] - 16):
                            meeting_id_last[i] = int(summary_last[s][global_mtg_seqno[i] - 16]["global_mtg_seqno__season_mtg_seqno__avg"])
                            num_cust_last[i] += summary_last[s][global_mtg_seqno[i] - 16]["cust_id__count"]
                            active_rate_sum_last[i] += summary_last[s][global_mtg_seqno[i] - 16]["active_rate_ytd__sum"]
                    else:
                        if summary.has_key(s) and summary[s].has_key(global_mtg_seqno[i] - 16):
                            meeting_id_last[i] = int(summary[s][global_mtg_seqno[i] - 16]["global_mtg_seqno__season_mtg_seqno__avg"])
                            num_cust_last[i] += summary[s][global_mtg_seqno[i] - 16]["cust_id__count"]
                            active_rate_sum_last[i] += summary[s][global_mtg_seqno[i] - 16]["active_rate_ytd__sum"]
        active_rate_current = [float(active_rate_sum[i]) / float(num_cust[i]) for i in range(len(active_rate_sum))]
        active_rate_last = [float(active_rate_sum_last[i]) / float(num_cust_last[i]) for i in range(len(active_rate_sum_last))]
        active_growth = [(active_rate_current[i] - active_rate_last[i]) / active_rate_last[i] for i in range(len(active_rate_current))]
        end = time.time()
        print "Task time: " + str(end - start) + " seconds..."
        return Response({
            "active_rate_last": active_rate_last,
            "active_rate": active_rate_current,
            "num_cust_last": num_cust_last,
            "num_cust": num_cust,
            "meeting_id_last": meeting_id_last,
            "meeting_id": meeting_id,
            "cumulative_growth_rate_of_active_rate": active_growth
        })
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def active_rate_latest(request):
    if "season" in request.GET:
        start = time.time()
        season = int(request.GET["season"])
        transact = Summary.objects.filter(global_mtg_seqno__season=season, global_mtg_seqno__mtg_status="N")
        if "segment" in request.GET:
            transact = transact.filter(cust_id__segment_code__in=request.GET["segment"].split(","))
        latest_seqno = transact.aggregate(Max("global_mtg_seqno"))['global_mtg_seqno__max']
        summary = transact.filter(global_mtg_seqno=latest_seqno).values_list("active_rate_ytd", flat=True)
        if request.GET["categorical"] == "true":
            hist = numpy.divide(Counter(summary).values(), [float(len(summary))])
            bin_edges = Counter(summary).keys()
        else:
            bins = 10
            if "bins" in request.GET:
                bins = numpy.fromstring(request.GET["bins"], dtype=float, sep=',')
            hist, bin_edges = numpy.histogram([float(s) for s in summary], bins)
            hist = numpy.divide(hist, [float(len(summary))])
            bin_edges = bin_edges.tolist()
        end = time.time()
        print "Task time: " + str(end - start) + " seconds..."
        return Response({
            "hist": hist,
            "bin_edges": bin_edges
        })
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def bet_type(request):
    if "season" in request.GET:
        start = time.time()
        season = int(request.GET["season"])
        bettype = get_bet_type_by_season(season)
        if "segment" in request.GET:
            segment = request.GET["segment"].split(",")
        else:
            segment = bettype.keys()
        major_type = bettype[bettype.keys()[0]].keys()
        turnover = [0.0 for i in range(len(major_type))]
        for i in range(len(major_type)):
            for s in segment:
                if bettype.has_key(s) and bettype[s].has_key(major_type[i]):
                    turnover[i] += bettype[s][major_type[i]]["turnover"]
        ratio = [s / sum(turnover) for s in turnover]
        end = time.time()
        print "Task time: " + str(end - start) + " seconds..."
        return Response({
            "major_type": major_type,
            "turnover_ytd": ratio,
        })
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
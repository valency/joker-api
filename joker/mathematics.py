from statsmodels.tools import categorical

from models import *
from common import *
from kmeans import *


class Mathematics:
    def __init__(self):
        pass

    @staticmethod
    def joker_kmeans(header, weight, pred_label, n_clusters, n_records, model):
        if model == 1:
            cust_obj = Customer1.objects
        elif model == 2:
            cust_obj = Customer2.objects
        else:
            return None
        cust_set = cust_obj.order_by("-" + pred_label)[:n_records]
        cust_matrix = numpy.array([])
        id_list = numpy.array([cust.id for cust in cust_set])
        for h in header:
            # Choose header
            if h == "segment":
                cust_column = numpy.array([cust.segment for cust in cust_set])
                cust_column = categorical(cust_column, drop=True).argmax(1)
            elif h == "age":
                cust_column = numpy.array([cust.age for cust in cust_set])
                cust_column = categorical(cust_column, drop=True).argmax(1)
            elif h == "gender":
                cust_column = numpy.array([cust.gender for cust in cust_set])
                cust_column = categorical(cust_column, drop=True).argmax(1)
            elif h == "yrs_w_club":
                cust_column = numpy.array([cust.yrs_w_club for cust in cust_set])
            elif h == "is_member":
                cust_column = numpy.array([cust.is_member for cust in cust_set])
                cust_column = categorical(cust_column, drop=True).argmax(1)
            elif h == "is_hrs_owner":
                cust_column = numpy.array([cust.is_hrs_owner for cust in cust_set])
                cust_column = categorical(cust_column, drop=True).argmax(1)
            elif h == "major_channel":
                cust_column = numpy.array([cust.major_channel for cust in cust_set])
                cust_column = categorical(cust_column, drop=True).argmax(1)
            elif h == "mtg_num":
                cust_column = numpy.array([cust.mtg_num for cust in cust_set])
            elif h == "inv":
                cust_column = numpy.array([cust.inv for cust in cust_set])
            elif h == "div":
                cust_column = numpy.array([cust.div for cust in cust_set])
            elif h == "rr":
                cust_column = numpy.array([cust.rr for cust in cust_set])
            elif h == "end_bal":
                cust_column = numpy.array([cust.end_bal for cust in cust_set])
            elif h == "recharge_times":
                cust_column = numpy.array([cust.recharge_times for cust in cust_set])
            elif h == "recharge_amount":
                cust_column = numpy.array([cust.recharge_amount for cust in cust_set])
            elif h == "withdraw_times":
                cust_column = numpy.array([cust.withdraw_times for cust in cust_set])
            elif h == "withdraw_amount":
                cust_column = numpy.array([cust.withdraw_amount for cust in cust_set])
            else:
                continue
            # Stack to matrix
            if cust_matrix.size == 0:
                cust_matrix = cust_column
            else:
                cust_matrix = numpy.column_stack((cust_matrix, cust_column))
        # Normalize
        cust_matrix = Common.scale_linear_by_column(cust_matrix)
        # Weight
        cust_matrix = numpy.nan_to_num(numpy.multiply(cust_matrix, numpy.array([numpy.array(weight)] * cust_set.count())))
        # Clustering
        kmeans_centres, kmeans_xtoc, kmeans_dist = kmeans(cust_matrix, randomsample(cust_matrix, n_clusters))
        # k_means = KMeans(init="k-means++", n_clusters=n_clusters)
        # k_means.fit(cust_matrix)
        result = []
        for i in range(0, len(id_list)):
            entity = {
                "id": id_list[i],
                "cluster": kmeans_xtoc[i]
            }
            cust = cust_obj.get(id=id_list[i])
            for h in header:
                entity[h] = cust.__dict__[h]
            result.append(entity)
        return result

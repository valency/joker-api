from statsmodels.tools import categorical
from sklearn.cluster import KMeans

from models import *
from common import *


class Mathematics:
    def __init__(self):
        pass

    @staticmethod
    def kmeans(header, weight, pred_label, n_clusters):
        cust_set = Customer.objects.filter(prediction__label=pred_label)
        cust_matrix = numpy.array([])
        id_list = numpy.array([cust.id for cust in cust_set])
        for h in header:
            # Choose header
            if h == "cust_code":
                cust_column = numpy.array([cust.cust_code for cust in cust_set])
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
        k_means = KMeans(init="k-means++", n_clusters=n_clusters)
        k_means.fit(cust_matrix)
        result = []
        for i in range(0, len(id_list)):
            entity = {
                "id": id_list[i],
                "cluster": k_means.labels_[i]
            }
            for h in header:
                entity[h] = cust_set.get(id=id_list[i]).__dict__[h]
            result.append(entity)
        return result

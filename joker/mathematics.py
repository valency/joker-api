from statsmodels.tools import categorical

from models import *
from common import *
from kmeans import *


class Mathematics:
    def __init__(self):
        pass

    @staticmethod
    def joker_kmeans(header, pred_label, n_clusters, n_records, model):
        CATEGORICAL_COLUMNS = ["id", "segment", "age", "gender", "is_member", "is_hrs_owner", "major_channel"]
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
            cust_column = numpy.array([getattr(cust, h) for cust in cust_set])
            if h in CATEGORICAL_COLUMNS: cust_column = categorical(cust_column, drop=True)
            # Stack to matrix
            if cust_matrix.size == 0:
                cust_matrix = cust_column
            else:
                cust_matrix = numpy.column_stack((cust_matrix, cust_column))
        # Normalize
        cust_matrix = Common.scale_linear_by_column(cust_matrix)
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
            cust = cust_obj.get(id=id_list[i])
            for h in header:
                entity[h] = cust.__dict__[h]
            result.append(entity)
        return result

import numpy
from django.contrib.auth import authenticate


class Common:
    DATA_PATH = "/var/www/html/joker/data/"

    def __init__(self):
        pass

    @staticmethod
    def scale_linear_by_column(rawpoints, high=1.0, low=0.0):
        mins = numpy.min(rawpoints, axis=0)
        maxs = numpy.max(rawpoints, axis=0)
        rng = maxs - mins
        return numpy.nan_to_num(high - (((high - low) * (maxs - rawpoints)) / rng))

    @staticmethod
    def user_auth(username, password):
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            return user
        else:
            return None

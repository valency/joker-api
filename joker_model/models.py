from django.db import models


class ModelResultMaster(models.Model):
    update_id = models.BigIntegerField()
    update_status = models.IntegerField(null=True)
    update_nature = models.TextField(null=True)
    update_start_time = models.DateTimeField(null=True)
    update_end_time = models.DateTimeField(null=True)
    raw_data_time = models.DateTimeField(null=True)
    model_type = models.IntegerField(null=True)
    update_server = models.TextField(null=True)
    update_port = models.IntegerField(null=True)
    csv_name = models.TextField(null=True)
    predict_from = models.DateTimeField(null=True)
    predict_to = models.DateTimeField(null=True)
    lead_days = models.IntegerField(null=True)
    input_profile = models.TextField(null=True)
    is_imported = models.IntegerField(null=True)


class ModelTypeMaster(models.Model):
    model_type_no = models.IntegerField(null=True)
    model_type_nature = models.TextField(null=True)


class ReasonCodeMaster(models.Model):
    reason_code_id = models.IntegerField(null=True)
    description = models.TextField(null=True)

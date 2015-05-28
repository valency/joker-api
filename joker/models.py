import csv

from django.db import models


class Prediction(models.Model):
    label_prob = models.CharField(max_length=255)
    reason_code_1 = models.CharField(max_length=255, null=True)
    reason_code_2 = models.CharField(max_length=255, null=True)
    reason_code_3 = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.cust.id


class Customer(models.Model):
    id = models.IntegerField(primary_key=True)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=1, choices=(
        ('M', 'Male'),
        ('F', 'Female')
    ), null=True)
    yrs_w_club = models.IntegerField(null=True)
    is_member = models.BooleanField(null=True)
    is_hrs_owner = models.BooleanField(null=True)
    major_channel = models.CharField(max_length=8, choices=(
        ('AOSBS', 'AOSBS'),
        ('API', 'API'),
        ('CIT', 'CIT'),
        ('ESC', 'ESC'),
        ('EWIN', 'EWIN'),
        ('IBUT', 'IBUT'),
        ('IOSBS', 'IOSBS'),
        ('MANGO', 'MANGO'),
        ('MBSN', 'MBSN'),
        ('MISSING', 'MISSING'),
        ('MULTI', 'MULTI'),
        ('TEL', 'TEL')
    ), null=True)
    mtg_num = models.IntegerField(null=True)
    inv = models.FloatField(null=True)
    inv_seg_1 = models.FloatField(null=True)
    inv_seg_2 = models.FloatField(null=True)
    inv_seg_3 = models.FloatField(null=True)
    div = models.FloatField(null=True)
    rr = models.FloatField(null=True)
    end_bal = models.FloatField(null=True)
    recharge_times = models.IntegerField(null=True)
    recharge_amount = models.FloatField(null=True)
    withdraw_times = models.IntegerField(null=True)
    withdraw_amount = models.FloatField(null=True)
    prediction = models.ManyToManyField(Prediction, null=True)

    def __str__(self):
        return self.id

    def from_csv(self, src):
        try:
            f = open(src, "rb")
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    self.id = int(row["CUST_ID"])
                    if "AGE" in row.keys(): self.age = int(row["AGE"])
                    if "GENDER" in row.keys(): self.gender = row["GENDER"]
                    if "YRS_W_CLUB" in row.keys(): self.yrs_w_club = int(row["YRS_W_CLUB"])
                    if "IS_MEMBER" in row.keys(): self.is_member = int(row["IS_MEMBER"]) > 0
                    if "IS_HRS_OWNER" in row.keys(): self.is_hrs_owner = int(row["IS_HRS_OWNER"]) > 0
                    if "MAJOR_CHANNEL" in row.keys(): self.major_channel = row["MAJOR_CHANNEL"]
                    if "MTG_NUM" in row.keys(): self.mtg_num = int(row["MTG_NUM"])
                    if "INV" in row.keys(): self.inv = float(row["INV"])
                    if "INV_SEG1" in row.keys(): self.inv_seg_1 = float(row["INV_SEG1"])
                    if "INV_SEG2" in row.keys(): self.inv_seg_2 = float(row["INV_SEG2"])
                    if "INV_SEG3" in row.keys(): self.inv_seg_3 = float(row["INV_SEG3"])
                    if "DIV" in row.keys(): self.div = float(row["DIV"])
                    if "RR" in row.keys(): self.rr = float(row["RR"])
                    if "END_BAL" in row.keys(): self.end_bal = float(row["END_BAL"])
                    if "RECHARGE_TIMES" in row.keys(): self.recharge_times = int(row["RECHARGE_TIMES"])
                    if "RECHARGE_AMOUNT" in row.keys(): self.recharge_amount = float(row["RECHARGE_AMOUNT"])
                    if "WITHDRAW_TIMES" in row.keys(): self.withdraw_times = int(row["WITHDRAW_TIMES"])
                    if "WITHDRAW_AMOUNT" in row.keys(): self.withdraw_amount = float(row["WITHDRAW_AMOUNT"])
                    self.save()
                except TypeError:
                    continue
            f.close()
        except IOError as exp:
            return {"status": 500, "content": exp.strerror}
        return {"status": 200, "content": "ok"}

    def assign_pred(self, label_prob, reason_code_1, reason_code_2, reason_code_3):
        try:
            pred = Prediction(label_prob=label_prob, reason_code_1=reason_code_1, reason_code_2=reason_code_2, reason_code_3=reason_code_3)
            pred.save()
            self.prediction = pred
            self.save()
        except TypeError as exp:
            return {"status": 500, "content": exp.message}
        return {"status": 200, "content": "ok"}

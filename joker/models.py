from django.db import models


class Prediction(models.Model):
    id = models.ForeignKey(Customer, primary_key=True)
    label_prob = models.CharField(max_length=255)
    reason_code_1 = models.CharField(max_length=255, null=True)
    reason_code_2 = models.CharField(max_length=255, null=True)
    reason_code_3 = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.id


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

    def __str__(self):
        return self.id

        # def from_csv(self, src, header):
        #     trace = Trace(id=self.id)
        #     trace.save()
        #     try:
        #         f = open(src, "rb")
        #         reader = csv.reader(f)
        #         for row in reader:
        #             try:
        #                 sampleid = row[header.index("id")]
        #                 p = Point(lat=float(row[header.index("lat")]), lng=float(row[header.index("lng")]))
        #                 p.save()
        #                 t = datetime.datetime.strptime(row[header.index("t")], "%Y-%m-%d %H:%M:%S")
        #                 speed = int(row[header.index("speed")])
        #                 angle = int(row[header.index("angle")])
        #                 occupy = int(row[header.index("occupy")])
        #                 sample = Sample(id=sampleid, p=p, t=t, speed=speed, angle=angle, occupy=occupy, src=0)
        #                 sample.save()
        #                 trace.p.add(sample)
        #             except TypeError:
        #                 continue
        #         f.close()
        #     except IOError:
        #         return False
        #     trace.save()
        #     self.trace = trace
        #     self.path = None
        #     self.save()
        #     return True

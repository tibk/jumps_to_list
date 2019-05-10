from django.db import models


class Jumper(models.Model):
    name = models.CharField(max_length=250)


class Spot(models.Model):
    name = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    height = models.CharField(max_length=250)


class Suit(models.Model):
    name = models.CharField(max_length=250)
    brand =models.CharField(max_length=250)
    kind = models.CharField(max_length=250)


class JumpeKind(models.Model):
    kind = models.CharField(max_length=250)


class Jump(models.Model):
    __tablename__ = 'jump'
    date = models.DateTimeField('jump date')
    jumper_id = models.ForeignKey(Jumper, on_delete=models.CASCADE)
    spot_id = models.ForeignKey(Spot, on_delete=models.CASCADE)
    suit_id = models.ForeignKey(Suit, on_delete=models.CASCADE)
    jump_kind_id = models.ForeignKey(JumpeKind, on_delete=models.CASCADE)
    comments = models.CharField(max_length=500)

from django.db import models


class Jumper(models.Model):
    name = models.CharField(max_length=250)


class Spot(models.Model):
    name = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    height = models.CharField(max_length=250)


class Suit(models.Model):
    name = models.CharField(max_length=250)
    brand = models.CharField(max_length=250)
    kind = models.CharField(max_length=250)


class JumpKind(models.Model):
    kind = models.CharField(max_length=250)


class Jump(models.Model):
    __tablename__ = 'jump'
    date = models.DateField('jump date')
    number = models.IntegerField(default=0)
    jumper_id = models.ForeignKey(Jumper, on_delete=models.CASCADE, db_column='jumper_id')
    spot_id = models.ForeignKey(Spot, on_delete=models.CASCADE, db_column='spot_id')
    suit_id = models.ForeignKey(Suit, on_delete=models.CASCADE, db_column='suit_id')
    jump_kind_id = models.ForeignKey(JumpKind, on_delete=models.CASCADE, db_column='jump_kind_id')
    comments = models.CharField(max_length=500)
    # UniqueConstraint(fields=['jumper_id', 'number'], name='jump_number_unique_per_jumper')

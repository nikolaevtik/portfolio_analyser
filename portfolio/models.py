from django.db import models

class Portfolio(models.Model):
    name = models.CharField(max_length=100)
    ticker = models.CharField(max_length=20)
    quantity = models.IntegerField()

class Ticker(models.Model):
    search_by_ticker = models.CharField(max_length=5)
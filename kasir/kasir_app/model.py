from django.db import models

class Barang(models.Model):
    nama = models.CharField(max_length=100)
    harga = models.IntegerField()
    jumlah = models.IntegerField()
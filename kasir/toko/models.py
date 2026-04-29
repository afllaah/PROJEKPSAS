from django.db import models

class Barang(models.Model):
    nama = models.CharField(max_length=100)
    harga = models.IntegerField()
    barcode = models.CharField(max_length=100)

    def __str__(self):
        return self.nama
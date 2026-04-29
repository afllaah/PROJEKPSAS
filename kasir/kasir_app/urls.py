from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tambah/', views.tambah_barang, name='tambah'),
    path('lihat/', views.lihat_barang, name='lihat'),  # ← INI YANG PENTING
    path('transaksi/', views.transaksi, name='transaksi'),
]
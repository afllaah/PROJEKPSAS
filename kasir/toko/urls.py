from django.urls import path
from . import views
from .views import export_pdf

urlpatterns = [
    

    path('', views.dashboard, name='dashboard'),
    path('kasir/', views.kasir, name='kasir'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('lihat/', views.lihat_barang, name='lihat'),

    path('tambah/<int:id>/', views.tambah_ke_keranjang, name='tambah_ke_keranjang'),
    path('checkout/', views.checkout, name='checkout'),
    path('struk/<int:id>/', views.struk, name='struk'),
    path('scan/<str:code>/', views.scan_barcode, name='scan_barcode'),

    path('export-pdf/', views.export_pdf, name='export_pdf'),
    path('selesai/', views.selesai_transaksi, name='selesai_transaksi'),
]
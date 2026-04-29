from django.shortcuts import render, redirect
from .model import Barang

def home(request):
    return render(request, 'home.html')

def tambah_barang(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        harga = request.POST.get('harga')
        jumlah = request.POST.get('jumlah')

        Barang.objects.create(
            nama=nama,
            harga=harga,
            jumlah=jumlah
        )

        return redirect('home')

    return render(request, 'tambah.html')

def transaksi(request):
    return render(request, 'transaksi.html')
from .model import Barang

def lihat_barang(request):
    data = Barang.objects.all()
    return render(request, 'lihat.html', {'data': data})
def lihat_barang(request):
    return render(request, 'lihat.html')
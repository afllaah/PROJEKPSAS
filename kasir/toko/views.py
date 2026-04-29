from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Sum
from reportlab.pdfgen import canvas

from .templates.toko.models import Barang, Transaksi, DetailTransaksi


# ================= LOGIN =================
from django.contrib.auth import authenticate, login, logout

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Username / Password salah'})

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('login')


# ================= DASHBOARD =================
@login_required
def dashboard(request):
    total_barang = Barang.objects.count()
    total_transaksi = Transaksi.objects.count()
    total_pendapatan = Transaksi.objects.aggregate(Sum('total'))['total__sum'] or 0

    return render(request, 'dashboard.html', {
        'total_barang': total_barang,
        'total_transaksi': total_transaksi,
        'total_pendapatan': total_pendapatan
    })


# ================= HALAMAN KASIR =================
@login_required
def kasir(request):
    barang = Barang.objects.all()
    cart = request.session.get('cart', {})

    return render(request, 'kasir.html', {
        'barang': barang,
        'cart': cart
    })


# ================= TAMBAH KE KERANJANG =================
def tambah_ke_keranjang(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        cart[str(id)] += 1
    else:
        cart[str(id)] = 1

    request.session['cart'] = cart

    return redirect('kasir')


# ================= CHECKOUT (INI YANG DIPAKAI TOMBOL BAYAR) =================
def checkout(request):
    cart = request.session.get('cart', {})
    total = 0

    if not cart:
        return redirect('kasir')

    trx = Transaksi.objects.create(total=0)

    for id, qty in cart.items():
        barang = Barang.objects.get(id=id)
        subtotal = barang.harga * qty
        total += subtotal

        DetailTransaksi.objects.create(
            transaksi=trx,
            barang=barang,
            qty=qty,
            subtotal=subtotal
        )

        barang.stok -= qty
        barang.save()

    trx.total = total
    trx.save()

    # 🔥 kosongkan keranjang
    request.session['cart'] = {}

    return redirect('struk', id=trx.id)


# ================= STRUK =================
def struk(request, id):
    trx = Transaksi.objects.get(id=id)
    detail = DetailTransaksi.objects.filter(transaksi=trx)

    return render(request, 'struk.html', {
        'trx': trx,
        'detail': detail
    })


# ================= EXPORT PDF =================
def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    p = canvas.Canvas(response)

    p.drawString(100, 800, "Laporan Penjualan")

    y = 750
    data = Transaksi.objects.all()

    for d in data:
        p.drawString(100, y, f"ID: {d.id} - Total: {d.total}")
        y -= 20

    p.save()
    return response

def scan_barcode(request, code):
    from .models import Barang

    try:
        barang = Barang.objects.get(barcode=code)
        return tambah_ke_keranjang(request, barang.id)
    except Barang.DoesNotExist:
        return HttpResponse("Barcode tidak ditemukan")
    
from django.shortcuts import render

def selesai_transaksi(request):
    request.session['keranjang'] = {}
    return render(request, 'toko/selesai.html')

from .models import Barang
from django.shortcuts import render

def lihat_barang(request):
    data = Barang.objects.all()
    return render(request, 'lihat.html', {'data': data})
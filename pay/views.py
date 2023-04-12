from django.shortcuts import render, HttpResponse
import razorpay

from shop.settings import KEY,SECRET
from basket.basket import Basket


def index(request):
    basket = Basket(request)
    total = str(basket.get_total_price())
    total = total.replace('.', '')
    total = int(total)
    order_currency = "INR"
    order_receipt = "order_rcptid_11"

    client = razorpay.Client(auth=(KEY, SECRET))

    payment_order=client.order.create(dict(amount=total, currency = order_currency, receipt=order_receipt,))
    payment_order_id = payment_order['id']

    context = {
        'amount' : basket.get_total_price(),
        'payment':payment_order,
        'api_key':KEY,
        'order_id':payment_order_id
    }
    return render(request,'pay/home.html', context)

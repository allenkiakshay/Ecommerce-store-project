from django.shortcuts import render
from django.conf import settings

from account.models import UserBase
from basket.basket import Basket
import razorpay


def BasketView(request):
    basket = Basket(request)
    total = str(basket.get_total_price())
    total = total.replace('.', '')
    total = int(total)

    client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
    payment = client.order.create({'amount' : total, 'currency' : 'INR', 'payment_capture': 1})

    context = {
        'cart' : total,
        'payment':payment,
        "amount": basket.get_total_price(),
        'email':UserBase.email,
        'phone_number':UserBase.phone_number,
        'name':UserBase.user_name,
    }
    return render(request, 'payments/home.html', context)

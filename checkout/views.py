from .models import Orders,OrderItem
from django.shortcuts import render, HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt

import razorpay

from shop.settings import KEY,SECRET
from basket.basket import Basket


def checkout(request):
    basket = Basket(request)
    amount = basket.get_total_price()
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '') + " " + request.POST.get('address1', '')
        country = request.POST.get('country', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        order = Orders(items_json=items_json, name=name, email=email, address1=address, country=country,
                       state=state, zip_code=zip_code, phone=phone, is_paid=True)
        order.save()
        order_id = order.order_id

        for item in basket:
            OrderItem.objects.create(order_id=order_id, product=item['product'],
                                     price = item['price'], quantity=item['qty'])

            '''total = str(basket.get_total_price())
            total = total.replace('.', '')
            total = int(total)
            order_currency = "INR"
            order_receipt = "order_rcptid_11"

            client = razorpay.Client(auth=(KEY, SECRET))

            payment_order = client.order.create(dict(amount=total, currency=order_currency, receipt=order_receipt, ))
            payment_order_id = payment_order['id']

            # callback_url = "127.0.0.1:800/checkout/success/"

            context = {
                'amount': basket.get_total_price(),
                'payment': payment_order,
                'api_key': KEY,
                'order_id': payment_order_id,
                # 'callback_url': callback_url
            }
            return render(request, 'pay/home.html')'''
        return redirect('clear/')
    else:
        orders = Orders()
    return render(request, 'checkout/home.html', {"orders": orders, "amount":amount})

    # return render(request,'checkout/home.html')
    # return render(request, 'checkout/home.html')


'''@csrf_exempt
def success(request):
    if request.method == "POST":
        order_id = request.POST.get('request.razorpay_order_id')
        payment_id = request.POST.get('razorpay_payment_id')
        sign = request.POST.get('razorpay_signature')

        params_dict = {
            'razor_pay_order_id' : order_id,
            'razor_pay_payment_id':payment_id,
            'razor_pay_payment_signature':sign
        }
        cart = Orders.objects.filter(order_id=order_id)
        cart.razor_pay_order_id = order_id
        cart.razor_pay_payment_id = payment_id
        cart.razor_pay_payment_signature = sign
        cart.update()
    return HttpResponse("payment success")'''


def clear(data):
    basket = Basket(data)
    basket.clear()
    return render(data, 'pay/success.html')
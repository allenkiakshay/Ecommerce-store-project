from django.conf import settings
from store.models import Products
from decimal import Decimal


class Basket():
    """
    A base basket class, providing some default behaviours that can
    be inherited or overrided, as necessary
    """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket

    def add(self, product, qty):

        product_id = str(product.id)

        if product_id not in self.basket:
            self.basket[product_id] = {'price': str(product.price), 'qty': int(qty)}
            self.save()

    def __iter__(self):
        """
        collect the product_id in the session data to query the database
        and return products
        """

        product_ids = self.basket.keys()
        products = Products.products.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']

            yield item

    def __len__(self):
        """
        Get the basket data and count the qty of items
        """
        return sum(item['qty'] for item in self.basket.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty']  for item in self.basket.values())

    def delete(self, product):
        """
        Delete item from session data
        :param product:
        :return:
        """
        product_id = str(product)

        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def update(self, product, qty):
        """
        update session data

        :param product:
        :param qty:
        :return:
        """
        product_id = str(product)

        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty

        self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        # Remove basket from session
        del self.session['skey']
        self.save()

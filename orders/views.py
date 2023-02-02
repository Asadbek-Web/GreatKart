from django.shortcuts import redirect, render
from carts.models import CartItem
from orders.models import Order, OrderProduct, Payment
from store.models import Product
from .forms import OrderForm
from django.contrib import messages

# datetime classes
from time import strftime
import datetime
from django.http import HttpResponse, JsonResponse
# import json


#send mail
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


def payments(request):
    # body = json.loads(request.body)
    # print(body)


    # Move the cart items to Order Product table 
    # cart_items = CartItem.objects.filter(user=request.user)

    # for item in cart_items:
    #     order_product = OrderProduct()
    #     # order_product.order_id = order
    #     # order_product.payment = payment
    #     order_product.user_id = request.user.id
    #     order_product.product_id = item.product.id
    #     order_product.quantity = item.quantity
    #     order_product.product_price = item.product.price
    #     order_product.ordered = True
    #     # order_product.save()

    #     cart_item = CartItem.objects.get(id=item.id)
    #     product_variation = cart_item.variations.all()
    #     order_product = OrderProduct.objects.get(id=order_product.id)
    #     order_product.variations.set(product_variation)
    #     order_product.save()


    #     # Reduce the quantity of the sold products 
    #     product = Product.objects.get(id=item.product.id)
    #     product.stock -= item.quantity   
    #     product.save() 

    # Clear cart
    CartItem.objects.filter(user=request.user).delete()


    # Send order received email to customer
    mail_subject = 'Thank you for your order!'
    message = render_to_string('orders/order_recieved_email.html', {
        'user': request.user,
        'order': request.order
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    # Send order number nad transaction id back to sendData method via JsonResponse
    # data = {
    #     'order_number': order.order_number,
    #     'trans_ID': payment.payment_id
    # }
    

    # return JsonResponse(data)

    return render(request, 'orders/payments.html')






def place_order(request, total=0, quantity=0):
    current_user = request.user

    # if the cart count is less then or equal to0, then redirect to the shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        messages.error(request, 'You have no products in your cart!')

        return redirect('store')    


    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax


    # if request.method == "POST":
    #     form = OrderForm(request.POST)
    #     if form.is_valid():
    #         # Store all the billing information inside Order table
    #         data = Order()
    #         data.user = current_user
    #         data.first_name = form.cleaned_data['first_name']
    #         data.last_name = form.cleaned_data['last_name']
    #         data.phone = form.cleaned_data['phone']
    #         data.email = form.cleaned_data['email']
    #         data.address_line_1 = form.cleaned_data['address_line_1']
    #         data.address_line_2 = form.cleaned_data['address_line_2']
    #         data.country = form.cleaned_data['country']
    #         data.city = form.cleaned_data['city']
    #         data.state = form.cleaned_data['state']
    #         data.order_note = form.cleaned_data['order_note']
    #         data.order_total = grand_total
    #         data.tax = tax
    #         data.ip = request.META.get('REMOTE_ADDR')
    #         data.save()

    #         # Generate order number
    #         yr = int(datetime.date.today(), strftime('%Y'))
    #         dt = int(datetime.date.today(), strftime('%d'))
    #         mt = int(datetime.date.today(), strftime('%m'))
    #         d = datetime.date(dt, mt, yr)
    #         current_date = d.strftime('%d%m%Y')
    #         order_number = current_date + str(data.id)
    #         data.order_number = order_number
    #         data.save()

    #         order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
    #         context = {
    #             'order': order, 
    #             'cart_items': cart_items,
    #             'tax': tax,
    #             'total': total, 
    #             'grand_total': grand_total 
    #         }
    return render(request, 'orders/payments.html')
    # else:
    #     return redirect('checkout')


def order_complete(request):
    order_number = request.GET.get('order_number')
    trans_ID = request.GET.get('payment_id')

    # try:
    #     order = Order.objects.get(order_number=order_number, is_ordered=True)
    #     ordered_products = OrderProduct.objects.filter(order_id=order.id)

    #     payment = Payment.objects.get(payment_id=trans_ID)

    #     subtotal = 0
    #     for i in ordered_products:
    #         subtotal += i.product_price * i.quantity

    #     context = {
    #         'order': order,
    #         'ordered_products': ordered_products,
    #         'order_number': order.order_number,
    #         'trans_id': payment.payment_id,
    #         'payment': payment,
    #         'subtotal': subtotal
    #     }
    return render(request, 'orders/order_complete.html')

    # except (Payment.DoesNotExist, Order.DoesNotExist):
    #     return redirect('home')




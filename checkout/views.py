from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MakePaymentForm, OrderForm
from .models import OrderLineItem
from django.conf import settings
from products.models import Product
from django.utils import timezone
import stripe
from datetime import date
import time
from datetime import datetime

stripe.api_key = settings.STRIPE_SECRET

@login_required()
def checkout(request):
    if request.method=="POST":
        order_form = OrderForm(request.POST)
        payment_form = MakePaymentForm(request.POST)
        
        if order_form.is_valid() and payment_form.is_valid():
            order = order_form.save(commit=False)
            order.date = timezone.now()
            order.save()

            cart = request.session.get('cart', {})
            total = 0
            print("user", request.user.username)
            cliente = stripe.Customer.create(
                name = request.user.username,
                email = request.user.email,)
            for id, quantity in cart.items():
                product = get_object_or_404(Product, pk=id)
                print(product)
                total += quantity * product.price
                stripe.InvoiceItem.create(
                    unit_amount=int(product.price),
                    currency='CLP',
                    quantity = quantity,
                    customer = cliente.id,
                    description= product.name,
                    )
                order_line_item = OrderLineItem(
                    order = order,
                    product = product,
                    quantity = quantity
                    )
                order_line_item.save()

            try:
                print("email: ", request.user.email)
                #cliente = stripe.Customer.create(email = request.user.email)
                #customer = stripe.Charge.create(
                #    amount= int(total * 1000),
                #    currency="CLP",
                #    description="nueva compra",
               #     card=payment_form.cleaned_data['stripe_id'],
               #     receipt_email=request.user.email,
               #     )
                invoice = stripe.Invoice.create(
                    customer=cliente.id,
                    collection_method='send_invoice',
                    days_until_due=30,
                    #due_date = int(t + 1000),
                    )
                #t = datetime.timestamp(datetime.now())
                #print(t)
                #invoice.send_invoice()
                #print("send invoice: ", invoice)
                #invoice.finalize_invoice()
                #invoice.send_invoice()
                #invoice = stripe.Invoice.finalize_invoice(invoice.id)
                #print("finalice invoice: ", invoice)
            except stripe.error.CardError:
                messages.error(request, "Your card was declined!")

            if True:
                messages.error(request, "You have successfully paid")
                request.session['cart'] = {}
                return redirect(reverse('products'))
            else:
                messages.error(request, "Unable to take payment")
        else:
            print(payment_form.errors)
            messages.error(request, "We were unable to take a payment with that card!")
    else:
        payment_form = MakePaymentForm()
        order_form = OrderForm()

    return render(request, "checkout.html", {'order_form': order_form, 'payment_form': payment_form, 'publishable': settings.STRIPE_PUBLISHABLE })
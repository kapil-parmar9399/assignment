from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import OrderRequestForm
from .models import Order, OrderItem
from .recommendations import recommend_box


def home(request):
    result = None
    order = None
    if request.method == "POST":
        form = OrderRequestForm(request.POST)
        if form.is_valid():
            order = Order.objects.create()
            OrderItem.objects.bulk_create([
                OrderItem(order=order, product=product, quantity=form.cleaned_data["quantity"])
                for product in form.cleaned_data["products"]
            ])
            result = recommend_box(order)
            if result is None:
                messages.warning(request, "No available box can safely fit this order within its weight limit.")
            else:
                messages.success(request, f"Recommended {result.box.name} for order #{order.pk}.")
    else:
        form = OrderRequestForm()
    return render(request, "shipping/home.html", {"form": form, "result": result, "order": order})

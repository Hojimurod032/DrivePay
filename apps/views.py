import stripe
from decouple import config
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import TemplateView, DetailView

from apps.models import Item, Order
from root import settings


class HomeViewList(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['item_data'] = Item.objects.all()
        return data


class SearchOrderView(TemplateView):
    template_name = 'order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        order_id = self.request.GET.get('order_id')
        if order_id:
            order = Order.objects.filter(order_id=order_id).first()

            context['order'] = order
        return context

class DetailViewList(DetailView):
    queryset = Item.objects.all()
    pk_url_kwarg = 'id'
    template_name = 'detail.html'
    context_object_name = 'item_detail_data'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stripe_public_key'] = settings.STRIPE_PK
        return context


class BuyItemView(View):
    def get(self, request, id):
        item = get_object_or_404(Item, pk=id)

        stripe.api_key = config('STRIPE_SK')

        order = Order.objects.create(
            total_price=item.price,
            status=Order.Status.PENDING,
        )

        order.items.add(item)
        session = stripe.checkout.Session.create(
            mode='payment',
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": item.name,
                        "description": item.description,
                    },
                    "unit_amount": int(item.price * 100),
                },
                "quantity": 1,
            }],

            success_url=request.build_absolute_uri(
                reverse('success')
            ) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse('cannel')),
        )
        order.stripe_session_id = session.id
        order.save(update_fields=['stripe_session_id'])

        return JsonResponse({'id': session.id})


class SuccessView(TemplateView):
    template_name = 'success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session_id = self.request.GET.get('session_id')
        if session_id:
            stripe.api_key = config('STRIPE_SK')
            session = stripe.checkout.Session.retrieve(session_id)

            order = Order.objects.filter(
                stripe_session_id=session.id
            ).first()

            if order and session.payment_status == 'paid':
                order.status = Order.Status.PAID
                order.save(update_fields=['status'])
                context['order'] = order

        return context


class CannelView(TemplateView):
    template_name = 'cancel.html'

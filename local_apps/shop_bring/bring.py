# -*- coding: utf-8 -*-
from decimal import Decimal

from django.conf import settings
from django.conf.urls.defaults import patterns, url
from django.shortcuts import render_to_response
from django.template import RequestContext
from django import forms

from shop.util.decorators import on_method, shop_login_required
from shop.models.ordermodel import OrderExtraInfo

import requests
import simplejson

tmp_choices = (
    (90, 'Fast'),
    (50, 'Slow')
)

class BringChoicesForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices')
        self.zipcode = kwargs.pop('zipcode')
        super(BringChoicesForm, self).__init__(*args, **kwargs)
        self.fields['shipment_method'].choices = choices

    shipment_method = forms.ChoiceField()
    
    def clean(self):
        cleaned_data = super(BringChoicesForm, self).clean()
        cleaned_data['zipcode'] = self.zipcode
        return cleaned_data
        
class BringShipping(object):

    url_namespace = 'posten'
    backend_name = 'Posten'
    
    def __init__(self, shop):
        self.shop = shop  # This is the shop reference, it allows this backend
        # to interact with it in a tidy way (look ma', no imports!)

    def get_bound_form(self, request, items, shipping_adress_form=False, billing_adress_form=False):
        if not shipping_adress_form:
            zipcode = self.shop.get_order(request).shipping_address.zip_code
        else:
            zipcode = shipping_adress_form.data['ship-zip_code']
            
        choices = self.get_product_choices()[1]    
        if request.method == 'POST':
            form = BringChoicesForm(request.POST, choices=choices, zipcode=zipcode)
        else:
             form = BringChoicesForm(choices=choices)   
        return form
    
    def get_choice(self, product):
        name = product['GuiInformation']['ProductName']
        price = product['Price']['PackagePriceWithoutAdditionalServices']['AmountWithVAT']
        return (product['ProductId'], u'%s %skr' % (name, price))
    
    def get_product_choices(self):
        url = 'http://fraktguide.bring.no/fraktguide/products/all.json'
        params = {
            'weightInGrams': 1500,
            'from': 3242,
            'to': 7600
        }
        data = simplejson.loads(requests.get(url, params=params).text)
        form_choices = []
        choices = {}
        for product in data['Product']:
            choices[product['ProductId']] = product
            form_choices.append(self.get_choice(product))
        return (choices, form_choices)
    
    def get_rate(self, products, choices, items):
        product_type = choices['shipment_method']
        product = products[0][product_type]
        return Decimal(product['Price']['PackagePriceWithoutAdditionalServices']['AmountWithVAT'])
        
    def get_info(self, products, choices, items):
        product_type = choices['shipment_method']
        product = products[0][product_type]
        return product['GuiInformation']['ProductName']

    @on_method(shop_login_required)
    def view_process_order(self, request):
        rate = None
        choices = request.session.get('shipping_choices', None)
        order = self.shop.get_order(request)
        items = order.items.all()
        
        products = self.get_product_choices()
        if choices:
            rate = self.get_rate(products, choices, items)
            info = self.get_info(products, choices, items)
        else:
            form = self.get_bound_form(request, items)
            if request.method == 'POST':
                if form.is_valid():
                    rate = self.get_rate(products, form.cleaned_data, items)
                    info = self.get_info(products, choices, items)
    
        if rate:
            OrderExtraInfo.objects.create(order=order, text=info)
            self.shop.add_shipping_costs(order,
                'Posten shipping', rate)
            return self.shop.finished(order)
            
        ctx = {}
        ctx.update({'form': form})
        return render_to_response('shop_bring/choices.html',
            ctx, context_instance=RequestContext(request))
        
    def get_urls(self):
        """
        Return the list of URLs defined here.
        """
        urlpatterns = patterns('',
            url(r'^$', self.view_process_order, name='posten'),
        )
        return urlpatterns
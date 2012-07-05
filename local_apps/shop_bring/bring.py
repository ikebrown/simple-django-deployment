# -*- coding: utf-8 -*-
from decimal import Decimal

from django.conf import settings
from django.conf.urls.defaults import patterns, url
from django.shortcuts import render_to_response
from django.template import RequestContext
from django import forms

from shop.util.decorators import on_method, shop_login_required
from shop.models.ordermodel import OrderExtraInfo
from shop.util.address import get_shipping_address_from_request

import requests
import simplejson
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as gettext

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
        if not self.zipcode:
            raise forms.ValidationError(gettext("Zipcode required to calculate shipping"))
        else:
            cleaned_data['zipcode'] = self.zipcode
        return cleaned_data
        
class BringShipping(object):

    url_namespace = 'posten'
    backend_name = 'Posten'
    
    def __init__(self, shop):
        self.shop = shop  # This is the shop reference, it allows this backend
        # to interact with it in a tidy way (look ma', no imports!)
        
    def get_zipcode(self, request, shipping_adress_form=False):
        if not shipping_adress_form:
            return get_shipping_address_from_request(request).zip_code
        else:
            return shipping_adress_form.data.get('ship-zip_code', None)

    def get_bound_form(self, request, items, shipping_adress_form=False, billing_adress_form=False):
        zipcode = self.get_zipcode(request, shipping_adress_form=shipping_adress_form)
            
        choices = self.get_product_choices(zipcode, items)[1]    
        if request.method == 'POST':
            form = BringChoicesForm(request.POST, choices=choices, zipcode=zipcode)
        else:
             form = BringChoicesForm(choices=choices, zipcode=zipcode)   
        return form
    
    def get_choice(self, product):
        name = product['GuiInformation']['ProductName']
        price = product['Price']['PackagePriceWithoutAdditionalServices']['AmountWithVAT']
        return (product['ProductId'], u'%s %skr' % (name, price))
    
    def get_item_params(self, items):
        weight = 0
        packets = []
        for item in items:
            if item.product.weight:
                weight = weight + item.product.weight
            else:
                packets.append(item.product.dimensions)
                
        data = {}
        data['weightInGrams'] = weight
        if packets:
            if len(packets) > 1:
                for packet in packets:
                    i = 1
                    for k, v in packet.items():
                        data['%s%s' % (k, i) ] = v
                    i += 1
            else:
                data.update(packets[0])
        return data
                
    
    def get_product_choices(self, tozip, items):
        if not getattr(self, '_product_choices_cache', None):
            url = 'http://fraktguide.bring.no/fraktguide/products/all.json'
            params = self.get_item_params(items)
            params.update({'from': '7650', 'to': tozip})
            data = simplejson.loads(requests.get(url, params=params).text)
            form_choices = []
            choices = {}
            for product in data['Product']:
                choices[product['ProductId']] = product
                form_choices.append(self.get_choice(product))
            self._product_choices_cache = (choices, form_choices)
        return self._product_choices_cache
    
    def get_rate(self, products, choices):
        product_type = choices['shipment_method']
        product = products[0][product_type]
        return Decimal(product['Price']['PackagePriceWithoutAdditionalServices']['AmountWithVAT'])
        
    def get_info(self, products, choices):
        product_type = choices['shipment_method']
        product = products[0][product_type]
        return product['GuiInformation']['ProductName']

    @on_method(shop_login_required)
    def view_process_order(self, request):
        rate = None
        choices = request.session.get('shipping_choices', None)
        order = self.shop.get_order(request)
        items = order.items.all()

        if choices:
            products = self.get_product_choices(choices['zipcode'], items)
            rate = self.get_rate(products, choices)
            info = self.get_info(products, choices)
            request.session['shipping_choices'] = None
        else:
            form = self.get_bound_form(request, items)
            if request.method == 'POST':
                if form.is_valid():
                    products = self.get_product_choices(form.cleaned_data['zipcode'], items)
                    rate = self.get_rate(products, form.cleaned_data)
                    info = self.get_info(products, form.cleaned_data)
    
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
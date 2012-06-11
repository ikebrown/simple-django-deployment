# -*- coding: utf-8 -*-
from decimal import Decimal

from django.conf import settings
from django.conf.urls.defaults import patterns, url
from django.shortcuts import render_to_response
from django.template import RequestContext
from django import forms

from shop.util.decorators import on_method, shop_login_required

class BringChoicesForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        del kwargs['zipcode']
        super(BringChoicesForm, self).__init__(*args, **kwargs)
        
    rate = forms.DecimalField()

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
            
        if request.method == 'POST':
            form = BringChoicesForm(request.POST, zipcode=zipcode)
        else:
             form = BringChoicesForm(zipcode=zipcode)   
        return form
    
    def get_rate(self, choices, items):
        return choices['rate']

    @on_method(shop_login_required)
    def view_process_order(self, request):
        rate = None
        choices = request.session.get('shipping_choices', None)
        order = self.shop.get_order(request)
        items = order.items.all()
        
        if choices:
            rate = self.get_rate(choices, items)
        else:
            form = self.get_bound_form(request, items)
            if request.method == 'POST':
                if form.is_valid():
                    rate = self.get_rate(form.cleaned_data, items)
    
        if rate:
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
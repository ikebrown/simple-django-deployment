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

    def get_bound_form(self, request, shipping_adress_form=False, billing_adress_form=False):
        if not shipping_adress_form:
            zipcode = self.shop.get_order(request).shipping_address.zip_code
        else:
            zipcode = shipping_adress_form.data['ship-zip_code']        
            
        if request.method == 'POST':
            form = BringChoicesForm(request.POST, zipcode=zipcode)
        else:
             form = BringChoicesForm(zipcode=zipcode)   
        return form

    @on_method(shop_login_required)
    def view_process_order(self, request):
        choices = request.session.get('shipping_choices', None)
        rate = choices and choices['rate']
        if rate:
            self.shop.add_shipping_costs(self.shop.get_order(request),
                'Posten shipping', form.cleaned_data['rate'])
            return self.shop.finished(self.shop.get_order(request))            
        
        form = self.get_bound_form(request)
        if request.method == 'POST':
            if form.is_valid():
                self.shop.add_shipping_costs(self.shop.get_order(request),
                    'Posten shipping', form.cleaned_data['rate'])
                return self.shop.finished(self.shop.get_order(request))
                # That's an HttpResponseRedirect
        ctx = {}
        ctx.update({'form': form})
        return render_to_response('shop/shipping/bring/choices.html',
            ctx, context_instance=RequestContext(request))
            
    def get_urls(self):
        """
        Return the list of URLs defined here.
        """
        urlpatterns = patterns('',
            url(r'^$', self.view_process_order, name='posten'),
        )
        return urlpatterns
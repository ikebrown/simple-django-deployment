from django.http import HttpResponseRedirect

from shop.views.checkout import CheckoutSelectionView
from django.core.urlresolvers import reverse
from shop.backends_pool import backends_pool
from shop.util.order import add_order_to_request, get_order_from_request
from shop.util.address import (
    assign_address_to_request,
    get_billing_address_from_request,
    get_shipping_address_from_request,
)

class CheckoutShippingSelectionView(CheckoutSelectionView):
    
    def handle_billingshipping_forms(self, update_only, shipping_adress_form, billing_address_form):
        
        all_valid = False
        
        billingshipping_form = \
            self.get_billing_and_shipping_selection_form()
        if billingshipping_form.is_valid():
            self.request.session['payment_backend'] = \
                billingshipping_form.cleaned_data['payment_method']
            self.request.session['shipping_backend'] = \
                billingshipping_form.cleaned_data['shipping_method']
                
        shipping_choices_form = False
        payment_choices_form = False
                            
        if billingshipping_form.is_valid():
            all_valid = True
            
            shipping_method = billingshipping_form.cleaned_data['shipping_method']
            payment_method = billingshipping_form.cleaned_data['payment_method']
            
            if update_only:
                shipping_choices_form = self.get_backend_choices_form('shipping', shipping_method,
                    shipping_adress_form, billing_address_form)         
                payment_choices_form = self.get_backend_choices_form('payment', payment_method,
                    shipping_adress_form, billing_address_form)         
    
                if shipping_choices_form:
                    if shipping_choices_form.is_valid():
                        self.request.session['shipping_choices'] = shipping_choices_form.cleaned_data
                    else:
                        all_valid = False
                if payment_choices_form:
                    if payment_choices_form.is_valid():
                        self.request.session['payment_choices'] = payment_choices_form.cleaned_data
                    else:
                        all_valid = False
                        
        return (billingshipping_form, shipping_choices_form, payment_choices_form)
       
    def handle_forms(self, update_only=False):
        forms = getattr(self, '_forms', None)
        if not forms:
            shipping_form = self.get_shipping_address_form()
            billing_form = self.get_billing_address_form()
        
            if not update_only and shipping_form.is_valid() and billing_form.is_valid():
                shipping_address = shipping_form.save()
                billing_address = billing_form.save()
                order = self.create_order_object_from_cart()
    
                self.save_addresses_to_order(order, shipping_address,
                    billing_address)
    
                # The following marks addresses as being default addresses for
                # shipping and billing. For more options (amazon style), we should
                # remove this
                assign_address_to_request(self.request, shipping_address,
                    shipping=True)
                assign_address_to_request(self.request, billing_address,
                    shipping=False)                
                    
            billingshipping_form, shipping_choices_form, payment_choices_form = \
                self.handle_billingshipping_forms(update_only, shipping_form, billing_form)
                
            self._forms = {
                'shipping_address': shipping_form,
                'billing_address': billing_form,
                'billing_shipping_form': billingshipping_form,
                'shipping_choices_form': shipping_choices_form,
                'payment_choices_form': payment_choices_form
            }
        return self._forms
        
    def all_forms_valid(self, update_only=False):
        valid = True
        for form in self.handle_forms().values():
            if form:
                valid = valid and form.is_valid()
        return valid
                
    def get_backend_choices_form(self, backend_type, backend_namespace, shipping_adress_form, billing_address_form):
        form = getattr(self, '_%s_%s_form' % (backend_type, backend_namespace), None)
        if form is None: # Not tried getting this form yet
            form = False # Is no choices form on this backend
            backends = getattr(backends_pool, 'get_%s_backends_list' % backend_type)()
            for backend in backends:
                if backend.url_namespace == backend_namespace:
                    func = getattr(backend, 'get_bound_form', False)
                    if func:
                        form = func(self.request, shipping_adress_form, billing_address_form)
        setattr(self, '_%s_%s_form' % (backend_type, backend_namespace), form)
        return form

    def post(self, *args, **kwargs):
        """ Called when view is POSTed """
        update_only = self.request.POST.get('update_only', False)
        self.handle_forms(update_only=update_only)
        if self.all_forms_valid() and not update_only:
            return HttpResponseRedirect(reverse('checkout_confirm'))
        return self.get(self, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        This overrides the context from the normal template view
        """
        ctx = super(CheckoutSelectionView, self).get_context_data(**kwargs)
        ctx.update(self.handle_forms())
        return ctx    
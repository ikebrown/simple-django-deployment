from django.conf.urls.defaults import *
from shop_singlestep.views import CheckoutSinglestepSelectionView

urlpatterns = patterns('',
    url(r'^$', CheckoutSinglestepSelectionView.as_view(),
        name='checkout_selection'  # First step of the checkout process
    )
)


    



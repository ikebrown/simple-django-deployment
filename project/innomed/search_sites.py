from cms.models import monkeypatch_reverse
monkeypatch_reverse()

import haystack
haystack.autodiscover()
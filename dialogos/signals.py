import django.dispatch


commented = django.dispatch.Signal(providing_args=["comment", "request"])
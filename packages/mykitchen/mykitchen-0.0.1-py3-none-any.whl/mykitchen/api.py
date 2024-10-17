from ninja import NinjaAPI
from django.conf import settings

api = NinjaAPI(version=settings.VERSION, title="mykitchen_cookbook_sdk")

api.add_router("/mykitchen/", "mykitchen.mykitchen_cookbook.kitchen.router")  #   or by Python path


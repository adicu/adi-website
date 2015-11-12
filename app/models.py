from eventum.models import Event
from flask import url_for, current_app




def augment_models():
    Event.register_method(image_url)

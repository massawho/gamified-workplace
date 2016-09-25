from django.dispatch import Signal

update_score = Signal(providing_args=["instance", "current_user", "args", "kwargs"])

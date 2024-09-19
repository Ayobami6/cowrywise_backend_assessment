from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    
    # def ready(self) -> None:
    #     from .subscriber import listen_save_user_event
    #     listen_save_user_event()

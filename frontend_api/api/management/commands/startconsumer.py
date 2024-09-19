from typing import Any
from django.core.management.base import BaseCommand
from api.subscriber import listen_save_user_event
import time


class Command(BaseCommand):
    help = "Start consumer"
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        listen_save_user_event()
        # self.stdout.write("Started Consumer Thread")
        

from typing import Any
from django.core.management.base import BaseCommand
from api.subscriber import start_listening
import time


class Command(BaseCommand):
    help = "Start consumer"
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        start_listening()
        

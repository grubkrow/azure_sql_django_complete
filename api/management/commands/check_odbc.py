from django.core.management.base import BaseCommand
import pyodbc
from django.conf import settings


class Command(BaseCommand):
    help = "Print available ODBC drivers and attempt a test connection using DATABASES setting."

    def handle(self, *args, **options):
        self.stdout.write("Detected pyodbc drivers:")
        drivers = pyodbc.drivers()
        for d in drivers:
            self.stdout.write(f"  {d}")

        cfg = settings.DATABASES.get('default', {})
        self.stdout.write("\nDatabase configuration:")
        for k, v in cfg.items():
            if k != 'PASSWORD':
                self.stdout.write(f"  {k}: {v}")
        self.stdout.write("
Attempting connection...")
        try:
            conn = pyodbc.connect(
                'DRIVER={driver};SERVER={host},{port};DATABASE={name};UID={user};PWD={password}'
                .format(
                    driver=cfg.get('OPTIONS', {}).get('driver', ''),
                    host=cfg.get('HOST', ''),
                    port=cfg.get('PORT', ''),
                    name=cfg.get('NAME', ''),
                    user=cfg.get('USER', ''),
                    password=cfg.get('PASSWORD', ''),
                ),
                timeout=5,
            )
            self.stdout.write("Connection succeeded!")
            conn.close()
        except Exception as e:
            self.stderr.write(f"Connection failed: {e}")

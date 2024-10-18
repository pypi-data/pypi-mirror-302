import importlib.util
import subprocess
from multiprocessing import Pool

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from falco.conf import app_settings


class Command(BaseCommand):
    help = "Run every dev process needed in one command"

    def add_arguments(self, parser):
        parser.add_argument(
            "address",
            type=str,
            nargs="?",
            default="127.0.0.1:8000",
            help="Address to run the django server on",
        )

    def handle(self, *_, **options):
        address = options["address"]
        settings_flag = f""
        commands = {"runserver": "django-admin runserver {address}" + settings_flag}
        if "django_tailwind_cli" in settings.INSTALLED_APPS:
            commands["tailwind"] = f"django-admin tailwind {settings_flag} watch"
        if "tailwind" in settings.INSTALLED_APPS:
            commands["tailwind"] = f"django-admin tailwind {settings_flag} start"
        if "django_q" in settings.INSTALLED_APPS:
            commands["qcluster"] = f"django-admin qcluster {settings_flag}"

        commands.update(app_settings.WORK)
        commands["runserver"] = commands["runserver"].format(address=address)

        call_command("migrate")
        if importlib.util.find_spec("honcho"):
            self.run_with_honcho(commands)
        else:
            self.run_with_multiprocess(commands)

    @classmethod
    def run_with_multiprocess(cls, commands: dict):
        with Pool(processes=len(commands)) as pool:
            try:
                pool.map(subprocess.run, [cmd.split() for cmd in commands.values()])
            except KeyboardInterrupt:
                pool.terminate()
            finally:
                pool.close()
                pool.join()

    @classmethod
    def run_with_honcho(cls, commands: dict):
        from honcho.manager import Manager

        manager = Manager()
        for name, cmd in commands.items():
            manager.add_process(
                name,
                cmd,
            )

        try:
            manager.loop()
        finally:
            manager.terminate()

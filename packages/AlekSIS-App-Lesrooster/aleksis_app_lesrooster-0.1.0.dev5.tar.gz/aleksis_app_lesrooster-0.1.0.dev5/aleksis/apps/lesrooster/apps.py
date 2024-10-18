from django.db.models import signals

from aleksis.core.util.apps import AppConfig

from .util.signal_handlers import create_time_grid_for_new_validity_range


class DefaultConfig(AppConfig):
    name = "aleksis.apps.lesrooster"
    verbose_name = "AlekSIS — Lesrooster"
    dist_name = "AlekSIS-App-Lesrooster"

    urls = {
        "Repository": "https://edugit.org/AlekSIS/onboarding//AlekSIS-App-Lesrooster",
    }
    licence = "EUPL-1.2+"
    copyright_info = (([2023], "Jonathan Weth", "dev@jonathanweth.de"),)

    def ready(self):
        from .models import ValidityRange

        signals.post_save.connect(create_time_grid_for_new_validity_range, sender=ValidityRange)

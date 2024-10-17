import datetime
import logging

from tidsreg.api import TidsRegger
from tidsreg.models import Registration
from playwright.sync_api import sync_playwright

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    with sync_playwright() as p:
        tr = TidsRegger(p)
        if not tr.state.exists():
            tr.log_in()
            #    tr.clear_registrations()
        tr.register_hours(
            Registration(
                "Fagkoordination (Koordinator",
                datetime.time(6),
                datetime.time(6, 30),
            )
        )
        tr.register_hours(
            Registration(
                "Fagkoordination (Koordinator",
                datetime.time(10),
                datetime.time(11),
                "Min kommentar",
            )
        )
        tr.get_registrations()
        tr.clear_registrations()

        tr.close()

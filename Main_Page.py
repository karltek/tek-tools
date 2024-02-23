#!/usr/bin/env python3

from nicegui import Tailwind, ui
with ui.tabs() as tabs:
        ui.tab("Home")
        ui.tab("Cortex XDR")
        ui.tab("Carbon Black")
        ui.tab("Crowdstrike")

with ui.tab_panels(tabs, value='Home').classes('w-full h-full p-4 font-mono text-white-900 '):
        with ui.tab_panel('Home'):
            from Home_Page import home
            home()
        with ui.tab_panel('Cortex XDR'):
            from CortexXDR_Page import CortexPage
            CortexPage()
        with ui.tab_panel('Carbon Black'):
            from CarbonBlack_Page import CarbonBlackPage
            CarbonBlackPage()
        with ui.tab_panel('Crowdstrike'):
            ui.label("Nothing to see here for now. It's still a work in progress")

ui.run(title="ktek", dark=True, binding_refresh_interval=2, port=8888)
#!/usr/bin/env python3
from nicegui import ui
from CarbonBlack_Alerts import CBCloudAlerts, CBCloudTable
import json

class CarbonBlackPage:
    def __init__(self) -> None:
        ui.label('Carbon Black Cloud').classes('text-2xl')
        with ui.row().classes("flex-nowrap w-full h-full"):
            with ui.column().classes("w-1/3"):
                self.BASE_URL = ui.input("Base URL", placeholder="https://defense-prod05.conferdeploy.net").classes("w-full pr-10")       
                self.ORG_KEY = ui.input("Org Key").classes("w-full pr-10")   
                self.API_ID = ui.input("API ID").classes("w-full pr-10")
                self.API_SECRET = ui.input("API Secret", password=True, password_toggle_button=True).classes("w-full pr-10")
                self.DATE_RANGE = ui.input("Date Range").classes("w-full pr-10")
            with ui.column().classes("w-2/3 w-full h-full"):
                ui.button("Run", on_click=lambda: results.set_value(get_alerts()))
                # ui.button("Run", on_click=lambda: print(BASE_URL.value, APP_ID.value, API_SECRET.value, DATE_RANGE.value.split()))
                results = ui.textarea("Raw JSON Results").classes("w-full h-full font-mono")
    
        with ui.row().classes("flex flex-nowrap w-full h-full pt-5 font-mono") as self.TABLED_RESULTS:
            with ui.column().classes("flex flex-nowrap w-1/3 h-full"):
                ui.label("Fusion Query").classes("text-2xl underline nderline-offset-8")
                ui.label("In Fusion, do an Advanced Search and use the query below ↓").classes("p-0")
        
            with ui.column().classes("w-2/3"):
                ui.label("Tabulated Alerts").classes("text-2xl underline nderline-offset-8")
                self.tabled_alerts = ui.html()
            self.TABLED_RESULTS.set_visibility(False)

        def get_alerts():
            try:
                if self.BASE_URL.value == "":
                    self.BASE_URL.set_value("https://defense-prod05.conferdeploy.net")
                cb_cloud = CBCloudAlerts(self.BASE_URL.value, self.ORG_KEY.value, self.API_ID.value, self.API_SECRET.value, self.DATE_RANGE.value)
                if cb_cloud.getAlerts().status_code == 200:
                    data = cb_cloud.getAlerts().json()
                    content = CBCloudTable(data).table()
                    self.tabled_alerts.set_content(f"<pre>{content}</pre>")
                    self.TABLED_RESULTS.set_visibility(True)
                    return json.dumps(data, indent=4)
                    
            except Exception as e:
                if self.BASE_URL.value == '' or self.ORG_KEY.value == '' or self.API_ID.value == '' or self.API_SECRET.value =='' or self.DATE_RANGE.value == '':
                    ui.notify("Error. Some or all API Credential is empty",  position="top-right", type="warning")
                elif cb_cloud.getAlerts().status_code != 200:
                    return cb_cloud.getAlerts().text
                else:
                    ui.notify("Error. Please check if the API Credentials are correct") 
                return f"Error: {e}"
            

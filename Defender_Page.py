#!/usr/bin/env python3
from Defender_Alerts import DefenderAlerts, DefenderTable
from nicegui import ui
import json

class DefenderPage:
    def __init__(self) -> None:
        ui.label('Microsoft Defender').classes('text-2xl')
        with ui.row().classes("flex flex-nowrap w-full h-full"):
            with ui.column().classes("w-1/3 pr-10"):
                self.BASE_URL = "https://api.securitycenter.windows.com"
                self.JSON_RESPONSE = ui.textarea("Enter Token or the JSON Response that contains the Token").classes("w-full h-full font-mono")
                # self.BASE_URL = ui.input("Base URL", placeholder="https://api.securitycenter.windows.com").classes("w-full ")       
                # self.TOKEN = ui.input("Token", placeholder="Enter the TOKEN or the JSON Response that contains the Token").classes("w-full h-full flex flex-wrap")
                self.DATE_RANGE = ui.input("Date Range").classes("w-full")
        
            with ui.column().classes("w-2/3 w-full h-full"):
                ui.button("Run", on_click=lambda: results.set_value(get_alerts()))
                # ui.button("Run", on_click=lambda: print(BASE_URL.value, APP_ID.value, API_SECRET.value, DATE_RANGE.value.split()))
                results = ui.textarea("Raw Results").classes("w-full h-full font-mono")
        
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
                TOKEN = json.loads(self.JSON_RESPONSE.value)["access_token"]
                mdatp_alerts = DefenderAlerts(self.BASE_URL, TOKEN, self.DATE_RANGE.value) 
                if mdatp_alerts.getAlerts().status_code == 200:
                    data = mdatp_alerts.getAlerts().json()
                    content = DefenderTable(data).table()
                    self.tabled_alerts.set_content(f"<pre>{content}</pre>")
                    self.TABLED_RESULTS.set_visibility(True)
                    return json.dumps(data, indent=4)
                
            except json.decoder.JSONDecodeError:
                TOKEN = self.JSON_RESPONSE.value
                mdatp_alerts = DefenderAlerts(self.BASE_URL.value, TOKEN, self.DATE_RANGE.value) 
                if mdatp_alerts.getAlerts().status_code == 200:
                    data = mdatp_alerts.getAlerts().json()
                    content = DefenderTable(data).table()
                    self.tabled_alerts.set_content(f"<pre>{content}</pre>")
                    self.TABLED_RESULTS.set_visibility(True)
                    return json.dumps(data, indent=4)
                
            except Exception as e:
                if self.TOKEN.value == '' or self.DATE_RANGE.value =='':
                    ui.notify("Error. Some or all API Credential is empty",  position="top-right", type="warning")
                elif mdatp_alerts.getAlerts().status_code != 200:
                    return mdatp_alerts.getAlerts().text
                else:
                    ui.notify("Error. Please check if the API Credentials are correct", position="top-right", type="warning") 
                return f"Error: {e}"
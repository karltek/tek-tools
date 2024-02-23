#!/usr/bin/env python3
from nicegui import ui
import time, calendar
from prettytable import PrettyTable, ALL
import json 

class home:    
    def __init__(self):
        ui.label("Welcome to the STM API Tool. This is a work in progress and may contain bugs").classes('py-4')
        with ui.row().classes("flex flex-nowrap inline w-1/2 border rounded-lg p-4 shadow-lg shadow-indigo-500/40"):
            with ui.column().classes("flex flex-nowrap inline w-2/3"):
                ui.label("Date Range Converter").classes("p-0 w-full")
                self.date_range = ui.input("Enter Date Range", placeholder="Date should look like → 2023-01-28T15:01:01Z to 2023-01-28T16:01:01Z").classes("inline w-full")
                ui.button("Convert", on_click=self.convert).classes("inline p-2")
            with ui.column().classes("w-1/3 font-mono items-center"):
                self.WAITING = ui.label("Waiting for Date Range input")
                self.EPOCH_TIMES = ui.html()

        with ui.column().classes("w-full h-full flex flex-nowrap py-4"):
            with ui.row().classes("w-full h-full border rounded-lg p-4 shadow-lg shadow-indigo-500/40 flex-nowrap "):
                with ui.column().classes("w-1/3"):
                    ui.label("JSON Formatter").classes("p-0")
                    self.JSON_ENTRY = ui.textarea("Insert JSON").classes("w-full")
                    ui.button("Format JSON", on_click= lambda: self.JSON_RESULT.set_value(JSON_Convert()))
                with ui.column().classes("flex flex-nowrap w-2/3"):
                    self.JSON_RESULT = ui.textarea("Result").classes("flex flex-nowrap w-full h-100")
            
        def JSON_Convert():
                try:
                    json_data = self.JSON_ENTRY.value
                    if json_data == "":
                        return "Error: No JSON value"
                    else:
                        json_data = json.loads(json_data)
                        data = json.dumps(json_data, indent=4)
                        return data
                    # self.JSON_RESULT.set_content(f"<pre>{data}</pre>")
                except Exception as e:
                    return f"Error: {e}.\nPlease Enter a valid JSON string"


    def convert(self):
        try:
            if  self.date_range.value == "": 
                self.WAITING.set_text(f"Error: Empty Date Range value. Try again!")
            else:
                self.EPOCH_TIMES.set_content("")
                # self.END_TIME.set_text("")
                self.WAITING.set_text("")
                x = self.date_range.value.split()
                timestamp1 = time.strptime(x[0], "%Y-%m-%dT%H:%M:%SZ")
                timestamp2 = time.strptime(x[2], "%Y-%m-%dT%H:%M:%SZ")
                timestart  = calendar.timegm(timestamp1) * 1000
                timeend = calendar.timegm(timestamp2) * 1000
                myTable = PrettyTable()
                myTable.field_names = ["START TIME", "END TIME"]
                myTable.add_row([timestart, timeend])
                self.EPOCH_TIMES.set_content(f"<pre>{myTable}<pre>")
        except Exception as e:
            self.WAITING.set_text(f"Error: {e}")

    # def page(self):
    #     # ui.label("Welcome to the STM API Tool. This is a work in progress and may contain bugs").classes('py-4')
    #     # with ui.row().classes("flex-nowrap"):
    #     #     ui.label("ROW 1").classes("w-1/2 bg-red-400")
    #     #     ui.label("ROW 2").classes("w-1/2 bg-red-400")
    #     with ui.column().classes("flex flex-nowrap inline w-1/2 border rounded-lg p-4 shadow-lg shadow-indigo-500/40"):
    #         ui.label("Date Range Converter").classes("p-0 w-2/3")
    #         date_range = ui.input("Enter Date Range").classes("inline w-2/3")
    #         ui.button("Convert", on_click=home.convert).classes("inline")
    #         WAIT = ui.label("Waiting for Data Range input")
    #         START_TIME = ui.label("")
    #         END_TIME = ui.label("")
        
    #     return date_range, WAIT, START_TIME, END_TIME



#!/usr/bin/env python3
from prettytable import PrettyTable, ALL
import requests
import json


class DefenderAlerts:
    def __init__(self, base_url, token, date_range) -> None:
        self.date_range = date_range
        self.base_url = base_url 
        self.token = token 

    def getAlerts(self):
        TIME_START = self.date_range.split()[0]
        TIME_END = self.date_range.split()[2]
        URI = f"/api/alerts?$filter=(alertCreationTime gt {TIME_START} and alertCreationTime lt {TIME_END})"
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        results = requests.get(self.base_url+URI, headers=headers)
        return results 

class DefenderTable:
    def __init__(self, alerts):
        self.alerts = alerts
    
    def table(self):

        # Initialize the Table to put the Alerts on
        myTable = PrettyTable()

        # Add Column Headers on the Alert Table
        myTable.field_names = ["RBAC GROUP NAME", "ALERT CREATION TIME", "SEVERITY", "STATUS", "RESOLVED TIME", "ID", "Incident ID", "DETECTOR ID", "COMPUTER NAME",]

        # This For Loop is used to insert values on the Alerts Table
        for alert in self.alerts["value"]:
            myTable.add_row(
                [
                    alert["rbacGroupName"],
                    alert["alertCreationTime"],
                    alert["severity"],
                    alert["status"],
                    alert["resolvedTime"],
                    alert["id"],
                    alert["incidentId"],
                    alert["detectorId"],
                    alert["computerDnsName"],
                ]
            )

        myTable.hrules = ALL
        return myTable
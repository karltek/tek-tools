#!/usr/bin/env python3
import requests
from prettytable import PrettyTable, ALL
# import json

class CBCloudAlerts:
    def __init__(self, base_url, org_key, api_id, api_key, date_range):
        self.base_url = base_url
        self.org_key = org_key
        self.api_id = api_id
        self.api_key = api_key
        self.date_range = date_range

    def dateRange(self):
        x = self.date_range.split()
        time_start = x[0].replace("Z", ".000Z")
        time_end = x[2].replace("Z", ".000Z")
        return (time_start, time_end)

    def getAlerts(self):
        headers = {"X-Auth-Token": f"{self.api_key}/{self.api_id}"}
        START_TIME = self.dateRange()[0]
        END_TIME = self.dateRange()[1]
        json_data = {
            "criteria": {
                "group_results": False,
                "minimum_severity": "1",
                "target_value": [
                    "LOW",
                    "MEDIUM",
                    "HIGH",
                    "MISSION_CRITICAL",
                ],
                "category": [
                    "THREAT",
                ],
                "create_time": {
                    "start": START_TIME,
                    "end": END_TIME,
                },
            },
            "query": "",
            "sort": [
                {
                    "field": "first_event_time",
                    "order": "ASC",
                },
            ],
            "start": 1,
            "rows": 1000,
        }
        results = requests.post(
            f"{self.base_url}/appservices/v6/orgs/{self.org_key}/alerts/_search",
            headers=headers,
            json=json_data,
        )

        return results

class CBCloudTable:
    def __init__(self, data):
        self.data = data 

    def table(self):
        if type(self.data) is dict:

            final_data = []
            key_list = ["id", "create_time", "threat_id", "workflow"]

            alerts = self.data

            for data in alerts["results"]:
                temp = {}
                for key in data.keys():
                    if key in key_list:
                        temp[key] = data[key]
                final_data.append(temp)

            ThreatIDs = []
            AlertIDs = []

            for alert in final_data:
                ThreatIDs.append(alert["threat_id"])
                AlertIDs.append(alert["id"])

            uniqueThreats = set(ThreatIDs)

            table_data = {}
            alerts_comments = {}

            for threat in uniqueThreats:
                table_data[threat] = {}
                table_data[threat]["alert_id"] = []
                table_data[threat]["create_time"] = []
                table_data[threat]["workflow_state"] = []

            for alert in final_data:
                alert_id = alert["id"]
                threat = alert["threat_id"]
                table_data[threat]["alert_id"].append(alert["id"])
                table_data[threat]["create_time"].append(alert["create_time"])
                table_data[threat]["workflow_state"].append(alert["workflow"]["state"])
                alerts_comments[alert_id] = alert["workflow"]["comment"]

            myTable = PrettyTable()
            myTable.field_names = ["THREAT ID", "ALERT ID", "CREATE TIME", "STATE"]

            for data in table_data:
                threat_id = data
                alert_id = "\n".join(table_data[data]["alert_id"])
                create_time = "\n".join(table_data[data]["create_time"])
                workflow_state = "\n".join(table_data[data]["workflow_state"])
                myTable.add_row([threat_id, alert_id, create_time, workflow_state])

            myTable.sortby = "THREAT ID"
            myTable.hrules = ALL
            return myTable
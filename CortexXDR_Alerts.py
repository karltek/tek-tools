#!/usr/bin/env python3
from datetime import datetime, timezone
from prettytable import PrettyTable, ALL
import secrets
import string
import hashlib
import time
import calendar
import requests
import json


class CortexAlerts:
    def __init__(self, base_url, api_id, api_key, date_range):
        self.base_url = base_url
        self.api_id = api_id
        self.api_key = api_key
        self.date_range = date_range

    def dateRange(self):
        x = self.date_range.split()
        timestamp1 = time.strptime(x[0], "%Y-%m-%dT%H:%M:%SZ")
        timestamp2 = time.strptime(x[2], "%Y-%m-%dT%H:%M:%SZ")
        time_start = calendar.timegm(timestamp1) * 1000
        time_end = calendar.timegm(timestamp2) * 1000
        return (time_start, time_end)

    def advanceAuth(self):
        # Generate a 64 bytes random string
        nonce = "".join(
            [secrets.choice(string.ascii_letters + string.digits) for _ in range(64)]
        )
        # Get the current timestamp as milliseconds.
        timestamp = int(datetime.now(timezone.utc).timestamp()) * 1000
        # Generate the auth key:
        auth_key = "%s%s%s" % (self.api_key, nonce, timestamp)
        # Convert to bytes object
        auth_key = auth_key.encode("utf-8")
        # Calculate sha256:
        api_key_hash = hashlib.sha256(auth_key).hexdigest()
        # Generate HTTP call headers
        headers = {
            "x-xdr-timestamp": str(timestamp),
            "x-xdr-nonce": nonce,
            "x-xdr-auth-id": str(self.api_id),
            "Authorization": api_key_hash,
            "Content-Type": "application/json",
        }
        return headers

    def getAlerts(self):
        uri = "/public_api/v1/incidents/get_incidents/"
        gte = self.dateRange()[0]
        lte = self.dateRange()[1]
        headers = self.advanceAuth()
        # return (uri, gte, lte, headers)


        data = {
            "request_data": {
                "filters": [
                    {"field": "creation_time", "operator": "gte", "value": gte},
                    {"field": "creation_time", "operator": "lte", "value": lte},
                ]
            }
        }

        results = requests.post(f"{self.base_url}{uri}", headers=headers, data=json.dumps(data))
        return results
    
class CortexTable:
    def __init__(self, alerts):
        self.data = alerts 

    def table(self):
        if type(self.data) is dict:

            final_data = []
            key_list = ["incident_id", "creation_time", "description", "status", "severity"]

            alerts = self.data

            for data in alerts["reply"]["incidents"]:
                temp = {}
                for key in data.keys():
                    if key in key_list:
                        temp[key] = data[key]
                final_data.append(temp)

            myTable = PrettyTable()
            myTable.field_names = ["INCIDENT ID", "CREATION TIME","DESCRIPTION", "STATUS", "SEVERITY"]

            for data in final_data:
                incident_id = data["incident_id"]
                creation_time = data["creation_time"]
                description = data["description"]
                status = data["status"]
                severity = data["severity"]
                myTable.add_row([incident_id, creation_time, description, status, severity])

            myTable.sortby = "INCIDENT ID"
            myTable.hrules = ALL
            return myTable
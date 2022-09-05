from helpers import *


# Dsource API

def dsource_list():
    resp = url_GET("/dsources?limit=50&sort=id")
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - DSOURCES LIST", report_data)
            return report_data
        else:
            print(f"\nNo DSources defined.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def dsource_search(dsource_filter):
    payload = {"filter_expression": "SEARCH '" + dsource_filter + "'"}
    resp = url_POST("/dsources/search?limit=50&sort=id", payload)
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - DSOURCE SEARCH", report_data)
            return report_data
        else:
            print(f"\nNo DSOURCE match search criteria.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def dsource_by_id(dsource_id):
    resp = url_GET("/dsources/" + urllib.parse.quote(dsource_id))
    if resp.status_code == 200:
        result = json.loads(resp.text)
        content_formatter(result)
        return result
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def dsource_snapshot_list(dsource_id):
    resp = url_GET("/dsources/" + urllib.parse.quote(dsource_id) + "/snapshots")
    if resp.status_code == 200:
        report_data = resp.json()['items']
        if report_data:
            tabular_report("DELPHIX Data Control Tower - DSOURCE SNAPSHOTS LIST", report_data)
            return report_data
        else:
            print(f"\nNo Snapshots for this DSource defined.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def dsource_tags_view(dsource_id):
    resp = url_GET("/dsources/" + urllib.parse.quote(dsource_id) + "/tags")
    if resp.status_code == 200:
        report_data = resp.json()
        if report_data:
            tabular_report("DELPHIX Data Control Tower - DSOURCE TAGS LIST", report_data)
            return report_data
        else:
            print(f"\nNo Tags for this DSource defined.")
            return
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)

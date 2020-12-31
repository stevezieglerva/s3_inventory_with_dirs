import json
import os
import boto3
import pandas as pd
from datetime import datetime
from atlassian import Jira
from collections import namedtuple
from abc import ABC, abstractmethod

IssueFields = namedtuple(
    "IssueFields",
    "project key issuetype status created resolutiondate component priority summary",
)
S3Object = namedtuple("S3Object", "bucket key date size")


class S3Base(ABC):
    @abstractmethod
    def put_object(self, bucket, key, data):
        raise NotImplementedError

    @abstractmethod
    def list_objects(self, bucket, key, prefix, total_max=0):
        raise NotImplementedError


class S3(S3Base):
    def put_object(self, bucket, key, data):
        s3 = boto3.client("s3")
        resp = s3.put_object(Bucket=bucket, Key=key, Body=data)
        print(f"key: {key} resp {resp}")
        result = S3Object(bucket=bucket, key=key)
        return result


def lambda_handler(event, context):
    s3_object = S3()
    return main(event, context, s3_object)


def main(event, context, s3_object):
    total = int(os.environ.get("TOTAL", 0))
    batch_limit = int(os.environ.get("BATCH_LIMIT", 1000))
    bucket = os.environ["S3_BUCKET"]

    jira = Jira(
        url="https://icfpsg.atlassian.net",
        username="Stephen.Ziegler@icf.com",
        password=os.environ["JIRA_API_KEY"],
    )
    jql = " ORDER BY issuekey"
    print("Calling get_jira_data_with_simple_format")
    data = get_jira_data_with_simple_format(jira, jql, total, batch_limit)
    count = len(data)
    print(f"Count: {count}")

    number_of_fields = 0
    if len(data) > 0:
        number_of_fields = len(data[0]) + 1  # add date
    csv_text = format_csv_data(data)

    pandas_data = format_pandas_data(data)
    df = pd.DataFrame(pandas_data)
    print("\n\n\n\n\n")
    print(df)
    component_json = create_component_by_priority(df)
    component_html = format_2d_backlog_as_html(component_json)
    new_csv_key = s3_object.put_object(
        bucket, f"2d_backlog/component_by_priority.html", component_html
    )

    tmsp = datetime.now().isoformat().replace(":", "")
    new_csv_key = s3_object.put_object(
        bucket, f"full_exports/jira_full_export_{tmsp}.csv", csv_text
    )

    results = {
        "options": {"total": total, "batch_limit": batch_limit},
        "issue_count": count,
        "issues": data,
        "daily_csv_s3_info": new_csv_key,
        "daily_csv_column_count": number_of_fields,
    }
    return results


def get_jira_data_with_simple_format(jira, jql, total, batch_limit):
    print("in get_jira_data")
    raw_api_results = call_jira_jql_api(jira, jql, total, batch_limit)
    simple_issues = []
    for issue in raw_api_results:
        key = issue["key"]
        issuetype = issue["fields"]["issuetype"]["name"]
        project = issue["fields"]["project"]["key"]
        status = issue["fields"]["status"]["name"]
        created = replace_none_with_empty_string(issue["fields"]["created"])
        resolutiondate = replace_none_with_empty_string(
            issue["fields"]["resolutiondate"]
        )
        component = ""
        if len(issue["fields"]["components"]) > 0:
            component = issue["fields"]["components"][0]["name"]
        summary = issue["fields"]["summary"]
        priority = issue["fields"]["priority"]["name"]
        issue_fields = IssueFields(
            key=key,
            issuetype=issuetype,
            project=project,
            status=status,
            created=created,
            resolutiondate=resolutiondate,
            component=component,
            priority=priority,
            summary=summary,
        )
        simple_issues.append(issue_fields)

    return simple_issues


def replace_none_with_empty_string(value):
    if value == None:
        return ""
    return value


def call_jira_jql_api(jira, jql, total, batch_limit):
    keep_processing = True
    start = 0
    issues = []
    while keep_processing:
        print(f"start = {start}")
        batch = jira.jql(jql, start=start, limit=batch_limit)
        # print(json.dumps(batch["issues"][0], indent=3, default=str))
        found_count = len(batch["issues"])
        print(f"found_count: {found_count}")
        start = start + found_count
        if start > total and total > 0:
            break
        issues.extend(batch["issues"])
        if found_count > 0:
            keep_processing = True
        else:
            keep_processing = False
    return issues


def format_csv_data(issues):
    date = datetime.now().strftime("%Y-%m-%d")
    csv_text = f'"date","project","key","issuetype","status","component","created","resolutiondate","priority","summary","created_flag","resolved_flag"\n'
    for issue in issues:
        created = issue.created[0:10]
        created_flag = 0
        if created != "":
            created_flag = 1

        resolutiondate = issue.resolutiondate[0:10]
        resolved_flag = 0
        if resolutiondate != "":
            resolved_flag = 1
        line = f'{date},{issue.project},{issue.key},{issue.issuetype},{issue.status},{issue.component},{created},{resolutiondate},{issue.priority},"{issue.summary}",{created_flag},{resolved_flag}'
        csv_text = csv_text + line + "\n"
    print(f"\n\ncsv_test:\n {csv_text}")
    return csv_text


def format_pandas_data(issues):
    rows = []
    for issue in issues:
        new_item = {}
        new_item["project"] = issue.project
        new_item["key"] = issue.key
        new_item["issuetype"] = issue.issuetype
        new_item["status"] = issue.status
        new_item["created"] = issue.created
        new_item["resolutiondate"] = issue.resolutiondate
        new_item["component"] = issue.component
        new_item["priority"] = issue.priority
        new_item["summary"] = issue.summary
        rows.append(new_item)
    return rows


def create_component_by_priority(df_data):
    df = pd.DataFrame(df_data)

    # get unique components
    components = df.component.unique()
    print(f"components: {components}")

    # Get unique priorities
    priorities = ["Critical", "High", "Medium", "Low"]

    # loop through each combo and get
    list = []
    for priority in priorities:
        new_priority_item = {}
        new_priority_item["priority"] = priority
        component_list = []
        for component in sorted(components):
            new_component_item = {}
            new_component_item["component"] = component
            print(f"\n\n{priority} / {component}")
            matching_issues = df[
                (df["priority"] == priority) & (df["component"] == component)
            ]
            print(matching_issues)
            matching_issues_list = matching_issues["key"]
            issues_list = []
            # new_component_item["issues"] = matching_issues_list.to_list()
            for index, row in matching_issues.iterrows():
                new_issue = {}
                new_issue["key"] = row["key"]
                new_issue["summary"] = row["summary"]
                issues_list.append(new_issue)
            new_component_item["issues"] = issues_list
            component_list.append(new_component_item)
        new_priority_item["components"] = component_list
        print(new_priority_item)
        list.append(new_priority_item)

    return list


def format_2d_backlog_as_html(input_json):
    html = "<html>\n<table rules='all' border='1'>\n"
    component_list = [c["component"] for c in input_json[0]["components"]]
    component_headers = "".join([f"<th>{c}</th>" for c in component_list])
    header_row = f"\t <tr><th>Priority</th>{component_headers}</tr>\n"
    print(header_row)
    html = html + header_row

    for priority_row in input_json:
        priority = priority_row["priority"]
        component_data = ""
        for component in priority_row["components"]:
            print(component)
            component_data = component_data + "<td>"
            issue_list = ""
            for issue in component["issues"]:
                issue_list = (
                    issue_list + "- " + issue["key"] + " " + issue["summary"] + "<br/>"
                )
            component_data = component_data + issue_list + "</td>"
            print(component_data)

        html = html + f"\t <tr><td>{priority}</td>{component_data}</tr>\n"

    html = html + "</table>\n</html>"
    return html
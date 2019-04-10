#!/usr/bin/python3

import getopt
import os
import sys
import mysql.connector

mydb = mysql.connector.connect(
  host="eng-sea-bugsdb02.west.isilon.com",
  user="readonly",
  passwd="secretpassword",
  database="bugs42"
)

mycursor = mydb.cursor()

try:
    release = os.environ['CURRENT_RELEASE']
except:
    release = None

#TODO
def usage():
    print("doh!")
    sys.exit(2)

#TODO
def help():
    pass

def error(msg, udage=False):
    print("bugs: {}".format(msg))
    if usage():
        usage()
    sys.exit(1)

def comments():
    pass

columns = {
    "id":"bug_id",
    "assignee":"assigned_to", # Must resolve to login_name in 'profiles'
    "bug_file_loc":"bug_file_loc",
    "severity":"bug_severity",
    "status":"bug_status",
    "reported":"creation_ts",
    "modified":"delta_ts",
    "title":"short_desc",
    "operating_system":"op_sys",
    "priority":"priority",
    "platform":"rep_platform",
    "reporter":"reporter", # Must resolve to login_name in 'profiles'
    "version":"version",
    "resolution":"resolution",
    "target_milestone":"target_milestone",
    "qa_contact":"qa_contact", # Must resolve to login_name in 'profiles'
    "whiteboard":"status_whiteboard",
    "votes":"votes",
    "lastdiffed":"lastdiffed",
    "everconfirmed":"everconfirmed",
    "reporter_accessible":"reporter_accessible",
    "cclist_accessible":"cclist_accessible",
    "estimated_time":"estimated_time",
    "remaining_time":"remaining_time",
    "deadline":"deadline",
    "alias":"alias",
    "product":"product_id", # Must resolve to name in 'products'
    "component":"component_id", # Must resolve to name in 'components'
    "cf_project_milestone":"cf_project_milestone",
    "cf_project_milestone_orig":"cf_project_milestone_orig",
    "project_milestone":"project_milestone",
    "cf_sched_val_dev":"cf_sched_val_dev",
    "cf_sched_val_qa":"cf_sched_val_qa",
    "cf_sched_val_support":"cf_sched_val_support",
    "cf_sched_val_mkt":"cf_sched_val_mkt",
    "cf_sched_val_mfg":"cf_sched_val_mfg",
    "cf_sched_time_dev_est":"cf_sched_time_dev_est",
    "cf_sched_time_qa_est":"cf_sched_time_qa_est",
    "entry_type":"cf_bug_type",
    "found_in_build":"cf_build_found_in",
    "fixed_after_build":"cf_build_fixed_in",
    "cf_associated_test":"cf_associated_test",
    "cf_salesforce_case_id":"cf_salesforce_case_id",
    "release_note":"cf_release_note",
    "risk":"cf_code_change_risk",
    "cf_customer_impact":"cf_customer_impact",
    "release_note_status":"cf_release_note_status",
    "cf_esc_summary_correct":"cf_esc_summary_correct",
    "cf_esc_log_link":"cf_esc_log_link",
    "cf_esc_customer_impact_set":"cf_esc_customer_impact_set",
    "cf_esc_product_bug":"cf_esc_product_bug",
    "cf_esc_succinct_summary":"cf_esc_succinct_summary",
    "cf_esc_problem_description":"cf_esc_problem_description",
    "cf_esc_customer_impact_described":"cf_esc_customer_impact_described",
    "cf_esc_under_duress":"cf_esc_under_duress",
    "cf_rally_id":"cf_rally_id",
    "cf_lab_location":"cf_lab_location",
    "cf_sbr":"cf_sbr",
    "cf_next_action":"cf_next_action",
    "cf_build_introduced2":"cf_build_introduced2",
    "campaign":"cf_campaign",
    "cf_subproject":"cf_subproject",
    "cf_frequency":"cf_frequency",
    "cf_opt_related":"cf_opt_related",
    "cf_infodev_function":"cf_infodev_function",
    "limit":None,
    "comments":comments,
    "help":help
}

def build_query(filters):
    query = []
    limit = None
    not_tbv = True
    pieces = []
    cols = []

    for opt, arg in filters:
        if opt == 'help':
            help()
            sys.exit(0)
        if opt == "limit":
            limit = arg
            continue
        if arg:
            pieces.append("{}='{}'".format(columns[opt],arg))
        else:
            error("specific column queries not supported.")

    query.append("SELECT * FROM bugs")

    if len(pieces) > 0:
        query.append('WHERE')
        query.append(' and '.join(pieces))

    if limit:
        query.append("LIMIT {}".format(limit))
    if len(filters) > 0:
        return ' '.join(query)
    else:
        error("No arguments given.")

fields = []
for y in columns.keys():
    fields.append(y)

#cols,_ = os.get_terminal_size()

def tuple_to_dict(l):
    d = {}
    i = 0
    for item in l:
        if fields[i] == "assigned_to" or fields[i] == "reporter" or fields[i] == "qa_contact":
            mycursor.execute("SELECT login_name FROM profiles WHERE userid='{}'".format(item))
            result = mycursor.fetchall()
            d[fields[i]] = result[0]
        elif fields[i] == "product_id":
            mycursor.execute("SELECT name FROM products WHERE product_id='{}'".format(item))
            result = mycursor.fetchall()
            d[fields[i]] = result[0]
        elif fields[i] == "component_id":
            mycursor.execute("SELECT name FROM components WHERE component_id='{}'".format(item))
            result = mycursor.fetchall()
            d[fields[i]] = result[0]
        else:
            d[columns[fields[i]]] = item
        i = i + 1
    mycursor.execute("SELECT comments FROM bugs_fulltext WHERE bug_id='{}'".format(d['bug_id']))
    result = mycursor.fetchall()
    d["comments"] = result[0]
    return d

def get_bugs(filters):
    query = build_query(filters)

    mycursor.execute(query)
    result = mycursor.fetchall()
    
    l = []

    for x in result:
        l.append(tuple_to_dict(x))

    return l

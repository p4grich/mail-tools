#!/usr/bin/env python
import argparse
import json
import os
import sendgrid
from python_http_client import exceptions

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--delete", type=str, help="delete email from sendgrid")
parser.add_argument("-e", "--email", type=str, help="email address")
parser.add_argument("-l", "--list", action="store_true", help="list all by category")
parser.add_argument("-v", "--verbose", action="store_true", help="make more verbose")
args = parser.parse_args()

if "SENDGRID_API_KEY" in os.environ:
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
else:
    print("source your API Key from .env first")
    exit(1)

if args.list:
    try:
        #params = {'start_time': 1, 'limit': 100, 'end_time': 1, 'offset': 0}
        params = {}
        response = sg.client.suppression.invalid_emails.get(query_params=params)
        if args.verbose:
            print(response.status_code)
            print(response.body)
            print(response.headers)
        parsed = json.loads(response.body)
        if parsed:
            print("--- list all invalid emails ---")
            print(json.dumps(parsed, indent=2, sort_keys=True))
            print("--- list all invalid emails ---")
        else:
            print("--- no invalid emails ---")

    except exceptions.BadRequestsError as e:
        print(e.body)
        exit()

if args.email:
    email = args.email

    try:
        response = sg.client.suppression.blocks._(email).get()
        if args.verbose:
            print(response.status_code)
            print(response.body)
            print(response.headers)
        parsed = json.loads(response.body)
        if parsed:
            print("--- blocks ---")
            print(json.dumps(parsed, indent=2, sort_keys=True))
            print("--- blocks ---")
        else:
            print("--- no blocks ---")

        response = sg.client.suppression.bounces._(email).get()
        if args.verbose:
            print(response.status_code)
            print(response.body)
            print(response.headers)
        parsed = json.loads(response.body)
        if parsed:
            print("--- bounces ---")
            print(json.dumps(parsed, indent=2, sort_keys=True))
            print("--- bounces ---")
        else:
            print("--- no bounces ---")

        response = sg.client.suppression.invalid_emails._(email).get()
        if args.verbose:
            print(response.status_code)
            print(response.body)
            print(response.headers)
        parsed = json.loads(response.body)
        if parsed:
           print("--- invalid emails ---")
           print(json.dumps(parsed, indent=2, sort_keys=True))
           print("--- invalid emails ---")
        else:
           print("--- no invalid emails ---")

        response = sg.client.suppression.spam_reports._(email).get()
        if args.verbose:
            print(response.status_code)
            print(response.body)
            print(response.headers)
        parsed = json.loads(response.body)
        if parsed:
            print("--- Enduser flagged your email as spam ---")
            print(json.dumps(parsed, indent=2, sort_keys=True))
            print("--- Enduser flagged your email as spam  ---")
        else:
            print("--- no spam reports ---")

    except exceptions.BadRequestsError as e:
        print(e.body)
        exit()

if args.delete:
    email = args.delete

    try:
        response = sg.client.suppression.blocks._(email).delete()
        print("deleted blocks for:", email)
        if args.verbose:
            print(response.status_code)
            print(response.body)
            print(response.headers)
    except exceptions.NotFoundError as e:
        print("delete_blocks:", e.body)

    try:
        response = sg.client.suppression.invalid_emails._(email).delete()
        print("deleted invalid email:", email)
        if args.verbose:
            print(response.status_code)
            print(response.body)
            print(response.headers)
    except exceptions.NotFoundError as e:
        print("delete_invalid_emails:", e.body)

    try:
        params = {'email_address': email}
        response = sg.client.suppression.bounces._(email).delete(query_params=params)
        print("delete bounces for:", email)
        if args.verbose:
            print(response.status_code)
            print(response.body)
            print(response.headers)
    except exceptions.NotFoundError as e:
        print("delete_bounces:", e.body)

    try:
        response = sg.client.suppression.spam_reports._(email).delete()
        print("delete spam report for:", email)
        if args.verbose:
            print(response.status_code)
            print(response.body)
            print(response.headers)
    except exceptions.NotFoundError as e:
        print("delete_spam_report:", e.body)

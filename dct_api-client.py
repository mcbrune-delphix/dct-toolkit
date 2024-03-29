#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright (c) 2022 by Delphix. All rights reserved.
#
# Author  : Matteo Ferrari, Ruben Catarrunas
# Date    : September 2022

import argparse
from helpers import *


# Api-client functions
def api_client_create(base_url, api_client_id, name):
    payload = {"generate_api_key": 'true', "api_client_id": api_client_id, "name": name}
    resp = url_POST(base_url, payload)
    if resp.status_code == 201:
        rsp = resp.json()
        print(f"Registered API-client with ID={rsp['api_client_entity_id']}")
        return rsp
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


def api_client_update(base_url, id, api_client_id, name):
    payload = {"api_client_id": api_client_id, "name": name}
    resp = url_PUT(base_url + "/" + id, payload)
    if resp.status_code == 200:
        rsp = resp.json()
        print(f"Updated API-client with ID={rsp['id']}")
        return rsp
    else:
        print(f"ERROR: Status = {resp.status_code} - {resp.text}")
        sys.exit(1)


# Init
parser = argparse.ArgumentParser(description="Delphix DCT API-client operations")
subparser = parser.add_subparsers(dest='command')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument('--config', type=str, required=False, help="Config file")

# define commands
lst = subparser.add_parser('list')
create = subparser.add_parser('create')
delete = subparser.add_parser('delete')
view = subparser.add_parser('view')
updt = subparser.add_parser('update')

# define create parms
create.add_argument('--name', type=str, required=True, help="Client name of the new API-client")
create.add_argument('--api_client_id', type=str, required=True, help="API client ID of the new API-client")

# define update parms
updt.add_argument('--id', type=str, required=True, help="Client_id name of the new API-client")
updt.add_argument('--name', type=str, required=True, help="Client name of the new API-client")
updt.add_argument('--api_client_id', type=str, required=True, help="API client ID of the new API-client")

# define delete parms
delete.add_argument('--id', type=str, required=True, help="API-client ID to be deleted")

# define view parms
view.add_argument('--id', type=str, required=True, help="API-client ID to be viewed")

# define list parms
lst.add_argument('--format', type=str, required=False, help="Type of output", choices=['json', 'report'])

# force help if no parms
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

# Start processing
dct_read_config(args.config)

dct_base_url = "/management/api-clients"

if args.command == 'view':
    rs = dct_view_by_id(dct_base_url, args.id)
    print(rs)

if args.command == 'list':
    rs = dct_search("API-clients List", dct_base_url, None, "No API-clients defined.", args.format)
    print(rs)

if args.command == 'create':
    print("Processing API-clients create")
    rs = api_client_create(dct_base_url, args.api_client_id, args.name)
    print(rs)

if args.command == 'update':
    print("Processing API-client update")
    rs = api_client_update(dct_base_url, args.id, args.api_client_id, args.name)
    print(rs)

if args.command == 'delete':
    print("Processing API-client delete ID=" + args.id)
    rs = dct_delete_by_id(dct_base_url, "Deleted API-client", args.id)

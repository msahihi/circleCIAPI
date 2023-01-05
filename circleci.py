

import pandas as pd
import requests
import json

allContext = []
allEnv = []
CIRCLE_TOKEN = "TOKEN"
ORG_ID = "ORGID"


def getAllContext():
    global allContext
    NEXT_PAGE_TOKEN = "NEXT_PAGE_TOKEN"
    while NEXT_PAGE_TOKEN is not None:
        headers = {'Circle-Token': CIRCLE_TOKEN}
        r = requests.get(
            'https://circleci.com/api/v2/context?owner-id='+ORG_ID+'&page-token='+NEXT_PAGE_TOKEN,
             headers=headers)
        res = r.json()
        NEXT_PAGE_TOKEN = res['next_page_token']
        allContext = allContext + res['items']


def getAllEnv(contextId):
    global allEnv
    NEXT_PAGE_TOKEN = "NEXT_PAGE_TOKEN"
    while NEXT_PAGE_TOKEN is not None:
        headers = {'Circle-Token': CIRCLE_TOKEN}
        r = requests.get('https://circleci.com/api/v2/context/'+contextId+
                         '/environment-variable?page-token='+NEXT_PAGE_TOKEN, headers=headers)
        if r.status_code == 200:
          res = r.json()
          NEXT_PAGE_TOKEN = res['next_page_token']
          allEnv = allEnv + res['items']
        else:
          print("{}{}".format("error:", r.status_code))
          break

getAllContext()
for context in allContext:
    print("Getting information from " + context['name'])
    getAllEnv(context['id'])

for envs in allEnv:
  for context in allContext:
    if envs['context_id'] == context['id']:
      envs['context_name']=context['name']

json_object = json.dumps(allEnv, indent=4)
with open("allenvs.json", "w") as outfile:
    outfile.write(json_object)


input_json_file = 'allenvs.json'
output_csv_file = 'csv_file.csv'
with open(input_json_file) as inputfile:
    df = pd.read_json(inputfile)

df.to_csv(output_csv_file, index=False)

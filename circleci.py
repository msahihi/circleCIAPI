

from os import environ as env
from dotenv import load_dotenv
import pandas as pd
import requests
import json

allContext = []
allEnv = []
load_dotenv()
JSON_OUTPUT_FILE = "output.json"
CSV_OUTPUT_FILE = "output.csv"
CIRCLE_TOKEN = env['CIRCLE_TOKEN']
ORG_ID = env['ORG_ID']

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


def getEnvs(contextId):
    global allEnv
    NEXT_PAGE_TOKEN = "NEXT_PAGE_TOKEN"
    while NEXT_PAGE_TOKEN is not None:
        headers = {'Circle-Token': CIRCLE_TOKEN}
        r = requests.get('https://circleci.com/api/v2/context/'+contextId +
                         '/environment-variable?page-token='+NEXT_PAGE_TOKEN, headers=headers)
        if r.status_code == 200:
            res = r.json()
            NEXT_PAGE_TOKEN = res['next_page_token']
            allEnv = allEnv + res['items']
        else:
            print("{}{}".format("error:", r.status_code))
            break


def getAllEnvs(contexts):
    for context in contexts:
        print("Reading all variables from {} context".format(context['name']))
        getEnvs(context['id'])


def updateEnvsWithContextName(envs, contexts):
    for env in envs:
        for context in contexts:
            if env['context_id'] == context['id']:
                env['context_name'] = context['name']


def toJsonFile(jsonData, outputFile=JSON_OUTPUT_FILE):
    json_object = json.dumps(jsonData, indent=4)
    with open(outputFile, "w") as outfile:
        outfile.write(json_object)


def toCSVFileFromJsonFile(inputFile=JSON_OUTPUT_FILE, outputFile=CSV_OUTPUT_FILE):
    with open(inputFile) as inputfile:
        df = pd.read_json(inputfile)
    df.to_csv(outputFile, index=False)


getAllContext()
getAllEnvs(allContext)
updateEnvsWithContextName(allEnv, allContext)
toJsonFile(allEnv)
toCSVFileFromJsonFile(JSON_OUTPUT_FILE)

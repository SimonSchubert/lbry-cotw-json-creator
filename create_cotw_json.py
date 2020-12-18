import requests
import json

# This script takes a text file(channels.txt) with a list of channel. Each line represents 1 channel
# and each line can be comma seperated. The first entry must be the claim id of the channel. Everything behind 
# the comma will be ignored and is used for documentation reasons.
# Author: Simon Schubert

print("#####################")
print("# COTW JSON CREATOR #")
print("#####################")
print()

try:
    channelsFile = open("channels.txt", "r")
except:
    print("Error: channels.txt not found")
    print("Copy channels.txt into same directory as the python script and run the script again.")
    exit()

channels = []

week = 1
for line in channelsFile.readlines():
    claimId = line.split(",")[0]
    print("Fetch info for COTW " + str(week) + ": " + claimId)
    try:
        response = requests.post("http://localhost:5279", json={"method": "claim_search", "params": {"claim_id": claimId.strip()}}).json()
    except:
        print("Error: connection to http://localhost:5279")
        print("Is LBRY running? https://lbry.tech/api/sdk")
        exit()

    for item in response["result"]["items"]:
        name = item.get("name", "")[1:]
        title = item["value"].get("title", "")
        if(title == ""):
            title = name
        thumbnailUrl = item["value"]["thumbnail"]["url"]
        tags = item["value"].get("tags", [])
        channel = {'week': week, 'name':name, 'claimId':claimId, 'title':title, 'thumbnailUrl':thumbnailUrl, 'tags':tags}
        channels.append(channel)

    week = week+1

channelsFile.close()

print("Export all.json")

f = open("all.json", "w")
f.write(json.dumps(channels))
f.close()

print("Export current.json")

f = open("current.json", "w")
f.write(json.dumps(channels[-1]))
f.close()

print()
print("Job done :)")
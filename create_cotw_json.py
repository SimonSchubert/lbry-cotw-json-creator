import requests
import json

# This script takes a text file(channels.txt) with a list of channel. Each line represents 1 channel
# and each line can be comma separated. The first entry must be the claim id of the channel. Everything behind
# the comma will be ignored and is used for documentation reasons.
# Author: Simon Schubert


print("#####################")
print("# COTW JSON CREATOR #")
print("#####################")
print()


def get_info_by_claim_id(claim_id, week):
    try:
        response = requests.post("http://localhost:5279",
                                 json={"method": "claim_search", "params": {"claim_id": claim_id.strip()}}).json()

        for item in response["result"]["items"]:
                name = item.get("name", "")[1:]
                title = item["value"].get("title", "")
                if title == "":
                    title = name
                thumbnail_url = item["value"]["thumbnail"]["url"]
                tags = item["value"].get("tags", [])
                return {'week': week, 'name': name, 'claimId': claimId, 'title': title, 'thumbnailUrl': thumbnail_url,
                        'tags': tags}
    except:
        print("Error: connection to http://localhost:5279")
        print("Is LBRY running? https://lbry.tech/api/sdk")
        exit()


with open('channels.txt') as channels_file:
    channels = []

    for week, line in enumerate(channels_file.readlines()):
        claimId = line.split(",")[0]
        if claimId != "":
            print("Fetch info for COTW " + str(week+1) + ": " + claimId)
            info = get_info_by_claim_id(claimId, (week+1))
            if info is not None:
                channels.append(info)

    print("Export all.json")
    with open('all.json', 'w') as f:
        f.write(json.dumps(channels))

    print("Export current.json")
    with open('current.json', 'w') as f:
        f.write(json.dumps(channels[-1]))


with open('nominations.txt') as nominations_file:
    channels = []

    for week, line in enumerate(nominations_file.readlines()):
        claimId = line.split(",")[0]
        print("Fetch info for nomination: " + claimId)
        info = get_info_by_claim_id(claimId, (week+1))
        if info is not None:
            channels.append(info)

    print("Export nominations.json")
    with open('nominations.json', 'w') as f:
        f.write(json.dumps(channels))


print()
print("Job done :)")
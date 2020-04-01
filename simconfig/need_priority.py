from model import person


def getNeedPrio(thePerson):
    sleep = [k for k in thePerson.needs.needs.keys() if k.getName() == "SLEEP"][0]
    sortedNeeds = sorted([k for k in thePerson.needs.needs.keys()], key=lambda k: thePerson.needs.needs[k], reverse=True)
    sortedNeeds.append(sleep)
    return sortedNeeds

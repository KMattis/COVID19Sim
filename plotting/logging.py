
_categories = []

def registerCategory(category):
    #Clear the log file
    with open("logfiles/" + category + ".log", "w") as _:
        pass
    _categories.append(category)

def write(category, *values):
    if category not in _categories:
        raise Exception("Unknown category: '" + category + "'")
    with open("logfiles/" + category + ".log", "a") as f:
        for v in values:
            f.write(str(v))
            f.write(",")
        f.write("\n")

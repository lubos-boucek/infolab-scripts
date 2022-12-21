#!/usr/bin/env python3
import csv
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from calendar import monthrange

# Replace with the current file name
SOURCE_FILE_NAME = "Infolab_2011-2020_1032.csv"
# SAVE_DIR_NAME = ""
DAYS_BEFORE = 3
DAYS_AFTER = 3
# Lower limit
YEAR = 2020

def parseRow(row, keys):
    r = {}

    for index, key in enumerate(keys):
        r[key] = row[index]

    return r

def readFile(fileName = SOURCE_FILE_NAME):
    rows = []
    with open(fileName, newline = '') as csv_file:
        reader = csv.reader(csv_file, delimiter = ',')
        keys = next(reader)
        for row in reader:
            rows.append(parseRow(row, keys))
    return rows

# TODO: Merge makeConjunction and makeDisjunction
def makeDisjunction(conditions):
    result = "("
    first = True
    for condition in conditions:
        if not first:
            result += " OR "
        result += condition
        first = False
    return result + ")"

def makeConjunction(conditions):
    result = "("
    first = True
    for condition in conditions:
        if not first:
            result += " AND "
        result += condition
        first = False
    return result + ")"

def join(key, sign, value):
    return "(" + key + " " + sign + " " + str(value) + ")"

def makeCondition(sample, key, sign, quoted = False):
    value = sample[key]
    if quoted:
        value = "'" + value + "'"
    return join(key, sign, value)

def processDate(date0):
    conditions = []
    date_before = date0 - relativedelta(days = DAYS_BEFORE)
    date_after = date0 + relativedelta(days = DAYS_AFTER)
    start_day = -1
    end_day = -1
    if date_before.month != date0.month:
        conditions.append(makeConjunction([
            join("ROK", "=", date_before.year),
            join("MESIC", "=", date_before.month),
            join("DEN", ">=", date_before.day)]))
        # start_day = 1
    else:
        start_day = date_before.day
    if date_after.month != date0.month:
        conditions.append(makeConjunction([
            join("ROK", "=", date_after.year),
            join("MESIC", "=", date_after.month),
            join("DEN", "<=", date_after.day)]))
        # end_day = monthrange(date0.year, date0.month)[1]
    else:
        end_day = date_after.day
    current = []
    if start_day != -1:
        current.append(makeConjunction([
            join("ROK", "=", date0.year),
            join("MESIC", "=", date0.month),
            join("DEN", ">=", start_day)]))
    if end_day != -1:
        current.append(makeConjunction([
            join("ROK", "=", date0.year),
            join("MESIC", "=", date0.month),
            join("DEN", "<=", end_day)]))
    conditions.append(makeConjunction(current))
    return makeDisjunction(conditions)

def processSample(sample):
    condition = ""

    # rc_cond = makeCondition(sample, "RC", "=", quoted = True)
    date0 = date(int(sample["ROK"]), int(sample["MESIC"]), int(sample["DEN"]))
    date_cond = processDate(date0)

    # return makeConjunction([rc_cond, date_cond])
    return date_cond

def main():
    samples = readFile()
    patientConditions = []
    
    # TODO: Unhardcode year limit
    for sample in [s for s in samples if int(s["ROK"]) >= YEAR]:
    # for sample in samples:
        patientConditions.append(processSample(sample))
    pass
    condition = makeDisjunction(patientConditions)
    # TODO: Unhardcode department condition
    condition = makeConjunction([
        join("ODDELENI", "=", "1032"),
        condition])
    
    print(condition)

    # file_name = SAVE_DIR_NAME + "query-" + str(YEAR) + "-b" + str(DAYS_BEFORE) + "-a" + str(DAYS_AFTER) + ".txt"
    
    # file_name = SAVE_DIR_NAME + "query" + "-b" + str(DAYS_BEFORE) + "-a" + str(DAYS_AFTER) + ".txt"
    # with open(file_name, "w") as writer:
    #     writer.write(condition)

if __name__ == "__main__":
    main()
    
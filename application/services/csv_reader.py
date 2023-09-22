import csv

import requests


def read_csv(url):
    response = requests.get(url)
    content = response.text.splitlines()

    reader = csv.DictReader(content)

    return reader


def calculate_average_height_weight(reader):
    total_height = 0
    total_weight = 0
    count = 0

    for row in reader:
        height_cm = float(row["Height(Inches)"]) * 2.54
        weight_kg = float(row["Weight(Pounds)"]) * 0.45359237
        total_height += height_cm
        total_weight += weight_kg
        count += 1

    average_weight = total_weight / count
    average_height = total_height / count
    return f"Average height = {average_height}, Average weight = {average_weight}"

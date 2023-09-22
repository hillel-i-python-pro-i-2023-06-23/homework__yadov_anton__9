import requests


def getting_request(url) -> dict:
    return requests.get(url).json()


def output_json(data: dict) -> str:
    json_file = data
    number = json_file["number"]
    return f"Numbers of cosmonauts for now is: {number}"

#!/usr/bin/env python3

import json
import sys
import requests
import yaml
import pandas as pd


def main():
    if len(sys.argv) != 4:
        print(
            f"Usage: {sys.argv[0]} <endpoint_base_url> <data_url> <data_keywords_yaml>")
        return

    endpoint = sys.argv[1] + "/keyword/match/summary"
    data_url = sys.argv[2]
    data_keywords_yaml = sys.argv[3]

    with open(data_keywords_yaml, "r", encoding="utf-8") as yaml_file:
        yaml_content = yaml.safe_load(yaml_file)

    request_data = {
        "url": data_url,
        "keywords": json.dumps(yaml_content["keywords"]),
        "threshold": "90",
    }

    request_data_json = json.dumps(request_data)

    headers = {
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            endpoint, headers=headers, data=request_data_json, timeout=10)
        response.raise_for_status()
        response_data = response.json()

        if response_data:
            df = pd.DataFrame(response_data)
            column_order = ["keyword", "count", "min", "max", "average"]
            df_reordered = df[column_order]
            print(df_reordered)

    except requests.exceptions.RequestException as error:
        print(f"Request error: {error}")
        response_data = response.json()

        if response_data:
            print(json.dumps(response_data, indent=4))

    except json.JSONDecodeError as error:
        print(f"JSON decoding error: {error}")

    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    main()

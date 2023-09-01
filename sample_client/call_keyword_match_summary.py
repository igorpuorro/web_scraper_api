#!/usr/bin/env python3

import json
import sys
import requests
import yaml
import pandas as pd


def main():
    if len(sys.argv) != 4:
        print(
            f"Usage: {sys.argv[0]} <endpoint_base_url> <param_url> <param_keywords_yaml>")
        return

    endpoint = sys.argv[1] + "/keyword/match/summary"
    param_url = sys.argv[2]
    param_keywords_yaml = sys.argv[3]

    with open(param_keywords_yaml, "r", encoding="utf-8") as yaml_file:
        yaml_content = yaml.safe_load(yaml_file)

    request_data = {
        "url": param_url,
        "keywords": json.dumps(yaml_content),
    }

    response = requests.post(endpoint, params=request_data, timeout=10)

    if response.status_code == 200:
        response_data = response.json()

        if response_data:
            df = pd.DataFrame(response.json())
            column_order = ["keyword", "count", "min", "max", "average"]
            df_reordered = df[column_order]
            print(df_reordered)
    else:
        print("Error:", response.status_code)


if __name__ == "__main__":
    main()

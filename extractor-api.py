import json
import re
import requests
import pandas as pd


# TODO: Asynchronously download the json data for each roll number
def get_json(rollno):
    form_body = {
        "rollno": rollno,
        "course": "PG",
        "semester": "1",
        "stream": "M.C.A.",
    }
    base_url = "https://www.exam.ranchiuniversity.co.in/results"
    print(f"[FETCHING] {rollno=}")
    req = requests.post(base_url, data=form_body)
    if req.status_code == 200:
        print(f"[FETCHED] {rollno=}")
        return extract_marks_save(req.text, f'results_json/{rollno}.json')
    return None


def extract_marks_save(html, filename="results.json"):
    pattern = r'var\s+myObject\s*=\s*(\{[\s\S]*?\});'
    search = re.search(pattern, html, re.MULTILINE)
    if search.group(1) is None:
        return
    data = search.group(1)
    json_data = json.loads(data)
    return json_data


def get_all_marks_json():
    results = []
    # downloading the json data for each roll number
    with open("roll_numbers.txt", "r") as f:
        roll_numbers = f.read().splitlines()
        for rollno in roll_numbers:
            r = get_json(rollno)
            if r is not None:
                results.append(r)
    json.dump(results, open("results.json", "w"))


def generate_excel():
    df = pd.read_json("results.json")
    # Delete all columns where value is NaN or null
    df = df.dropna(axis=1, how="all")
    # Delete all the rows where rollno is null
    df = df[~df["rollno"].isna()]
    # setting rollno as index
    df.set_index("rollno", inplace=True)
    df.to_excel("results.xlsx")


def main():
    get_all_marks_json()
    generate_excel()


if __name__ == "__main__":
    main()

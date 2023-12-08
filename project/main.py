from template import prompt_template
import os
import glob
import json
import pandas as pd
from openai import OpenAI
import os

os.environ["OPENAI_API_KEY"] = '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'

client = OpenAI()


def collect_data():
    text_file_pattern = "*.txt"  # You can adjust the pattern to match your file extensions
    text_files = glob.glob(os.path.join("../nhs/content", text_file_pattern))
    data = {}
    for file_path in text_files:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_name = os.path.basename(file_path)
            file_content = file.read()
            data[file_name] = file_content
    return data


def get_qna_from_data(text, count=20):
    current_count = 0
    global df
    df = pd.DataFrame()
    while current_count < count:
        print("1")
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"{prompt_template}"},
                {"role": "user", "content": text}
            ]
        )
        resp = completion.choices[0].message.content
        print("response ", resp[:10])
        df1 = pd.DataFrame(eval(resp))
        df = pd.concat([df, df1])
        current_count += len(df1)
    return df


if __name__ == '__main__':
    corpus = collect_data()
    name = "Shortsightedness myopia  NHS.txt"
    df = get_qna_from_data(corpus[name], 6)
    df.to_csv(f"./{name}")



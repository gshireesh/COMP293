import glob
import os
import re
import time
from multiprocessing import Pool, Semaphore

import pandas as pd
from openai import OpenAI
from rich import pretty

pretty.install()
from utils import collect_data

os.environ["OPENAI_API_KEY"] = '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'

client = OpenAI()

prompt_template = """
You are asked to come up with a set of 10 diverse task instructions. These task instructions will be given to a GPT model and we will evaluate the GPT model for completing the instructions.

Here are the requirements:
1. Try not to repeat the verb for each instruction to maximize diversity.
2. The language used for the instruction also should be diverse. For example, you should combine questions with imperative instrucitons.
3. The type of instructions should be diverse. The list should include diverse types of tasks like open-ended generation, classification, editing, etc.
2. A GPT language model should be able to complete the instruction. For example, do not ask the assistant to create any visual or audio output. For another example, do not ask the assistant to wake you up at 5pm or set a reminder because it cannot perform any action.
3. The instructions should be in English.
4. The instructions should be 1 to 2 sentences long. Either an imperative sentence or a question is permitted.
5. You should generate an appropriate input to the instruction. The input field should contain a specific example provided for the instruction. It should involve realistic data and should not contain simple placeholders. The input should provide substantial content to make the instruction challenging but should ideally not exceed 100 words.
6. Not all instructions require input. For example, when a instruction asks about some general information, "what is the highest peak in the world", it is not necssary to provide a specific context. In this case, we simply put "<noinput>" in the input field.
7. The output should be an appropriate response to the instruction and the input. Make sure the output is less than 100 words.
8. Do not deviate to other topics. keep it related to medical information and questions and answers from a patient or information seeker.
9. the input data is from NHS. remove all the data related to NHS from generation.
10. give the output as a json. following is the example.
    ""----
        [
            {
                "q" : "question1",
                "i" : "some input1",
                "a" : "answer2"
            },
            {
                "q" : "question2",
                "i" : "some input2",
                "a" : "answer2"
            },
        ]
    ""----
11. run a test of python json.loads on the output to make sure its json
"""


def collect_error(text):
    with open(f"errors/error{time.time_ns()}.txt", 'w', encoding='utf-8') as file:
        file.write(text)


def remove_links(text):
    # Define a regular expression pattern to match URLs
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

    # Use re.sub to replace URLs with an empty string
    cleaned_text = re.sub(url_pattern, '', text)

    return cleaned_text

def get_qna_from_data(text, count=20):
    current_count = 0
    results = []
    text = remove_links(text)
    text = text[:10000]
    while current_count < count:
        try:
            print("made open api query")
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"{prompt_template}"},
                    {"role": "user", "content": text}
                ]
            )
            resp = completion.choices[0].message.content
            print("got resp open api query")

            if not resp.startswith("["):
                collect_error(resp)
                continue
            data = eval(resp)
            df1 = pd.DataFrame(data)
            current_count += len(df1)
            print(f"resp for {current_count} / {count}")
            results.append(df1)
        except Exception as e:
            print("error")
            collect_error(resp)
            # print(resp)
            # print(e)

    df = pd.concat(results)
    return df


class QnaGenerator:
    skipExisting = True
    corpus = None
    semaphore = Semaphore()

    def __init__(self):
        self.corpus = collect_data()
        self.keys = list(self.corpus.keys())
        self.keys_index = {v: i for i, v in enumerate(self.keys)}

    def generate_for_file(self, name):
        count = self.keys_index[name]

        path = f"./qna/{name}.csv"
        qna_exists = len(glob.glob(path)) != 0
        if qna_exists and self.skipExisting:
            # print(f"skipped for {count}: {name}")
            return 1
        df_old = None
        if qna_exists:
            df_old = pd.read_csv(path)
        required_count = 20 - (len(df_old) if df_old is not None else 0)
        if required_count <= 0:
            # print(f"skipped for {len(df_old)}: {name}")
            return 1
        print(f"started for {count}: {name}")
        df = get_qna_from_data(self.corpus[name], required_count)
        df = pd.concat([df_old, df])
        df.to_csv(path)
        print(f"completed for {count}: {name}")
        return 1

    def run(self):
        try:
            p = Pool(processes=10)
            p.map(self.generate_for_file, self.keys)
            p.close()
            p.join()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    qna = QnaGenerator()
    qna.run()

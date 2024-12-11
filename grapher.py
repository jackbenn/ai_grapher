import os
import io
import argparse
import logging

from dotenv import load_dotenv

load_dotenv()

import pandas as pd
import openai


class Grapher:

    prompt_check = """I have a pandas DataFrame called `df`.
    The results of `df.info()` are ```{}```.
    Could the following question be used to generate some sort of graph or chart from the data in the DataFrame? Answer 'yes' or 'no' only, with no other response.
    Question: '''{}'''"""

    prompt_code = """I have a pandas DataFrame called `df`.
    The results of `df.info()` are ```{}```.
    Produce python code based on the following Question to produce a graph with the matplotlib library.
    While writing the code, make sure the columns you use match those in the DataFrame.
    Respond with python code and nothing else; do not wrap it in quotes or backtics.
    The python code should not affect the computer in any other way, including reading, writing, modifying, or deleting files.
    Question: '''{}'''"""

    prompt_fix = """I have a pandas DataFrame called `df`.
    The results of `df.info()` are ```{}```.
    Produce python code based on the following Question to produce a graph with the matplotlib library.
    While writing the code, make sure the columns you use match those in the DataFrame.
    Respond with python code and nothing else; do not wrap it in quotes or backtics.
    The python code should not affect the computer in any other way, including reading, writing, modifying, or deleting files.
    Your Previous Answer gave me the Error below; try to avoid that next time.
    Question: '''{}'''
    Previous Answer ```{}```
    Error ```{}```
    """

    def __init__(self, filename):
        self.df = pd.read_csv(filename)
        buffer = io.StringIO()
        self.df.info(buf=buffer)

        self.info = buffer.getvalue()

        logging.info("info() from dataframe")
        logging.info(self.info)
        self.max_error_count = 3

        if "OPENAI_API_KEY" in os.environ:
            api_key = os.environ["OPENAI_API_KEY"]
        else:
            logging.error("Environment variable `OPEN_API_KEY` must be set")
            exit()

        self.client = openai.OpenAI(api_key=api_key)
        self.questions = []

    def call(self, prompt):
        response = self.client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt},
            ],
            model="gpt-4o-mini",
        )
        return response.choices[0].message.content

    def check_graphability(self, question):
        prompt = self.prompt_check.format(self.info, question)

        content = self.call(prompt)
        if content.lower() == "yes":
            return True
        else:
            return False

    def generate_graph_code(self, question):
        prompt = self.prompt_code.format(self.info, question)
        code = self.call(prompt)

        return code

    def execute(self, question):
        self.questions.append(question)

        question = "\n".join(self.questions)
        if self.check_graphability(question):
            code = grapher.generate_graph_code(question)

            # This is (should be) used in exec of genai-generated code
            df = grapher.df.copy()

            for _ in range(self.max_error_count):
                logging.info(code)
                try:
                    exec(code)
                    break
                except Exception as e:
                    logging.info("Initial code failed with error {e}; trying again")
                    prompt = self.prompt_code.format(
                        self.info,
                        question,
                        code,
                        e,
                    )
                    code = self.call(prompt)
                    logging.info(code)

            else:  # NB: for/else clause
                print("I'm having trouble turning that into code.")

        else:
            print("I can't make a graph out of that.")

    def main(self):
        while True:
            question = input("What can I graph for you?  ")
            if not question.strip() or question.lower() in ("q", "quit", "x", "exit"):
                logging.info(f"Questions so far:\n {"\n".join(grapher.questions)}")
                break
            self.execute(question)

        print("Thanks for graphing stuff with me!")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="grapher",
        description="grapher is a program to use GenAI to make graphs from data",
        epilog="""
grapher is a program to use GenAI to make graphs from data

Usage:
  python grapher.py <filename.csv>
<filename.csv> must be a csv file; the first row is expected to contain feature names.

WARNING: This contains no guardrails and will run GenAI-created code directly on your
system. Running it outside of a container may have dire consequences, including data loss,
particularly if you ask it do delete things.
                    """,
    )
    parser.add_argument(
        "filename",
        type=str,
        help="The csv file to graph; the first row is expected to contain feature names.",
    )

    parser.add_argument("-v", "--verbose", action="store_true", help="Print ")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

    grapher = Grapher(args.filename)
    grapher.main()

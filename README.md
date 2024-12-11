# ai_grapher
A simple command-line GenAI application to graph data

In to use you must create a `.env` file in this directory with an OpenAI API Key; containing something like `OPENAI_API_KEY=sk-proj-y5dg....`. **Do not share this file**.

To use, run

```sh
python grapher.py [-v] <csv file>
```

where `<csv file>` is the name of a csv file with the feature names in the first row (so it can be read by `pd.read_csv()`) The repo includes `iris.csv` as an example.


It will then ask you what to graph; reply in English (e.g., "graph petal length vs width") and it will pop up a graph in a new window. After closing the graph you can add additional details (e.g., "plot the species in different colors", "make the dots larger and more transparent"). If it can't graph the results it will tell you.

Use the `-v` flag to get additional output, including the code it is executing.

**WARNING: This contains no guardrails and will run GenAI-created code directly on your system. Running it outside of a container may have dire consequences, including data loss. While it is probably safe if used as intended, DO NOT ask it to do anything unsafe to your system, because it might. Run at your own risk.**

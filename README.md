# ai_grapher
A simple command-line GenAI application to graph data

To use, run

```sh
python grapher.py [-v] <csv file>
```

where `<csv file>` is the name of a csv file with the feature names in the first row (so it can be read by `pd.read_csv()`) The repo includes `iris.csv` as an example.

It will then ask you what to graph; reply in English (e.g., "graph petal length vs width") and pop up a graph. After closing the graph you can add additional details (e.g., "plot the species in different colors", "make the dots larger and more transparent")

Use the `-v` flag to get additional output, including the code it is executing.

**WARNING: This contains no guardrails and will run GenAI-created code directly on your system. Running it outside of a container may have dire consequences, including data loss, particularly if you ask it do delete things.**
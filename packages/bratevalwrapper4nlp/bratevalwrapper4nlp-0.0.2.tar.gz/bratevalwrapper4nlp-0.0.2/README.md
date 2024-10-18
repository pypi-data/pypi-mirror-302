# BratEval Wrapper for NLP

This library wraps the Java-based [BratEval](https://github.com/READ-BioMed/brateval) utility to evaluate annotation data for named-entity-recognition (NER).
Given the availability of the Git, Java JDK and Maven, it clones and compiles brateval and wraps the io interactions into Python.

**Note that currently the release v0.3.2 of brateval is used.** See: https://github.com/READ-BioMed/brateval/tree/v0.3.2

**Note that a valid Java JDK and Maven environment must be set up correctly.**

### Install
First, make sure to install a Java JDK environment as well as Maven (for compiling the JAR file) before using the wrapper.

<details>
<summary>[Click to show] Preparation instructions for Ubuntu</summary>

```bash
# Install Java (11, or 21), Maven and Git first
sudo apt install -y openjdk-21-jdk-headless maven git

# Add JAVA_HOME variable to ~/.bashrc
echo 'export JAVA_HOME=$(readlink -f /usr/bin/javac | sed "s:/bin/javac::")' >> $HOME/.bashrc

# Login again to re-load the JAVA_HOME environment variable (or export the variable manually)
export JAVA_HOME=$(readlink -f /usr/bin/javac | sed "s:/bin/javac::")
```

</details>

Eventually, install the package using pip: **`python3 -m pip install bratevalwrapper4nlp`**

### Example
The following script demonstrates the use of the `evaluate` function.
```python
import json
from bratevalwrapper4nlp import evaluate

# Define document (ground truth and prediction)
doc_ground_truth = {
    "text": "This is a fine example.",
    "label": [
        (10, 14, "LABEL2"),
        (15, 22, "LABEL1"),
    ]
}
doc_prediction = {
    "text": "This is a fine example.",
    "label": [
        (10, 22, "LABEL1"),
    ]
}

# Verify the text spans
for src, doc in {"Ground Truth": doc_ground_truth, "Prediction": doc_prediction}.items():
    for lbl_start, lbl_stop, lbl_cls in doc.get("label", []):
        print("[{}] {} has label {}".format(
            src,
            repr(doc["text"][lbl_start:lbl_stop]),
            lbl_cls
        ))

# Run evaluation
score_response = evaluate(
    doc_ground_truth,     # or list of docs: [doc_ground_truth]
    doc_prediction,       # or list of docs: [doc_prediction]
    span_match="overlap", # "overlap", "exact", or float (overlap percentage between 1.0 and 0.0)
    type_match="exact"    # "exact", or "inexact" (ignores label classes)
)
scores = score_response["scores"]

print("Obtained scores:")
print(json.dumps(scores, indent=2))
```

# BiasRV
Sentiment analysis (SA) systems, though widely applied in many domains, have been demonstrated to produce biased results. Some research works have been done in automatically generating test cases to reveal unfairness in SA systems, but the community still lacks tools that can monitor and uncover biased predictions at runtime. This paper fills this gap by proposing *BiasRV*, the first tool to raise an alarm when a deployed SA system makes a biased prediction on a given input text. 

*BiasRV* dynamically extracts a template from an input text and from the template generates gender-discriminatory mutants (semantically-equivalent texts that only differ in gender information). Based on popular metrics used to evaluate the overall fairness of an SA system,, we define distributional fairness property for an individual prediction of an SA system.. This property specifies a requirement that for one piece of text, mutants from different gender classes should be treated similarly as a whole. Verifying the distributional fairness property causes much overhead to the running system. To run more efficiently, *BiasRV* adopts a two-step heuristic: (1) sampling several mutants from each gender and check if the system predicts them as of the same sentiment, (2) checking distributional fairness only when sampled mutants have conflicting results. Experiments show that compared to directly checking the distributional fairness property for each input text,, our two-step heuristic can decrease overhead used for analyzing mutants by 73.81% while only resulting in 6.7% of biased predictions being missed.

Hope this tool can help build more stable, fair and ethical sentiment analysis systems.

# Uasage

## Installation

*BiasRV* can be installed using a simple command: `pip install bias_rv`. The installed library contains all neceesary functions to generate mutants and check fairness properties.

You can also clone this repository and add it into your own project for further usage.

### Build `neuralcoref` from source code

One of the library that `biasRV` depends on, `neuralcoref`, recently can also some issues when installed via pip. So we recommend users to build `neuralcoref` from source code with the following commands:

```
git clone https://github.com/huggingface/neuralcoref.git
cd neuralcoref
pip install -r requirements.txt
pip install -e .
```

You also need to run the following commands if you meet problem ModuleNotFoundError: No module named 'en_core_web_lg'.
```
python -m spacy download en
```

## Monitoring Sentiment Analysis Systems
*BiasRV* requires no implementation information of the SA systems. It assumes that an SA system has a function that takes a piece of text as input and returns a boolean value indicating the predicted sentiment. Assuming we have a SA prediction function (`sa_system.predict(text: str) -> bool`) satisfying *BiasRV*'s requirements.

Then we can import *BiasRV* and instantiate a verifier with the following code:

```
from bias_rv.BiasRV import biasRV
rv = biasRV(sa_system.predict,X=4,alpha=0.10)
```

To instantiate a verifier, we must pass the SA prediction function to the initializer. Besides, we need to specify two parameters `X` and `alpha`. Larger $X$ can lead to more accurate results but introduce more overhead. `alpha` is a threshold representing our tolerance of difference in SA systems' predictions on male and female mutants. By default, we set `X` and `alpha` to 4 and 0.10 respectively.

After create the verifier, we can simply replace the original prediction function with `rv.verify(text: str) -> bool, bool`. It also takes a piece of text as input, but it will monitor the original prediction function and check fairness properties to detect biased prediction. It returns two boolean value: the first one indicating predicted sentiments and the second one indicating whether the prediction is potentially biased.

```
text = "Dee Snider was inspired to do a two part song by a horror movie. This movie he wrote/directed/produced and starred in details the subjects from those songs (Horror-terria,from TwistedSister/ Stay Hungry). People have commented he must have a sick mind to put something like this out. I don't hear anybody making comments like that about Stephen King, Wes Craven,Dean Koontz,or in his own time Alfred Hitchcock. The movie profiles a modern Psychotic created by current trends in society. Personally I thought it was pretty well done from sheer imagination and inspiration,also without the benefit of a large budget and interviews with actual victims/criminals. This movie is perfect if you want something to give you nightmares and make you cringe about the possible and probable. IT COULD HAPPEN!!"


result, is_bias = rv.verify(text)

print(result)
print(is_bias)
```

## Replicating results in the accompanying paper
We also provide necessary models and dataset to replicate results in the paper accompanying *BiasRV*.

### SA Model
We refer to [BERT-based-SA-System](https://github.com/soarsmu/BERT-based-SA-System) for using the same sentiment analysis in our paper. It also provides a configured docker image that can be easily used. Users can use the docker and install bias_rv.

### Data
[BERT-based-SA-System](https://github.com/soarsmu/BERT-based-SA-System) also contains IMDb dataset under `./assert/imdb/test.csv`.
In each line, the first value indicates the true sentiment of the text (1 for positive and 0 for negative), and the second value
is the corresponding text.

### Results
When we set `X` and `alpha` to 4 and 0.10, BiasRV can find biased predictions on texts in `biased_predictions.xlsx`.



# Contribution
We plan to extend this tool with:
1. support for more types of bias, e.g. occupation and nationality;
2. support for more fainess properties
3. more efficient mutant generation engines
4. and more ...

We are welcome if the communitiy can contribute to making *BiasRV* more powerful.

# Contact
If you meet any problem when using *BiasRV*, be free to contact zyang@smu.edu.sg

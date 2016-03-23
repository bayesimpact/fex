# A Simple Feature Extraction Framework


## Motivation

Feature extraction is something we are doing over and over at Bayes. This task usually includes querying one or multiple databases, complex joins to compute the features (e.g. number of different diagnoses for one patient, which might be spread over several tables) and then saving the results of this procedure into one flat table, that can be used to train a model. This flat table has to be re-computed regularly (e.g. after changes to a feature) and has to be shared between multiple people. We furthermore always want to record the code that was used to compute a certain feature set. Without that we might end up in situations where we have a model that works, but we don't remember anymore how we computed the features to train it. This python module simplifies this process.


## Quickstart

Simply write a class that inherits from `FeatureExtractor` and override its `extract` method. Then execute it using the fex runner.

```
#!/usr/bin/env python
from fex import runner
import fex

class ExampleFeature1(fex.FeatureExtractor):
    """First example feature extractor, super cool."""

    def extract(self):
        """Overriden method with custom logic.

        This is the place where one would do the data extraction and transformation.
        """
        self.emit(1, 'col1', 42)

runner.run(ExampleFeature1())
```

See [examples/simple_example.py](examples/simple_example.py) for a slightly more complex example that you can directly run to see the results.


## All Features

* Path to the output CSV file can be specified on the commandline.
* Run `python examples/simple_example.py --help` to see all commandline parameters.

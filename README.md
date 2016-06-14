# A Simple Feature Extraction Framework


## Motivation

Feature extraction is something we are doing over and over at Bayes. This task usually includes querying one or multiple databases, complex joins to compute the features (e.g. number of different diagnoses for one patient, which might be spread over several tables) and then saving the results of this procedure into one flat table, that can be used to train a model. This flat table has to be re-computed regularly (e.g. after changes to a feature) and has to be shared between multiple people. We furthermore always want to record the code that was used to compute a certain feature set. Without that we might end up in situations where we have a model that works, but we don't remember how we computed the features to train it. FEX simplifies this process.


## All Features

* Deployment mode: Execution of the runner with `--deploy` records the current source code version with the generated dataset. This mode makes sure that there are no uncommited changes and prepends a unique identifier, computed from the git remote URL and the latest commit hash, to the generated data file. Note that this mechanism only tracks changes to the code and would not notice if arguments are passed to the feature extractors.
* Results from a feature extractor are cached into a pickle, as long as the source code of the feature extractor did not change.
* The path to the cache file can be specified via commandline arguments of the runner (`--cache-path`).
* Path to the output CSV file can be specified on the commandline (`--path`).
* Caching can be deactivated with the `--no-cache` flag of the runner.


## Quickstart

Simply write a class that inherits from `FeatureExtractor` and override its `extract` method. At one point, it should call `emit` with a pandas DataFrame, which is the result of the extraction. (In the future we may expand this to allow multiple emits, but for now it must emit exactly once.)

Then execute it using the fex runner.

```
#!/usr/bin/env python
import pandas as pd
import fex

class ExampleFeature1(fex.FeatureExtractor):
    """First example feature extractor, super cool."""

    def extract(self):
        """Overriden method with custom logic.

        This is the place where one would do the data extraction and transformation.
        """
        data = {'col1': [42]}
        data_frame = pd.DataFrame(data, index=[1])
        self.emit(data_frame)

fex.runner.run(ExampleFeature1())
```

See [examples/simple_example.py](examples/simple_example.py) for a slightly more complex example that you can directly run to see the results. Run `examples/simple_example.py --help` to see all commandline parameters.

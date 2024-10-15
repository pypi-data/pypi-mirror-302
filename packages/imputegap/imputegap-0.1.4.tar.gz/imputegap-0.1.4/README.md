![My Logo](https://www.naterscreations.com/imputegap/logo_imputegab.png)

# Welcome to ImputeGAP
ImputeGAP is a unified framework for imputation algorithms that provides a narrow-waist interface between algorithm evaluation and parameterization for datasets issued from various domains ranging from neuroscience, medicine, climate to energy.

The interface provides advanced imputation algorithms, construction of various missing values patterns, and different evaluation metrics. In addition, the framework offers support for AutoML parameterization techniques, feature extraction, and, potentially, analysis of feature impact using SHAP. The framework should allow a straightforward integration of new algorithms, datasets, and metrics.



<br /><hr /><br />



## Requirements
In order to use **ImputeGAP**, you must have :
* Python **3.12.0** or higher
* Run your implementation on a **Unix-compatible environment**.
<br><br>

To install these two prerequisites, please refer to the following documentation: <a href="https://github.com/eXascaleInfolab/ImputeGAP/tree/main/docs/installation" >install requirements</a><br><br>




<br /><hr /><br />




## Installation
To install ImputeGAP locally, download the package from GitHub, move inside the folder.<br />
<br />

### Pip installation
```bash
$ pip install imputegap
``` 
<br />

### Local installation
```bash
$ git init
$ git clone https://github.com/eXascaleInfolab/ImputeGAP
$ cd ./ImputeGAP
``` 

Then, once inside, run the command : 

```bash
$ pip install -e .
``` 



<br /><hr /><br />

## Datasets
All datasets preconfigured in this library can be found here : <a href="https://github.com/eXascaleInfolab/ImputeGAP/tree/naterq_skeleton_refac_3/imputegap/dataset" >link to datasets</a>



<br /><hr /><br />



## Loading and pre-process
The model of management is able to load any kind of time series datasets in text format that respect this condition :<br /><br />
<b>(Values,Series)</b> : *series are seperated by space et values by a carriage return \n.*<br><br>

### Example Loading
```python
from imputegap.recovery.manager import TimeSeries
from imputegap.tools import utils

# 1. initiate the TimeSeries() object that will stay with you throughout the analysis
ts_1 = TimeSeries()

# 2. load the timeseries from file or from the code
ts_1.load_timeseries(utils.search_path("eeg"))
ts_1.normalize(normalizer="z_score")

# [OPTIONAL] you can plot your raw data / print the information
ts_1.plot(raw_data=ts_1.data, title="raw data", max_series=10, max_values=100, save_path="./imputegap/assets")
ts_1.print(limit=10)

```

<br /><hr /><br />



## Contamination
ImputeGAP allows to contaminate datasets with a specific scenario to reproduce a situation. Up to now, the scenarios are : <b>MCAR, MISSING POURCENTAGE, ...</b><br />
Please find the documentation in this page : <a href="https://github.com/eXascaleInfolab/ImputeGAP/tree/main/imputegap/recovery#readme" >missing data scenarios</a><br><br>


### Example Contamination
```python
from imputegap.recovery.manager import TimeSeries
from imputegap.tools import utils

# 1. initiate the TimeSeries() object that will stay with you throughout the analysis
ts_1 = TimeSeries()

# 2. load the timeseries from file or from the code
ts_1.load_timeseries(utils.search_path("eeg"))
ts_1.normalize(normalizer="min_max")

# 3. contamination of the data with MCAR scenario
infected_data = ts_1.Contaminate.mcar(ts_1.data, series_impacted=0.4, missing_rate=0.2, use_seed=True)

# [OPTIONAL] you can plot your raw data / print the contamination
ts_1.print(limit=10)
ts_1.plot(ts_1.data, infected_data, title="contamination", max_series=1, save_path="./imputegap/assets")
```

<br /><hr /><br />

## Imputation
ImputeGAP proposes many algorithms of imputation categorized in families, such as : <b>Matrix Decomposition, Machine Learning, Regression, Pattern Recognition, Statistical metods, ...</b><br />

It is also possible de add your own algorithm. To do so, just follow the min-impute template and replace the logic by your code.<br /><br />


### Example Imputation
```python
from imputegap.recovery.imputation import Imputation
from imputegap.recovery.manager import TimeSeries
from imputegap.tools import utils

# 1. initiate the TimeSeries() object that will stay with you throughout the analysis
ts_1 = TimeSeries()

# 2. load the timeseries from file or from the code
ts_1.load_timeseries(utils.search_path("eeg"))
ts_1.normalize(normalizer="min_max")

# 3. contamination of the data
infected_data = ts_1.Contaminate.mcar(ts_1.data)

# 4. imputation of the contaminated data
# choice of the algorithm, and their parameters (default, automl, or defined by the user)
cdrec = Imputation.MD.CDRec(infected_data)

# imputation with default values
cdrec.impute()
# OR imputation with user defined values
cdrec.impute(params={"rank": 5, "epsilon": 0.01, "iterations": 100})

# [OPTIONAL] save your results in a new Time Series object
ts_3 = TimeSeries().import_matrix(cdrec.imputed_matrix)

# 5. score the imputation with the raw_data
cdrec.score(ts_1.data, ts_3.data)

# [OPTIONAL] print the results
ts_3.print_results(cdrec.metrics)
```


<br /><hr /><br />

## Auto-ML
ImputeGAP provides optimization techniques that automatically find the right hyperparameters for a specific algorithm in relation to a certain dataset.

The optimizers available are : <b>Greedy Optimizer, Bayesian Optimizer, Particle Swarm Optimizer and Successive Halving</b>.<br /><br />

### Example Auto-ML
```python
from imputegap.recovery.imputation import Imputation
from imputegap.recovery.manager import TimeSeries
from imputegap.tools import utils

# 1. initiate the TimeSeries() object that will stay with you throughout the analysis
ts_1 = TimeSeries()

# 2. load the timeseries from file or from the code
ts_1.load_timeseries(utils.search_path("eeg"))
ts_1.normalize(normalizer="min_max")

# 3. contamination of the data
infected_data = ts_1.Contaminate.mcar(ts_1.data)

# 4. imputation of the contaminated data
# imputation with AutoML which will discover the optimal hyperparameters for your dataset and your algorithm
cdrec = Imputation.MD.CDRec(infected_data).impute(user_defined=False, params={"ground_truth": ts_1.data, "optimizer": "bayesian", "options": {"n_calls": 5}})

# 5. score the imputation with the raw_data
cdrec.score(ts_1.data, cdrec.imputed_matrix)

# [OPTIONAL] print the results
ts_1.print_results(cdrec.metrics)
```


<br /><hr /><br />


## Explainer
ImputeGap provides you with an algorithm based on the SHAP library, which explains the results of your Imputations using features specific to your dataset.<br /><br />

### Example Explainer
```python
from imputegap.explainer.explainer import Explainer
from imputegap.recovery.manager import TimeSeries
from imputegap.tools import utils

# load your data form ImputeGAP TimeSeries()
ts_1 = TimeSeries()
ts_1.load_timeseries(utils.search_path("eeg"))

# call the explanation of your dataset with a specific algorithm to gain insight on the Imputation results
shap_values, shap_details = Explainer.shap_explainer(raw_data=ts_1.data, file_name="eeg", algorithm="cdrec")

# [OPTIONAL] print the results with the impact of each feature.
Explainer.print(shap_values, shap_details)
```


<br /><hr /><br />

## Contributors
Quentin Nater (<a href="mailto:quentin.nater@unifr.ch">quentin.nater@unifr.ch</a>) and Dr. Mourad Khayati (<a href="mailto:mkhayati@exascale.info">mkhayati@exascale.info</a>)

<br /><br />

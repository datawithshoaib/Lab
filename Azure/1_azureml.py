from azureml.train.estimator import Estimator
file_dataset = ws.datasets.get('csv_folder')
estimator = Estimator(
    source_directory=script_folder,
    compute_target=remote_cluster,
    entry_script='script.py')
run = experiment.submit(config=estimator)
run.wait_for_completion(show_output=True)

# pass the dataset to ensure the script can read the files it references
inputs = [file_dataset.as_named_input('training_files').as_mount()]

# --------------------------------------------------------------------------

## to load file directly into pandas dataframe
from azureml.core import Workspace, Dataset
ws = Workspace.from_config()
blob_ds = ws.get_default_datastore()

target_data = [(blob_ds, 'data/files/archive/*.csv')]
data1 = Dataset.Tabular.from_delimited_files(path=target_data)
registered_data = data1.register(workspace=ws, name="my_dataset")

# --------------------------------------------------------------------------

## display all curated environments and their respective packages in the workspace

from azureml.core import Workspace, Environment
ws = Workspace.from_config()
environments = Environment.list(workspace=ws)
for env_name in environments:
    if env_name.startswith('AzureML'):
        print("Name:", env_name)
        print("Packages:", environments[env_name].python.conda_dependencies.serialize_to_string())

# --------------------------------------------------------------------------

# attach existing DSVM to the workspace

from azureml.core.compute import RemoteCompute, ComputeTarget
compute_target_name = 'dsvm'
config = RemoteCompute.attach_configuration(
    resource_id = '<resource_id>',
    ssh_port = 22,
    username = '<username>',
    private_key_file = '<private_key_file>')

compute = ComputeTarget.attach(ws, compute_target_name, config)
compute.wait_for_completion(show_output=True)

# --------------------------------------------------------------------------

from azureml.core import Workspace, Experiment
import pandas as pd
import datetime as dt
ws = Workspace.from_config()
experiment = Experiment(workspace=ws, name='my_experiment')
run = experiment.start_logging()
print('run_time:', dt.datetime.now())
row_count = len(data)
run.log('observations', row_count)
run.complete()

# --------------------------------------------------------------------------

## create a dataset from remote paths
from azureml.core import Dataset
from azureml.data.dataset_factory import DataType
web_paths = [
    'https://raw.githubusercontent.com/Azure/azureml-examples/master/tutorials/data-science-virtual-machine/iris.tsv',
    'https://raw.githubusercontent.com/Azure/azureml-examples/master/tutorials/data-science-virtual-machine/iris2.tsv'
]

ds = Dataset.Tabular.from_delimited_files(path=web_paths)
ds = ds.register(workspace=ws, name='iris_dataset', description='Iris dataset from web')

# --------------------------------------------------------------------------

## create and register Azure Data Lake Storage Gen2 datastore for the workspace
from azureml.core import Workspace, Datastore
ws = Workspace.from_config()
datastore = Datastore.register_azure_data_lake_gen2(
    workspace=ws,
    datastore_name='myadls',
    account_name='myadlsaccount',
    filesystem='myfilesystem',
    tenant_id='mytenantid',
    client_id='myclientid',
    client_secret=client_secret
)

# --------------------------------------------------------------------------

from azureml.core import Workspace
from azureml.core import Experiment, ScriptRunConfig, Environment
from azureml.widget import RunDetails

ws = Workspace.from_config()
env = Environment.from_conda_specification(
    name='myenv',
    file_path='environment.yml'
)
object1 = ScriptRunConfig(
    source_directory='sample_dir',
    script='sample_training_script.py',
    environment=env)
object2 = Experiment(workspace=ws, name='sample_object2')
run = object2.submit(object1)
run.wait_for_completion(show_output=True)

# --------------------------------------------------------------------------

import os, argparse, glob
from azureml.core import Run

parser = argparse.ArgumentParser()
parser.add_argument('--input_data', type=str, dest='data_folder')
args = parser.parse_args()
data_path = args.data_folder
file_paths = glob.glob(data_path + '/*.jpg')

# --------------------------------------------------------------------------

from azureml.core import ScriptRunConfig
src = ScriptRunConfig(
    source_directory=project_folder,
    script='train.py',
    environment=my_env
)

# 1. compute not mentioned, so it will run on the local compute
# 2. Default environment will not be created, it used environment specified.

# --------------------------------------------------------------------------

from azureml.core import Workspace, Experiment, Environment, ScriptRunConfig
from azureml.core.conda_dependencies import CondaDependencies

ws = Workspace.from_config()
py_sk = Environment(name='sklearn-training')
pkgs = CondaDependencies.create(pip_packages=['scikit-learn', 'azureml-defaults'])
py_sk.python.conda_dependencies = pkgs
script_config = ScriptRunConfig(
    source_directory='scripts',
    script='train.py',
    environment=py_sk
)
experiment = Experiment(workspace=ws, name='training_experiment')
run = experiment.submit(config=script_config)

# --------------------------------------------------------------------------

from azureml.pipeline.core import PipelineData
from azureml.pipeline.steps import PythonScriptStep
from azureml.data import OutputFileDatasetConfig

# Define an output for a step
output_data = OutputFileDatasetConfig(name="pipeline_output_data_unregistered")

# Configure this output to be registered as 'my_registered_dataset' upon completion
output_data.register_on_complete(name='my_registered_dataset')

# Define a pipeline step that produces this output
step1 = PythonScriptStep(
    name="process_data",
    script_name="process.py",
    outputs=[output_data],
    compute_target=compute_target,
    source_directory=source_directory
)

# When a pipeline containing this step runs and completes,
# the data written to 'output_data' will be registered as a new version
# of the 'my_registered_dataset'.

# --------------------------------------------------------------------------












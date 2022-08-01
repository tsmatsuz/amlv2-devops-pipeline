import argparse, os, json
from pathlib import Path
from azureml.core import Run
import mlflow
from mlflow.tracking import MlflowClient

# some housekeeping before running the script
# client = MlflowClient()
run = Run.get_context()
ws = run.experiment.workspace
tracking_uri = ws.get_mlflow_tracking_uri()
mlflow.set_tracking_uri(tracking_uri)


def parse_args():
        
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_dir", type=str, help="model folder")
    parser.add_argument("--experiment_name", type=str, help="Name of experiment")
    parser.add_argument('--deploy_flag', type=str, help='A deploy flag')

    args = parser.parse_args()

    return args


def main():

    args = parse_args()
    
    lines = [
        f"model dir: {args.model_dir}",
        f"experiment name: {args.experiment_name}",
        f"deploy flag: {args.deploy_flag}"
    ]
    for line in lines:
        print(line)

    # Read metric.json
    with open(os.path.join(args.model_dir, 'metric.json')) as f:
        metric = json.load(f)
                
    run_id = metric['run_id']
    last_rmse = metric['RMSE']

    all_runs = None
    experiments = mlflow.get_experiment_by_name(args.experiment_name)
    # Get run history
    if experiments is not None:
        all_runs = mlflow.search_runs(
            experiment_ids=experiments.experiment_id
            )
    all_runs
    print(all_runs)
    print("rmse in last run: ", last_rmse)

    # Filter experiments that FINISHED, and drop the last run  
    filtered_rows  = all_runs[(all_runs["status"] == "FINISHED") & (all_runs["run_id"] != run_id)]

    if len(filtered_rows) > 0 :
        # Sort by RMSE
        sorted_rows = filtered_rows.sort_values(by='metrics.rmse')  # ascending order
        print("rmse in past runs: ", sorted_rows.iloc[0,:]["metrics.rmse"])

        if sorted_rows.iloc[0,:]["metrics.rmse"] > last_rmse:
            print("*** register the last model ***")
            deploy_flag = 1
        else:
            print("*** do not register the last model ***")
            deploy_flag = 0
    else:
        print("*** this is the first run, then register it ***")
        deploy_flag = 1
    

    with open((Path(args.deploy_flag) / "deploy_flag"), 'w') as f:
        f.write('%d' % int(deploy_flag))




if __name__ == "__main__":
    main()
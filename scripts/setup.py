import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

import fire


def select_longest_output(outputs: List[str]):
    """Selects the output with the most words from a list of outputs."""
    return max(outputs, key=lambda x: len(x.split()))


def load_sni(data_dir_path: Path, instance_id_dict: Dict[str, str]):
    """Loads SNI data from the specified directory and updates instances based on instance_id_dict."""
    tasks_path = data_dir_path / "raw" / "tasks"
    files = sorted(tasks_path.glob("*.json"))

    for file in files:
        task_id = file.stem.split("_")[0]
        if task_id in instance_id_dict:
            with open(file, "r") as f:
                data = json.load(f)
            for instance in data["Instances"]:
                instance_id = instance["id"].split("-")[1]
                if instance_id in instance_id_dict[task_id]:
                    longest_output = select_longest_output(instance["output"])
                    instance["output"] = longest_output
                    instance["instruction"] = data["Definition"][0]
                    instance_id_dict[task_id][instance_id] = instance

    return instance_id_dict


def create_task_dict(task_list):
    """Creates a dictionary of tasks from a list of task ids."""
    task_dict = defaultdict(dict)
    for item in task_list:
        task_id, instance_id = item.split("-")
        task_dict[task_id][instance_id] = []
    return task_dict


def run(
    data_dir_path: str = "./data", output_path: str = "./data/merged_dataset.jsonl"
):
    """Main execution function to load, process, and save the data."""
    data_dir_path = Path(data_dir_path)
    assert (data_dir_path / "ambigSNI_NLG.jsonl").exists(), "Data file does not exist"
    ambigsni = [json.loads(line) for line in open(data_dir_path / "ambigsni_nlg.jsonl")]

    instance_id_dict = create_task_dict([item["id"] for item in ambigsni])
    sni_dataset = load_sni(data_dir_path, instance_id_dict)

    with open(output_path, "w") as file:
        for ins in ambigsni:
            task_id, example_id = ins["id"].split("-")
            raw_ins = sni_dataset[task_id][example_id]
            print(json.dumps({**ins, **raw_ins}), file=file)


if __name__ == "__main__":
    fire.Fire(run)

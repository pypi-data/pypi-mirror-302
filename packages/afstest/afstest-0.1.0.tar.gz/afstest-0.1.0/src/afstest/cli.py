import argparse
import os
import shutil
from pathlib import Path

base_path = Path(__file__).resolve().parent


def create_project(project_dir, project_type):
    if os.path.exists(project_dir):
        print(f"Warning: {project_dir} already exists.")
        return
    match project_type:
        case "1":
            shutil.copytree(str(base_path / "webui_frame"), project_dir)
        case "2":
            print("api frame not supported now ")
        case "3":
            print("appui frame not supported now ")
        case _:
            print(f"Error: {project_type} not supported")
    if os.path.exists(project_dir):
        print(f"test project {project_dir} created successfully!")


def main():
    parser = argparse.ArgumentParser(description="Autotest init tool")
    parser.add_argument("name", help="project name")
    parser.add_argument(
        "-t",
        "--type",
        choices=["1", "2", "3"],
        required=True,
        help="test type:\n"
             "1、webui test。\n"
             "2、api test。\n"
             "3、appui test。",
    )

    args = parser.parse_args()
    project_dir = os.path.join(os.getcwd(), args.name)
    create_project(project_dir, args.type)

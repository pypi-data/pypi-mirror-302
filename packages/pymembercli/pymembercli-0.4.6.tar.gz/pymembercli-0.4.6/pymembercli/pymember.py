import argparse
import json
from pathlib import Path

from platformdirs import user_data_dir

from pymembercli import cmds
from pymembercli.task_item import TaskItem


def main():
    path = user_data_dir("pymembercli", "mekumotoki")
    args = make_parser()
    tasks = load_file(path)
    tasks = handle_args(tasks, args)
    # save before exit
    with open(path + "/tasks.json", "w") as file:
        json.dump(tasks, file, indent=4, default=vars)


# implement groups as a dict with names with a list of tasks
def load_file(path) -> list:
    """Loads the tasks.json file and returns it as an object."""
    tasks = []
    Path(path).mkdir(parents=True, exist_ok=True)
    # check if file already exists
    try:
        open(path + "/tasks.json", "x")
    except FileExistsError:
        with open(path + "/tasks.json") as file:
            data = json.load(file)
            for i, d in enumerate(data):
                t = TaskItem(
                    id=i,
                    name=d["name"],
                    desc=d["desc"],
                    status=d["status"],
                    start_date=d["start_date"],
                )
                tasks.append(t)
    return tasks


def make_parser() -> argparse.Namespace:
    """Setup the CLI"""
    parser = argparse.ArgumentParser(
        description="A tool for todo-list keeping and helpful reminders.",
        prog="pymember",
    )

    subparsers = parser.add_subparsers(dest="command")

    ls = subparsers.add_parser("ls", help="list tasks")
    ls.add_argument(
        "lstype",
        type=str,
        default="all",
        nargs="?",
        choices=["all", "todo", "doing", "done"],
    )
    ls.add_argument(
        "-m", "--min", action="store_true", help="print raw task names"
    )

    count = subparsers.add_parser("count", help="count tasks")
    count.add_argument(
        "taskgroup",
        type=str,
        default="all",
        nargs="?",
        choices=["all", "todo", "doing", "done"],
    )

    # TODO tree

    add = subparsers.add_parser("new", help="add a new task to the list")
    add.add_argument("taskname", type=str, help="name of task")
    add.add_argument("-d", "--desc", type=str, help="set a description")

    set_state = subparsers.add_parser("set", help="set the status of task(s)")
    set_state.add_argument(
        "taskids", type=int, nargs="+", help="taskid(s) to set"
    )
    set_state.add_argument(
        "status", type=str, choices=["todo", "doing", "done"]
    )

    del_task = subparsers.add_parser("del", help="delete task(s)")
    del_task.add_argument(
        "-id", dest="taskids", type=int, nargs="+", help="taskid(s) to delete"
    )
    del_task.add_argument(
        "-grp",
        dest="taskgroup",
        type=str,
        choices=["all", "todo", "doing", "done"],
        help="taskgroup to delete",
    )

    return parser.parse_args()


def handle_args(tasks: list[TaskItem], args: argparse.Namespace) -> list:
    match args.command:
        case "ls":
            cmds.list_tasks(args.lstype, tasks, args.min)
        case "count":
            cmds.count_tasks(args.taskgroup, tasks)
        case "tree":
            pass
        case "new":
            if args.desc is not None:
                cmds.add_task(args.taskname, tasks, args.desc)
            else:
                cmds.add_task(args.taskname, tasks)
        case "set":
            cmds.set_task(args.taskids, tasks, args.status)
        case "del":
            if args.taskids is None and args.taskgroup is None:
                print("please use -id or -grp")
                return tasks
            if args.taskids is not None:
                tasks = cmds.del_task_by_id(args.taskids, tasks)
            if args.taskgroup is not None:
                tasks = cmds.del_task_by_grp(args.taskgroup, tasks)

    return tasks

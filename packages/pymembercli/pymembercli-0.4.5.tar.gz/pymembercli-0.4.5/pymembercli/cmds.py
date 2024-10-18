from datetime import datetime

from pympmyansi import pymp

from pymembercli.task_item import TaskItem


def print_all(tasks: list[TaskItem]) -> None:
    for t in tasks:
        print(t)


def list_tasks(listarg: str, tasks: list[TaskItem], just_names: bool) -> None:
    if just_names:
        for t in tasks:
            print(t.name)
        return
    if len(tasks) == 0:
        print("You have no todos!")
        return
    if listarg == "all":
        print_all(tasks)
    else:
        tolist = [t for t in tasks if t.status == listarg]
        if tolist:
            print_all(tolist)
        else:
            print(f"nothing in {listarg}s!")


def count_tasks(listarg: str, tasks: list[TaskItem]) -> None:
    if listarg == "all":
        print(f"you have {len(tasks)} total tasks")
    else:
        tcount = len([t for t in tasks if t.status == listarg])
        print(f"you have {tcount} {listarg}s")


# group1
#   task (colored by status)
#   task (colored by status)
# group2
# ...etc
def print_task_tree():
    pass


def add_task(name: str, tasks: list, desc: str = "") -> None:
    date = datetime.now()
    newdate = str(date.month) + "/" + str(date.day) + "/" + str(date.year)
    # id is irrelevant now since its updated on app start
    id = len(tasks)
    t = TaskItem(id=id, name=name, desc=desc, status="todo", start_date=newdate)
    tasks.append(t)
    print("added", t)


def del_task_by_id(taskids: list[int], tasks: list[TaskItem]) -> list:
    newlist = [t for t in tasks if t.id not in taskids]
    print(pymp(pymp("deleted", "underline"), "fg_red"))
    return newlist


def del_task_by_grp(taskset: str, tasks: list[TaskItem]) -> list:
    if taskset == "all":
        newlist = []
    else:
        newlist = [t for t in tasks if t.status != taskset]
    print(pymp(pymp("deleted", "underline"), "fg_red"), "all in", taskset)
    return newlist


def set_task(taskids: list[int], tasks: list[TaskItem], group: str) -> None:
    color = ""
    match group:
        case "todo":
            color = "fg_red"
        case "doing":
            color = "fg_yellow"
        case "done":
            color = "fg_green"
    for t in tasks:
        if t.id in taskids:
            t.status = group
            print(f"marked {t.name} as", pymp(group, color))


# TODO let you update tasks
def update_task(
    taskids: list[int],
):
    pass

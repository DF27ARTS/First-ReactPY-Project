from reactpy import component, html, hooks
from reactpy.backend.fastapi import configure
from fastapi import FastAPI
from styles.style import styles


@component
def Task(task, set_done=None, set_new_tasks=None):

    def handleDelete(e):
        set_new_tasks(task["id"])
        pass

    def handleClick(e):
        set_done(task["id"])
        pass

    attrs = styles["single task container"]

    # if not task["done"]:
    return html.li(
        attrs["single task"],
        html.button({
            "style": attrs["close task btn"]["style"] if not task["done"] else attrs["close task btn active"]["style"],
            "onClick": handleClick
        }, ""),
        html.span(
            attrs["task text"] if not task["done"] else attrs["task text active"],
            task["task"]
        ),
        html.button({
            "style": attrs["delete btn"]["style"],
            "onClick": handleDelete
        }, "+")
    )


@component
def ToDoList():

    tasks, set_tasks = hooks.use_state([
        {"id": 101, "done": False, "task": "Whatch the next space-x starchip launche"},
        {"id": 102, "done": False, "task": "Star learning ReactPY"},
        {"id": 103, "done": False, "task": "Create an App with GPT-4"},
        {"id": 104, "done": False, "task": "Whatch the the serie secret wars"},
    ])

    new_task, set_new_task = hooks.use_state("")

    # hooks.use_effect(lambda: print(tasks), tasks)

    def set_done(id):
        set_tasks(
            [
                task if task["id"] != id else {**task, "done": not task["done"]} for task in tasks
            ]
        )
        pass

    def handleChange(e):
        value = e["target"]["value"]
        set_new_task(value)
        pass

    def handleClick(e):
        if new_task:
            set_tasks(lambda tasks: [
                {"id": int(len(tasks)), "done": False, "task": new_task}] + tasks)
            set_new_task("")
        pass

    def set_new_tasks(index):
        set_tasks(lambda tasks: [
                  task for task in tasks if task["id"] != index])
        pass

    return html.div(
        styles["main container"],
        html.div(
            styles["task container"],
            html.h1(styles["tasks title"], "Pending Tasks"),
            html.form(
                styles["tasks form"],
                html.input({
                    "style": styles["form imput"]["style"], "value": new_task,
                    "onChange": handleChange
                }),
                html.button({
                    "style": styles["form button"]["style"], "type": "button",
                    "onClick": handleClick
                }, "New Task")
            ),
            html.ul(
                styles["tasks container"],
                [
                    html.li(Task(task, set_done=set_done, set_new_tasks=set_new_tasks), key=task["id"]) for task in tasks
                ]
                if len(tasks) > 0 else
                html.span({
                    "style": {"width": "100%", "text-align": "center", "padding-top": "2rem"}
                }, "No pending taks")
            )

        )
    )


app = FastAPI()
configure(app, ToDoList)

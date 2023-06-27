from reactpy import component, html, hooks
from reactpy.backend.fastapi import configure

from fastapi import FastAPI

styles = {
    "main container": {
        "style": {
            "display": "flex",
            "min-hieght": "50rem",
            "width": "100vw",
            "justify-content": "center",
            "padding": "2rem",
            "font-family": "Helvetica",
            "box-sizing": "border-box",
            "background": "#ccc1",
        }
    },
    "task container": {
        "style": {
            "display": "flex",
            "flex-direction": "column",
            "align-items": "center",
            "padding": "2rem",
            "border-radius": "1rem",
            "width": "30rem",
            "box-shadow": "-.3rem .3rem 1.3rem #0002",
            "background": "#fff",
        }
    },
    "tasks title": {
        "style": {
            "background": "linear-gradient(90deg, blue, purple)",
            "-webkit-background-clip": "text",
            "background-clip": "text",
            "color": "transparent",
        }
    },
    "tasks form": {
        "style": {
            "height": "3rem",
            "width": "100%",
            "border": "1px solid #ccc",
            "display": "flex",
            "border-radius": "50rem",
            "overflow": "hidden",
        }
    },
    "form imput": {
        "style": {
            "flex-grow": "1",
            "border": "none",
            "outline": "none",
            "padding": "0 1rem 0 2rem",
            "font-family": "Helvetica",
            "font-size": "1rem",
        }
    },
    "form button": {
        "style": {
            "width": "7rem",
            "border": "none",
            "outline": "none",
            "color": "#3339",
            "border-left": "1px solid #ccc",
            "background": "white",
            "font-family": "Helvetica",
            "font-weight": "700",
            "font-size": "1rem",
            "color": "#ccc",
            "cursor": "pointer",
            "margin": ".3rem 0",
        }
    },
    "tasks container": {
        "style": {
            "width": "100%",
            "display": "flex",
            "flex-direction": "column",
            "gap": "1rem",
            "list-style-type": "none",
            "padding": "0",
        }
    },
    "single task container": {
        "single task": {
            "style": {
                "height": "4rem",
                "flex-grow": "1",
                "display": "flex",
                "gap": "1rem",
                "align-items": "center",
                "padding": "0 1rem",
                "box-shadow": ".2rem .2rem .7rem #0003",
                "border-radius": ".5rem",
            }
        },
        "delete btn": {
            "style": {
                "opacity": "1",
                "transform": "rotate(45deg)",
                "border": "none",
                "outline": "none",
                "background": "#fff",
                "height": "2rem",
                "aspect-ratio": "1 / 1",
                "font-size": "2rem",
                "color": "#3339",
                "cursor": "pointer",
            },
        },
        "task text": {
            "style": {
                "flex-grow": "1",
            }
        },
        "task text active": {
            "style": {
                "flex-grow": "1",
                "text-decoration": "line-through",
                "color": "#ccc",
            }
        },
        "close task btn": {
            "style": {
                "height": "1.5rem",
                "aspect-ratio": "1 / 1",
                "border-radius": "50%",
                "border": "3px solid purple",
                "background": "white",
                "cursor": "pointer",
            }
        },
        "close task btn active": {
            "style": {
                "height": "1.5rem",
                "aspect-ratio": "1 / 1",
                "border-radius": "50%",
                "border": "none",
                "background": "purple",
                "cursor": "pointer",
            }
        },
    }
}


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
        html.button({"style": attrs["close task btn"]
                    ["style"], "onClick": handleClick}, "")
        if not task["done"] else
        html.button(
            {"style": attrs["close task btn active"]["style"], "onClick": handleClick}, ""),

        html.span(attrs["task text"], task["task"])
        if not task["done"] else
        html.span(attrs["task text active"], task["task"]),

        html.button({"style": attrs["delete btn"]
                    ["style"], "onClick": handleDelete}, "+")
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
                html.input(
                    {"style": styles["form imput"]["style"], "value": new_task, "onChange": handleChange}),
                html.button({
                            "style": styles["form button"]["style"], "type": "button", "onClick": handleClick}, "New Task")
            ),
            html.ul(
                styles["tasks container"],
                [
                    html.li(Task(task, set_done=set_done, set_new_tasks=set_new_tasks), key=task["id"]) for task in tasks
                ] if len(tasks) > 0 else html.span({"style": {"width": "100%", "text-align": "center", "padding-top": "2rem"}}, "No pending taks")
            )

        )
    )


app = FastAPI()
configure(app, ToDoList)

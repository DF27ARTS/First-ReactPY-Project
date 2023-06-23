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
            "box-shadow": "-.3rem .3rem 1.3rem #0001",
            "background": "#fff",
        }
    },
    "tasks title": {
        "style": {
            "color": "darkblue",
        }
    },
    "tasks form": {
        "style": {
            "height": "3rem",
            "width": "100%",
            "border": "1px solid darkblue",
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
            "border-left": "1px solid darkblue",
            "background": "white",
            "font-family": "Helvetica",
            "font-weight": "700",
            "font-size": "1rem",
            "color": "darkblue",
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
                "box-shadow": "0 0 5px #0003",
                "border-radius": ".5rem",
            }
        },
        "delete btn": {
            "style": {
                "display": "none",
            }
        },
        "delete btn active": {
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
                "border": "3px solid lightblue",
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
                "background": "lightblue",
                "cursor": "pointer",
            }
        },
    }
}


@component
def Task(taks, set_new_tasks=None):
    done, set_done = hooks.use_state(False)

    def handleClick(e):
        # e["stopPropagation"]()
        set_done(not done)

    def handleDelete(e):
        set_new_tasks(taks["id"])

    attrs = styles["single task container"]

    if not done:
        return html.li(
            attrs["single task"],
            html.button({
                "style": attrs["close task btn"]["style"],
                "onClick": handleClick
            }, ""),
            html.span(attrs["task text"], taks["task"]),
            html.button({
                "style": attrs["delete btn"]["style"],
                "onClick": handleDelete
            }, "+")
        )
    else:
        return html.li(
            attrs["single task"],
            html.button({
                "style": attrs["close task btn active"]["style"],
                "onClick": handleClick
            }, ""),
            html.span(attrs["task text active"], taks["task"]),
            html.button({
                "style": attrs["delete btn active"]["style"],
                "onClick": handleDelete
            }, "+")
        )


@component
def ToDoList():

    tasks, set_tasks = hooks.use_state([
        {"id": 101, "task": "Whatch the next space-x starchip launche"},
        {"id": 102, "task": "Star learning ReactPY"},
        {"id": 103, "task": "Create an App with GPT-4"},
        {"id": 104, "task": "Whatch the the serie secret wars"},
    ])
    new_task, set_new_task = hooks.use_state("")

    def handleChange(e):
        value = e["target"]["value"]
        set_new_task(value)

    def handleClick(e):
        set_tasks(lambda tasks: [{"id": len(tasks), "task": new_task}] + tasks)

    def set_new_tasks(index):
        set_tasks(lambda tasks: [
                  task for task in tasks if task["id"] != index])

    return html.div(
        styles["main container"],
        html.div(
            styles["task container"],
            html.h1(styles["tasks title"], "Pending Tasks"),
            html.form(
                styles["tasks form"],
                html.input(
                    {"style": styles["form imput"]["style"], "onChange": handleChange}),
                html.button({
                            "style": styles["form button"]["style"], "type": "button", "onClick": handleClick}, "New Task")
            ),
            html.ul(
                styles["tasks container"],
                [
                    html.li(Task(task, set_new_tasks=set_new_tasks)) for task in tasks
                ]
            )

        )
    )


app = FastAPI()
configure(app, ToDoList)

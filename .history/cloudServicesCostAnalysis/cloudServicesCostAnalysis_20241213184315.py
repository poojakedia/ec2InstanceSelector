"""Welcome to Pynecone! This file outlines the steps to create a basic app."""
from pcconfig import config

import pynecone as pc


filename = f"{config.app_name}/{config.app_name}.py"


class State(pc.State):
    """The app state."""

    pass


def index() -> pc.Component:
    return pc.vstack(
        pc.heading("EC2 Instance Cost Analysis", size = "2xl")
        pc.markdown(
               """
            Welcome to your very own `AWS Cloud Analysis Tool`.
            """
        )
    )



app = pc.App(state=State)
app.add_page(index)
app.compile()

"""Welcome to Pynecone! This file outlines the steps to create a basic app."""
from pcconfig import config

import pynecone as pc


filename = f"{config.app_name}/{config.app_name}.py"


class State(pc.State):
    """The app state."""

    pass

class FormState(pc.State):
    form_data: dict = {}
    def handle_submit(self, form_data: dict):
        self.form_data = form_data

def index() -> pc.Component:
    return pc.vstack(
        pc.heading("EC2 Instance Cost Analysis", size = "2xl"),
        pc.markdown(
               """
            Welcome to your very own `AWS Cloud Analysis Tool`.
            """
        ),
        pc.form(
            pc.vstack(
                pc.markdown("""
                            Desired computational power
                            -> enter a numeric value of CPUs
                            """),
                pc.input(
                    placeholder="Compute Requirements",
                    id="computation_reqs",
                ),
                pc.switch("Exclude", id = "exclude_comp"),
                pc.markdown("""
                            Enter your choice memory requirements as a discrete value (GiB) (e.g. 1.0)
                            """),
                pc.input(
                    placeholder="Memory Requirements", id="memory_reqs"
                ),
                pc.switch("Exclude", id = "exclude_mem"),
                pc.markdown("""
                            Enter your choice storage requirements as a discrete value (GB) (e.g. 59)
                            """),
                pc.checkbox("EBS only", id="ebs"),
                pc.input(
                    placeholder="Storage Requirements", id="storage_reqs"
                ),
                pc.switch("Exclude", id = "exclude_storage"),
                pc.button("Apply", typ_="submit")
            ),
            on_submit = FormState.handle_submit,
        ),
        pc.divider(),
        pc.heading("Results"),
        pc.text(FormState.form_data.to_string())
    )



app = pc.App(state=State)
app.add_page(index)
app.compile()

"""Welcome to Pynecone! This file outlines the steps to create a basic app."""
from pcconfig import config

import pynecone as pc
from cloudServicesCostAnalysis.filterServices import filter

filename = f"{config.app_name}/{config.app_name}.py"


class FormState(pc.State):
    form_data: dict = {
    "os_type":"",
    "computation_reqs": "",
    "exclude_comp": False,
    "memory_reqs": "",
    "exclude_mem": False,
    "storage_reqs": "",
    "exclude_storage": False,
    "ebs": False,
    }
    results: list = []
    def handle_submit(self, form_data: dict):
        self.form_data = form_data
        if(form_data["exclude_comp"] == True):
            comp_reqs = "n"
        else:
            comp_reqs = form_data["computation_reqs"]
        
        if(form_data["exclude_mem"] ==True):
            mem_reqs = "n"
        else:
            mem_reqs = form_data["memory_reqs"]
        
        ebs_storage = form_data["ebs"]
        
        if(form_data["exclude_storage"] == True):
            storage_reqs = "n"
        else:
            storage_reqs = form_data["storage_reqs"]
        
        self.results = filter(form_data["os_type"],comp_reqs, mem_reqs, ebs_storage, storage_reqs)
        
            

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
                pc.input(
                    placeholder="OS Type",
                    id="os_type",
                ),
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
                pc.button("Apply", type_="submit")
            ),
            on_submit = FormState.handle_submit,
        ),
        pc.divider(),
        pc.heading("Results"),
        pc.cond(
            FormState.results,
            pc.vstack(
                *[
                    pc.text(f"Result {i+1}: {result}")
                    for i, result in enumerate(FormState.results)
                ]
            ),
            pc.text("No results yet. Submit the form to see results."),
        ),
    )



app = pc.App(state=FormState)
app.add_page(index)
app.compile()

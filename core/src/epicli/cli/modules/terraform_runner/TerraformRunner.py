import os
import subprocess


def run(command, terraform_command, working_directory, auto_approve=False):
    if auto_approve:
        status_run = subprocess.run([command, terraform_command, "--auto-approve", working_directory])
    else:
        status_run = subprocess.run([command, terraform_command, working_directory])

    if status_run.returncode != 0:
        print(command + " " + terraform_command + " run failed")
    else:
        print(command + " " + terraform_command + " run successfully.")


class TerraformRunner:

    def __init__(self, working_directory=os.path.dirname(__file__)):
        self.COMMAND = "terraform"
        self.APPLY_COMMAND = "apply"
        self.DESTROY_COMMAND = "destroy"
        self.PLAN_COMMAND = "plan"
        self.INIT_COMMAND = "init"
        self.working_directory = working_directory

    def apply(self, auto_approve=False):
        if auto_approve:
            status_run = subprocess.run([self.COMMAND, self.APPLY_COMMAND,
                                         "--auto-approve", "-state=" + self.working_directory + "terraform.tfstate",
                                         self.working_directory])
        else:
            status_run = subprocess.run([self.COMMAND, self.APPLY_COMMAND,
                                        "-state=" + self.working_directory + "terraform.tfstate",
                                         self.working_directory])

        if status_run.returncode != 0:
            print(self.COMMAND + " " + self.APPLY_COMMAND + " run failed")
        else:
            print(self.COMMAND + " " + self.APPLY_COMMAND + " run successfully.")

    def destroy(self, auto_approve=False):
        run(self.COMMAND, self.DESTROY_COMMAND, working_directory=self.working_directory,
            auto_approve=auto_approve)

    def plan(self):
        run(self.COMMAND, self.PLAN_COMMAND, working_directory=self.working_directory)

    def init(self):
        run(self.COMMAND, self.INIT_COMMAND, working_directory=self.working_directory)

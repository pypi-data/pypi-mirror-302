from agenticos.node.models import AgenticConfig, Workflow, WorkflowRunner

workflows : dict[Workflow] = {}

# Example workflow
# Import the Crew class. If you used the flow from CrewAI docs the following import should work
from {{folder_name}}.crew import {{class_name}}Crew as Crew

# Implement runner for the workflow. This will be instantiated every time the workflow is run.
class CrewAIRunner(WorkflowRunner):
    def __init__(self):
        super().__init__()
        self.crew = Crew()

    # Pass the kickoff function of the crew.
    def kickoff(self, inputs: dict[str, str]):
        self.crew.crew().kickoff(inputs)

    # Final output of the workflow
    def output(self):
        return (self.crew.crew().tasks[-1].output.raw)

    # Intermediate steps of the workflow
    def ongoing_steps(self):
        return self.crew.crew().tasks

# Define the workflow name
my_workflow_name = "research_and_report"
# Define the workflow
workflows[my_workflow_name] = Workflow(
    # Name of the workflow
    name=my_workflow_name,
    # Description of the workflow
    description="This workflow will get you a joke which is not a PR nightmare",
    # Inputs of the workflow. This is what you pass to Crew.kickoff function
    inputs={"topic": "The topic to joke about"},
    # Description of the steps in the workflow
    step_description=[t.description for t in Crew().crew().tasks],
    # Pass the runner for the workflow
    workflowRunner=CrewAIRunner,
)

config = AgenticConfig(name="Test Node", workflows=workflows)

from typing import List
from .types import StepType  # Assuming StepType is defined in a separate file
from util4all.cli import log_info, log_error  # Assuming logging utility functions

class PipelineManager:
    """
    Manages the execution of the data pipeline steps.
    """

    def __init__(self):
        self.steps = []

    @classmethod
    def newPipeline(cls, steps: List[StepType]):
        """
        Creates a new pipeline with the provided steps.
        
        Args:
            steps (List[StepType]): List of steps to include in the pipeline.
        
        Returns:
            PipelineManager: An instance of PipelineManager initialized with the steps.
        """
        manager = cls()
        manager.steps = sorted(steps, key=lambda step: step.position)  # Sort steps by position
        return manager

    def run(self):
        """
        Runs all the steps in the pipeline in the order of their position.
        """
        for step in self.steps:
            try:
                log_info(f"Running step {step.position}: {step.name}")
                step.run()  # Execute the step's method
                log_info(f"Step {step.position}: {step.name} completed successfully.")
            except Exception as e:
                log_error(f"Error in step {step.position}: {step.name} - {str(e)}")
                raise e  # Optionally, you can raise the error or continue to the next step

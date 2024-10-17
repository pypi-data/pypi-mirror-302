from typing import Callable
from util4all.cli import log_step

class StepType:
    """
    A class representing a step in the data pipeline.
    """
    def __init__(self, position: int, name: str, description: str, method: Callable):
        """
        Initializes a StepType instance.
        
        Args:
            position (int): The position of the step in the pipeline.
            name (str): The name of the step.
            description (str): A brief description of the step.
            method (Callable): The function/method that will execute the step.
        """
        self.position = position
        self.name = name
        self.description = description
        self.method = method

    def run(self):
        """
        Execute the method associated with this step.
        """
        print(f"Running step {self.position}: {self.name} - {self.description}")
        self.method()  # Call the method

    def __repr__(self):
        return f"StepType(position={self.position}, name={self.name}, description={self.description}, method={self.method.__name__})"

import numpy as np
import pandas as pd
from process_steps import ProcessStep

class Process:
    """
    Represents a sequential single step process.

    Attributes:
        head (None , ProcessStep): First step in the process

    """

    def __init__(self):
        self.head = None  # By defaults None
        self.tail = None
    
    def insertAtEnd(self, new_process_step: ProcessStep) -> None:

        if not isinstance(new_process_step, ProcessStep):
            raise TypeError(f"Expected a ProcessStep, but got {type(new_process_step)}")

        if self.head is None:
            self.head = self.tail = new_process_step
        else:
            self.tail.next = new_process_step
            self.tail = new_process_step
    
    def deleteStep(self, step_name: str) -> bool:
        """
        Deletes step by name

        Args:
            step_name (str): Step name

        Returns:
            bool: True if deleted, False if not found.

        """

        if self.head is None:
            raise ValueError("No process steps to delete.")
    
        if self.head.name == step_name:
            self.head = self.head.next
            return True
        
        current_step = self.head
        while current_step and current_step.name != step_name:
            previous_step = current_step
            current_step = current_step.next
        
        if current_step is None:
            return False
        else:
            previous_step.next = current_step.next
            return True

    def get_names(self) -> list[str]:
        """
        Returns step names in a list

        Returns:
            list : List with step names

        """
        names = []
        current = self.head
        if current is None:
            return names
        
        current = self.head
        while current:
            names.append(current.name)
            current = current.next

        return names

    def get_steps(self) -> list[ProcessStep]:
        """
        Returns step names in a list

        Returns:
            list: List with process steps. 

        """
        current = self.head
        if current is None:
            return None

        steps = []

        while current:
            steps.append(current)
            current = current.next

        return steps

    def update_step(self, step_name:str, **kwargs):
        """
        Updates a process step by name with the provided keyword arguments.


        Args:
            step_name (str): Step name to update
            **kwargs: Attribute-value pairs to update

        """
        current_step = self.head
        while current_step:
            if current_step.name == step_name:
                for key, value in kwargs.items():
                    setattr(current_step, key, value)
            current_step = current_step.next

    def simulate_process(self, n_simulations=1000) -> pd.DataFrame:
        """
        Simulates number of samples and calculates the total time.

        Args:
            n_simualtions (int): number of samples to draw. By default 1000

        Returns:
            results (pd.DataFrame) : returns a Pandas dataframe with results

        """
        results = {}
        total_time = np.zeros(n_simulations)
        current = self.head

        while current:
            step_time = current.simulate(n_simulations=n_simulations)
            results[current.name] = step_time
            total_time += step_time

            current = current.next

        results["Total"] = total_time
        return pd.DataFrame(results)

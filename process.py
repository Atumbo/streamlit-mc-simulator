import numpy as np
import pandas as pd

class ProcessStep:
    """
    Represents a single step in a process

    Attributes:
        name (str): Name of the process
        next (ProcessStep or None): Next step in the process.

    Args:
        name (str): Name of the process

    """
    def __init__(self, name : str):
        self.name = name
        self.next  = None

# TODO Add PERT Distribution
# Child classes e.g. types of process steps

class UniformStep(ProcessStep):
    """
    Represents a process step with a uniform distribution.

    Attributes:
        low (float): Lower bound of the distribution.
        high (float): Upper bound of the distribution.

    Inheritance:
        ProcessStep: Base class.

    Args:
        name (str): Name of the step,
        low (float): Lower bound of the distribution.
        high (float): Upper bound of the distribution.

    """
    def __init__(self, name : str, low : float, high : float):
        super().__init__(name)
        self.low = low
        self.high = high

    def simulate(self, n_simulations: int) -> np.ndarray:
        """
        Draws samples from a uniform distribution.

        Args:
            n_simulations (int): number of samples to draw.

        Returns:
            np.ndarray: An array of drawn samples.

        """
        return np.random.uniform(low=self.low, high=self.high, size=n_simulations)
        

class NormalStep(ProcessStep):
    """
    Description of NormalStep

    Attributes:
        mean (type):
        stdev (type):

    Inheritance:
        ProcessStep:

    Args:
        name (str):
        mean (float):
        stdev (float):

    """
    def __init__(self, name : str, mean : float, stdev : float):
        super().__init__(name)
        self.mean = mean
        self.stdev = stdev
    
    def simulate(self, n_simulations : int)-> np.ndarray:
        return np.random.normal(loc=self.mean, scale=self.stdev, size=n_simulations)

class ExponentialStep(ProcessStep):
    """
    Description of ExponentialStep

    Attributes:
        rate (type):

    Inheritance:
        ProcessStep:

    Args:
        name (str):
        rate (float):

    """
    def __init__(self, name : str, rate : float):
        super().__init__(name)
        self.rate = rate
    
    def simulate(self, n_simulations : int) -> np.ndarray:
        """
        Description of simulate

        Args:
            self (undefined):
            n_simulations (int):

        Returns:
            np.ndarray

        """
        return np.random.exponential(1 / self.rate, size=n_simulations)

class Process:
    """
    Description of Process

    Attributes:
        head (None , ProcessStep): first step in the process

    """
    def __init__(self):
        self.head = None

    def insertAtBeginning(self, new_process_step : ProcessStep) -> None:
        """
        Description of insertAtBeginning

        Args:
            new_process_step (ProcessStep):

        Returns:
            None

        """
        new_process_step.next = self.head
        self.head = new_process_step
    
    def insertAtEnd(self, new_process_step : ProcessStep) -> None:
        """
        Description of insertAtEnd

        Args:
            new_process_step (ProcessStep):

        Returns:
            None

        """
        if self.head is None:
            self.head = new_process_step
            return

        
        last_step = self.head
        while last_step.next:
            last_step = last_step.next
        last_step.next = new_process_step

    def deleteStep(self, step_name : str) -> None:
        """
        Description of deleteStep

        Args:
            step_name (str):

        Returns:
            None

        """
    
        if self.head is None:
            print("No process steps to delete")
            

        if self.head.name == step_name:
            self.head = self.head.next
            print(f"Step {step_name} deleted")

        current_step = self.head
        previous_step = None

        while current_step and current_step.name != step_name:
            previous_step = current_step
            current_step = current_step.next

        if current_step is None:
            return None
        else:
            previous_step.next = current_step.next
        print(f"deleted step: {step_name}")

    
    def display_steps(self):
        """
        Prints process steps.

        """
        current = self.head
        if current is None:
            print("The list is empty.")
        
        while current:
            if isinstance(current, UniformStep):
                dist_info = f"Uniform(low={current.low}, high={current.high})"
            elif isinstance(current, NormalStep):
                dist_info = f"Normal(mean={current.mean}, stdev={current.stdev})"
            elif isinstance(current, ExponentialStep):
                dist_info = f"Exponential(rate={current.rate})"
            else:
                dist_info = "Unknown Distribution"

            try: 
                print(f"Step Name: {current.name}, Distribution: {dist_info}, {current.next.name}")
            except Exception:
                print(f"Step Name: {current.name}, Distribution: {dist_info}, {current.next}")
            
            current = current.next
        
    def get_names(self) -> list:
        """
        Returns step names in a  list

        Returns:
            list : List with step names

        """
        current = self.head
        if current is None:
            return []
        names = []
        
        while current:
            names.append(current.name)
            current = current.next
        
        return names
    
    def get_steps(self) -> list:
        current = self.head
        if current is None:
            return None
        steps = []
        
        while current:
            steps.append(current)
            current = current.next
        
        return steps

    def update_step(self, step_name, **kwargs):
        current_step = self.head
        while current_step:
            if current_step.name == step_name:
                for key, value in kwargs.items():
                    setattr(current_step, key, value)
            current_step = current_step.next
    
    def simulate_process(self, n_simulations= 1000) -> pd.DataFrame:
        """
        Description of simulate_process

        Args:
            n_simualtions=1000 (int): 

        Returns:
            pd.DataFrame

        """
        results = {}
        total_time = np.zeros(n_simulations)
        current = self.head

        while current:
            step_time = current.simulate(n_simulations = n_simulations)
            results[current.name] = step_time
            total_time += step_time
            
            current = current.next

        results['Total']  = total_time
        return pd.DataFrame(results)


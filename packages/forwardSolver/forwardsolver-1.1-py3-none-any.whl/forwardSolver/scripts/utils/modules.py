from abc import ABC, abstractmethod


class SimulationModule(ABC):
    """
    Abstract base class for simulation modules.
    This class defines the interface for simulation modules, which includes methods
    for checking inputs, running simulations, and visualizing results. All methods
    are abstract and must be implemented by subclasses.
    Methods
    -------
    check_inputs()
        Check the inputs for the simulation.
    check_simulation()
        Check the status or configuration of the simulation.
    simulate()
        Run the simulation.
    visualise()
        Visualize the results of the simulation.
    """

    @abstractmethod
    def check_inputs(self):
        pass

    @abstractmethod
    def check_simulation(self):
        pass

    @abstractmethod
    def simulate(self):
        pass

    @abstractmethod
    def visualise(self):
        pass


class EvaluationModule(ABC):
    """
    Abstract base class for evaluation modules.
    This class defines the interface for evaluation modules, which must implement
    the following abstract methods:
    Methods
    -------
    evaluate()
        Perform the evaluation process. This method must be implemented by any
        subclass.
    visualise()
        Visualize the results of the evaluation. This method must be implemented
        by any subclass.
    """

    @abstractmethod
    def evaluate(self):
        pass

    @abstractmethod
    def visualise(self):
        pass


class CalculationModule(ABC):
    """
    Abstract base class for calculation modules.
    This class serves as a blueprint for creating calculation modules.
    Any subclass must implement the `calculate` method.
    Methods
    -------
    calculate()
        Abstract method that must be implemented by any subclass.
    """

    @abstractmethod
    def calculate(self):
        pass

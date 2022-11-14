import random
import typing
import base
import numpy as np
import re
import attrib

class Distribution(base.Component):
    """
    Generic distribution class.
    """

    def __init__(self, 
        name: str, 
        default_observer: base.Observer, 
        default_store: typing.Optional[base.Store]
    ) -> None:
        super(Distribution, self).__init__(name, default_observer, default_store)
        self._inputs = base.InputContainer(self, [])

    def sample(self, **keywords) -> typing.Any:
        raise NotImplementedError("sampling-function was not implemented!")

class NormalDistribution(Distribution):
    """
    Implementation of the normal distribution.

    INPUTS
    Mean: Mean of normal distribution.
    SD: Standard deviation of normal distribution.
    """

    def __init__(self, 
        name: str, 
        default_observer: base.Observer, 
        default_store: typing.Optional[base.Store]
    ) -> None:
        super(NormalDistribution, self).__init__(name, default_observer, default_store)
        self._inputs = base.InputContainer(self, [
            base.Input(
                "Mean",
                (attrib.Class(float, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "SD",
                (attrib.Class(float, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer
            )
        ])
        self._mean = None
        self._sd = None

    def initialize(self):
        self._mean = self._inputs["Mean"].read().values
        self._sd = self._inputs["SD"].read().values
        if self._sd < 0.0:
            raise ValueError("Standard deviation has to be positive!")

    def sample(self) -> float:
        if self._mean is None or self._sd is None:
            raise Exception("Parameters were not initialized!")
        return random.gauss(self._mean, self._sd)
        
class UniformDistribution(Distribution):
    """
    Implementation of the continuous uniform distribution.

    INPUTS
    Lower: Lower bound of uniform distribution.
    Upper: Upper bound of uniform distribution.
    """

    def __init__(self, 
        name: str, 
        default_observer: base.Observer, 
        default_store: typing.Optional[base.Store]
    ) -> None:
        super(UniformDistribution, self).__init__(name, default_observer, default_store)
        self._inputs = base.InputContainer(self, [
            base.Input(
                "Lower",
                (attrib.Class(float, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "Upper",
                (attrib.Class(float, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer
            )
        ])
        self._lower = None
        self._upper = None

    def initialize(self):
        self._lower = self._inputs["Lower"].read().values
        self._upper = self._inputs["Upper"].read().values
        if self._lower > self._upper:
            raise ValueError("Lower bound has to be smaller than upper bound!")

    def sample(self) -> float:
        if self._lower is None or self._upper is None:
            raise Exception("Parameters were not initialized!")
        return random.uniform(self._lower, self._upper)

class DiscreteUniformDistribution(Distribution):
    """
    Implementation of the discrete uniform distribution.

    INPUTS
    Lower: Lower bound of uniform distribution.
    Upper: Upper bound of uniform distribution.
    """

    def __init__(self, 
        name: str, 
        default_observer: base.Observer, 
        default_store: typing.Optional[base.Store]
    ) -> None:
        super(DiscreteUniformDistribution, self).__init__(name, default_observer, default_store)
        self._inputs = base.InputContainer(self, [
            base.Input(
                "Lower",
                (attrib.Class(int, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "Upper",
                (attrib.Class(int, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer
            )
        ])
        self._lower = None
        self._upper = None

    def initialize(self):
        self._lower = self._inputs["Lower"].read().values
        self._upper = self._inputs["Upper"].read().values
        if self._lower > self._upper:
            raise ValueError("Lower bound has to be smaller than upper bound!")

    def sample(self) -> float:
        if self._lower is None or self._upper is None:
            raise Exception("Parameters were not initialized!")
        return random.uniform(self._lower, self._upper)

class Choice(base.Component):
    """
    Implementation of a single choice in a distribution over a set.

    INPUTS
    Name: Name of object.
    Probability: Probability of sampling the object.
    """

    def __init__(self, 
        name: str, 
        default_observer: base.Observer, 
        default_store: typing.Optional[base.Store]
    ) -> None:
        super(Choice, self).__init__(name, default_observer, default_store)
        self._inputs = base.InputContainer(self, [
            base.Input(
                "Probability",
                (attrib.Class(float, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer
            )
        ])
        self._object = None
        self._probability = None

    @property
    def inputs(self) -> base.InputContainer:
        return self._inputs

    @property
    def Object(self) -> typing.Any:
        return self._object

    @Object.setter
    def Object(self, value: typing.Any) -> None:
        self._object = value

    @property
    def Probability(self) -> base.Input:
        if self._probability is None:
            raise Exception("Parameters were not initialized!")
        return self._probability

    def initialize(self):
        if hasattr(self._object, "initialize") and callable(getattr(self._object, "initialize")):
            self._object.initialize()
        self._probability = self._inputs["Probability"].read().values

class ChoiceDistribution(Distribution):
    """
    Implementation of a distribution over a set of objects.

    INPUTS
    ChoiceList: A list of name-probability-pairs.
    """

    def __init__(self, 
        name: str, 
        default_observer: base.Observer, 
        default_store: typing.Optional[base.Store]
    ) -> None:
        super(ChoiceDistribution, self).__init__(name, default_observer, default_store)
        self._choiceList = None

    @property
    def ChoiceList(self) -> typing.List[Choice]:
        return self._choiceList

    @ChoiceList.setter
    def ChoiceList(self, value: typing.List[Choice]) -> None:
        self._choiceList = value

    def initialize(self):
        for choice in self._choiceList:
            choice.initialize()

    def sample(self) -> typing.Any:
        objects = [choice.Object for choice in self._choiceList]
        probabilities = [choice.Probability for choice in self._choiceList]
        if np.sum(probabilities) != 1.0:
            raise ValueError("Probability sum is not 1.0!")
        if np.any(np.array(probabilities) < 0.0) or np.any(np.array(probabilities) > 1.0):
            raise ValueError("Probabilities have to be between 0.0 and 1.0!")
        return random.choices(objects, weights=probabilities)[0]

class RandomVariable:
    """
    Implementation of random variables over scales. A random variable keeps realizations in memory so that the sampling is done only once for a given index.

    INPUTS
    Scales: Add description.
    Distribution: Add description.
    """

    def __init__(self) -> None:
        self._scales = None
        self._distribution = None
        self._realizations = {}

    @property
    def Scales(self) -> str:
        return self._scales

    @Scales.setter
    def Scales(self, value: str) -> None:
        self._scales = value

    @property
    def Distribution(self) -> Distribution:
        return self._distribution

    @Distribution.setter
    def Distribution(self, value: Distribution) -> None:
        self._distribution = value

    def initialize(self):
        self._distribution.initialize()

    def get_scale(self, scale_name: str) -> str:
        match = re.search(f"{scale_name}\/.*?((?=,)|$)", self._scales)
        if not match:
            return "global"
        return match.group(0)

    def correct_index(self, index: typing.Tuple[int]) -> typing.Tuple[int]:
        if self._scales == "global":
            index = ()
        else:
            index = index[:len(self._scales.split(","))]
        return index            

    def was_realized(self, index: typing.Tuple[int]) -> bool:
        index = self.correct_index(index)
        return index in self._realizations

    def get_realization(self, random_variable_index: typing.Tuple[int], **keywords) -> typing.Any:
        random_variable_index = self.correct_index(random_variable_index)
        return self._realizations.setdefault(random_variable_index, self._distribution.sample(**keywords))

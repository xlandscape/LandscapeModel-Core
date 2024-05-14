import random
import typing
import numpy as np
from .functions import *

class Distribution:
    """
    Generic base distribution class.
    """

    def __init__(self) -> None:
        pass

    def sample(self, index: typing.Tuple[int], scales: str) -> typing.Any:
        raise NotImplementedError("sampling-function was not implemented for base-distribution!")

class Variable:
    """
    Generic variable base class.
    """

    def __init__(self, unit: str, scales: str, type: str, value: typing.Any) -> None:
        self._unit = unit
        self._scales = scales
        self._type = type
        self._value = value

    @property
    def Unit(self) -> typing.Optional[str]:
        return self._unit

    @Unit.setter
    def Unit(self, value: typing.Optional[str]) -> None:
        self._unit = value

    @property
    def Scales(self) -> typing.Optional[str]:
        return self._scales

    @Scales.setter
    def Scales(self, value: typing.Optional[str]) -> None:
        self._scales = value

    @property
    def Type(self) -> typing.Optional[str]:
        return self._type

    @Type.setter
    def Type(self, value: typing.Optional[str]) -> None:
        self._type = value

    @property
    def Value(self) -> typing.Any:
        return self._value

    @Value.setter
    def Value(self, value: typing.Any) -> None:
        self._value = value

    def get(self, index: typing.Tuple[int], scales: str) -> typing.Any:
        raise NotImplementedError("get-method not implemented for base-class Variable!")

class NormalDistribution(Distribution):
    """
    Implementation of the normal distribution.

    INPUTS
    Mean: Mean of normal distribution.
    SD: Standard deviation of normal distribution.
    """

    def __init__(self) -> None:
        super(NormalDistribution, self).__init__()
        self._mean = None
        self._sd = None

    @property
    def Mean(self) -> Variable:
        return self._mean

    @Mean.setter
    def Mean(self, value: Variable) -> None:
        self._mean = value

    @property
    def SD(self) -> Variable:
        return self._sd

    @SD.setter
    def SD(self, value: Variable) -> None:
        self._sd = value

    def sample(self, index: typing.Tuple[int], scales: str) -> Variable:
        if self._mean is None or self._sd is None:
            raise Exception("Parameters were not initialized!")
        return random.gauss(self._mean.get(index, scales), self._sd.get(index, scales))
        
class UniformDistribution(Distribution):
    """
    Implementation of the continuous uniform distribution.

    INPUTS
    Lower: Lower bound of uniform distribution.
    Upper: Upper bound of uniform distribution.
    """

    def __init__(self) -> None:
        super(UniformDistribution, self).__init__()
        self._lower = None
        self._upper = None

    @property
    def Lower(self) -> Variable:
        return self._lower

    @Lower.setter
    def Lower(self, value: Variable) -> None:
        self._lower = value

    @property
    def Upper(self) -> Variable:
        return self._upper

    @Upper.setter
    def Upper(self, value: Variable) -> None:
        self._upper = value

    def sample(self, index: typing.Tuple[int], scales: str) -> float:
        if self._lower is None or self._upper is None:
            raise Exception("Parameters were not initialized!")
        return random.uniform(self._lower.get(index, scales), self._upper.get(index, scales))

class DiscreteUniformDistribution(Distribution):
    """
    Implementation of the discrete uniform distribution.

    INPUTS
    Lower: Lower bound of uniform distribution.
    Upper: Upper bound of uniform distribution.
    """

    def __init__(self) -> None:
        super(DiscreteUniformDistribution, self).__init__()
        self._lower = None
        self._upper = None

    @property
    def Lower(self) -> Variable:
        return self._lower

    @Lower.setter
    def Lower(self, value: Variable) -> None:
        self._lower = value

    @property
    def Upper(self) -> Variable:
        return self._upper

    @Upper.setter
    def Upper(self, value: Variable) -> None:
        self._upper = value

    def sample(self, index: typing.Tuple[int], scales: str) -> float:
        if self._lower is None or self._upper is None:
            raise Exception("Parameters were not initialized!")
        return random.uniform(self._lower.get(index, scales), self._upper.get(index, scales))

class Choice:
    """
    Implementation of a single choice in a distribution over a set.

    INPUTS
    Name: Name of object.
    Probability: Probability of sampling the object.
    """

    def __init__(self) -> None:
        self._object = None
        self._probability = None

    @property
    def Object(self) -> typing.Any:
        return self._object

    @Object.setter
    def Object(self, value: typing.Any) -> None:
        self._object = value

    @property
    def Probability(self) -> float:
        return self._probability

    @Probability.setter
    def Probability(self, value: typing.Any) -> None:
        self._probability = value

class ChoiceDistribution(Distribution):
    """
    Implementation of a distribution over a set of objects.

    INPUTS
    ChoiceList: A list of name-probability-pairs.
    """

    def __init__(self) -> None:
        super(ChoiceDistribution, self).__init__()
        self._choiceList = None

    @property
    def ChoiceList(self) -> typing.List[Choice]:
        return self._choiceList

    @ChoiceList.setter
    def ChoiceList(self, value: typing.List[Choice]) -> None:
        self._choiceList = value

    def sample(self, index: typing.Tuple[int], scales: str) -> typing.Any:
        objects = [choice.Object for choice in self._choiceList]
        probabilities = [choice.Probability for choice in self._choiceList]
        if round(np.sum(probabilities),5) != 1.0:
            raise ValueError("Probability sum is not 1.0!")
        if np.any(np.array(probabilities) < 0.0) or np.any(np.array(probabilities) > 1.0):
            raise ValueError("Probabilities have to be between 0.0 and 1.0!")
        return random.choices(objects, weights=probabilities)[0]

class RandomVariable(Variable):
    """
    Implementation of random variables over scales. A random variable keeps realizations in memory so that the sampling is done only once for a given index.

    INPUTS
    Scales: Add description.
    Distribution: Add description.
    """

    def __init__(self, unit: str, scales: str, type: str, value: typing.Any) -> None:
        super(RandomVariable, self).__init__(unit, scales, type, value)
        self._realizations = {}

    def get(self, index: typing.Tuple[int], scales: str) -> typing.Any:
        conv_index = convert_index(index, scales, self._scales)
        if conv_index not in self._realizations:
            self._realizations[conv_index] = self._value.sample(index, scales)
        return self._realizations[conv_index]

    @classmethod
    def convert_to_random_variable(self, variable: Variable) -> None:
        variable.__class__ = RandomVariable

class ConstantVariable(Variable):
    """
    Implementation of deterministic variables over scales.

    INPUTS
    Scales: Add description.
    Distribution: Add description.
    """

    def __init__(self, unit: str, scales: str, type: str, value: typing.Any) -> None:
        super(ConstantVariable, self).__init__(unit, scales, type, value)

    def get(self, index: typing.Tuple[int], scales: str) -> typing.Any:
        conv_index = convert_index(index, scales, self._scales)
        return self._value[conv_index]

    @classmethod
    def convert_to_random_variable(self, variable: Variable) -> None:
        variable.__class__ = ConstantVariable

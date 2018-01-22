import numpy as np

from .base import Dependence

class Bound(Dependence):
    """Subclass this to specify how bounds vary with time.

    This abstract class provides the methods which define a dependence
    of the bounds on t.  To subclass it, implement get_bound.  All
    subclasses must include a parameter `B` in required_parameters,
    which is the upper bound at the start of the simulation.  (The
    lower bound is symmetrically -B.)

    Also, since it inherits from Dependence, subclasses must also
    assign a `name` and `required_parameters` (see documentation for
    Dependence.)
    """
    depname = "Bound"
    ## Second effect of Collapsing Bounds: Collapsing Center: Positive
    ## and Negative states are closer to each other over time.
    def get_bound(self, t, conditions, **kwargs):
        """Return the bound at time `t`."""
        raise NotImplementedError
    def B_base(self, conditions):
        assert "B" in self.required_parameters, "B must be a required parameter"
        return self.B

class BoundConstant(Bound):
    """Bound dependence: bound is constant throuhgout the simulation.

    Takes only one parameter: `B`, the constant bound."""
    name = "constant"
    required_parameters = ["B"]
    def get_bound(self, t, conditions, **kwargs):
        return self.B

class BoundCollapsingLinear(Bound):
    """Bound dependence: bound collapses linearly over time.

    Takes two parameters: 

    `B` - the bound at time t = 0.
    `t` - the slope, i.e. the coefficient of time, should be greater
    than zero.
    """
    name = "collapsing_linear"
    required_parameters = ["B", "t"]
    def get_bound(self, t, conditions, **kwargs):
        return max(self.B - self.t*t, 0.)

class BoundCollapsingExponential(Bound):
    """Bound dependence: bound collapses exponentially over time.

    Takes two parameters: 

    `B` - the bound at time t = 0.
    `tau` - the time constant for the collapse, should be greater than
    zero.
    """
    name = "collapsing_exponential"
    required_parameters = ["B", "tau"]
    def get_bound(self, t, conditions, **kwargs):
        return self.B * np.exp(-self.tau*t)


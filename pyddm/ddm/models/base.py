class Dependence(object): # TODO Base this on ABC
    """An abstract class describing how one variable depends on other variables.

    This is an abstract class which is inherrited by other abstract
    classes only, and has the highest level machinery for describing
    how one variable depends on others.  For example, an abstract
    class that inherits from Dependence might describe how the drift
    rate may change throughout the simulation depending on the value
    of x and t, and then this class would be inherited by a concrete
    class describing an implementation.  For example, the relationship
    between drift rate and x could be linear, exponential, etc., and
    each of these would be a subsubclass of Dependence.

    In order to subclass Dependence, you must set the (static) class
    variable `depname`, which gives an alpha-numeric string describing
    which variable could potentially depend on other variables.

    Each subsubclass of dependence must also define two (static) class
    variables.  First, it must define `name`, which is an
    alpha-numeric plus underscores name of what the algorithm is, and
    also `required_parameters`, a python list of names (strings) for
    the parameters that must be passed to this algorithm.  (This does
    not include globally-relevant variables like dt, it only includes
    variables relevant to a particular instance of the algorithm.)  An
    optional (static) class variable is `default_parameters`, which is
    a dictionary indexed by the parameter names from
    `required_parameters`.  Any parameters referenced here will be
    given a default value.

    Dependence will check to make sure all of the required parameters
    have been supplied, with the exception of those which have default
    versions.  It also provides other convenience and safety features,
    such as allowing tests for equality of derived algorithms and for
    ensuring extra parameters were not assigned.
    """
    def __init__(self, **kwargs):
        """Create a new Dependence object with parameters specified in **kwargs.

        This function will only be called by classes which have been
        inherited from this one.  Errors here are caused by invalid
        subclass declarations.
        """
        assert hasattr(self, "depname"), "Dependence needs a parameter name"
        assert hasattr(self, "name"), "Dependence classes need a name"
        assert hasattr(self, "required_parameters"), "Dependence needs a list of required params"
        if hasattr(self, "default_parameters"):
            args = self.default_parameters
            args.update(kwargs)
        else:
            args = kwargs
        if not hasattr(self, "required_conditions"):
            object.__setattr__(self, 'required_conditions', [])
        passed_args = sorted(args.keys())
        expected_args = sorted(self.required_parameters)
        assert passed_args == expected_args, "Provided %s arguments, expected %s" % (str(passed_args), str(expected_args))
        for key, value in args.items():
            setattr(self, key, value)

    def __eq__(self, other):
        """Equality is defined as having the same algorithm type and the same parameters."""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __setattr__(self, name, val):
        """Only allow the required parameters to be assigned."""
        if name in self.required_parameters:
            return object.__setattr__(self, name, val) # No super() for python2 compatibility
        raise LookupError
    def __delattr__(self, name):
        """No not allow a required parameter to be deleted."""
        raise LookupError
    def __repr__(self):
        params = ""
        # If it is a sub-sub-class, then print the parameters it was
        # instantiated with
        if self.name:
            for p in self.required_parameters:
                params += str(p) + "=" + getattr(self, p).__repr__()
                if p != self.required_parameters[-1]:
                    params += ", "
        return type(self).__name__ + "(" + params + ")"
    def __str__(self):
        return self.__repr__()
    def __hash__(self):
        return hash(repr(self))



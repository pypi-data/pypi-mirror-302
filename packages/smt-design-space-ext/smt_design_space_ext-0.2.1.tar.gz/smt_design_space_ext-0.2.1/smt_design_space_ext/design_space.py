"""
Author: Jasper Bussemaker <jasper.bussemaker@dlr.de>

This package is distributed under New BSD license.
"""

from typing import List, Sequence, Tuple, Union

import numpy as np

from smt.sampling_methods import LHS

# Here we import design space base classes from smt
# We do not import smt.design_space as it would be circular!!!
from smt.design_space.design_space import (
    DesignVariable,
    FloatVariable,
    IntegerVariable,
    OrdinalVariable,
    CategoricalVariable,
    BaseDesignSpace,
)

try:
    from ConfigSpace import (
        CategoricalHyperparameter,
        Configuration,
        ConfigurationSpace,
        EqualsCondition,
        ForbiddenAndConjunction,
        ForbiddenEqualsClause,
        ForbiddenInClause,
        ForbiddenLessThanRelation,
        InCondition,
        OrdinalHyperparameter,
        UniformFloatHyperparameter,
        UniformIntegerHyperparameter,
    )
    from ConfigSpace.exceptions import ForbiddenValueError
    from ConfigSpace.util import get_random_neighbor

    HAS_CONFIG_SPACE = True

except ImportError:
    HAS_CONFIG_SPACE = False
try:
    from adsg_core.graph.graph_edges import EdgeType
    from adsg_core import GraphProcessor, SelectionChoiceNode
    from adsg_core.graph.adsg import ADSG
    from adsg_core import BasicADSG, NamedNode, DesignVariableNode

    HAS_ADSG = True
except ImportError:
    HAS_ADSG = False

    class Configuration:
        pass

    class ConfigurationSpace:
        pass

    class UniformIntegerHyperparameter:
        pass


def ensure_design_space(xt=None, xlimits=None, design_space=None) -> "BaseDesignSpace":
    """Interface to turn legacy input formats into a DesignSpace"""

    if design_space is not None and isinstance(design_space, BaseDesignSpace):
        return design_space
    if HAS_ADSG and design_space is not None and isinstance(design_space, ADSG):
        return _convert_adsg_to_legacy(design_space)

    if xlimits is not None:
        return DesignSpace(xlimits)

    if xt is not None:
        return DesignSpace([[np.min(xt) - 0.99, np.max(xt) + 1e-4]] * xt.shape[1])

    raise ValueError("Nothing defined that could be interpreted as a design space!")


VarValueType = Union[int, str, List[Union[int, str]]]


class DesignSpace(BaseDesignSpace):
    """
    Class for defining a (hierarchical) design space by defining design variables, defining decreed variables
    (optional), and adding value constraints (optional).

    Numerical bounds can be requested using `get_num_bounds()`.
    If needed, it is possible to get the legacy SMT < 2.0 `xlimits` format using `get_x_limits()`.

    Parameters
    ----------
    design_variables: list[DesignVariable]
       - The list of design variables: FloatVariable, IntegerVariable, OrdinalVariable, or CategoricalVariable

    Examples
    --------
    Instantiate the design space with all its design variables:

    >>> from smt.utils.design_space import *
    >>> ds = DesignSpace([
    >>>     CategoricalVariable(['A', 'B']),  # x0 categorical: A or B; order is not relevant
    >>>     OrdinalVariable(['C', 'D', 'E']),  # x1 ordinal: C, D or E; order is relevant
    >>>     IntegerVariable(0, 2),  # x2 integer between 0 and 2 (inclusive): 0, 1, 2
    >>>     FloatVariable(0, 1),  # c3 continuous between 0 and 1
    >>> ])
    >>> assert len(ds.design_variables) == 4

    You can define decreed variables (conditional activation):

    >>> ds.declare_decreed_var(decreed_var=1, meta_var=0, meta_value='A')  # Activate x1 if x0 == A

    Decreed variables can be chained (however no cycles and no "diamonds" are supported):
    Note: only if ConfigSpace is installed! pip install smt[cs]
    >>> ds.declare_decreed_var(decreed_var=2, meta_var=1, meta_value=['C', 'D'])  # Activate x2 if x1 == C or D

    If combinations of values between two variables are not allowed, this can be done using a value constraint:
    Note: only if ConfigSpace is installed! pip install smt[cs]
    >>> ds.add_value_constraint(var1=0, value1='A', var2=2, value2=[0, 1])  # Forbid x0 == A && x2 == 0 or 1

    After defining everything correctly, you can then use the design space object to correct design vectors and get
    information about which design variables are acting:

    >>> x_corr, is_acting = ds.correct_get_acting(np.array([
    >>>     [0, 0, 2, .25],
    >>>     [0, 2, 1, .75],
    >>> ]))
    >>> assert np.all(x_corr == np.array([
    >>>     [0, 0, 2, .25],
    >>>     [0, 2, 0, .75],
    >>> ]))
    >>> assert np.all(is_acting == np.array([
    >>>     [True, True, True, True],
    >>>     [True, True, False, True],  # x2 is not acting if x1 != C or D (0 or 1)
    >>> ]))

    It is also possible to randomly sample design vectors conforming to the constraints:

    >>> x_sampled, is_acting_sampled = ds.sample_valid_x(100)

    You can also instantiate a purely-continuous design space from bounds directly:

    >>> continuous_design_space = DesignSpace([(0, 1), (0, 2), (.5, 5.5)])
    >>> assert continuous_design_space.n_dv == 3

    If needed, it is possible to get the legacy design space definition format:

    >>> xlimits = ds.get_x_limits()
    >>> cont_bounds = ds.get_num_bounds()
    >>> unfolded_cont_bounds = ds.get_unfolded_num_bounds()

    """

    def __init__(
        self,
        design_variables: Union[List[DesignVariable], list, np.ndarray],
        random_state=None,
    ):
        self.sampler = None

        # Assume float variable bounds as inputs
        def _is_num(val):
            try:
                float(val)
                return True
            except ValueError:
                return False

        if len(design_variables) > 0 and not isinstance(
            design_variables[0], DesignVariable
        ):
            converted_dvs = []
            for bounds in design_variables:
                if len(bounds) != 2 or not _is_num(bounds[0]) or not _is_num(bounds[1]):
                    raise RuntimeError(
                        f"Expecting either a list of DesignVariable objects or float variable "
                        f"bounds! Unrecognized: {bounds!r}"
                    )
                converted_dvs.append(FloatVariable(bounds[0], bounds[1]))
            design_variables = converted_dvs

        self.random_state = random_state  # For testing
        seed = self.random_state
        self._cs = None
        self._cs_cate = None
        if HAS_CONFIG_SPACE:
            cs_vars = {}
            cs_vars_cate = {}
            self.isinteger = False
            for i, dv in enumerate(design_variables):
                name = f"x{i}"
                if isinstance(dv, FloatVariable):
                    cs_vars[name] = UniformFloatHyperparameter(
                        name, lower=dv.lower, upper=dv.upper
                    )
                    cs_vars_cate[name] = UniformFloatHyperparameter(
                        name, lower=dv.lower, upper=dv.upper
                    )
                elif isinstance(dv, IntegerVariable):
                    cs_vars[name] = FixedIntegerParam(
                        name, lower=dv.lower, upper=dv.upper
                    )
                    listvalues = []
                    for i in range(int(dv.upper - dv.lower + 1)):
                        listvalues.append(str(int(i + dv.lower)))
                    cs_vars_cate[name] = CategoricalHyperparameter(
                        name, choices=listvalues
                    )
                    self.isinteger = True
                elif isinstance(dv, OrdinalVariable):
                    cs_vars[name] = OrdinalHyperparameter(name, sequence=dv.values)
                    cs_vars_cate[name] = CategoricalHyperparameter(
                        name, choices=dv.values
                    )

                elif isinstance(dv, CategoricalVariable):
                    cs_vars[name] = CategoricalHyperparameter(name, choices=dv.values)
                    cs_vars_cate[name] = CategoricalHyperparameter(
                        name, choices=dv.values
                    )

                else:
                    raise ValueError(f"Unknown variable type: {dv!r}")
            seed = self._to_seed(random_state)

            self._cs = NoDefaultConfigurationSpace(space=cs_vars, seed=seed)
            ## Fix to make constraints work correctly with either IntegerVariable or OrdinalVariable
            ## ConfigSpace is malfunctioning
            self._cs_cate = NoDefaultConfigurationSpace(space=cs_vars_cate, seed=seed)

        # dict[int, dict[any, list[int]]]: {meta_var_idx: {value: [decreed_var_idx, ...], ...}, ...}
        self._meta_vars = {}
        self._is_decreed = np.zeros((len(design_variables),), dtype=bool)

        super().__init__(design_variables=design_variables, random_state=seed)

    def declare_decreed_var(
        self, decreed_var: int, meta_var: int, meta_value: VarValueType
    ):
        """
        Define a conditional (decreed) variable to be active when the meta variable has (one of) the provided values.

        Parameters
        ----------
        decreed_var: int
           - Index of the conditional variable (the variable that is conditionally active)
        meta_var: int
           - Index of the meta variable (the variable that determines whether the conditional var is active)
        meta_value: int | str | list[int|str]
           - The value or list of values that the meta variable can have to activate the decreed var
        """

        # ConfigSpace implementation
        if self._cs is not None:
            # Get associated parameters
            decreed_param = self._get_param(decreed_var)
            meta_param = self._get_param(meta_var)

            # Add a condition that checks for equality (if single value given) or in-collection (if sequence given)
            if isinstance(meta_value, Sequence):
                condition = InCondition(decreed_param, meta_param, meta_value)
            else:
                condition = EqualsCondition(decreed_param, meta_param, meta_value)

            ## Fix to make constraints work correctly with either IntegerVariable or OrdinalVariable
            ## ConfigSpace is malfunctioning
            self._cs.add_condition(condition)
            decreed_param = self._get_param2(decreed_var)
            meta_param = self._get_param2(meta_var)
            # Add a condition that checks for equality (if single value given) or in-collection (if sequence given)
            if isinstance(meta_value, Sequence):
                try:
                    condition = InCondition(
                        decreed_param,
                        meta_param,
                        list(np.atleast_1d(np.array(meta_value, dtype=str))),
                    )
                except ValueError:
                    condition = InCondition(
                        decreed_param,
                        meta_param,
                        list(np.atleast_1d(np.array(meta_value, dtype=float))),
                    )
            else:
                try:
                    condition = EqualsCondition(
                        decreed_param, meta_param, str(meta_value)
                    )
                except ValueError:
                    condition = EqualsCondition(decreed_param, meta_param, meta_value)

            self._cs_cate.add_condition(condition)

        # Simplified implementation
        else:
            # Variables cannot be both meta and decreed at the same time
            if self._is_decreed[meta_var]:
                raise RuntimeError(
                    f"Variable cannot be both meta and decreed ({meta_var})!"
                )

            # Variables can only be decreed by one meta var
            if self._is_decreed[decreed_var]:
                raise RuntimeError(f"Variable is already decreed: {decreed_var}")

            # Define meta-decreed relationship
            if meta_var not in self._meta_vars:
                self._meta_vars[meta_var] = {}

            meta_var_obj = self.design_variables[meta_var]
            for value in (
                meta_value if isinstance(meta_value, Sequence) else [meta_value]
            ):
                encoded_value = value
                if isinstance(meta_var_obj, (OrdinalVariable, CategoricalVariable)):
                    if value in meta_var_obj.values:
                        encoded_value = meta_var_obj.values.index(value)

                if encoded_value not in self._meta_vars[meta_var]:
                    self._meta_vars[meta_var][encoded_value] = []
                self._meta_vars[meta_var][encoded_value].append(decreed_var)

        # Mark as decreed (conditionally acting)
        self._is_decreed[decreed_var] = True

    def add_value_constraint(
        self, var1: int, value1: VarValueType, var2: int, value2: VarValueType
    ):
        """
        Define a constraint where two variables cannot have the given values at the same time.

        Parameters
        ----------
        var1: int
           - Index of the first variable
        value1: int | str | list[int|str]
           - Value or values that the first variable is checked against
        var2: int
           - Index of the second variable
        value2: int | str | list[int|str]
           - Value or values that the second variable is checked against
        """
        # Get parameters
        param1 = self._get_param(var1)
        param2 = self._get_param(var2)
        mixint_types = (UniformIntegerHyperparameter, OrdinalHyperparameter)
        self.has_valcons_ord_int = isinstance(param1, mixint_types) or isinstance(
            param2, mixint_types
        )
        if not (isinstance(param1, UniformFloatHyperparameter)) and not (
            isinstance(param2, UniformFloatHyperparameter)
        ):
            # Add forbidden clauses
            if isinstance(value1, Sequence):
                clause1 = ForbiddenInClause(param1, value1)
            else:
                clause1 = ForbiddenEqualsClause(param1, value1)

            if isinstance(value2, Sequence):
                clause2 = ForbiddenInClause(param2, value2)
            else:
                clause2 = ForbiddenEqualsClause(param2, value2)

            constraint_clause = ForbiddenAndConjunction(clause1, clause2)
            self._cs.add_forbidden_clause(constraint_clause)
        else:
            if value1 in [">", "<"] and value2 in [">", "<"] and value1 != value2:
                if value1 == "<":
                    constraint_clause = ForbiddenLessThanRelation(param1, param2)
                    self._cs.add_forbidden_clause(constraint_clause)
                else:
                    constraint_clause = ForbiddenLessThanRelation(param2, param1)
                    self._cs.add_forbidden_clause(constraint_clause)
            else:
                raise ValueError("Bad definition of DesignSpace.")

        ## Fix to make constraints work correctly with either IntegerVariable or OrdinalVariable
        ## ConfigSpace is malfunctioning
        # Get parameters
        param1 = self._get_param2(var1)
        param2 = self._get_param2(var2)
        # Add forbidden clauses
        if not (isinstance(param1, UniformFloatHyperparameter)) and not (
            isinstance(param2, UniformFloatHyperparameter)
        ):
            if isinstance(value1, Sequence):
                clause1 = ForbiddenInClause(
                    param1, list(np.atleast_1d(np.array(value1, dtype=str)))
                )
            else:
                clause1 = ForbiddenEqualsClause(param1, str(value1))

            if isinstance(value2, Sequence):
                try:
                    clause2 = ForbiddenInClause(
                        param2, list(np.atleast_1d(np.array(value2, dtype=str)))
                    )
                except ValueError:
                    clause2 = ForbiddenInClause(
                        param2, list(np.atleast_1d(np.array(value2, dtype=float)))
                    )
            else:
                try:
                    clause2 = ForbiddenEqualsClause(param2, str(value2))
                except ValueError:
                    clause2 = ForbiddenEqualsClause(param2, value2)

            constraint_clause = ForbiddenAndConjunction(clause1, clause2)
            self._cs_cate.add_forbidden_clause(constraint_clause)

    def _get_param(self, idx):
        try:
            return self._cs.get_hyperparameter(f"x{idx}")
        except KeyError:
            raise KeyError(f"Variable not found: {idx}")

    def _get_param2(self, idx):
        try:
            return self._cs_cate.get_hyperparameter(f"x{idx}")
        except KeyError:
            raise KeyError(f"Variable not found: {idx}")

    @property
    def _cs_var_idx(self):
        """
        ConfigurationSpace applies topological sort when adding conditions, so compared to what we expect the order of
        parameters might have changed.

        This property contains the indices of the params in the ConfigurationSpace.
        """
        names = self._cs.get_hyperparameter_names()
        return np.array(
            [names.index(f"x{ix}") for ix in range(len(self.design_variables))]
        )

    @property
    def _inv_cs_var_idx(self):
        """
        See _cs_var_idx. This function returns the opposite mapping: the positions of our design variables for each
        param.
        """
        return np.array(
            [int(param[1:]) for param in self._cs.get_hyperparameter_names()]
        )

    def _is_conditionally_acting(self) -> np.ndarray:
        # Decreed variables are the conditionally acting variables
        return self._is_decreed

    def _correct_get_acting(self, x: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Correct and impute design vectors"""
        x = x.astype(float)
        if self._cs is not None:
            # Normalize value according to what ConfigSpace expects
            self._normalize_x(x)

            # Get corrected Configuration objects by mapping our design vectors
            # to the ordering of the ConfigurationSpace
            inv_cs_var_idx = self._inv_cs_var_idx
            configs = []
            for xi in x:
                configs.append(self._get_correct_config(xi[inv_cs_var_idx]))

            # Convert Configuration objects to design vectors and get the is_active matrix
            x_out, is_act = self._configs_to_x(configs)
            self._impute_non_acting(x_out, is_act)
            return x_out, is_act

        # Simplified implementation
        # Correct discrete variables
        x_corr = x.copy()
        self._normalize_x(x_corr, cs_normalize=False)

        # Determine which variables are acting
        is_acting = np.ones(x_corr.shape, dtype=bool)
        is_acting[:, self._is_decreed] = False
        for i, xi in enumerate(x_corr):
            for i_meta, decrees in self._meta_vars.items():
                meta_var_value = xi[i_meta]
                if meta_var_value in decrees:
                    i_decreed_vars = decrees[meta_var_value]
                    is_acting[i, i_decreed_vars] = True

        # Impute non-acting variables
        self._impute_non_acting(x_corr, is_acting)

        return x_corr, is_acting

    def _sample_valid_x(
        self, n: int, random_state=None
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Sample design vectors"""
        # Simplified implementation: sample design vectors in unfolded space
        x_limits_unfolded = self.get_unfolded_num_bounds()
        if self.random_state is None:
            self.random_state = random_state

        if self._cs is not None:
            # Sample Configuration objects
            if self.seed is None:
                seed = self._to_seed(random_state)
                self.seed = seed
            self._cs.seed(self.seed)
            if self.seed is not None:
                self.seed += 1
            configs = self._cs.sample_configuration(n)
            if n == 1:
                configs = [configs]
            # Convert Configuration objects to design vectors and get the is_active matrix
            return self._configs_to_x(configs)

        else:
            if self.sampler is None:
                self.sampler = LHS(
                    xlimits=x_limits_unfolded,
                    random_state=random_state,
                    criterion="ese",
                )
            x = self.sampler(n)
            # Fold and cast to discrete
            x, _ = self.fold_x(x)
            self._normalize_x(x, cs_normalize=False)
            # Get acting information and impute
            return self.correct_get_acting(x)

    def _get_correct_config(self, vector: np.ndarray) -> Configuration:
        config = Configuration(self._cs, vector=vector)

        # Unfortunately we cannot directly ask which parameters SHOULD be active
        # https://github.com/automl/ConfigSpace/issues/253#issuecomment-1513216665
        # Therefore, we temporarily fix it with a very dirty workaround: catch the error raised in check_configuration
        # to find out which parameters should be inactive
        while True:
            try:
                ## Fix to make constraints work correctly with either IntegerVariable or OrdinalVariable
                ## ConfigSpace is malfunctioning
                if self.isinteger and self.has_valcons_ord_int:
                    vector2 = np.copy(vector)
                    self._cs_denormalize_x_ordered(np.atleast_2d(vector2))
                    indvec = 0
                    for hp in self._cs_cate:
                        if (
                            (str(self._cs.get_hyperparameter(hp)).split()[2])
                            == "UniformInteger,"
                            and (
                                str(self._cs_cate.get_hyperparameter(hp)).split()[2][:3]
                            )
                            == "Cat"
                            and not (np.isnan(vector2[indvec]))
                        ):
                            vector2[indvec] = int(vector2[indvec]) - int(
                                str(self._cs_cate.get_hyperparameter(hp)).split()[4][
                                    1:-1
                                ]
                            )
                        indvec += 1
                    self._normalize_x_no_integer(np.atleast_2d(vector2))
                    config2 = Configuration(self._cs_cate, vector=vector2)
                    config2.is_valid_configuration()

                config.is_valid_configuration()
                return config

            except ValueError as e:
                error_str = str(e)
                if "Inactive hyperparameter" in error_str:
                    # Deduce which parameter is inactive
                    inactive_param_name = error_str.split("'")[1]
                    param_idx = self._cs.get_idx_by_hyperparameter_name(
                        inactive_param_name
                    )

                    # Modify the vector and create a new Configuration
                    vector = config.get_array().copy()
                    vector[param_idx] = np.nan
                    config = Configuration(self._cs, vector=vector)

                # At this point, the parameter active statuses are set correctly, so we only need to correct the
                # configuration to one that does not violate the forbidden clauses
                elif isinstance(e, ForbiddenValueError):
                    if self.seed is None:
                        seed = self._to_seed(self.random_state)
                        self.seed = seed
                    if not (self.has_valcons_ord_int):
                        return get_random_neighbor(config, seed=self.seed)
                    else:
                        vector = config.get_array().copy()
                        indvec = 0
                        vector2 = np.copy(vector)
                        ## Fix to make constraints work correctly with either IntegerVariable or OrdinalVariable
                        ## ConfigSpace is malfunctioning
                        for hp in self._cs_cate:
                            if (
                                str(self._cs_cate.get_hyperparameter(hp)).split()[2][:3]
                            ) == "Cat" and not (np.isnan(vector2[indvec])):
                                vector2[indvec] = int(vector2[indvec])
                            indvec += 1

                        config2 = Configuration(self._cs_cate, vector=vector2)
                        config3 = get_random_neighbor(config2, seed=self.seed)
                        vector3 = config3.get_array().copy()
                        config4 = Configuration(self._cs, vector=vector3)
                        return config4
                else:
                    raise

    def _configs_to_x(
        self, configs: List["Configuration"]
    ) -> Tuple[np.ndarray, np.ndarray]:
        x = np.zeros((len(configs), len(self.design_variables)))
        is_acting = np.zeros(x.shape, dtype=bool)
        if len(configs) == 0:
            return x, is_acting

        cs_var_idx = self._cs_var_idx
        for i, config in enumerate(configs):
            x[i, :] = config.get_array()[cs_var_idx]

        # De-normalize continuous and integer variables
        self._cs_denormalize_x(x)

        # Set is_active flags and impute x
        is_acting = np.isfinite(x)
        self._impute_non_acting(x, is_acting)

        return x, is_acting

    def _impute_non_acting(self, x: np.ndarray, is_acting: np.ndarray):
        for i, dv in enumerate(self.design_variables):
            if isinstance(dv, FloatVariable):
                # Impute continuous variables to the mid of their bounds
                x[~is_acting[:, i], i] = 0.5 * (dv.upper - dv.lower) + dv.lower

            else:
                # Impute discrete variables to their lower bounds
                lower = 0
                if isinstance(dv, (IntegerVariable, OrdinalVariable)):
                    lower = dv.lower

                x[~is_acting[:, i], i] = lower

    def _normalize_x(self, x: np.ndarray, cs_normalize=True):
        for i, dv in enumerate(self.design_variables):
            if isinstance(dv, FloatVariable):
                if cs_normalize:
                    dv.lower = min(np.min(x[:, i]), dv.lower)
                    dv.upper = max(np.max(x[:, i]), dv.upper)
                    x[:, i] = np.clip(
                        (x[:, i] - dv.lower) / (dv.upper - dv.lower + 1e-16), 0, 1
                    )

            elif isinstance(dv, IntegerVariable):
                x[:, i] = self._round_equally_distributed(x[:, i], dv.lower, dv.upper)

                if cs_normalize:
                    # After rounding, normalize between 0 and 1, where 0 and 1 represent the stretched bounds
                    x[:, i] = (x[:, i] - dv.lower + 0.49999) / (
                        dv.upper - dv.lower + 0.9999
                    )

    def _normalize_x_no_integer(self, x: np.ndarray, cs_normalize=True):
        ordereddesign_variables = [
            self.design_variables[i] for i in self._inv_cs_var_idx
        ]
        for i, dv in enumerate(ordereddesign_variables):
            if isinstance(dv, FloatVariable):
                if cs_normalize:
                    x[:, i] = np.clip(
                        (x[:, i] - dv.lower) / (dv.upper - dv.lower + 1e-16), 0, 1
                    )

            elif isinstance(dv, (OrdinalVariable, CategoricalVariable)):
                # To ensure equal distribution of continuous values to discrete values, we first stretch-out the
                # continuous values to extend to 0.5 beyond the integer limits and then round. This ensures that the
                # values at the limits get a large-enough share of the continuous values
                x[:, i] = self._round_equally_distributed(x[:, i], dv.lower, dv.upper)

    def _cs_denormalize_x(self, x: np.ndarray):
        for i, dv in enumerate(self.design_variables):
            if isinstance(dv, FloatVariable):
                x[:, i] = x[:, i] * (dv.upper - dv.lower) + dv.lower

            elif isinstance(dv, IntegerVariable):
                # Integer values are normalized similarly to what is done in _round_equally_distributed
                x[:, i] = np.round(
                    x[:, i] * (dv.upper - dv.lower + 0.9999) + dv.lower - 0.49999
                )

    def _cs_denormalize_x_ordered(self, x: np.ndarray):
        ordereddesign_variables = [
            self.design_variables[i] for i in self._inv_cs_var_idx
        ]
        for i, dv in enumerate(ordereddesign_variables):
            if isinstance(dv, FloatVariable):
                x[:, i] = x[:, i] * (dv.upper - dv.lower) + dv.lower

            elif isinstance(dv, IntegerVariable):
                # Integer values are normalized similarly to what is done in _round_equally_distributed
                x[:, i] = np.round(
                    x[:, i] * (dv.upper - dv.lower + 0.9999) + dv.lower - 0.49999
                )

    def __str__(self):
        dvs = "\n".join([f"x{i}: {dv!s}" for i, dv in enumerate(self.design_variables)])
        return f"Design space:\n{dvs}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.design_variables!r})"


class DesignSpaceGraph(BaseDesignSpace):
    """ """

    def __init__(
        self,
        adsg=None,
        design_variables=None,
        random_state=None,
    ):
        self.random_state = random_state  # For testing
        seed = self._to_seed(random_state)
        if adsg is not None:
            self.adsg = adsg
        elif design_variables is not None:
            # to do
            self.ds_leg = DesignSpace(
                design_variables=design_variables, random_state=seed
            )
            self.adsg = _legacy_to_adsg(self.ds_leg)
            pass
        else:
            raise ValueError("Either design_variables or adsg should be provided.")

        self.graph_proc = GraphProcessor(graph=self.adsg)

        if not (HAS_ADSG):
            raise ImportError("ADSG is not installed")
        if not (HAS_CONFIG_SPACE):
            raise ImportError("ConfigSpace is not installed")

        design_space = ensure_design_space(design_space=self.adsg)
        self._design_variables = design_space.design_variables
        super().__init__(design_variables=self._design_variables, random_state=seed)
        self._cs = design_space._cs
        self._cs_cate = design_space._cs_cate
        self._is_decreed = design_space._is_decreed

    def declare_decreed_var(
        self, decreed_var: int, meta_var: int, meta_value: VarValueType
    ):
        """
        Define a conditional (decreed) variable to be active when the meta variable has (one of) the provided values.

        Parameters
        ----------
        decreed_var: int
           - Index of the conditional variable (the variable that is conditionally active)
        meta_var: int
           - Index of the meta variable (the variable that determines whether the conditional var is active)
        meta_value: int | str | list[int|str]
           - The value or list of values that the meta variable can have to activate the decreed var
        """

        self.ds_leg.declare_decreed_var(
            decreed_var=decreed_var, meta_var=meta_var, meta_value=meta_value
        )
        self.adsg = _legacy_to_adsg(self.ds_leg)
        design_space = ensure_design_space(design_space=self.adsg)
        self._design_variables = design_space.design_variables
        self._cs = design_space._cs
        self._cs_cate = design_space._cs_cate
        self._is_decreed = design_space._is_decreed
        self.graph_proc = GraphProcessor(graph=self.adsg)

    def add_value_constraint(
        self, var1: int, value1: VarValueType, var2: int, value2: VarValueType
    ):
        """
        Define a constraint where two variables cannot have the given values at the same time.

        Parameters
        ----------
        var1: int
           - Index of the first variable
        value1: int | str | list[int|str]
           - Value or values that the first variable is checked against
        var2: int
           - Index of the second variable
        value2: int | str | list[int|str]
           - Value or values that the second variable is checked against
        """

        self.ds_leg.add_value_constraint(
            var1=var1, value1=value1, var2=var2, value2=value2
        )
        self.adsg = _legacy_to_adsg(self.ds_leg)
        design_space = ensure_design_space(design_space=self.adsg)
        self._design_variables = design_space.design_variables
        self._cs = design_space._cs
        self._cs_cate = design_space._cs_cate
        self._is_decreed = design_space._is_decreed
        self.graph_proc = GraphProcessor(graph=self.adsg)

    def _sample_valid_x(
        self,
        n: int,
        random_state=None,
        return_render=False,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Sample design vectors"""
        # Get design vectors and get the is_active matrix
        configs0 = []
        configs1 = []
        configs2 = []
        for i in range(n):
            gp_get_i = self.graph_proc.get_graph(
                self.graph_proc.get_random_design_vector(), create=return_render
            )
            configs0.append(gp_get_i[0])
            configs1.append(gp_get_i[1])
            configs2.append(gp_get_i[2])

        if return_render:
            return np.array(configs1), np.array(configs2), np.array(configs0)
        else:
            return np.array(configs1), np.array(configs2)

    def correct_get_acting(self, x: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Correct the given matrix of design vectors and return the corrected vectors and the is_acting matrix.
        It is automatically detected whether input is provided in unfolded space or not.

        Parameters
        ----------
        x: np.ndarray [n_obs, dim]
           - Input variables

        Returns
        -------
        x_corrected: np.ndarray [n_obs, dim]
           - Corrected and imputed input variables
        is_acting: np.ndarray [n_obs, dim]
           - Boolean matrix specifying for each variable whether it is acting or non-acting
        """
        return self._correct_x(x)

    def _correct_x(self, x: np.ndarray):
        """
        Fill the activeness matrix (n x nx) and if needed correct design vectors (n x nx) that are partially inactive.
        Imputation of inactive variables is handled automatically.
        """
        is_discrete_mask = self.is_cat_mask
        is_active = np.copy(x)
        for i, xi in enumerate(x):
            x_arch = [
                int(val) if is_discrete_mask[j] else float(val)
                for j, val in enumerate(xi)
            ]
            _, x_imputed, is_active_arch = self.graph_proc.get_graph(
                x_arch, create=False
            )
            x[i, :] = x_imputed
            is_active[i, :] = is_active_arch
        is_active = np.array(is_active, dtype=bool)
        return x, is_active

    def _is_conditionally_acting(self) -> np.ndarray:
        # Decreed variables are the conditionally acting variables
        return np.array(self.graph_proc.dv_is_conditionally_active)


class NoDefaultConfigurationSpace(ConfigurationSpace):
    """ConfigurationSpace that supports no default configuration"""

    def get_default_configuration(self, *args, **kwargs):
        raise NotImplementedError

    def _check_default_configuration(self, *args, **kwargs):
        pass


class FixedIntegerParam(UniformIntegerHyperparameter):
    def get_neighbors(
        self,
        value: float,
        rs: np.random.RandomState,
        number: int = 4,
        transform: bool = False,
        std: float = 0.2,
    ) -> List[int]:
        # Temporary fix until https://github.com/automl/ConfigSpace/pull/313 is released
        center = self._transform(value)
        lower, upper = self.lower, self.upper
        if upper - lower - 1 < number:
            neighbors = sorted(set(range(lower, upper + 1)) - {center})
            if transform:
                return neighbors
            return self._inverse_transform(np.asarray(neighbors)).tolist()

        return super().get_neighbors(
            value, rs, number=number, transform=transform, std=std
        )


def _convert_adsg_to_legacy(adsg) -> "BaseDesignSpace":
    """Interface to turn adsg input formats into legacy DesignSpace"""
    gp = GraphProcessor(adsg)
    listvar = []
    gvars = gp._all_des_var_data[0]
    varnames = [ii.name for ii in gvars]
    for i in gvars:
        if i._bounds is not None:
            listvar.append(FloatVariable(lower=i._bounds[0], upper=i._bounds[1]))
        elif type(i.node) is SelectionChoiceNode:
            a = (
                str(i._opts)
                .replace("[", "")
                .replace("]", "")
                .replace(" ", "")
                .replace("'", "")
                .split(",")
            )
            listvar.append(CategoricalVariable(a))
        else:
            a = (
                str(i._opts)
                .replace("[", "")
                .replace("]", "")
                .replace(" ", "")
                .replace("'", "")
                .split(",")
            )
            listvar.append(OrdinalVariable(a))

    design_space = DesignSpace(listvar)

    active_vars = [i for i, x in enumerate(gp.dv_is_conditionally_active) if x]
    nodelist = list(adsg._graph.nodes)
    nodenamelist = [
        element.strip()[1:-1]
        for element in str(list(adsg._graph.nodes))[1:-1]
        .replace("D[Sel:", "[")
        .replace("DV[", "[")
        .replace(" ", "")
        .split(",")
        if element.strip().startswith("[") and element.strip().endswith("]")
    ]
    for i in range(np.sum(gp.dv_is_conditionally_active)):
        meta_values = [
            metav
            for metav in iter(
                adsg._graph.predecessors(
                    nodelist[nodenamelist.index(gvars[active_vars[i]].name)]
                )
            )
        ]
        meta_variable = next(iter(adsg._graph.predecessors(meta_values[0])))
        while str(meta_variable).split("[")[0] != "D":
            meta_values = [
                metav for metav in iter((adsg._graph.predecessors(meta_values[0])))
            ]
            meta_variable = next(iter(adsg._graph.predecessors(meta_values[0])))
        namemetavar = (
            str(meta_variable)
            .replace("D[Sel:", "")
            .replace("DV[", "")
            .replace(" ", "")
            .replace("[", "")
            .replace("]", "")
        )
        design_space.declare_decreed_var(
            decreed_var=active_vars[i],
            meta_var=varnames.index(namemetavar),
            meta_value=[str(metaval)[1:-1] for metaval in meta_values],
        )

    edges = np.array(list(adsg._graph.edges.data()))
    edgestype = [edge["type"] for edge in edges[:, 2]]
    incomp_nodes = []
    for i, edge in enumerate(edges):
        if edgestype[i] == EdgeType.INCOMPATIBILITY:
            incomp_nodes.append([edges[i][0], edges[i][1]])

    def remove_symmetry(lst):
        unique_pairs = set()

        for pair in lst:
            # Sort the pair based on the _id attribute of NamedNode
            sorted_pair = tuple(sorted(pair, key=lambda node: node._id))
            unique_pairs.add(sorted_pair)

        # Convert set of tuples back to list of lists if needed
        return [list(pair) for pair in unique_pairs]

    incomp_nodes = remove_symmetry(incomp_nodes)

    for pair in incomp_nodes:
        node1, node2 = pair
        vars1 = next(iter(adsg._graph.predecessors(node1)))
        while str(vars1).split("[")[0] != "D":
            vars1 = next(iter(adsg._graph.predecessors(node1)))
        vars2 = next(iter(adsg._graph.predecessors(node2)))
        while str(vars1).split("[")[0] != "D":
            vars2 = next(iter(adsg._graph.predecessors(node2)))
    for pair in incomp_nodes:
        node1, node2 = pair
        vars1 = next(iter(adsg._graph.predecessors(node1)))
        while str(vars1).split("[")[0] != "D":
            vars1 = next(iter(adsg._graph.predecessors(node1)))
        vars2 = next(iter(adsg._graph.predecessors(node2)))
        while str(vars1).split("[")[0] != "D":
            vars2 = next(iter(adsg._graph.predecessors(node2)))
        namevar1 = (
            str(vars1)
            .replace("D[Sel:", "")
            .replace("DV[", "")
            .replace(" ", "")
            .replace("[", "")
            .replace("]", "")
        )
        namevar2 = (
            str(vars2)
            .replace("D[Sel:", "")
            .replace("DV[", "")
            .replace(" ", "")
            .replace("[", "")
            .replace("]", "")
        )
        design_space.add_value_constraint(
            var1=varnames.index(namevar1),
            value1=[str(node1)[1:-1]],
            var2=varnames.index(namevar2),
            value2=[str(node2)[1:-1]],
        )  # Forbid more than 35 neurons with ASGD

    return design_space


def _legacy_to_adsg(legacy_ds: "DesignSpace") -> BasicADSG:
    """
    Interface to turn a legacy DesignSpace back into an ADSG instance.

    Parameters:
    legacy_ds (DesignSpace): The legacy DesignSpace instance.

    Returns:
    BasicADSG: The corresponding ADSG graph.
    """
    adsg = BasicADSG()

    # Create nodes for each variable in the DesignSpace
    nodes = {}
    value_nodes = {}  # This will store decreed value nodes
    start_nodes = set()
    for i, var in enumerate(legacy_ds._design_variables):
        if isinstance(var, FloatVariable) or isinstance(var, IntegerVariable):
            # Create a DesignVariableNode with bounds for continuous variables
            var_node = DesignVariableNode(f"x{i}", bounds=(var.lower, var.upper))
        elif isinstance(var, CategoricalVariable):
            # Create a SelectionChoiceNode for categorical variables
            var_node = NamedNode(f"x{i}")
            choices = [NamedNode(value) for value in var.values]
            value_nodes[f"x{i}"] = (
                choices  # Store decreed value nodes for this variable
            )
            adsg.add_selection_choice(f"choice_x{i}", var_node, choices)
        elif isinstance(var, OrdinalVariable):
            # Create a SelectionChoiceNode for ordinal variables (ordinal treated like categorical)
            var_node = NamedNode(f"x{i}")
            choices = [NamedNode(value) for value in var.values]
            value_nodes[f"x{i}"] = (
                choices  # Store decreed value nodes for this variable
            )
            adsg.add_selection_choice(f"choice_x{i}", var_node, choices)
        else:
            raise ValueError(f"Unsupported variable type: {type(var)}")

        adsg.add_node(var_node)
        nodes[f"x{i}"] = var_node
        start_nodes.add(var_node)

    # Handle decreed variables (conditional dependencies)
    for decreed_var in legacy_ds._cs._conditionals:
        decreed_node = nodes[f"{decreed_var}"]
        if decreed_node in start_nodes:
            start_nodes.remove(decreed_node)
        # Get parent condition(s) from the legacy design space
        parent_conditions = legacy_ds._cs._parent_conditions_of[decreed_var]
        for condition in parent_conditions:
            meta_var = condition.parent.name  # Parent variable
            try:
                meta_values = (
                    condition.values
                )  # Values that activate the decreed variable
            except AttributeError:
                meta_values = [condition.value]

            # Add conditional decreed edges
            for value in meta_values:
                meta_nodes = [node for node in value_nodes[f"{meta_var}"]]
                meta_node_ind = [
                    node.name for node in value_nodes[f"{meta_var}"]
                ].index(str(value)[:])
                value_node = meta_nodes[meta_node_ind]

                nodes[f"x{legacy_ds._cs._hyperparameter_idx[meta_var]}"]
                adsg.add_edge(
                    value_node, decreed_node
                )  # Linking decreed node to meta node

    # Handle value constraints (incompatibilities)
    for value_constraint in legacy_ds._cs.forbidden_clauses:
        clause1 = value_constraint.components[0]
        var1 = clause1.hyperparameter.name
        values1 = clause1.value or clause1.values
        clause2 = value_constraint.components[1]
        var2 = clause2.hyperparameter.name
        values2 = clause2.value or clause2.values

        for value1 in values1:
            for value2 in values2:
                # Retrieve decreed value nodes from value_nodes
                value_nodes1 = [node for node in value_nodes[f"{var1}"]]
                value_node1_ind = [node.name for node in value_nodes[f"{var1}"]].index(
                    str(value1)[:]
                )
                value_node1 = value_nodes1[value_node1_ind]
                value_nodes2 = [node for node in value_nodes[f"{var2}"]]
                value_node2_ind = [node.name for node in value_nodes[f"{var2}"]].index(
                    str(value2)[:]
                )
                value_node2 = value_nodes2[value_node2_ind]
                if value_node1 and value_node2:
                    # Add incompatibility constraint between the two value nodes
                    adsg.add_incompatibility_constraint([value_node1, value_node2])
    adsg = adsg.set_start_nodes(start_nodes)
    return adsg

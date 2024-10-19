from .iai import _IAI, _iai_version_less_than, _requires_iai_version
from .iaitrees import (Learner, TreeLearner, ClassificationTreeLearner,
                       RegressionTreeLearner, SurvivalTreeLearner,
                       PrescriptionTreeLearner, PolicyTreeLearner,
                       ClassificationTreeMultiLearner,
                       RegressionTreeMultiLearner)
import warnings as _warnings


class OptimalTreeLearner(TreeLearner):
    """Abstract type encompassing all optimal tree learners.

    Julia Equivalent:
    `IAI.OptimalTreeLearner <https://docs.interpretable.ai/v3.2.2/OptimalTrees/reference/#IAI.OptimalTreeLearner>`
    """
    def __init__(self, f, *args, refit_learner=None, **kwargs):
        if refit_learner:
            if not isinstance(refit_learner, Learner):
                raise TypeError(
                    "`refit_learner` needs to be a learner or grid search")
            kwargs = dict(kwargs, refit_learner=refit_learner._jl_obj)

        jl_obj = f(*args, **kwargs)
        super().__init__(jl_obj)

    def refit_leaves(self, *args, refit_learner=None, **kwargs):
        """Refit the models in the leaves of the trained learner using the
        supplied data.

        Julia Equivalent:
        `IAI.refit_leaves! <https://docs.interpretable.ai/v3.2.2/OptimalTrees/reference/#IAI.refit_leaves!>`

        Examples
        --------
        >>> lnr.refit_leaves(X, y)

        Parameters
        ----------
        Refer to the Julia documentation for available parameters.

        Compatibility
        -------------
        Requires IAI version 3.0 or higher.
        """
        _requires_iai_version("3.0.0", "refit_leaves")

        if refit_learner:
            if not isinstance(refit_learner, Learner):
                raise TypeError(
                    "`refit_learner` needs to be a learner or grid search")
            kwargs = dict(kwargs, refit_learner=refit_learner._jl_obj)

        _IAI.refit_leaves_convert(self._jl_obj, *args, **kwargs)
        return self

    def copy_splits_and_refit_leaves(self, orig_lnr, *args, refit_learner=None,
                                     **kwargs):
        """Copy the tree split structure from `orig_lnr` into this learner and
        refit the models in each leaf of the tree using the supplied data.

        Julia Equivalent:
        `IAI.copy_splits_and_refit_leaves! <https://docs.interpretable.ai/v3.2.2/OptimalTrees/reference/#IAI.copy_splits_and_refit_leaves!>`

        Examples
        --------
        >>> lnr.copy_splits_and_refit_leaves(orig_lnr, X, y)

        Parameters
        ----------
        Refer to the Julia documentation for available parameters.

        Compatibility
        -------------
        Requires IAI version 3.0 or higher.
        """
        _requires_iai_version("3.0.0", "copy_splits_and_refit_leaves")

        if not isinstance(orig_lnr, Learner):
            raise TypeError("`orig_lnr` needs to be a learner or grid search")
        orig_lnr = orig_lnr._jl_obj

        if refit_learner:
            if not isinstance(refit_learner, Learner):
                raise TypeError(
                    "`refit_learner` needs to be a learner or grid search")
            kwargs = dict(kwargs, refit_learner=refit_learner._jl_obj)

        _IAI.copy_splits_and_refit_leaves_convert(
            self._jl_obj, orig_lnr, *args, **kwargs)
        return self

    def prune_trees(self, *args, **kwargs):
        """Use the trained trees in the learner along with the supplied
        validation data `X` and `y` to determine the best value for the `cp`
        parameter and then prune the trees according to this value.

        Julia Equivalent:
        `IAI.prune_trees! <https://docs.interpretable.ai/v3.2.2/OptimalTrees/reference/#IAI.prune_trees!>`

        Examples
        --------
        >>> lnr.prune_trees(X, y)

        Parameters
        ----------
        Refer to the Julia documentation for available parameters.

        Compatibility
        -------------
        Requires IAI version 3.0 or higher.
        """
        _requires_iai_version("3.0.0", "prune_trees")
        _IAI.prune_trees_convert(self._jl_obj, *args, **kwargs)
        return self


class OptimalTreeClassifier(OptimalTreeLearner, ClassificationTreeLearner):
    """Learner for training Optimal Classification Trees.

    Julia Equivalent:
    `IAI.OptimalTreeClassifier <https://docs.interpretable.ai/v3.2.2/OptimalTrees/reference/#IAI.OptimalTreeClassifier>`

    Examples
    --------
    >>> iai.OptimalTreeClassifier(**kwargs)

    Parameters
    ----------
    Use keyword arguments to set parameters on the resulting learner. Refer to
    the Julia documentation for available parameters.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(_IAI.OptimalTreeClassifier_convert, *args, **kwargs)


class OptimalTreeRegressor(OptimalTreeLearner, RegressionTreeLearner):
    """Learner for training Optimal Regression Trees.

    Julia Equivalent:
    `IAI.OptimalTreeRegressor <https://docs.interpretable.ai/v3.2.2/OptimalTrees/reference/#IAI.OptimalTreeRegressor>`

    Examples
    --------
    >>> iai.OptimalTreeRegressor(**kwargs)

    Parameters
    ----------
    Use keyword arguments to set parameters on the resulting learner. Refer to
    the Julia documentation for available parameters.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(_IAI.OptimalTreeRegressor_convert, *args, **kwargs)


class OptimalTreeSurvivalLearner(OptimalTreeLearner, SurvivalTreeLearner):
    """Learner for training Optimal Survival Trees.

    Julia Equivalent:
    `IAI.OptimalTreeSurvivalLearner <https://docs.interpretable.ai/v3.2.2/OptimalTrees/reference/#IAI.OptimalTreeSurvivalLearner>`

    Examples
    --------
    >>> iai.OptimalTreeSurvivalLearner(**kwargs)

    Parameters
    ----------
    Use keyword arguments to set parameters on the resulting learner. Refer to
    the Julia documentation for available parameters.
    """
    def __init__(self, *args, **kwargs):
        if _iai_version_less_than("2.0.0"):
            f = _IAI.OptimalTreeSurvivor_convert
        else:
            f = _IAI.OptimalTreeSurvivalLearner_convert
        super().__init__(f, *args, **kwargs)


class OptimalTreeSurvivor(OptimalTreeSurvivalLearner):
    """Learner for training Optimal Survival Trees.

    This class was deprecated and renamed to OptimalTreeSurvivalLearner in
    interpretableai 2.0.2. This is for consistency with the IAI v2.0.0 Julia
    release.
    """
    def __init__(self, *args, **kwargs):
        _warnings.warn(
            "'OptimalTreeSurvivor' is deprecated, use " +
            "'OptimalTreeSurvivalLearner'",
            FutureWarning
        )
        super().__init__(*args, **kwargs)


class OptimalTreePrescriptionMinimizer(OptimalTreeLearner,
                                       PrescriptionTreeLearner):
    """Learner for training Optimal Prescriptive Trees where the prescriptions
    should aim to minimize outcomes.

    Julia Equivalent:
    `IAI.OptimalTreePrescriptionMinimizer <https://docs.interpretable.ai/v3.2.2/OptimalTrees/reference/#IAI.OptimalTreePrescriptionMinimizer>`

    Examples
    --------
    >>> iai.OptimalTreePrescriptionMinimizer(**kwargs)

    Parameters
    ----------
    Use keyword arguments to set parameters on the resulting learner. Refer to
    the Julia documentation for available parameters.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(_IAI.OptimalTreePrescriptionMinimizer_convert, *args,
                         **kwargs)


class OptimalTreePrescriptionMaximizer(OptimalTreeLearner,
                                       PrescriptionTreeLearner):
    """Learner for training Optimal Prescriptive Trees where the prescriptions
    should aim to maximize outcomes.

    Julia Equivalent:
    `IAI.OptimalTreePrescriptionMaximizer <https://docs.interpretable.ai/v3.2.2/OptimalTrees/reference/#IAI.OptimalTreePrescriptionMaximizer>`

    Examples
    --------
    >>> iai.OptimalTreePrescriptionMaximizer(**kwargs)

    Parameters
    ----------
    Use keyword arguments to set parameters on the resulting learner. Refer to
    the Julia documentation for available parameters.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(_IAI.OptimalTreePrescriptionMaximizer_convert, *args,
                         **kwargs)


class OptimalTreePolicyMinimizer(OptimalTreeLearner, PolicyTreeLearner):
    """Learner for training Optimal Policy Trees where the policy
    should aim to minimize outcomes.

    Julia Equivalent:
    `IAI.OptimalTreePolicyMinimizer <https://docs.interpretable.ai/v3.2.2/OptimalTrees/reference/#IAI.OptimalTreePolicyMinimizer>`

    Examples
    --------
    >>> iai.OptimalTreePolicyMinimizer(**kwargs)

    Parameters
    ----------
    Use keyword arguments to set parameters on the resulting learner. Refer to
    the Julia documentation for available parameters.

    Compatibility
    -------------
    Requires IAI version 2.0 or higher.
    """
    def __init__(self, *args, **kwargs):
        _requires_iai_version("2.0.0", "OptimalTreePolicyMinimizer")
        super().__init__(_IAI.OptimalTreePolicyMinimizer_convert, *args,
                         **kwargs)


class OptimalTreePolicyMaximizer(OptimalTreeLearner, PolicyTreeLearner):
    """Learner for training Optimal Policy Trees where the policy
    should aim to maximize outcomes.

    Julia Equivalent:
    `IAI.OptimalTreePolicyMaximizer <https://docs.interpretable.ai/v3.2.2/OptimalTrees/reference/#IAI.OptimalTreePolicyMaximizer>`

    Examples
    --------
    >>> iai.OptimalTreePolicyMaximizer(**kwargs)

    Parameters
    ----------
    Use keyword arguments to set parameters on the resulting learner. Refer to
    the Julia documentation for available parameters.

    Compatibility
    -------------
    Requires IAI version 2.0 or higher.
    """
    def __init__(self, *args, **kwargs):
        _requires_iai_version("2.0.0", "OptimalTreePolicyMaximizer")
        super().__init__(_IAI.OptimalTreePolicyMaximizer_convert, *args,
                         **kwargs)


class OptimalTreeMultiLearner(OptimalTreeLearner):
    """Abstract type encompassing all multi-task optimal tree learners.

    Julia Equivalent:
    `IAI.OptimalTreeMultiLearner <https://docs.interpretable.ai/v3.2.2/OptimalTrees/reference/#IAI.OptimalTreeMultiLearner>`
    """


class OptimalTreeMultiClassifier(OptimalTreeMultiLearner,
                                 ClassificationTreeMultiLearner):
    """Learner for training multi-task Optimal Classification Trees.

    Julia Equivalent:
    `IAI.OptimalTreeMultiClassifier <https://docs.interpretable.ai/v3.2.2/OptimalTrees/reference/#IAI.OptimalTreeMultiClassifier>`

    Examples
    --------
    >>> iai.OptimalTreeMultiClassifier(**kwargs)

    Parameters
    ----------
    Use keyword arguments to set parameters on the resulting learner. Refer to
    the Julia documentation for available parameters.

    Compatibility
    -------------
    Requires IAI version 3.2 or higher.
    """
    def __init__(self, *args, **kwargs):
        _requires_iai_version("3.2.0", "OptimalTreeMultiClassifier")
        super().__init__(_IAI.OptimalTreeMultiClassifier_convert, *args,
                         **kwargs)


class OptimalTreeMultiRegressor(OptimalTreeMultiLearner,
                                RegressionTreeMultiLearner):
    """Learner for training multi-task Optimal Regression Trees.

    Julia Equivalent:
    `IAI.OptimalTreeMultiRegressor <https://docs.interpretable.ai/v3.2.2/OptimalTrees/reference/#IAI.OptimalTreeMultiRegressor>`

    Examples
    --------
    >>> iai.OptimalTreeMultiRegressor(**kwargs)

    Parameters
    ----------
    Use keyword arguments to set parameters on the resulting learner. Refer to
    the Julia documentation for available parameters.

    Compatibility
    -------------
    Requires IAI version 3.2 or higher.
    """
    def __init__(self, *args, **kwargs):
        _requires_iai_version("3.2.0", "OptimalTreeMultiRegressor")
        super().__init__(_IAI.OptimalTreeMultiRegressor_convert, *args,
                         **kwargs)

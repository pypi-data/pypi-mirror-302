from .iai import (_IAI, _Main, _requires_iai_version, _iai_version_less_than,
                  _get_learner_type, _load_julia_module)
import warnings as _warnings
import numpy as _np
import pandas as _pd


def split_data(*args, **kwargs):
    """Split the data (`X` and `y`) into a tuple of training and testing data,
    `(X_train, y_train), (X_test, y_test)`, for a problem of type `task`.

    Julia Equivalent:
    `IAI.split_data <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.split_data>`

    Examples
    --------
    >>> iai.split_data(task, X, *y, **kwargs)
    """
    return _IAI.split_data_convert(*args, **kwargs)


def set_rich_output_param(*args, **kwargs):
    """Sets the global rich output parameter `key` to `value`.

    Julia Equivalent:
    `IAI.set_rich_output_param! <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.set_rich_output_param!>`

    Examples
    --------
    >>> iai.set_rich_output_param(key, value)
    """
    return _IAI.set_rich_output_param_convert(*args, **kwargs)


def get_rich_output_params(*args, **kwargs):
    """Return the current global rich output parameter settings.

    Julia Equivalent:
    `IAI.get_rich_output_params <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.get_rich_output_params>`

    Examples
    --------
    >>> iai.get_rich_output_params()
    """
    return _IAI.get_rich_output_params_convert(*args, **kwargs)


def delete_rich_output_param(*args, **kwargs):
    """Delete the global rich output parameter `key`.

    Julia Equivalent:
    `IAI.delete_rich_output_param! <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.delete_rich_output_param!>`

    Examples
    --------
    >>> iai.delete_rich_output_param(key)
    """
    return _IAI.delete_rich_output_param_convert(*args, **kwargs)


def read_json(filename):
    """Read in a learner or grid saved in JSON format from `filename`.

    Julia Equivalent:
    `IAI.read_json <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.read_json>`

    Examples
    --------
    >>> iai.read_json(filename)
    """

    jl_obj = _IAI.read_json_convert(filename)
    return _wrap_jl_learner(jl_obj)


def resume_from_checkpoint(checkpoint_file):
    """Resume training from the supplied `checkpoint_file`.

    Julia Equivalent:
    `IAI.resume_from_checkpoint <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.resume_from_checkpoint>`

    Examples
    --------
    >>> iai.resume_from_checkpoint(checkpoint_file)

    Compatibility
    -------------
    Requires IAI version 3.1 or higher.
    """
    _requires_iai_version("3.1.0", "resume_from_checkpoint")
    out = _IAI.resume_from_checkpoint_convert(checkpoint_file)
    if type(out) == tuple:
        return _wrap_jl_learner(out[0]), out[1]
    else:
        return _wrap_jl_learner(out)


def _wrap_jl_learner(jl_obj):
    if _Main.isa(jl_obj, _IAI.GridSearch):
        lnr = _get_learner_type(_IAI.get_learner(jl_obj))()
        grid = GridSearch(lnr)
        grid._jl_obj = jl_obj
        return grid
    else:
        lnr = _get_learner_type(jl_obj)()
        Learner.__init__(lnr, jl_obj)
        return lnr


def score(*args, **kwargs):
    """Calculates the score attained by `predictions` against the true target
    `truths` for the problem type indicated by `task`.

    Julia Equivalent:
    `IAI.score <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.score-Tuple%7BUnion%7BAbstractString%2C%20Symbol%7D%2C%20Vararg%7BAny%7D%7D>`

    Examples
    --------
    >>> iai.score(task, predictions, *truths, **kwargs)

    Compatibility
    -------------
    Requires IAI version 2.1 or higher.
    """
    _requires_iai_version("2.1.0", "score")
    return _IAI.score_convert(*args, **kwargs)


class AbstractVisualization():
    """Abstract type encompassing objects related to visualization.

    Julia Equivalent:
    `IAI.AbstractVisualization <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.AbstractVisualization>`
    """
    def __init__(self, jl_obj):
        self._jl_obj = jl_obj

    def __repr__(self):
        return _IAI.string(self._jl_obj)

    def _repr_html_(self):
        return _IAI.to_html(self._jl_obj)

    def write_html(self, filename, **kwargs):
        """Write interactive browser visualization to `filename` as HTML.

        Julia Equivalent:
        `IAI.write_html <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.write_html-Tuple%7BAny%2C%20AbstractVisualization%7D>`

        Examples
        --------
        >>> treeplot.write_html(filename, **kwargs)
        """
        return _IAI.write_html_convert(filename, self._jl_obj, **kwargs)

    def show_in_browser(self, **kwargs):  # pragma: no cover
        """Show interactive visualization in default browser.

        Julia Equivalent:
        `IAI.show_in_browser <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.show_in_browser-Tuple%7BAbstractVisualization%7D>`

        Examples
        --------
        >>> treeplot.show_in_browser(**kwargs)
        """
        return _IAI.show_in_browser_convert(self._jl_obj, **kwargs)


class Questionnaire(AbstractVisualization):
    """Specifies an interactive questionnaire.

    Julia Equivalent:
    `IAI.Questionnaire <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.Questionnaire-Tuple%7BLearner%7D>`

    Parameters
    ----------

    Refer to the
    `Julia documentation on advanced tree visualization <https://docs.interpretable.ai/v3.2.2/IAITrees/advanced/#Advanced-Visualization-1>`
    for available parameters.

    Compatibility
    -------------
    Requires IAI version 1.1 or higher.
    """
    def __init__(self, lnr, **kwargs):
        _requires_iai_version("1.1.0", "Questionnaire")

        if isinstance(lnr, Learner):
            _warnings.warn(
                "'iai.Questionnaire(lnr)' is deprecated, use " +
                "`lnr.Questionnaire(...)`",
                FutureWarning
            )
            jl_obj = _IAI.Questionnaire_convert(lnr._jl_obj, **kwargs)
        else:
            jl_obj = _IAI.Questionnaire_convert(lnr, **kwargs)
        super().__init__(jl_obj)


class MultiQuestionnaire(AbstractVisualization):
    """Specify an interactive questionnaire of multiple learners

    Examples
    --------
    Constructs an interactive questionnaire using multiple learners from
    specified questions. Refer to the
    `documentation on advanced tree visualization <https://docs.interpretable.ai/v3.2.2/IAI-Python/julia/#Python-Interactive-Visualizations-1>`
    for more information.

    Julia Equivalent:
    `IAI.MultiQuestionnaire <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.MultiQuestionnaire-Tuple%7BPair%7D>`

    >>> iai.MultiQuestionnaire(questions)

    Compatibility
    -------------
    Requires IAI version 1.1 or higher.
    """
    def __init__(self, *args):
        if len(args) > 0 and isinstance(args[0], GridSearch):
            _requires_iai_version("2.0.0", "MultiQuestionnaire")
            args = list(args)
            grid = args.pop(0)

            _warnings.warn(
                "'iai.MultiQuestionnaire(grid, ...)' is deprecated, use " +
                "`grid.MultiQuestionnaire(...)`",
                FutureWarning
            )

            jl_obj = _IAI.MultiQuestionnaire_convert(grid._jl_obj, *args)
        else:
            _requires_iai_version("1.1.0", "MultiQuestionnaire")
            jl_obj = _IAI.MultiQuestionnaire_convert(*args)
        super().__init__(jl_obj)


class Learner():
    """Abstract type encompassing all learners.

    Julia Equivalent:
    `IAI.Learner <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.Learner>`
    """
    def __init__(self, jl_obj):
        self._jl_obj = jl_obj

    def __repr__(self):
        return _IAI.string(self._jl_obj)

    def _repr_html_(self):
        return _IAI.to_html(self._jl_obj)

    def __getstate__(self):
        if isinstance(self, GridSearch):
            _requires_iai_version("1.1.0", "pickle (for GridSearch)")
        return {'_jl_obj_json': _IAI.to_json(self._jl_obj)}

    def __setstate__(self, state):
        self._jl_obj = _IAI.from_json(state['_jl_obj_json'])
        if isinstance(self, GridSearch):
            self._lnr_type = _get_learner_type(_IAI.get_learner(self._jl_obj))
        return self

    def __copy__(self):
        raise NotImplementedError(
            "'copy.copy' is not supported, use 'copy.deepcopy' instead")

    def __deepcopy__(self, memo):
        new_lnr = object.__new__(type(self))
        Learner.__init__(new_lnr, _Main.deepcopy(self._jl_obj))
        if isinstance(self, GridSearch):
            new_lnr._lnr_type = self._lnr_type
        return new_lnr

    def __eq__(self, other):
        if isinstance(other, Learner):
            return _Main.isequal(self._jl_obj, other._jl_obj)
        return False

    # Fallback to hitting learner fields if not a grid search
    def __getattr__(self, item):
        if not isinstance(self, GridSearch):
            try:
                return getattr(self._jl_obj, item)
            except AttributeError:
                pass  # Show our nicer AttributeError instead
        raise AttributeError(
            "'{0}' object has no attribute '{1}'".format(type(self).__name__,
                                                         item),
        )

    # Fallback to hitting learner fields if not a grid search
    def __setattr__(self, item, value):
        if item.startswith('_'):
            return super().__setattr__(item, value)
        if not isinstance(self, GridSearch):
            # Only try to set the value if the field exists on the Julia object
            if _IAI.hasattr(self._jl_obj, item):
                return _IAI.setattr(self._jl_obj, item, value)
        raise AttributeError(
            "'{0}' object has no attribute '{1}'".format(type(self).__name__,
                                                         item),
        )

    def fit(self, *args, **kwargs):
        """Fit a model using the parameters in learner and the data `X` and `y`.

        Julia Equivalent:
        `IAI.fit! <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.fit%21-Tuple%7BLearner%7D>`

        Examples
        --------
        >>> lnr.fit(X, *y, sample_weight=None)

        Parameters
        ----------
        Refer to the documentation on
        `data preparation <https://docs.interpretable.ai/v3.2.2/IAI-Python/data/#Python-Data-Preparation-Guide-1>`
        for information on how to format and supply the data.
        """
        _IAI.fit_convert(self._jl_obj, *args, **kwargs)
        return self

    def write_json(self, filename, **kwargs):
        """Write learner or grid to `filename` in JSON format.

        Julia Equivalent:
        `IAI.write_json <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.write_json>`

        Examples
        --------
        >>> lnr.write_json(filename, **kwargs)
        """
        if isinstance(self, GridSearch):
            _requires_iai_version("1.1.0", "write_json (for GridSearch)")

        return _IAI.write_json_convert(filename, self._jl_obj, **kwargs)

    def get_params(self):
        """Return the value of all learner parameters.

        Julia Equivalent:
        `IAI.get_params <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.get_params>`

        Examples
        --------
        >>> lnr.get_params()
        """
        if isinstance(self, GridSearch):  # pragma: no cover
            raise AttributeError(
                "'GridSearch' object has no attribute 'get_params")
        return _IAI.get_params_convert(self._jl_obj)

    def set_params(self, **kwargs):
        """Set all supplied parameters on learner.

        Julia Equivalent:
        `IAI.set_params! <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.set_params!>`

        Examples
        --------
        >>> lnr.set_params(**kwargs)
        """
        if isinstance(self, GridSearch):  # pragma: no cover
            raise AttributeError(
                "'GridSearch' object has no attribute 'set_params")
        _IAI.set_params_convert(self._jl_obj, **kwargs)
        return self

    def clone(self):
        """Return an unfitted copy of the learner with the same parameters.

        Julia Equivalent:
        `IAI.clone <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.clone>`

        Examples
        --------
        >>> lnr.clone()
        """
        if isinstance(self, GridSearch):  # pragma: no cover
            raise AttributeError("'GridSearch' object has no attribute 'clone'")
        # Copy the object
        lnr = object.__new__(type(self))
        Learner.__init__(lnr, _IAI.clone(self._jl_obj))
        return lnr

    def variable_importance(self, *args, **kwargs):
        """Generate a ranking of the variables in the learner according to
        their importance during training. The results are normalized so that
        they sum to one.

        Julia Equivalent:
        `IAI.variable_importance <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.variable_importance-Tuple%7BLearner%7D>`

        Examples
        --------
        >>> lnr.variable_importance()
        """
        return _IAI.variable_importance_convert(self._jl_obj, *args, **kwargs)

    def get_features_used(self):
        """Return a list of feature names used by the learner.

        Julia Equivalent:
        `IAI.get_features_used <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.get_features_used-Tuple%7BLearner%7D>`

        Examples
        --------
        >>> lnr.get_features_used()

        Compatibility
        -------------
        Requires IAI version 2.2 or higher.
        """
        _requires_iai_version("2.2.0", "get_features_used")
        return _IAI.get_features_used_convert(self._jl_obj)


class MultiLearner(Learner):
    """Abstract type encompassing all multi-task learners for supervised tasks.

    Julia Equivalent:
    `IAI.MultiLearner <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.MultiLearner>`
    """
    pass


class SupervisedLearner(Learner):
    """Abstract type encompassing all learners for supervised tasks.

    Julia Equivalent:
    `IAI.SupervisedLearner <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.SupervisedLearner>`
    """

    def predict(self, *args, **kwargs):
        """Return the predictions made by the learner for each point in the
        features `X`.

        Julia Equivalent:
        `IAI.predict <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.predict-Tuple%7BSupervisedLearner%2C%20Union%7BDataFrames.AbstractDataFrame%2C%20AbstractMatrix%7B%3C%3AReal%7D%7D%7D>`

        Examples
        --------
        >>> lnr.predict(X)
        """
        return _IAI.predict_convert(self._jl_obj, *args, **kwargs)

    def score(self, *args, **kwargs):
        """Calculates the score for the learner on data `X` and `y`.

        Julia Equivalent:
        `IAI.score <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.score-Tuple%7BSupervisedLearner%7D>`

        Examples
        --------
        >>> lnr.score(X, *y, **kwargs)
        """
        return _IAI.score_convert(self._jl_obj, *args, **kwargs)


class SupervisedMultiLearner(MultiLearner):
    """Abstract type encompassing all multi-task learners for supervised tasks.

    Julia Equivalent:
    `IAI.SupervisedMultiLearner <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.SupervisedMultiLearner>`
    """

    def predict(self, *args, **kwargs):
        """Return the predictions made by the learner for each point in the
        features `X`.

        Examples
        --------
        Return the predictions for all tasks.

        Julia Equivalent:
        `IAI.predict <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.predict-Tuple%7BLearner%7BIAIBase.MultiTask%7BT%7D%7D%20where%20T%3C%3AIAIBase.SupervisedTask%2C%20Union%7BDataFrames.AbstractDataFrame%2C%20AbstractMatrix%7B%3C%3AReal%7D%7D%7D>`

        >>> lnr.predict(X)

        Return the predictions for a specified task.

        Julia Equivalent:
        `IAI.predict <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.predict-Tuple%7BLearner%7BIAIBase.MultiTask%7BT%7D%7D%20where%20T%3C%3AIAIBase.SupervisedTask%2C%20Union%7BDataFrames.AbstractDataFrame%2C%20AbstractMatrix%7B%3C%3AReal%7D%7D%2C%20Symbol%7D>`

        >>> lnr.predict(X, task_label)

        Compatibility
        -------------
        Requires IAI version 3.2 or higher.
        """
        _requires_iai_version("3.2.0", "predict")
        return super().predict(*args, **kwargs)

    def score(self, *args, **kwargs):
        """Calculates the score for the learner on data `X` and `y`.

        Julia Equivalent:
        `IAI.score <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.score-Tuple%7BSupervisedLearner%7D>`

        Examples
        --------
        Return the average score across all tasks.

        Julia Equivalent:
        `IAI.score <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.score-Tuple%7BLearner%7BIAIBase.MultiTask%7BT%7D%7D%20where%20T%3C%3AIAIBase.SupervisedTask%7D>`

        >>> lnr.score(X, *y, **kwargs)

        Return the score for a specified task.

        Julia Equivalent:
        `IAI.score <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.score-Tuple%7BLearner%7BIAIBase.MultiTask%7BT%7D%7D%20where%20T%3C%3AIAIBase.SupervisedTask%2C%20Symbol%7D>`

        >>> lnr.score(X, *y, task_label, **kwargs)

        Compatibility
        -------------
        Requires IAI version 3.2 or higher.
        """
        _requires_iai_version("3.2.0", "score")
        return super().score(*args, **kwargs)


class UnsupervisedLearner(Learner):
    """Abstract type encompassing all learners for unsupervised tasks.

    Julia Equivalent:
    `IAI.UnsupervisedLearner <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.UnsupervisedLearner>`
    """
    pass


class ClassificationLearner(SupervisedLearner):
    """Abstract type encompassing all learners for classification tasks.

    Julia Equivalent:
    `IAI.ClassificationLearner <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.ClassificationLearner>`
    """

    def predict_proba(self, *args, **kwargs):
        """Return the probabilities of class membership predicted by the
        learner for each point in the features `X`.

        Julia Equivalent:
        `IAI.predict_proba <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.predict_proba-Tuple%7BClassificationLearner%2C%20Union%7BDataFrames.AbstractDataFrame%2C%20AbstractMatrix%7B%3C%3AReal%7D%7D%7D>`

        Examples
        --------
        >>> lnr.predict_proba(X)
        """
        return _IAI.predict_proba_convert(self._jl_obj, *args, **kwargs)

    def ROCCurve(self, *args, **kwargs):
        """Construct an
        :meth:`interpretableai.iai.ROCCurve`
        using the trained learner on the features `X` and labels `y`

        Julia Equivalent:
        `IAI.ROCCurve <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.ROCCurve-Tuple%7BClassificationLearner%2C%20Union%7BDataFrames.AbstractDataFrame%2C%20AbstractMatrix%7B%3C%3AReal%7D%7D%2C%20AbstractVector%7D>`

        Examples
        --------
        >>> lnr.ROCCurve(X, y)
        """
        return ROCCurve(self._jl_obj, *args, **kwargs)


class ClassificationMultiLearner(SupervisedMultiLearner, ClassificationLearner):
    """Abstract type encompassing all multi-task learners for classification
    tasks.

    Julia Equivalent:
    `IAI.ClassificationMultiLearner <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.ClassificationMultiLearner>`
    """

    def predict_proba(self, *args, **kwargs):
        """Return the probabilities of class membership predicted by the
        learner for each point in the features `X`.

        Examples
        --------
        Return the predictions for all tasks.

        Julia Equivalent:
        `IAI.predict_proba <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.predict_proba-Tuple%7BLearner%7BIAIBase.MultiTask%7BIAIBase.ClassificationTask%7D%7D%2C%20Union%7BDataFrames.AbstractDataFrame%2C%20AbstractMatrix%7B%3C%3AReal%7D%7D%7D>`

        >>> lnr.predict_proba(X)

        Return the predictions for a specified task.

        Julia Equivalent:
        `IAI.predict_proba <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.predict_proba-Tuple%7BLearner%7BIAIBase.MultiTask%7BIAIBase.ClassificationTask%7D%7D%2C%20Union%7BDataFrames.AbstractDataFrame%2C%20AbstractMatrix%7B%3C%3AReal%7D%7D%2C%20Symbol%7D>`

        >>> lnr.predict_proba(X, task_label)

        Compatibility
        -------------
        Requires IAI version 3.2 or higher.
        """
        _requires_iai_version("3.2.0", "predict_proba")
        return super().predict_proba(*args, **kwargs)

    def ROCCurve(self, *args, **kwargs):
        """Construct an
        :meth:`interpretableai.iai.ROCCurve`
        using the trained learner on the features `X` and labels `y`

        Examples
        --------
        Return the curve for all tasks.

        Julia Equivalent:
        `IAI.ROCCurve <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.ROCCurve-Tuple%7BLearner%7BIAIBase.MultiTask%7BIAIBase.ClassificationTask%7D%7D%2C%20Union%7BDataFrames.AbstractDataFrame%2C%20AbstractMatrix%7B%3C%3AReal%7D%7D%2C%20Union%7BDataFrames.AbstractDataFrame%2C%20AbstractMatrix%7D%7D>`

        >>> lnr.ROCCurve(X)

        Return the curve for a specified task.

        Julia Equivalent:
        `IAI.ROCCurve <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.ROCCurve-Tuple%7BLearner%7BIAIBase.MultiTask%7BIAIBase.ClassificationTask%7D%7D%2C%20Union%7BDataFrames.AbstractDataFrame%2C%20AbstractMatrix%7B%3C%3AReal%7D%7D%2C%20Union%7BDataFrames.AbstractDataFrame%2C%20AbstractMatrix%7D%2C%20Symbol%7D>`

        >>> lnr.ROCCurve(X, task_label)

        Compatibility
        -------------
        Requires IAI version 3.2 or higher.
        """
        _requires_iai_version("3.2.0", "ROCCurve")
        out = super().ROCCurve(*args, **kwargs)
        if isinstance(out._jl_obj, dict):
            out = {k: ROCCurve(v) for k, v in out._jl_obj.items()}
        return out


class RegressionLearner(SupervisedLearner):
    """Abstract type encompassing all learners for regression tasks.

    Julia Equivalent:
    `IAI.RegressionLearner <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.RegressionLearner>`
    """
    pass


class RegressionMultiLearner(SupervisedMultiLearner, RegressionLearner):
    """Abstract type encompassing all multi-task learners for regression tasks.

    Julia Equivalent:
    `IAI.RegressionMultiLearner <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.RegressionMultiLearner>`
    """
    pass


class SurvivalLearner(SupervisedLearner):
    """Abstract type encompassing all learners for survival tasks.

    Julia Equivalent:
    `IAI.SurvivalLearner <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.SurvivalLearner>`
    """

    def predict(self, *args, **kwargs):
        """
        Return the predictions made by the learner for each point in the
        features `X` (see
        :meth:`interpretableai.iai.SupervisedLearner.predict`)..

        Julia Equivalent:
        `IAI.predict <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.predict-Tuple%7BSurvivalLearner%2C%20Union%7BDataFrames.AbstractDataFrame%2C%20AbstractMatrix%7B%3C%3AReal%7D%7D%7D>`

        Examples
        --------
        Return the :meth:`interpretableai.iai.SurvivalCurve` predicted by the
        trained learner for each point in the data.

        >>> lnr.predict(X)

        Return the probability that death occurs at or before time `t` as
        predicted by the trained learner for each point.

        >>> lnr.predict(X, t=t)
        """
        out = _IAI.predict_convert(self._jl_obj, *args, **kwargs)
        if len(out) > 0 and out[0].__class__.__name__ == 'jlwrap':
            return [SurvivalCurve(jl_curve) for jl_curve in out]
        else:
            return _np.array(out)

    def predict_expected_survival_time(self, *args, **kwargs):
        """Return the expected survival time estimate made by the learner for
        each point in the data `X`.

        Julia Equivalent:
        `IAI.predict_expected_survival_time <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.predict_expected_survival_time-Tuple%7BSurvivalLearner%2C%20Union%7BDataFrames.AbstractDataFrame%2C%20AbstractMatrix%7B%3C%3AReal%7D%7D%7D>`

        Examples
        --------
        >>> lnr.predict_expected_survival_time(X)

        Compatibility
        -------------
        Requires IAI version 2.0 or higher.
        """
        _requires_iai_version("2.0.0", "predict_expected_survival_time")
        return _IAI.predict_expected_survival_time_convert(self._jl_obj, *args,
                                                           **kwargs)

    def predict_hazard(self, *args, **kwargs):
        """Return the fitted hazard coefficient estimate made by the learner
        for each point in the data `X`.

        A higher hazard coefficient estimate corresponds to a smaller predicted
        survival time.

        Julia Equivalent:
        `IAI.predict_hazard <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.predict_hazard-Tuple%7BSurvivalLearner%2C%20Union%7BDataFrames.AbstractDataFrame%2C%20AbstractMatrix%7B%3C%3AReal%7D%7D%7D>`

        Examples
        --------
        >>> lnr.predict_hazard(X)

        Compatibility
        -------------
        Requires IAI version 1.2 or higher.
        """
        _requires_iai_version("1.2.0", "predict_hazard")
        return _IAI.predict_hazard_convert(self._jl_obj, *args, **kwargs)


class PrescriptionLearner(SupervisedLearner):
    """Abstract type encompassing all learners for prescription tasks.

    Julia Equivalent:
    `IAI.PrescriptionLearner <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.PrescriptionLearner>`
    """

    def predict_outcomes(self, *args, **kwargs):
        """Return the the predicted outcome for each treatment made by the
        learner for each point in the features `X`.

        Julia Equivalent:
        `IAI.predict_outcomes <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.predict_outcomes-Tuple%7BPrescriptionLearner%2C%20Union%7BDataFrames.AbstractDataFrame%2C%20AbstractMatrix%7B%3C%3AReal%7D%7D%7D>`

        Examples
        --------
        >>> lnr.predict_outcomes(X)
        """
        return _IAI.predict_outcomes_convert(self._jl_obj, *args, **kwargs)


class PolicyLearner(SupervisedLearner):
    """Abstract type encompassing all learners for policy tasks.

    Julia Equivalent:
    `IAI.PolicyLearner <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.PolicyLearner>`
    """

    def predict_outcomes(self, *args, **kwargs):
        """Return the outcome from `rewards` for each point in the features `X`
        under the prescriptions made by the learner.

        Julia Equivalent:
        `IAI.predict_outcomes <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.predict_outcomes-Tuple%7BPolicyLearner%2C%20Union%7BDataFrames.AbstractDataFrame%2C%20AbstractMatrix%7B%3C%3AReal%7D%7D%2C%20Union%7BDataFrames.AbstractDataFrame%2C%20AbstractMatrix%7B%3C%3AReal%7D%7D%7D>`

        Examples
        --------
        >>> lnr.predict_outcomes(X, rewards)

        Compatibility
        -------------
        Requires IAI version 2.0 or higher.
        """
        _requires_iai_version("2.0.0", "predict_outcomes")
        return _IAI.predict_outcomes_convert(self._jl_obj, *args, **kwargs)

    def predict_treatment_rank(self, *args, **kwargs):
        """Return the treatments in ranked order of effectiveness for each
        point in the features `X` as predicted by the learner.

        Julia Equivalent:
        `IAI.predict_treatment_rank <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.predict_treatment_rank>`

        Examples
        --------
        >>> lnr.predict_treatment_rank(X)

        Compatibility
        -------------
        Requires IAI version 2.1 or higher.
        """
        _requires_iai_version("2.1.0", "predict_treatment_rank")
        return _np.array(_IAI.predict_treatment_rank_convert(self._jl_obj,
                                                             *args, **kwargs))

    def predict_treatment_outcome(self, *args, **kwargs):
        """Return the estimated quality of each treatment in the trained model
        of the learner for each point in the features `X`.

        Julia Equivalent:
        `IAI.predict_treatment_outcome <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.predict_treatment_outcome>`

        Examples
        --------
        >>> lnr.predict_treatment_outcome(X)

        Compatibility
        -------------
        Requires IAI version 2.1 or higher.
        """
        _requires_iai_version("2.1.0", "predict_treatment_outcome")
        return _IAI.predict_treatment_outcome_convert(self._jl_obj, *args,
                                                      **kwargs)

    def predict_treatment_outcome_standard_error(self, *args, **kwargs):
        """Return the standard error for the estimated quality of each
        treatment in the trained model of the learner for each point in the
        features `X`.

        Julia Equivalent:
        `IAI.predict_treatment_outcome_standard_error <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.predict_treatment_outcome_standard_error>`

        Examples
        --------
        >>> lnr.predict_treatment_outcome_standard_error(X)

        Compatibility
        -------------
        Requires IAI version 3.2 or higher.
        """
        _requires_iai_version("3.2.0",
                              "predict_treatment_outcome_standard_error")
        return _IAI.predict_treatment_outcome_standard_error_convert(
            self._jl_obj, *args, **kwargs)


class GridSearch(Learner):
    """Controls grid search over parameter combinations in `params` for `lnr`.

    Julia Equivalent:
    `IAI.GridSearch <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.GridSearch>`

    Examples
    --------
    >>> iai.GridSearch(lnr, params)
    """
    def __init__(self, lnr, *args, **kwargs):
        if not isinstance(lnr, Learner):
            raise TypeError("lnr is not a Learner")

        self._lnr_type = type(lnr)

        jl_obj = _IAI.GridSearch_convert(lnr._jl_obj, *args, **kwargs)
        super().__init__(jl_obj)

    def _warn_deprecated(self, name):
        _warnings.warn(
            "'{0}' is deprecated for 'GridSearch', use ".format(name) +
            "'get_learner' followed by '{0}'".format(name),
            FutureWarning
        )

    def _check_delegate(self, check_name, call_name):
        # TODO is this the best way to do it? Some way of adding the task mixin
        #      to the grid seems like it could be better
        if not getattr(self._lnr_type(), check_name, None):
            raise TypeError("GridSearch over " + self._lnr_type.__name__ +
                            " does not support `{0}`.".format(call_name))

    # Fallback to hitting learner methods if not defined on grid search
    def __getattr__(self, item):
        if item in [
            "write_dot",
            "write_png",
            "write_pdf",
            "write_svg",
            "Questionnaire",
            "get_classification_label",
            "get_classification_proba",
            "get_depth",
            "get_lower_child",
            "get_num_nodes",
            "get_num_samples",
            "get_parent",
            "get_prediction_constant",
            "get_prediction_weights",
            "get_prescription_treatment_rank",
            "get_regression_constant",
            "get_regression_weights",
            "get_split_categories",
            "get_split_feature",
            "get_split_threshold",
            "get_split_weights",
            "get_survival_curve",
            "get_upper_child",
            "is_categoric_split",
            "is_hyperplane_split",
            "is_leaf",
            "is_mixed_ordinal_split",
            "is_mixed_parallel_split",
            "is_ordinal_split",
            "is_parallel_split",
            "missing_goes_lower",
            "reset_display_label",
            "set_display_label",
            "variable_importance",
            "set_threshold",
        ]:  # pragma: no cover
            if _iai_version_less_than("2.0.0"):
                self._warn_deprecated(item)
            else:
                raise AttributeError(
                    "'GridSearch' object has no attribute '{0}'".format(item),
                )
        # Fallback to learner method, but throw if we get a non-function back
        out = getattr(self.get_learner(), item)
        if not callable(out):
            raise AttributeError(
                "'GridSearch' object has no attribute '{0}'".format(item),
            )
        return out

    def get_learner(self):
        """Return the fitted learner using the best parameter combination from
        the grid.

        Julia Equivalent:
        `IAI.get_learner <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.get_learner>`

        Examples
        --------
        >>> grid.get_learner()
        """
        lnr = self._lnr_type()
        jl_obj = _IAI.get_learner(self._jl_obj)
        Learner.__init__(lnr, jl_obj)
        return lnr

    def get_best_params(self):
        """Return the best parameter combination from the grid.

        Julia Equivalent:
        `IAI.get_best_params <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.get_best_params>`

        Examples
        --------
        >>> grid.get_best_params()
        """
        return _IAI.get_best_params_convert(self._jl_obj)

    def get_grid_results(self):
        """This method was deprecated and renamed to get_grid_result_summary in
        interpretableai 2.4.0. This is for consistency with the IAI v2.2.0
        Julia release.
        """
        _warnings.warn(
            "'get_grid_results' is deprecated, use 'get_grid_result_summary'",
            FutureWarning
        )
        return self.get_grid_result_summary()

    def get_grid_result_summary(self):
        """Return a summary of the results from the grid search.

        Julia Equivalent:
        `IAI.get_grid_result_summary <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.get_grid_result_summary>`

        Examples
        --------
        >>> grid.get_grid_result_summary()
        """
        if _iai_version_less_than("2.2.0"):
            return _IAI.get_grid_results_convert(self._jl_obj)
        else:
            return _IAI.get_grid_result_summary_convert(self._jl_obj)

    def get_grid_result_details(self):
        """Return a `list` of `dict`s detailing the results of the grid search.

        Julia Equivalent:
        `IAI.get_grid_result_details <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.get_grid_result_details>`

        Examples
        --------
        >>> grid.get_grid_result_details()

        Compatibility
        -------------
        Requires IAI version 2.2 or higher.
        """
        _requires_iai_version("2.2.0", "get_grid_result_details")
        details = _IAI.get_grid_result_details_convert(self._jl_obj)

        # Convert all Julia learners in the grid to Python equivalents
        for d in details:
            for f in d["fold_results"]:
                jl_obj = f["learner"]
                lnr = _get_learner_type(jl_obj)()
                Learner.__init__(lnr, jl_obj)
                f["learner"] = lnr

        return details

    def fit(self, *args, **kwargs):
        """Fit a grid with data `X` and `y`.

        Julia Equivalent:
        `IAI.fit! <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.fit%21-Tuple%7BGridSearch%7D>`

        Examples
        --------
        >>> grid.fit(X, *y, **kwargs)

        Parameters
        ----------
        Refer to the documentation on
        `data preparation <https://docs.interpretable.ai/v3.2.2/IAI-Python/data/#Python-Data-Preparation-Guide-1>`
        for information on how to format and supply the data.
        """
        return super().fit(*args, **kwargs)

    def fit_cv(self, *args, **kwargs):
        """Fit a grid with data `X` and `y` using k-fold cross-validation.

        Julia Equivalent:
        `IAI.fit_cv! <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.fit_cv%21-Tuple%7BGridSearch%7D>`

        Examples
        --------
        >>> grid.fit_cv(X, *y, **kwargs)

        Parameters
        ----------
        Refer to the documentation on
        `data preparation <https://docs.interpretable.ai/v3.2.2/IAI-Python/data/#Python-Data-Preparation-Guide-1>`
        for information on how to format and supply the data.
        """
        _IAI.fit_cv_convert(self._jl_obj, *args, **kwargs)
        return self

    def fit_transform_cv(self, *args, **kwargs):
        """For imputation learners, fit a grid with features `X` using k-fold
        cross-validation and impute missing values in `X`.

        Julia Equivalent:
        `IAI.fit_transform_cv! <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.fit_transform_cv!>`

        Examples
        --------
        >>> grid.fit_transform_cv(X, **kwargs)

        Parameters
        ----------
        Refer to the documentation on
        `data preparation <https://docs.interpretable.ai/v3.2.2/IAI-Python/data/#Python-Data-Preparation-Guide-1>`
        for information on how to format and supply the data.
        """
        self._check_delegate("fit_transform", "fit_transform_cv")
        return _IAI.fit_transform_cv_convert(self._jl_obj, *args, **kwargs)

    def write_html(self, filename, **kwargs):
        self._check_delegate("write_html", "write_html")
        if _iai_version_less_than("2.0.0"):
            self._warn_deprecated("write_html")
            # IAI v1.0 doesn't define the forwarding method, so do it here
            return _IAI.write_html_convert(filename,
                                           self.get_learner()._jl_obj,
                                           **kwargs)
        return _IAI.write_html_convert(filename, self._jl_obj, **kwargs)

    def show_in_browser(self, *args, **kwargs):  # pragma: no cover
        self._check_delegate("show_in_browser", "show_in_browser")
        if _iai_version_less_than("2.0.0"):
            self._warn_deprecated("show_in_browser")
            # IAI v1.0 doesn't define the forwarding method, so do it here
            return _IAI.show_in_browser_convert(self.get_learner()._jl_obj,
                                                *args, **kwargs)
        return _IAI.show_in_browser_convert(self._jl_obj, *args, **kwargs)

    def write_questionnaire(self, filename, **kwargs):
        self._check_delegate("write_questionnaire", "write_questionnaire")
        if _iai_version_less_than("2.0.0"):
            self._warn_deprecated("write_questionnaire")
            # IAI v1.0 doesn't define the forwarding method, so do it here
            return _IAI.write_questionnaire_convert(filename,
                                                    self.get_learner()._jl_obj,
                                                    **kwargs)
        return _IAI.write_questionnaire_convert(filename, self._jl_obj,
                                                **kwargs)

    def MultiQuestionnaire(self, **args):
        """Construct a
        :meth:`interpretableai.iai.MultiQuestionnaire`
        containing the final fitted learner from the trained grid search as
        well as the learner found for each parameter combination.

        Julia Equivalent:
        `IAI.MultiQuestionnaire <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.MultiQuestionnaire-Tuple%7BGridSearch%7D>`

        Examples
        --------
        >>> grid.MultiQuestionnaire()

        Compatibility
        -------------
        Requires IAI version 2.0 or higher.
        """
        self._check_delegate("Questionnaire", "MultiQuestionnaire")
        _requires_iai_version("2.0.0", "MultiQuestionnaire")
        return MultiQuestionnaire(self._jl_obj, **args)

    def MultiTreePlot(self, **args):
        """Construct a
        :meth:`interpretableai.iai.MultiTreePlot`
        containing the final fitted learner from the trained grid search as
        well as the learner found for each parameter combination.

        Julia Equivalent:
        `IAI.MultiTreePlot <https://docs.interpretable.ai/v3.2.2/IAITrees/reference/#IAI.MultiTreePlot-Tuple%7BGridSearch%7D>`

        Examples
        --------
        >>> grid.MultiTreePlot()

        Compatibility
        -------------
        Requires IAI version 2.0 or higher.
        """
        self._check_delegate("TreePlot", "MultiTreePlot")
        _requires_iai_version("2.0.0", "MultiTreePlot")
        from .iai import MultiTreePlot
        return MultiTreePlot(self._jl_obj, **args)

    def show_questionnaire(self, *args, **kwargs):  # pragma: no cover
        self._check_delegate("show_questionnaire", "show_questionnaire")
        if _iai_version_less_than("2.0.0"):
            self._warn_deprecated("show_questionnaire")
            # IAI v1.0 doesn't define the forwarding method, so do it here
            return _IAI.show_questionnaire_convert(self.get_learner()._jl_obj,
                                                   *args, **kwargs)
        return _IAI.show_questionnaire_convert(self._jl_obj, *args, **kwargs)

    def plot(self, type=None):
        """Plot the grid search results for Optimal Feature Selection learners.

        Returns a
        `matplotlib.figure.Figure <https://matplotlib.org/stable/api/figure_api.html?highlight=figure#matplotlib.figure.Figure>`
        containing the plotted results.

        In a Jupyter Notebook, the plot will be shown automatically. In a
        terminal, you can show the plot with `grid.plot().show()`.

        Examples
        --------
        >>> grid.plot(type)

        Parameters
        ----------
        type : str
            The type of plot to construct, either `"validation"` or
            `"importance"`. For more information refer to the
            `Julia documentation for plotting grid search results <https://docs.interpretable.ai/v3.2.2/OptimalFeatureSelection/visualization/#Plotting-Grid-Search-Results-1>`.

        Compatibility
        -------------
        Requires IAI version 2.2 or higher.
        """
        _requires_iai_version("2.2.0", "plot")

        if _Main.isa(self.get_learner()._jl_obj,
                     _IAI.OptimalFeatureSelectionLearner):
            _OFS = _load_julia_module("Main.IAI.OptimalFeatureSelection")

            d = _OFS.get_plot_data(self._jl_obj)

            if type == 'validation':
                plot_data = _pd.DataFrame({'sparsity': d['sparsity'],
                                           'score': d['score']})
                ax = plot_data.plot(x='sparsity', y='score', legend=False)
                ax.set_xlabel('Sparsity')
                ax.set_ylabel('Validation Score')
                ax.set_title('Validation Score against Sparsity')
                return ax.get_figure()

            elif type == 'importance':
                import matplotlib.pyplot as plt
                f = plt.figure()
                ax = f.add_subplot(111)
                # ax.pcolormesh(d['sparsity'], d['feature_names'],
                #               d['importance'])

                plot_data = _pd.DataFrame(d['importance'],
                                          index=d['feature_names'],
                                          columns=d['sparsity'])
                c = ax.pcolor(plot_data)
                ax.set_yticks(_np.arange(0.5, len(plot_data.index), 1))
                ax.set_yticklabels(plot_data.index)
                ax.set_xticks(_np.arange(0.5, len(plot_data.columns), 1))
                ax.set_xticklabels(plot_data.columns)
                ax.set_xlabel('Sparsity')
                ax.set_title('Normalized Variable Importance')

                f.colorbar(c, ax=ax)

                return f

            else:
                raise ValueError(
                    '`type` has to be "validation" or "importance"')
        else:
            raise TypeError("GridSearch over " + self._lnr_type.__name__ +
                            " does not support `plot`.")


class ROCCurve():
    """Container for ROC curve information.

    Julia Equivalent:
    `IAI.ROCCurve <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.ROCCurve>`

    Examples
    --------

    Construct a
    :meth:`interpretableai.iai.ROCCurve`
    using predicted probabilities `probs` and true labels `y`, with
    probabilities indicating chance of predicting `positive_label`:

    Julia Equivalent:
    `IAI.ROCCurve <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.ROCCurve-Tuple%7BAbstractVector%7B%3C%3AReal%7D%2C%20AbstractVector%7D>`

    >>> iai.ROCCurve(probs, y, positive_label=positive_label)
    """
    def __init__(self, *args, **kwargs):
        if (len(args) == 1 and len(kwargs) == 0 and
                _Main.isa(args[0], _IAI.ROCCurve)):
            # A julia ROCCurve was passed - just wrap it in Python class
            self._jl_obj = args[0]
        elif len(args) > 0 and isinstance(args[0], Learner):
            # A grid or learner was passed as first arg
            args = list(args)
            lnr = args.pop(0)
            if isinstance(lnr, GridSearch):
                lnr = lnr.get_learner()

            if not isinstance(lnr, ClassificationLearner):
                raise TypeError("lnr is not a ClassificationLearner")

            _warnings.warn(
                "'iai.ROCCurve(lnr, X, y)' is deprecated, use " +
                "`lnr.ROCCurve(X, y)`",
                FutureWarning
            )

            self._jl_obj = _IAI.ROCCurve_convert(lnr._jl_obj, *args, **kwargs)
        else:
            # Check if the first argument is a Julia object
            # We need a ref to the `jlwrap` class, so get it from the
            # `ROCCurve_convert` function we are about to call
            if (len(args) > 0 and
                    not isinstance(args[0], type(_IAI.ROCCurve_convert))):
                _requires_iai_version("2.0.0", "ROCCurve",
                                      "with probabilities and true labels")
            self._jl_obj = _IAI.ROCCurve_convert(*args, **kwargs)

    def __repr__(self):
        return _IAI.string(self._jl_obj)

    def _repr_html_(self):
        return _IAI.to_html(self._jl_obj)

    def __eq__(self, obj):
        return (
            isinstance(obj, ROCCurve) and
            _Main.isequal(self._jl_obj, obj._jl_obj)
        )

    def write_html(self, filename, **kwargs):
        """Write interactive browser visualization of the ROC curve to
        `filename` as HTML.

        Julia Equivalent:
        `IAI.write_html <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.write_html-Tuple%7BAny,%20ROCCurve%7D>`

        Examples
        --------
        >>> lnr.write_html(filename, **kwargs)

        Compatibility
        -------------
        Requires IAI version 1.1 or higher.
        """
        _requires_iai_version("1.1.0", "write_html")
        return _IAI.write_html_convert(filename, self._jl_obj, **kwargs)

    def show_in_browser(self, **kwargs):  # pragma: no cover
        """Visualize the ROC curve in the browser.

        Julia Equivalent:
        `IAI.show_in_browser <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.show_in_browser-Tuple%7BROCCurve%7D>`

        Examples
        --------
        >>> curve.show_in_browser()
        """
        return _IAI.show_in_browser_convert(self._jl_obj, **kwargs)

    def get_data(self):
        """Extract the underlying data from the curve as a `dict` with two keys:
        - `coords`: a `dict` for each point on the curve with the following keys:
            - `'fpr'`: false positive rate at the given threshold
            - `'tpr'`: true positive rate at the given threshold
            - `'threshold'`: the threshold
        - `auc`: the area-under-the-curve (AUC)

        Julia Equivalent:
        `IAI.get_roc_curve_data <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.get_roc_curve_data>`

        Examples
        --------
        >>> curve.get_data()

        Compatibility
        -------------
        Requires IAI version 2.1 or higher.
        """
        _requires_iai_version("2.1.0", "get_data")
        return _IAI.get_roc_curve_data_convert(self._jl_obj)

    def plot(self):
        """Plot the ROC curve using `matplotlib`.

        Returns a
        `matplotlib.figure.Figure <https://matplotlib.org/stable/api/figure_api.html?highlight=figure#matplotlib.figure.Figure>`
        containing the ROC curve.

        In a Jupyter Notebook, the plot will be shown automatically. In a
        terminal, you can show the plot with `curve.plot().show()`.

        Examples
        --------
        >>> curve.plot()

        Compatibility
        -------------
        Requires IAI version 2.1 or higher.
        """
        _requires_iai_version("2.1.0", "plot")

        d = self.get_data()
        df = _pd.DataFrame({
            'fpr': [c['fpr'] for c in d['coords']],
            'tpr': [c['tpr'] for c in d['coords']],
        })

        ax = df.plot(x='fpr', y='tpr', legend=False)
        ax.set_xlabel('False Positive Rate')
        ax.set_ylabel('True Positive Rate')
        ax.set_title('AUC %.3f' % d['auc'])
        return ax.get_figure()


class SurvivalCurve():
    """Container for survival curve information.

    Use `curve[t]` to get the survival probability prediction from curve at
    time `t`.

    Julia Equivalent:
    `IAI.SurvivalCurve <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.SurvivalCurve>`
    """
    def __init__(self, jl_curve):
        self._jl_obj = jl_curve

    def __getitem__(self, item):
        if not isinstance(item, (int, float)):
            raise TypeError("only supports scalar indexing")
        return _IAI.getindex(self._jl_obj, item)

    def __repr__(self):
        return _IAI.string(self._jl_obj)

    def get_data(self):
        """Extract the underlying data from the curve as a `dict` with two keys:
        - `'times'`: the time for each breakpoint on the curve
        - `'coefs'`: the probablility for each breakpoint on the curve

        Julia Equivalent:
        `IAI.get_survival_curve_data <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.get_survival_curve_data>`

        Examples
        --------
        >>> curve.get_data()
        """
        return _IAI.get_survival_curve_data_convert(self._jl_obj)

    def predict_expected_survival_time(self):
        """Return the expected survival time according to the curve

        Julia Equivalent:
        `IAI.predict_expected_survival_time <https://docs.interpretable.ai/v3.2.2/IAIBase/reference/#IAI.predict_expected_survival_time-Tuple%7BSurvivalCurve%7D>`

        Examples
        --------
        >>> curve.predict_expected_survival_time()

        Compatibility
        -------------
        Requires IAI version 2.2 or higher.
        """
        _requires_iai_version("2.2.0", "predict_expected_survival_time")
        return _IAI.predict_expected_survival_time_convert(self._jl_obj)

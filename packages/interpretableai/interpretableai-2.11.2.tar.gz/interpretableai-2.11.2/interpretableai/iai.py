import os as _os

from .installation import iai_run_julia_setup, IAI_JULIA_SCRIPT_DIR


def _isnotebook():  # pragma: no cover
    try:
        from IPython import get_ipython
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except:
        return False      # Probably standard Python interpreter


def _iai_version_less_than(version):
    jleval = _Main.string("Base.thispatch(v\"", _Main.iai_version, "\")",
                          " < ",
                          "Base.thispatch(v\"", version, "\")")
    return _Main.eval(jleval)


def _requires_iai_version(required_iai_version, function_name, extra=''):
    if _iai_version_less_than(required_iai_version):
        raise RuntimeError(
            "The function `" + function_name + "` " + extra + " in this " +
            "version of the `interpretableai` Python package requires IAI " +
            "version " + required_iai_version + ". Please upgrade your IAI " +
            "installation to use this function.")


_Main = iai_run_julia_setup()


# Disable update check if running in a notebook so we can show it later
if _isnotebook():  # pragma: no cover
    _old_update_check = _os.getenv("IAI_DISABLE_UPDATE_CHECK")
    _os.environ["IAI_DISABLE_UPDATE_CHECK"] = "True"
# Run Julia setup code
try:
    _Main.include(_os.path.join(IAI_JULIA_SCRIPT_DIR, "setup.jl"))
    _Main.include(_os.path.join(IAI_JULIA_SCRIPT_DIR, "convert.jl"))
except ImportError as err:
    msg = str(err)

    # Trim Julia stacktrace from message
    # Message format depends on PyCall version
    if msg.startswith("Julia exception"):  # pragma: no cover
        line_index = 0
    else:
        line_index = 1
    msg = str(err).split("\n")[line_index]

    from future.utils import raise_from
    raise_from(ImportError(msg), None)
# Restore update check
if _isnotebook():  # pragma: no cover
    if _old_update_check:
        _os.environ["IAI_DISABLE_UPDATE_CHECK"] = _old_update_check
    else:
        del _os.environ["IAI_DISABLE_UPDATE_CHECK"]


# Hack to get a reference to IAI without `import`
import julia as _julia
def _load_julia_module(m):
    return _julia.core.JuliaModuleLoader().create_module(_julia.core._find_spec_from_fullname("julia." + m))
_IAI = _load_julia_module("Main.IAI")


from julia import Random as _Random
def set_julia_seed(*args):
    """Set the random seed in Julia to `seed`.

    Julia Equivalent:
    `Random.seed! <https://docs.julialang.org/en/v1/stdlib/Random/index.html#Random.seed!>`

    Examples
    --------
    >>> iai.set_julia_seed(seed)
    """
    return _Random.seed_b(*args)


from julia import Distributed as _Distributed
def add_julia_processes(*args):
    """Add additional Julia worker processes to parallelize workloads.

    Julia Equivalent:
    `Distributed.addprocs <https://docs.julialang.org/en/v1/stdlib/Distributed/#Distributed.addprocs>`

    For more information, refer to the
    `documentation on parallelization <https://docs.interpretable.ai/stable/IAIBase/advanced/#IAIBase-Parallelization-1>`

    Examples
    --------
    >>> iai.add_julia_processes(3)
    """
    out = _Distributed.addprocs(*args)

    # We need to load IAI on all processes
    # NB: If using system image this is automatic
    if not _Main.eval('isdefined(Main, :IAISysImg)'):
        _Main.eval('import Distributed; Distributed.@everywhere import IAI')

    return out


def get_machine_id():
    """Return the machine ID for the current computer.

    Examples
    --------
    >>> iai.get_machine_id()
    """
    return _IAI.get_machine_id_convert()


class acquire_license(object):
    """Acquire an IAI license for the current session.

    Julia Equivalent:
    `IAI.acquire_license <https://docs.interpretable.ai/v3.2.2/installation/#IAI.acquire_license>`

    Examples
    --------
    >>> iai.acquire_license()

    Compatibility
    -------------
    Requires IAI version 3.1 or higher.
    """
    def __init__(self, *args, parallel_processes=None, **kwargs):
        _requires_iai_version("3.1.0", "acquire_license")
        if parallel_processes is None:
            parallel_processes = _Distributed.procs()

        needed_license = (
            _IAI.acquire_license_all_procs_convert(parallel_processes))
        self.release_procs = [p for (i, p) in enumerate(parallel_processes)
                              if needed_license[i]]
        return None

    def __enter__(self):
        return None

    def __exit__(self, *exc):
        release_license(parallel_processes=self.release_procs)


def release_license(*args, parallel_processes=None, **kwargs):
    """Release any IAI license held by the current session.

    Julia Equivalent:
    `IAI.release_license <https://docs.interpretable.ai/v3.2.2/installation/#IAI.release_license>`

    Examples
    --------
    >>> iai.release_license()

    Compatibility
    -------------
    Requires IAI version 3.1 or higher.
    """
    _requires_iai_version("3.1.0", "release_license")
    if parallel_processes is None:
        parallel_processes = _Distributed.procs()
    if len(parallel_processes) > 0:
        return _IAI.release_license_convert(
            *args, **kwargs, parallel_processes=parallel_processes)


def load_graphviz(*args):
    """Loads the Julia Graphviz library to permit certain visualizations.

    The library will be installed if not already present.

    Examples
    --------
    >>> iai.load_graphviz()
    """
    try:
        from julia import Graphviz_jll
    except ImportError:
        from julia import Pkg
        Pkg.add("Graphviz_jll")
        from julia import Graphviz_jll


def _get_learner_type(jl_obj):
    if _Main.isa(jl_obj, _IAI.OptimalTreeClassifier):
        L = OptimalTreeClassifier
    elif _Main.isa(jl_obj, _IAI.OptimalTreeRegressor):
        L = OptimalTreeRegressor
    elif (_iai_version_less_than("2.0.0") and
          _Main.isa(jl_obj, _IAI.OptimalTreeSurvivor)):
        L = OptimalTreeSurvivalLearner
    elif (not _iai_version_less_than("2.0.0") and
          _Main.isa(jl_obj, _IAI.OptimalTreeSurvivalLearner)):
        L = OptimalTreeSurvivalLearner
    elif _Main.isa(jl_obj, _IAI.OptimalTreePrescriptionMinimizer):
        L = OptimalTreePrescriptionMinimizer
    elif _Main.isa(jl_obj, _IAI.OptimalTreePrescriptionMaximizer):
        L = OptimalTreePrescriptionMaximizer
    elif (not _iai_version_less_than("2.0.0") and
          _Main.isa(jl_obj, _IAI.OptimalTreePolicyMinimizer)):
        L = OptimalTreePolicyMinimizer
    elif (not _iai_version_less_than("2.0.0") and
          _Main.isa(jl_obj, _IAI.OptimalTreePolicyMaximizer)):
        L = OptimalTreePolicyMaximizer
    elif _Main.isa(jl_obj, _IAI.OptimalFeatureSelectionClassifier):
        L = OptimalFeatureSelectionClassifier
    elif _Main.isa(jl_obj, _IAI.OptimalFeatureSelectionRegressor):
        L = OptimalFeatureSelectionRegressor
    elif _Main.isa(jl_obj, _IAI.OptKNNImputationLearner):
        L = OptKNNImputationLearner
    elif _Main.isa(jl_obj, _IAI.OptSVMImputationLearner):
        L = OptSVMImputationLearner
    elif _Main.isa(jl_obj, _IAI.OptTreeImputationLearner):
        L = OptTreeImputationLearner
    elif _Main.isa(jl_obj, _IAI.SingleKNNImputationLearner):
        L = SingleKNNImputationLearner
    elif _Main.isa(jl_obj, _IAI.MeanImputationLearner):
        L = MeanImputationLearner
    elif _Main.isa(jl_obj, _IAI.RandImputationLearner):
        L = RandImputationLearner
    elif (not _iai_version_less_than("3.0.0") and
          _Main.isa(jl_obj, _IAI.ZeroImputationLearner)):
        L = ZeroImputationLearner
    elif (not _iai_version_less_than("2.1.0") and
          _Main.isa(jl_obj, _IAI.RandomForestClassifier)):
        L = RandomForestClassifier
    elif (not _iai_version_less_than("2.1.0") and
          _Main.isa(jl_obj, _IAI.RandomForestRegressor)):
        L = RandomForestRegressor
    elif (not _iai_version_less_than("2.1.0") and
          _Main.isa(jl_obj, _IAI.XGBoostClassifier)):
        L = XGBoostClassifier
    elif (not _iai_version_less_than("2.1.0") and
          _Main.isa(jl_obj, _IAI.XGBoostRegressor)):
        L = XGBoostRegressor
    elif (not _iai_version_less_than("3.0.0") and
          _Main.isa(jl_obj, _IAI.GLMNetCVClassifier)):
        L = GLMNetCVClassifier
    elif (not _iai_version_less_than("2.1.0") and
          _Main.isa(jl_obj, _IAI.GLMNetCVRegressor)):
        L = GLMNetCVRegressor
    elif (not _iai_version_less_than("3.0.0") and
          _Main.isa(jl_obj, _IAI.GLMNetCVSurvivalLearner)):
        L = GLMNetCVSurvivalLearner
    elif (not _iai_version_less_than("3.0.0") and
          _Main.isa(jl_obj, _IAI.CategoricalClassificationRewardEstimator)):
        L = CategoricalClassificationRewardEstimator
    elif (not _iai_version_less_than("3.0.0") and
          _Main.isa(jl_obj, _IAI.CategoricalRegressionRewardEstimator)):
        L = CategoricalRegressionRewardEstimator
    elif (not _iai_version_less_than("3.0.0") and
          _Main.isa(jl_obj, _IAI.CategoricalSurvivalRewardEstimator)):
        L = CategoricalSurvivalRewardEstimator
    elif (not _iai_version_less_than("3.0.0") and
          _Main.isa(jl_obj, _IAI.NumericClassificationRewardEstimator)):
        L = NumericClassificationRewardEstimator
    elif (not _iai_version_less_than("3.0.0") and
          _Main.isa(jl_obj, _IAI.NumericRegressionRewardEstimator)):
        L = NumericRegressionRewardEstimator
    elif (not _iai_version_less_than("3.0.0") and
          _Main.isa(jl_obj, _IAI.NumericSurvivalRewardEstimator)):
        L = NumericSurvivalRewardEstimator
    elif (not _iai_version_less_than("3.0.0") and
          _Main.isa(jl_obj, _IAI.EqualPropensityEstimator)):
        L = EqualPropensityEstimator

    return L


# Load all subpackages into main namespace
from .mixeddata import MixedData
from .iaibase import *
from .iaitrees import *
from .optimaltrees import *
from .optimpute import *
from .optimalfeatureselection import *
from .rewardestimation import *
from .heuristics import *


# If we are running in a notebook, display any license related warnings
def _show_license_warnings():  # pragma: no cover

    if _isnotebook():
        messages = _Main.eval("IAI.IAILicensing.validate_license(1, 1)")

        import logging
        for _, message in messages:
            logging.warning(message)


# `IAILicensing.validate_license` added in IAI v3
if not _iai_version_less_than("3.0.0"):
    _show_license_warnings()

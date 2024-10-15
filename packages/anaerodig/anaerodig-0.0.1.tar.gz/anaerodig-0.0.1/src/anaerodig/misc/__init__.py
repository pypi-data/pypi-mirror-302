"""
Miscellanous functions used throughout the package

Functions:
    blab: wrap up for silent
    timedrun: TimeOut option for function call decorator
    interpretation: right composition decorator
    post_modif: left composition decorator
    safe_call: Evaluation of any function without failure (returns None if Exception occured)
    par_eval: Parallelisation switch for function evaluation
    num_der: numerical differentiation
    vectorize: function vectorization

Function implementations may change but input/output structure sholud remain stable.
"""
from anaerodig.misc.composition import interpretation, post_modif
from anaerodig.misc.dataframes import get_last_valid_index
from anaerodig.misc.matrix_inversion import safe_inverse_ps_matrix
from anaerodig.misc.num_der import num_der
from anaerodig.misc.parallel import par_eval
from anaerodig.misc.prints import blab, tprint
from anaerodig.misc.raise_warn_call import raise_warn_call
from anaerodig.misc.safe_call import SafeCallWarning, safe_call
from anaerodig.misc.sets import are_set_equal, check_set_equal, set_diff_msg
from anaerodig.misc.shape import ShapeError, _get_pre_shape, check_shape, prod
from anaerodig.misc.timed_run import timedrun, timeout
from anaerodig.misc.vectorize import vectorize

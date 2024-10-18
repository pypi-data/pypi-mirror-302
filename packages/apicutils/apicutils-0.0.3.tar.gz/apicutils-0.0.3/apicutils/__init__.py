"""
miscealleanous shared between different packages

Functions:
    blab: wrap up for silent
    timedrun: TimeOut option for function call decorator
    interpretation: right composition decorator
    post_modif: left composition decorator
    safe_call: Evaluation of any function without failure (returns None if Exception occured)
    par_eval: Parallelisation switch for function evaluation
    num_der: numerical differentiation
    vectorize: function vectorization
"""

from apicutils.composition import interpretation, post_modif
from apicutils.dataframes import get_last_valid_index
from apicutils.matrix_inversion import safe_inverse_ps_matrix
from apicutils.num_der import num_der
from apicutils.parallel import par_eval
from apicutils.prints import blab, tprint
from apicutils.raise_warn_call import raise_warn_call
from apicutils.safe_call import SafeCallWarning, safe_call
from apicutils.sets import are_set_equal, check_set_equal, set_diff_msg
from apicutils.shape import ShapeError, check_shape, get_pre_shape, prod
from apicutils.timed_run import timedrun, timeout
from apicutils.vectorize import vectorize


def bin_op_dispatcher():
    registry = {}
    def dispatch(inst, other):
        fcn = registry[type(other)]
        return fcn(inst, other)
    dispatch.supported_types = lambda: registry.keys()

    def register(*op_types):
        def decorator(fcn):
            for op_type in op_types:
                registry[op_type] = fcn
            return dispatch
        return decorator

    return (dispatch, register)
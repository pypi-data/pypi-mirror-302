import inspect
import functools

from .context import ActiveContext


def forward(method):
    """
    Decorator to define a forward method for a module.

    Parameters
    ----------
    method: (Callable)
        The forward method to be decorated.

    Returns
    -------
    Callable
        The decorated forward method.
    """

    # Get kwargs from function signature
    method_kwargs = []
    for arg in inspect.signature(method).parameters.values():
        if arg.default is not arg.empty:
            method_kwargs.append(arg.name)

    @functools.wraps(method)
    def wrapped(self, *args, **kwargs):
        if self.active:
            kwargs.update(self.fill_kwargs(method_kwargs))
            return method(self, *args, **kwargs)

        # Extract params from the arguments
        if len(self.dynamic_params) == 0:
            params = {}
        elif "params" in kwargs:
            params = kwargs.pop("params")
        elif args:
            params = args.pop(0)
        else:
            raise ValueError(
                f"Params must be provided for dynamic modules. Expected {len(self.dynamic_params)} params."
            )

        with ActiveContext(self, params):
            kwargs.update(self.fill_kwargs(method_kwargs))
            return method(self, *args, **kwargs)

    return wrapped

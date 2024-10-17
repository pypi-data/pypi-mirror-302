import builtins
import logging


from rich.logging import RichHandler
from rich import print as rich_print
from types import ModuleType
from typing import Any, Optional


# Overrides the built-in print function with rich_print
# because i like it :)
# sorry not sorry
builtins.print = rich_print


def get_logger(module_name: str = __name__, level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger(module_name)

    # Remove any existing handlers to avoid duplicates
    if logger.hasHandlers():
        logger.handlers.clear()

    # Set the logging level
    logger.setLevel(level)

    # Create a RichHandler
    console_handler = RichHandler(
        markup=True,
        rich_tracebacks=True,
        show_time=True,
        omit_repeated_times=False,
        show_level=True,
        show_path=False,
    )

    # Set the format for the handler
    FORMAT = "[bold italic red]%(name)s[/bold italic red] - [italic dim]%(funcName)s[/italic dim] - %(message)s"
    console_handler.setFormatter(logging.Formatter(FORMAT))

    # Add the handler to the logger
    logger.addHandler(console_handler)

    # Ensure all messages are propagated
    logger.propagate = False

    return logger


# router
class LazyLoaderMeta(type):
    """
    Meta class for lazy loading attributes from a module.
    """

    def __getattr__(cls, name: str) -> Any:
        module = cls._load()
        try:
            return getattr(module, name)
        except AttributeError as e:
            raise e

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        module = cls._load()
        return module(*args, **kwargs)


class router(metaclass=LazyLoaderMeta):
    """
    Lazy loader for a module.
    Used internally in the zyx library.

    Refer to __init__.py files.
    """

    import threading

    _module_cache: Optional[ModuleType] = None
    _lock = threading.Lock()

    @classmethod
    def _load(cls) -> Any:
        import inspect
        from importlib import import_module

        if cls._module_cache is None:
            with cls._lock:
                if cls._module_cache is None:
                    try:
                        module = import_module(cls._module_name)
                        cls._module_cache = getattr(module, cls._attr_name)

                        if inspect.isclass(cls._module_cache):
                            return type(cls.__name__, (cls._module_cache,), {})
                        elif inspect.isgeneratorfunction(cls._module_cache):
                            return cls._wrap_generator(cls._module_cache)
                        elif inspect.isfunction(cls._module_cache):
                            return cls._wrap_function(cls._module_cache)
                    except (ImportError, AttributeError) as e:
                        raise e
        return cls._module_cache

    @staticmethod
    def _wrap_generator(gen_func):
        def wrapper(*args, **kwargs):
            return gen_func(*args, **kwargs)

        return wrapper

    @staticmethod
    def _wrap_function(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @classmethod
    def init(cls, module_name: str, attr_name: str) -> None:
        cls._module_name = module_name
        cls._attr_name = attr_name

    def __getattr__(self, name: str) -> Any:
        module = self._load()
        try:
            return getattr(module, name)
        except AttributeError as e:
            raise e

    def __iter__(self):
        module = self._load()
        if hasattr(module, "__iter__"):
            return iter(module)
        raise TypeError(f"{module} object is not iterable")

    def __next__(self):
        module = self._load()
        if hasattr(module, "__next__"):
            return next(module)
        raise TypeError(f"{module} object is not an iterator")

    def __getitem__(self, item):
        module = self._load()
        if hasattr(module, "__getitem__"):
            return module[item]
        raise TypeError(f"{module} object does not support indexing")

    def __len__(self):
        module = self._load()
        if hasattr(module, "__len__"):
            return len(module)
        raise TypeError(f"{module} object does not have a length")

    def __contains__(self, item):
        module = self._load()
        if hasattr(module, "__contains__"):
            return item in module
        raise TypeError(f"{module} object does not support membership test")





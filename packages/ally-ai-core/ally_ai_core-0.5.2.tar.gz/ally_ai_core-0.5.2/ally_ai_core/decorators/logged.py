import logging
import inspect
from functools import wraps
from typing import Callable, TypeVar, Any, cast
from random import randrange

# Configure logging (adjust as needed)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

F = TypeVar("F", bound=Callable[..., Any])


def logged(
    message: str,
    level: int = logging.INFO,
    show_in: bool = True,
    show_out: bool = True,
    show_data: bool = True,
    logger: logging.Logger = logging.getLogger(),
) -> Callable[[F], F]:
    """
    Decorator to log the start and finish of a function execution.

    Args:
        message (str): Custom message to include in logs.
        level (int): Logging level.
        show_in (bool): Whether to log the start of the function.
        show_out (bool): Whether to log the finish of the function.
        show_data (bool): Whether to log the args and kwargs of the function.

    Returns:
        Callable: The decorated function with logging.
    """

    def decorator(func: F) -> F:
        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def awrapper(*args, **kwargs) -> Any:
                id = randrange(1, 100_000_000_000)
                try:
                    if show_in:
                        logger.log(
                            level,
                            f"{message} - Starting({id}) *{func.__name__}* with args: {args if show_data else ''}, kwargs: {kwargs if show_data else ''}",
                        )

                    result = await func(*args, **kwargs)

                    if show_out:
                        logger.log(
                            level,
                            f"{message} - Finished({id}) *{func.__name__}* with result: {result if show_data else ''}",
                        )
                    return result
                except Exception as e:
                    logger.exception(
                        f"{message} - Exception({id}) *{func.__name__}* raised an exception: {e}"
                    )
                    raise  # Re-raise the exception after logger

            return cast(F, awrapper)
        else:

            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                id = randrange(1, 100_000_000_000)
                try:
                    if show_in:
                        logger.log(
                            level,
                            f"{message} - Starting({id}) *{func.__name__}* with args: {args if show_data else ''}, kwargs: {kwargs if show_data else ''}",
                        )

                    result = func(*args, **kwargs)

                    if show_out:
                        logger.log(
                            level,
                            f"{message} - Finished({id}) *{func.__name__}* with result: {result if show_data else ''}",
                        )
                    return result
                except Exception as e:
                    logger.exception(
                        f"{message} - Exception({id}) *{func.__name__}* raised an exception: {e}"
                    )
                    raise

            return cast(F, wrapper)

    return decorator

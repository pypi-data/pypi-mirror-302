import logging
import inspect
from functools import wraps
from typing import Callable, TypeVar, Any, cast
from random import randrange
from dataclasses import dataclass

default_logger = logging.getLogger()
default_logger.setLevel(logging.INFO)

F = TypeVar("F", bound=Callable[..., Any])


@dataclass(frozen=True)
class Logged:
    """
    Args:
            message (str): Custom message to include in logs.
            show_in (bool): Whether to log the start of the function.
            show_out (bool): Whether to log the finish of the function.
            show_data (bool): Whether to log the args and kwargs of the function.
    """

    show_in: bool = (True,)
    show_out: bool = (True,)
    show_data: bool = (True,)
    logger: logging.Logger = (default_logger,)

    def logged(self, message: str) -> Callable[[F], F]:
        """
        Decorator to log the start and finish of a function execution.

        Returns:
            Callable: The decorated function with logging.
        """

        def decorator(func: F) -> F:
            if inspect.iscoroutinefunction(func):

                @wraps(func)
                async def awrapper(*args, **kwargs) -> Any:
                    id = randrange(1, 100_000_000_000)
                    try:
                        if self.show_in:
                            self.logger.log(
                                level=self.logger.level,
                                msg=f"{message} - Starting({id}) *{func.__name__}* with args: {args if self.show_data else ''}, kwargs: {kwargs if self.show_data else ''}",
                            )

                        result = await func(*args, **kwargs)

                        if self.show_out:
                            self.logger.log(
                                level=self.logger.level,
                                msg=f"{message} - Finished({id}) *{func.__name__}* with result: {result if self.show_data else ''}",
                            )
                        return result
                    except Exception as e:
                        self.logger.exception(
                            f"{message} - Exception({id}) *{func.__name__}* raised an exception: {e}"
                        )
                        raise  # Re-raise the exception after logger

                return cast(F, awrapper)
            else:

                @wraps(func)
                def wrapper(*args, **kwargs) -> Any:
                    id = randrange(1, 100_000_000_000)
                    try:
                        if self.show_in:
                            self.logger.log(
                                level=self.logger.level,
                                msg=f"{message} - Starting({id}) *{func.__name__}* with args: {args if self.show_data else ''}, kwargs: {kwargs if self.show_data else ''}",
                            )

                        result = func(*args, **kwargs)

                        if self.show_out:
                            self.logger.log(
                                level=self.logger.level,
                                msg=f"{message} - Finished({id}) *{func.__name__}* with result: {result if self.show_data else ''}",
                            )
                        return result
                    except Exception as e:
                        self.logger.exception(
                            f"{message} - Exception({id}) *{func.__name__}* raised an exception: {e}"
                        )
                        raise

                return cast(F, wrapper)

        return decorator


def logged(
    message: str,
    level: int = logging.INFO,
    show_in: bool = True,
    show_out: bool = True,
    show_data: bool = True,
    logger: logging.Logger = logging.getLogger(),
) -> Callable[[F], F]:
    return Logged(
        show_in=show_in, show_out=show_out, show_data=show_data, logger=logger
    ).logged(message=message)

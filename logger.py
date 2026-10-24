import logging
from typing import Literal

from pydantic import ConfigDict, NonNegativeInt, validate_call

LoggingLevel = Literal[0, 10, 20, 30, 40, 50]
LoggerLevelOverrides = dict[LoggingLevel, list[str]]

VERBOSITY_LEVELS = {0: logging.WARNING, 1: logging.INFO, 2: logging.DEBUG}

LOGGER_LEVEL_OVERRIDES: LoggerLevelOverrides = {logging.WARNING: ["urllib3", "docker"]}


class LoggerFormatter(logging.Formatter):
    """
    Format log records with colored severity levels and module names.

    The module column dynamically expands when a longer module name
    appears and can shrink after a configurable number of consecutive
    records containing shorter module names.

    Attributes:
        COLORS:
            ANSI color codes for logging severity levels.

        MODULE_COLOR:
            ANSI True Color code used for module names (#6400D4).

        RESET:
            ANSI escape code to reset terminal formatting.

        min_module_width:
            Minimum width of the module column.

        module_width:
            Current width of the module column.

        module_width_shrink_after:
            Number of consecutive records with shorter module names
            required before the column width can shrink.
            A value of 0 disables shrinking.
    """

    COLORS = {
        logging.DEBUG: "\033[90m",  # Gray (Bright Black)
        logging.INFO: "\033[32m",  # Green
        logging.WARNING: "\033[33m",  # Yellow
        logging.ERROR: "\033[31m",  # Red
        logging.CRITICAL: "\033[1;31m",  # Bold Red
    }

    MODULE_COLOR = "\033[38;2;100;0;212m"  # #6400D4
    RESET = "\033[0m"  # Reset all formatting

    def __init__(
        self, module_width_shrink_after: int = 200, min_module_width: NonNegativeInt = 0
    ):
        super().__init__()

        self.min_module_width = min_module_width
        self.module_width = self.min_module_width
        self.module_width_shrink_after = module_width_shrink_after

        self.module_width_shrink_count = 0
        self.module_width_shrink_target = self.min_module_width

    def update_module_width(self, module_name: str) -> None:
        """
        Update the module column width based on the current module name.

        Expands immediately when a longer module name appears.
        Shrinks after the configured number of consecutive shorter
        module names, using the longest name observed during that period.

        The width never decreases below min_module_width.

        Args:
            module_name:
                Name of the module producing the log record.
        """

        module_length = len(module_name)

        if module_length >= self.module_width:
            self.module_width = module_length
            self.module_width_shrink_count = 0
            self.module_width_shrink_target = self.min_module_width
            return

        if self.module_width_shrink_after == 0:
            return

        self.module_width_shrink_count += 1
        self.module_width_shrink_target = max(
            self.module_width_shrink_target, module_length
        )

        if self.module_width_shrink_count >= self.module_width_shrink_after:
            self.module_width = self.module_width_shrink_target
            self.module_width_shrink_count = 0
            self.module_width_shrink_target = self.min_module_width

    def format(self, record: logging.LogRecord) -> str:
        """
        Format a log record with timestamp, severity, module and message.

        Args:
            record:
                Log record to format.

        Returns:
            Formatted log message with ANSI color codes.
        """

        timestamp = self.formatTime(record, "%H:%M:%S")
        color = self.COLORS.get(record.levelno, "")

        self.update_module_width(record.module)

        return (
            f"[{timestamp} {color}{record.levelname:<8}{self.RESET}] "
            f"[{self.MODULE_COLOR}{record.module:<{self.module_width}}{self.RESET}]: "
            f"{record.getMessage()}"
        )


@validate_call(config=ConfigDict(strict=True))
def setup_logging(
    verbosity: Literal[0, 1, 2],
    *,
    logger_level_overrides: LoggerLevelOverrides | Literal[False] | None = None,
    module_width_shrink_after: NonNegativeInt = 200,
    min_module_width: NonNegativeInt = 0,
) -> None:
    """
    Configure application logging with colored output and dynamic module widths.

    Configures the root logger using the selected verbosity level and
    applies optional logging-level overrides to specific loggers.

    Module names are displayed in a dynamically sized column that
    automatically expands and optionally shrinks based on recent records.

    Args:
        verbosity:
            Logging verbosity level.

            - 0: WARNING and above.
            - 1: INFO and above.
            - 2: DEBUG and above.

        logger_level_overrides:
            Optional logging-level overrides for specific loggers.

            - None: Use LOGGER_LEVEL_OVERRIDES.
            - False: Skip applying logger-level overrides.
            - dict: Replace the default overrides with the provided mapping.

            Dictionary keys must be valid standard logging levels
            (0, 10, 20, 30, 40, 50).

            Each value must be a list of logger names. Overrides also
            apply to child loggers that inherit their parent's level.

        module_width_shrink_after:
            Number of consecutive log records with module names shorter
            than the current column width before shrinking the column.

            When the threshold is reached, the width is reduced to the
            longest module name observed during that period, but never
            below min_module_width.

            A module name that reaches or exceeds the current width
            resets the shrink counter.

            Defaults to 200.
            Set to 0 to disable automatic shrinking.

        min_module_width:
            Minimum width of the module column in characters.

            The initial module width is set to this value.
            Longer module names automatically expand the column.

            The column never shrinks below this value.

            Defaults to 0, meaning no additional padding is required
            until a longer module name is encountered.

    Raises:
        pydantic.ValidationError:
            If any configuration argument fails validation.

    Returns:
        None.
    """

    handler = logging.StreamHandler()
    handler.setFormatter(LoggerFormatter(module_width_shrink_after, min_module_width))

    logging.basicConfig(
        level=VERBOSITY_LEVELS.get(verbosity, logging.DEBUG),
        handlers=[handler],
        force=True,
    )

    if logger_level_overrides is not False:
        if logger_level_overrides is None:
            logger_level_overrides = LOGGER_LEVEL_OVERRIDES

        for level, logger_names in logger_level_overrides.items():
            for logger_name in logger_names:
                logging.getLogger(logger_name).setLevel(level)

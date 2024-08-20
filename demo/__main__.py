"""Allow to use "python3 -m modersite" to run the manage command."""

import multiprocessing
import os
import sys
import warnings

from df_config.manage import manage


def main():
    """Run the manage command."""
    if not sys.warnoptions:
        warnings.simplefilter("default")  # Change the filter in this process
        os.environ["PYTHONWARNINGS"] = "default"  # Also affect subprocesses
    # avoid "django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet." during parallel testing
    multiprocessing.set_start_method("fork")

    # required for parallel testing on macOS and Python 3.8+
    os.environ["OBJC_DISABLE_INITIALIZE_FORK_SAFETY"] = "YES"
    manage(module_name="demo")


if __name__ == "__main__":
    """Allow to use "python3 -m demo"."""
    main()

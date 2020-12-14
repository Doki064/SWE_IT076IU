import argparse
import subprocess
import sys
from typing import Iterable


def _colored_text(r: int, g: int, b: int, text) -> str:
    # Returns colored text to print to stdout.
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


def _check_package_installed(package: Iterable[str]) -> bool:
    import pkg_resources

    required = set(package)
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed
    return bool(missing)


def main():
    try:
        parser = argparse.ArgumentParser(prog='wms',
                                         description='''Application with Streamlit.''')
        parser.add_argument("COMMAND", type=str, nargs='?', choices=["demo", "install"],
                            help="Argument when running the app.")
        parser.add_argument("--no-pipenv", dest="no_pipenv", action="store_true",
                            help="Flag implies whether to deactivate virtualenv and use system python interpreter.")
        args = parser.parse_args()

        if not args.no_pipenv:
            if _check_package_installed({"pipenv"}):
                print(f"""
                    Pipenv is not installed on your system, consider installing it with:\n
                    \t{_colored_text(91, 192, 222, 'pip3 install pipenv')}\n
                    or specifying --no-pipenv to the command line, for example:\n
                    \t{_colored_text(91, 192, 222, 'python wms --no-pipenv demo')}\n
                """)
                sys.exit(1)

        if args.COMMAND == "demo":
            try:
                if args.no_pipenv:
                    subprocess.run([sys.executable, "run_demo.py"])
                    print(f"{_colored_text(92, 184, 92, 'Demo is running.')}\n")
                else:
                    subprocess.run([sys.executable, "-m", "pipenv", "run", "python", "run_demo.py"])
                    print(f"{_colored_text(92, 184, 92, 'Demo is running.')}\n")

            except KeyboardInterrupt:
                print(f"{_colored_text(2, 117, 216, 'Demo process terminated.')}\n")
                sys.exit(0)

            except subprocess.CalledProcessError as e:
                from datetime import datetime

                print(f"\n{datetime.now()}\n", e.output, file=open("logfiles/demo.log", "w+"))
                print(f"""
                    An error occurred while running demo. Try installing the requirements of the application with:\n
                    \t{_colored_text(91, 192, 222, 'python wms install')}\n
                    If the error still persists, check the log file at logfiles/demo.log for details."\n
                """)
                sys.exit(1)

        elif args.COMMAND == "install":
            try:
                if args.no_pipenv:
                    print(f"{_colored_text(2, 117, 216, 'Installing requirements with pip...')}\n")
                    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
                else:
                    print(f"{_colored_text(2, 117, 216, 'Installing requirements with pipenv...')}\n")
                    try:
                        subprocess.check_call([sys.executable, "-m", "pipenv", "install", "--ignore-pipfile"])
                    except subprocess.CalledProcessError:
                        subprocess.check_call([sys.executable, "-m", "pipenv", "install"])
            except subprocess.CalledProcessError as e:
                from datetime import datetime

                print(f"\n{datetime.now()}\n", e.output, file=open("logfiles/install.log", "w+"))
                print(f"""
                    Make sure you have the required file for the installation:
                    \twith pip: requirements.txt
                    \twith pipenv: Pipfile.lock\n
                    If the error still persists, check the log file at logfiles/install.log for details."\n
                """)
                sys.exit(1)

    except Exception as e:
        sys.exit(f"{_colored_text(217, 83, 79, e)}")


if __name__ == '__main__':
    main()

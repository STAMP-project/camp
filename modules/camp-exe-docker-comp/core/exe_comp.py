import sys, getopt

from core.cli import CLI

def main(commands):
    cli = CLI()
    cli.execute(commands)


def exe_comp_cli():
	main(sys.argv[1:])


if __name__ == "__main__":
	main(sys.argv[1:])
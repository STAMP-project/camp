import sys, getopt, os
from camp_real_engine.cli import CLI

HELPTEXT = 'ramp.py -i <inputfile>'


def execute_cli_command(commands):
    cli = CLI()
    cli.execute(commands)


def main(argv):
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:d:",["ifile=","dir="])
    except getopt.GetoptError:
        print HELPTEXT
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print HELPTEXT
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg

    if not os.path.isfile(inputfile):
        print 'file does not exist: ' + inputfile
        sys.exit()

    commands = ['realize', inputfile]
    execute_cli_command(commands)


def rcamp_main():
    commands = sys.argv[1:]
    execute_cli_command(commands)


if __name__ == "__main__":
    main(sys.argv[1:])
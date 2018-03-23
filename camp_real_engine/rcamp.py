import sys, getopt, os
from camp_real_engine.cli import CLI

HELPTEXT = 'ramp.py -i <inputfile>'

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
    
    command = ['realize', inputfile]
    cli = CLI()
    cli.execute(command)


def rcamp_main():
    print "Call your main application code here"

if __name__ == "__main__":
    main(sys.argv[1:])
import argparse


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument("-l", "--pkgs", help="rpm pkg list")
    args = parse.parse_args()
    if args.pkgs:
        print(args.pkgs)
        print(type(args.pkgs))


main()

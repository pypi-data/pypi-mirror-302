import argparse
from ..src.phonon_to_json import read_file,read_to_write,write_file

AP = argparse.ArgumentParser(prog="phonon_to_json", description="Takes a CASTEp .phonon file and outputs a .json file readable by https://henriquemiranda.github.io/phononwebsite/phonon.html")
AP.add_argument("filename")
AP.add_argument("name", nargs="?", default=None)
AP.add_argument("formula", nargs="?", default=None)

def main():
    args = AP.parse_args()
    if not args.formula:
        args.formula = args.filename
    if not args.name:
        args.name = args.filename
    r_data = read_file(args.filename)
    w_data = read_to_write(r_data, args.name, args.formula)
    write_file(args.filename, w_data)

if __name__ == "__main__":
    main()
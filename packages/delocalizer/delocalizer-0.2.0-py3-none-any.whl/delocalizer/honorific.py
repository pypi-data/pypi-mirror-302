import os
import glob
import argparse

from subdeloc_tools.subtools import SubTools
from subdeloc_tools.modules import pairsubs
from subdeloc_tools.modules import honorific_fixer

parser = argparse.ArgumentParser(description='Modify a subtitle track to make a delocalized version from a JSON file.')
parser.add_argument('--f', dest='folder', type=str, action="store", default=False,
				   help='Folder to save')
parser.add_argument('--ref', dest='reference', type=str, action="store", default=False, required=True,
				   help='Reference subtitle in Japanese')
parser.add_argument('--i', dest='input', type=str, action="store", default=False, required=True,
				   help='Original subtitle')
parser.add_argument('--n', dest='names', type=str, action="store", default=False, required=True,
				   help='Names file')
parser.add_argument('--honor', dest='honorifics', type=str, action="store", default=False,
				   help='Honorifics file')

path = './Honorifics'

def fix_honorifics(sub, ref, names, honorifics=""):
	fname = sub.split(".")[0]
	st = SubTools(sub, ref, names, "./honorifics.json", "[Fixed]"+fname+".ass")
	return st.main()
	# res = pairsubs.pair_files(sub, ref)
	# s = st.search_honorifics(res)
	# return honorific_fixer.fix_original(sub, s, "[Fixed]"+fname+".ass")

def main():
	global path
	args = parser.parse_args()

	if args.folder:
		path = args.folder

	if not path.startswith("./"):
		path = "./"+path

	if not os.path.exists(path):
		os.mkdir(path)

	fix_honorifics(args.input, args.reference, args.names, args.honorifics)

	

if __name__ == '__main__':
	main()

import os,re,sys
import decomposeTDAs
def printInfo():
	print("Longman Dictionary Data Extractor")
	print("Version 1.0")
	print("Developer:")

if __name__=='__main__':
	cmd_options = sys.argv[1:]
	printInfo()
	output_toplevel_dir=os.getcwd()
	dict_toplevel_dir=os.getcwd()
	if len(cmd_options) == 2:
		output_toplevel_dir = os.path.abspath(cmd_options[0])
		dict_toplevel_dir = os.path.abspath(cmd_options[1])
	elif len(cmd_options) == 1:
		output_toplevel_dir = os.path.abspath(cmd_options[0])
	else:
		print("Use Current Directory.")
	if not (os.path.exists(dict_toplevel_dir) and os.path.exists(output_toplevel_dir)):
		os._exit(-1)
	print('Dictionary dir:',dict_toplevel_dir)
	print('Output	  dir:',output_toplevel_dir)
	print('Type any key to begin...')
	#input()
	#begin to parse dictionary data
	for current_dir,subdirs,filenames in os.walk(dict_toplevel_dir):
		# if current directory doesn't contain CONTENT.tda, it isn't the data dir.
		if('CONTENT.tda'.lower() not in [file.lower() for file in filenames]):
			continue
		output_full_dir = os.path.join(output_toplevel_dir, os.path.basename(current_dir))
		print('This directory contains data files:'+current_dir)
		print('Now, output to this path:'+output_full_dir)
		if not os.path.exists(output_full_dir):
			os.makedirs(output_full_dir)
		decps=decomposeTDAs.decompose(current_dir,output_full_dir)
		decps.inflateTDA()
		decps.writeFiles()

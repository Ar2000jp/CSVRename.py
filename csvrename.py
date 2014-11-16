#!/usr/bin/python3
# -*- coding:utf-8 -*-

#
# Copyright (C) 2014 Ahmad Draidi <ar2000jp@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import csv
import argparse

def main():
	csvSrcIndex = 0
	csvDstIndex = 1

	print("CSVRename.py\nCopyright (C) 2014 Ahmad Draidi "
		"<ar2000jp@gmail.com>")

	parser = argparse.ArgumentParser(description="Rename files listed in "
						"CSV file.")
	parser.add_argument("csvFile", help="CSV file to read old & new "
				"names from.", metavar="CSV-FileName")
	parser.add_argument("-i", "--input-dir", help="Folder to get files "
				"from. Default is local dir.", metavar="Dir",
				default="")
	parser.add_argument("-o", "--output-dir", help="Folder to put files "
				"into. Default is the same as input dir.",
				 metavar="Dir")
	parser.add_argument("-s", "--source-index", help="Source file name "
				"index in CSV file. Default is "
				"{0:d}".format(csvSrcIndex), type=int,
				default=csvSrcIndex, metavar="#Index")
	parser.add_argument("-t", "--target-index", help="Target file name "
				"index in CSV file. Default is "
				"{0:d}".format(csvDstIndex), type=int,
				default=csvDstIndex, metavar="#Index")
	parser.add_argument("-f", "--overwrite", help="Overwrite destination.",
				action="store_true")
	parser.add_argument("-d", "--dirs", help="Rename dirs too.",
				action="store_true")
	parser.add_argument("-n", "--nest-into-dirs", help="Put target files "
				"into folders with the same name, "
				"but without the extension.",
				action="store_true")
	args = parser.parse_args()

	csvFileName = args.csvFile
	csvSrcIndex = args.source_index
	csvDstIndex = args.target_index

	srcDir = args.input_dir
	if (args.output_dir):
		dstDir = args.output_dir
	else:
		dstDir = srcDir

	renameDirs = args.dirs
	overwriteDst = args.overwrite
	nestTargetFiles = args.nest_into_dirs

	if(csvSrcIndex == csvDstIndex):
		print("Source and target index can't be the same. Exiting.")
		exit(1)

	try:
		f = open(csvFileName, "r")
	except Exception as e:
		print("Opening CSV file failed!")
		print(e)

	csvReader = csv.reader(f)

	failed = 0
	succeeded = 0
	count = 0
	for row in csvReader:
		count += 1

		try:
			srcName = row[csvSrcIndex]
			dstName = row[csvDstIndex]
		except IndexError as e:
			print("Error while processing CSV file!")
			print(e)
			print()
			exit(1)

		print("Renaming \"{0:s}\" => \"{1:s}\"".format(srcName, dstName))

		dstBaseName = ""
		if (nestTargetFiles):
			(dstBaseName, ext) = os.path.splitext(dstName)

		srcPath = os.path.join(srcDir, srcName)
		dstPath = os.path.join(dstDir, dstBaseName, dstName)

		if not os.path.exists(srcPath):
			print("Source file \"{0:s}\" doesn't exist. Skipping.\n".format(srcPath))
			failed += 1
			continue

		if ((not renameDirs) and (not os.path.isfile(srcPath))):
			print("Source file \"{0:s}\" isn't a file. Skipping.\n".format(srcPath))
			failed += 1
			continue

		if os.path.exists(dstPath):
			print("Destination name \"{0:s}\" already exists. ".format(dstPath), end="")
			if overwriteDst:
				print("Overwriting.")
			else:
				print("Skipping.\n")
				continue

		if (nestTargetFiles):
			try:
				os.mkdir(os.path.join(dstDir, dstBaseName))
			except OSError as e:
				print("Failed while creating dir!")
				print(e)
				print()
				continue

		try:
			os.replace(srcPath, dstPath)
			succeeded += 1
		except OSError as e:
			failed += 1
			print("Rename/Move failed!")
			print(e)
			print()

	print("Finished.")
	print("{0:d} rows processed. {1:d} succeeded. {2:d} failed.".format(count, succeeded, failed))
	f.close()

main()

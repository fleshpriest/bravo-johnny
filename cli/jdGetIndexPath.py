#!/usr/bin/env python3

'''
Stand-alone script which takes a JD index, searches the JD file system for the index.
If the index exists, the full path is returned.

Accepts area, category, or ID (in AC.ID format)
'''

from os.path import abspath, join, isdir
from os import listdir
from sys import argv

root = abspath("/path/to/johnny/decimal/root/directory") # CHANGE ME
indexSeperator = '_' # CHANGE ME


# ======================================================================================================================


def listSubDirs (pathToDir: str) -> list[str]:
    # returns a list of all (non-hidden) subdirectories within a directory

    subDirs = listdir(pathToDir)
    output = []
    for dir in subDirs:
        # Filter out hidden directories & create full filepaths
        if dir[0] != '.':
            # full filepath needed to recursively go deeper into file system.
            output.append(join(pathToDir, dir))

    return output


def generateFsTree (pathToDir: str) -> list[str]:
    # Creates a list of full filepaths to represent a directory tree
    # Note: Fixed depth of 3, extended systems are not currently covered

    msgColorStop = '\033[0m'
    msgColorRed = '\033[91m'
    if not isdir(pathToDir):
        print(f'{msgColorRed}ERROR: {msgColorStop}'
              f'While attempting to generate a file system tree, a non existent path was passed.\n{pathToDir}')
        exit(1)

    tree_jdfs = []

    for area_jdfs in listSubDirs(pathToDir):
        if isdir(area_jdfs):
            tree_jdfs.append(area_jdfs)

            for cat_jdfs in listSubDirs(area_jdfs):
                if isdir(cat_jdfs):
                    tree_jdfs.append(cat_jdfs)

                    for id_jdfs in listSubDirs(cat_jdfs):
                        if isdir(id_jdfs):
                            tree_jdfs.append(id_jdfs)

    # Strip to relative path in directory to easily convert between JDex & Library
    for i in range(len(tree_jdfs)):
        tree_jdfs[i] = tree_jdfs[i].replace(pathToDir + '/', '')

    return tree_jdfs


# ======================================================================================================================

# Create a list of all area, category, & ID directories in the system
tree = generateFsTree(root)

targetIndex = argv[1] + indexSeperator

if targetIndex == "/" + indexSeperator or targetIndex.lower() == "root" + indexSeperator:
    print(root)
for dir in tree:
    if dir.split('/')[-1].startswith(targetIndex):
        print(join(root, dir))
        break
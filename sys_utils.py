from env import src, dst, sep
from os import listdir, makedirs
from os.path import isdir, exists, join
from jd_standardZeros import *

endColor = '\033[0m'
headColor = '\033[95m'
passColor = '\033[92mPASS' + endColor + ' -'
failColor = '\033[91mFAIL' + endColor + ' -'


def printDebug (msg):
    print(headColor, '  DEBUG:', endColor, msg)
    return


def trimPath (fullPathToDir: str, parentPaths: int = 0) -> str:
    # trims full filepath down to dir name, optionally include parent dirs
    # example = '/home/user/1_food/11_fruit/11.01_apple/'
    # trimPath(example)    -> '11.01_apple'
    # trimPath(example, 2) -> '1_food/11_fruit/11.01_apple'

    # TODO: this may not be needed anymore.
    # TODO: Add error handling for list out of range errors
    # TODO: Add logging

    # Sanitize '/' from the end of the filepath if present
    if fullPathToDir[-1] == '/':
        fullPathToDir = fullPathToDir[:-1]

    # Concatenate str for relative path with parent dirs & target dir
    relPath = fullPathToDir.split('/')[-parentPaths-1:]
    output = ''
    for dir in relPath:
        output += dir + '/'

    # remove unnecessary '/' from end of str
    return output[:-1]


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


def generateFsTree (pathToDir: str) -> list[list]:
    # Creates a list of full filepaths to represent a directory tree
    # TODO: Change in a future version to accept a depth of n, instead of a fixed 3

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

    # sanitize path to a relative
    for i in range(len(tree_jdfs)):
        tree_jdfs[i] = tree_jdfs[i].replace(pathToDir, '')

    return tree_jdfs


def convertFsTree (tree: list, outType: str, pathOptional: str = '') -> tuple[list]:
    # Changes a filesystem tree generated from the generateFsTree function for other uses

    # Validate option
    outTypeOptions = ('relative', 'relativeList', 'jdex', 'system', 'arbitrary')
    if not outType in outTypeOptions:
        print('Bad option passed for outType')
        exit(1)

    # Ensure a tuple was not passed
    tree = list(tree)

    # prepare tree (relative format)
    for i in range(len(tree)):
        tree[i] = tree[i].replace(src, '')
        tree[i] = tree[i].replace(dst, '')

    # relative option
    if outType == outTypeOptions[0]:
        return tuple(tree)

    # relativeList option
    elif outType == outTypeOptions[1]:
        for j in range(len(tree)):
            tree[j] = list(filter(None, tree[j].split('/')))
        return tuple(tree)

    # jdex option
    elif outType == outTypeOptions[2]:
        outPath = src

    # system option
    elif outType == outTypeOptions[3]:
        outPath = dst

    # arbitrary path
    elif outType == outTypeOptions[4]:
        # Verify optional path was passed
        if not pathOptional:
            print('No path specified for arbitrary fsTree join')
            exit(1)
        outPath = pathOptional

    print('\n\n\nDEBUG outpath:', outPath, '\n\n\n')

    for k in range(len(tree)):
        tree[k] = join(outPath, tree[k])

    return tuple(tree)


def makeDirAndZeros (path: str, rootDst: str) -> None:
    # path expects relative path to dir, rootDst expects full filepath

    pathsToMake = [join(rootDst, path)]
    for i in sz_getPathToZero(path):
        pathsToMake.append(join(rootDst, i))

    for dir in pathsToMake:
        if not exists(dir):
            # TODO: will make parent directories as needed, change in future to prevent file systemm errors
            makedirs(dir)

    return


#########
# Testing
#########

if __name__ == '__main__':
    foo = generateFsTree(src)
    for i in foo:
        print(i)
    bar = convertFsTree(foo, 'jdex')
    for j in bar:
        print(j)
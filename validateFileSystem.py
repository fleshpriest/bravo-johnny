from env import src, dst, indexSep
from generateLibraryTree import generateFsTree
from os.path import join
from main import JDir

msgColorStop = '\033[0m'
msgColorHead = '\033[95m'
msgColorRed = '\033[91m'
msgPass = '\033[92mPASS' + msgColorStop + ' -'
msgFail = '\033[91mFAIL' + msgColorStop + ' -'


def fsCheck_duplicateIndices (tree: list) -> tuple[str]:

    allDirs = []
    for i in tree:
        allDirs.append(JDir(i))
    allDirs = tuple(allDirs)

    seenIndices = []
    duplicateIndices = []
    for entry in allDirs:
        if not entry.dirIndex in seenIndices:
            seenIndices.append(entry.dirIndex)
        else:
            duplicateIndices.append(entry.pathRelative)

    issues = []
    for entry in allDirs:
        if entry.dirIndex in duplicateIndices:
            issues.append(entry.pathRelative)

    return tuple(issues)


def fsCheck_parentDirs (tree: list) -> tuple[str]:

    issues = []
    for i in tree:
       dir = JDir(i)
       if dir.dirDepth == 1:
           continue
       if dir.dirDepth == 3:
           if dir.idIndex[1] != dir.categoryIndex[1]:
               issues.append(dir.pathRelative)
       if dir.dirDepth >= 2:
           if dir.categoryIndex[0] != dir.areaIndex[0]:
               issues.append(dir.pathRelative)

    return tuple(issues)


def fsCheck_indicesUsed (tree: list) -> tuple[str]:

    issues = []
    for i in tree:
        dir = JDir(i)
        try:
            float(dir.dirIndex)
        except ValueError:
            issues.append(dir.pathRelative)

    return tuple(issues)


def fsCheck_dirsNotInJdex () -> tuple[str]:
    # returns list of any directories present in library which are not present in the Jdex

    srcTree = generateFsTree(src)
    dstTree = generateFsTree(dst)

    difference = list(set(dstTree) - set(srcTree))
    difference.sort()

    return tuple(difference)


def checkFileSystem (pathToDir):

    msgExit = f'{msgColorRed}Please make corrections before revalidating.\nTests stopped & exiting.\n{msgColorStop}'
    print(msgColorHead)
    if pathToDir == src:
        print('Validating JDex @', pathToDir, msgColorStop)
    elif pathToDir == dst:
        print('Validating JD library @', pathToDir, msgColorStop)
    else:
        print('Validating file system @', pathToDir, msgColorStop)
    tree = generateFsTree(pathToDir)

    failedIndexDirs = fsCheck_indicesUsed(tree)
    if not failedIndexDirs:
        print(msgPass, 'All entries use an index.')
    else:
        print(msgFail, 'Directories are missing an index:')
        for missingDir in failedIndexDirs:
            print(missingDir)
        print(msgExit)
        exit(1)

    duplicateIndexs = fsCheck_duplicateIndices(tree)
    if not duplicateIndexs:
        print(msgPass, 'All directories have a unique index.')
    else:
        print(msgFail, 'Duplicate indices present:')
        for duplicate in duplicateIndexs:
            print(duplicate)
        print(msgExit)
        exit(1)

    wrongParents = fsCheck_parentDirs(tree)
    if not wrongParents:
        print(msgPass, 'All directories have the correct parent directories assigned.')
    else:
        print(msgFail, 'Directories present which are assigned to an incorrect parent directory.')
        for bad in wrongParents:
            print(bad)
        print(msgExit)
        exit(1)

    if pathToDir == dst:
        badDirs = fsCheck_dirsNotInJdex()
        if not badDirs:
            print(msgPass, 'Library directories match JDex.')
        else:
            print(msgFail, 'Directories present in library which do not match JDex:')
            for bad in badDirs:
                print(bad)
            print(msgExit)
            exit(1)

    return


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    checkFileSystem(src)
    checkFileSystem(dst)

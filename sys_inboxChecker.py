from env import dst, indexSep, standardZeroTitles
from os import scandir
from os.path import isdir, join

inboxSubStr = standardZeroTitles[1]
somedaySubStr = standardZeroTitles[8]


def filterForInboxDirs (tree: tuple, inboxStr: str) -> tuple[str]:
    # Take a list of directory tree & filter for the passed standard Zero title

    output = []

    for dir in tree:
        if inboxStr in dir and '0' in dir:
            output.append(dir)

    return tuple(output)


def filterForNonEmptyDirs (inboxDirs: tuple, fsRoot: str) -> tuple[str]:
    # Checks list of directories in filesystem for non-empty directories (intended for standard zero inbox & someday)

    print('fsRoot:', fsRoot)
    nonEmptyDirs = []
    for dir in inboxDirs:
        dirFullPath = join(fsRoot, dir)
        print('fulldir:', dirFullPath)
        if not isdir(dirFullPath):
            print('Bad path @', dirFullPath)
            continue
        # TODO: current method only checks for content if inbox is populated, empty sub-directories trigger false positives
        with scandir(dirFullPath) as i:
            if any(i):
                nonEmptyDirs.append(dirFullPath)

    return tuple(nonEmptyDirs)


def checkInboxes () -> tuple[str]:
    treeDst = generateFsTree(dst)
    treeInboxes = filterForInboxDirs(treeDst)
    nonEmptyInboxes = filterForNonEmptyDirs(treeInboxes)
    return tuple(nonEmptyInboxes)


def checkSomedays () -> tuple[str]:
    treeDst = generateFsTree(dst)
    treeSomeday = filterForInboxDirs(treeDst)
    nonEmptySomedays = filterForNonEmptyDirs(treeSomeday)
    return tuple(nonEmptySomedays)


if __name__ == '__main__':
    from generateLibraryTree import generateFsTree
    from os import getcwd

    foo = generateFsTree(dst)
    treeDst = generateFsTree(dst)

    print('\n--- All inboxes in DST: ---')
    bar = filterForInboxDirs(foo, inboxSubStr)
    for i in bar:
        print(i)

    fullPathDst = join(getcwd(), dst)
    print('\n--- All non-empty inboxes in DST: ---')
    baz = filterForNonEmptyDirs(bar, fullPathDst)
    for i in baz:
        print(i)


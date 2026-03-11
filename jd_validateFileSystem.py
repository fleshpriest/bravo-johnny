from development.env import src, dst, sep
from development.sys_utils import convertFsTree, generateFsTree
from os.path import join


def fsCheck_duplicateIndices (tree: list) -> tuple[str]:

    tree = convertFsTree(tree, 'relativeList')
    seenIndices = []
    issues = []

    for i in range(len(tree)):

        # split @ seperator defined in env
        j = tree[i][-1].split(sep)[0]

        if not j in seenIndices:
            seenIndices.append(j)

        else:
            newEntry = ''
            for k in (tree[i]):
                # Convert to relative path
                newEntry = join(newEntry, k)
                # newEntry += k + '/'
            issues.append(newEntry)

    # WARN: Returned strs will be relative paths & will need to be concatenated into full filepaths
    return tuple(issues)


def fsCheck_parentDirs (tree: list) -> tuple[str]:
    # Checks file tree to ensure Indices are assigned to the correct areas & categories

    tree = convertFsTree(tree, 'relativeList')
    issues = []

    for i in tree:

        if len(i) == 1:
            continue

        elif len(i) == 2:
            jdArea_firstDigit = i[0][0]
            jdCat_firstDigit = i[1][0]
            if not jdArea_firstDigit == jdCat_firstDigit:
                issues.append(i)

        elif len(i) == 3:
            jdCat_secondDigit = i[1][1]
            jdId_secondDigit = i[2][1]
            if not jdCat_secondDigit == jdId_secondDigit:
                issues.append(i)

    # Convert to relative path
    issuesOutput = []
    for j in range(len(issues)):
        newEntry = ''
        for k in issues[j]:
            newEntry = join(newEntry, k)
            # TODO: legacy
            # newEntry += k + '/'
        issuesOutput.append(newEntry)

    # WARN: Returned strs will be relative paths & will need to be concatenated into full filepaths
    return tuple(issuesOutput)


def fsCheck_indicesUsed (tree: list) -> tuple[str]:
    # Checks to ensure each dir is using an index

    tree = convertFsTree(tree, 'relativeList')
    issues = []

    for i in tree:

        # split str using seperator defined in env
        jdIndex = i[-1].split(sep)[0]

        try:
            float(jdIndex)
        except ValueError:
            issues.append(i)

    # Convert to relative path
    issuesOutput = []
    for j in range(len(issues)):
        newEntry = ''
        for k in issues[j]:
            newEntry = join(newEntry, j)
            # TODO: legacy
            # newEntry += k + '/'
        issuesOutput.append(newEntry)

    # WARN: Returned strs will be relative paths & will need to be concatenated into full filepaths
    return tuple(issuesOutput)


def fsCheck_suite (pathToDir: str) -> tuple[list[str], list[str]]:
    # Executes all the previous tests
    # Takes path to directory to be tested (jdex or file system)

    treeToCheck = generateFsTree(pathToDir)

    print('\nChecking for duplicate indices.')
    duplicateIndices = tuple(fsCheck_duplicateIndices(treeToCheck))
    if duplicateIndices:
        print("FAIL: Duplicated indices.")
        duplicatePaths = convertFsTree(duplicateIndices, 'arbitrary', treeToCheck)
        for pathToBadDir in duplicatePaths:
            print(pathToBadDir)
    else:
        print("PASS: No duplicate indices.")

    print('\nChecking for correct IDs between child & parent directories.')
    badParentDirs = tuple(fsCheck_parentDirs(treeToCheck))
    if badParentDirs:
        print('FAIL: Wrong parent directories used.')
        badPaths = convertFsTree(badParentDirs, 'arbitrary', treeToCheck)
        for pathToBadDir in badPaths:
            print(pathToBadDir)
    else:
        print('PASS: Correct parent directories used.')

    print('\nChecking that all directories use an index.')
    indicesNeeded = tuple(fsCheck_indicesUsed(treeToCheck))
    if indicesNeeded:
        print('FAIL: Directories are missing indecies')
        badPaths = convertFsTree(indicesNeeded, 'arbitrary', treeToCheck)
        for pathToBadDir in badPaths:
            print(pathToBadDir)
    else:
        print('PASS: All directories have an index')

    # if duplicateIndices or badParentDirs or indicesNeeded:
    #     print('\nManual Intervention is required.')
    #     print('Please correct the above issues & rerun script when finished.')
    #     print('The script will exit now.')
    #     exit(0)

    return tuple(duplicateIndices, badParentDirs, indicesNeeded)


def fsCheck_mismatchedDirs (treeSrc: list, treeDst: list) -> tuple[str]:
    # Compares directory structure of jdex & file system.
    # Reports any unique directories which don't exist between the two.
    # Intended to be ran after fsCheck_suite has been performed to catch valid indices which are not recorded

    treeSrc = list(convertFsTree(treeSrc, 'relative'))
    treeDst = list(convertFsTree(treeDst, 'relative'))

    mismatchesSrc = tuple(set(treeSrc) - set(treeDst))
    mismatchesDst = tuple(set(treeDst) - set(treeSrc))

    srcErrors = tuple(convertFsTree(mismatchesSrc, 'jdex'))
    dstErrors = tuple(convertFsTree(mismatchesDst, 'system'))

    return srcErrors, dstErrors


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    print('\nTesting JDex')
    fsCheck_suite(src)
    jdexErrors, fsErrors = fsCheck_mismatchedDirs(src, dst)

    if jdexErrors:
        print('\nThe following directories exist in the JDex, but not in the file system.')
        for i in jdexErrors:
            print(i)
    else:
        print('\nNo mismatched directories in JDex.')

    if fsErrors:
        print('\nThe following directories exist in the file system, but not in the JDex.')
        for j in fsErrors:
            print(j)
    else:
        print('\nNo mismatched directories in file system.')
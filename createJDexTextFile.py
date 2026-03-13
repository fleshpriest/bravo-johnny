from env import jdexFileTabsPreferred, jdexFileSpacePerTab, jdexFileMarker
from utilDirObject import JDir

def generateJdexText (tree: list[JDir]) -> str:

    if jdexFileTabsPreferred:
        indentation = '\t'
    else:
        indentation = ' ' * jdexFileSpacePerTab

    output = ''
    for i in range(len(tree)):
        output += (tree[i].dirDepth - 1) * indentation + jdexFileMarker + tree[i].dirName
        if not i + 1 == len(tree):
            output += '\n'

    return output


def saveJdexFile (pathToJdexFile: str, pathToFileSystem: str) -> None:

    treeFs = []
    for entry in generateFsTree(pathToFileSystem):
        treeFs.append(JDir(entry))

    fileText = generateJdexText(treeFs)

    with open(pathToJdexFile, 'w') as f:
        f.write(fileText)

    return


if __name__ == '__main__':
    from env import src, jdexFilePath
    from generateLibraryTree import generateFsTree
    from os.path import isfile

    if isfile(jdexFilePath):
        print('Overwriting existing JDex file with updated information.')
    else:
        print('Generating new JDex file.')
    print('JDex File Location:')
    print(jdexFilePath)
    print('JDex Location:')
    print(src)
    saveJdexFile(jdexFilePath, src)
    print('Finished creating new JDex file.')
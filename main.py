from os import listdir, mkdir
from os.path import isdir, join, exists
from env import src, dst, indexSep, adminTitle, adminSep, sz_useAltMethod, standardZeroTitles, szSep


class JDir:
    def __init__(self, pathRelative: str):

        if type(pathRelative) != str:
            print('Class requires a str, but <', pathRelative, '> was passed with type', type(pathRelative))
            exit(1)
        # sanitize str before doing split operations
        if pathRelative[0] == '/':
            pathRelative = pathRelative[1:]
        if pathRelative[-1] == '/':
            pathRelative = pathRelative[:-1]

        # paths
        self.pathRelative = pathRelative
        self.pathInJDex = join(src, self.pathRelative)
        self.pathInFs = join(dst, self.pathRelative)
        self.pathSteps = tuple(pathRelative.split('/', 2))

        # Index & Titles for directories
        self.dirDepth = len(self.pathSteps)
        self.area = self.pathSteps[0]
        self.areaIndex, self.areaTitle = self.area.split(indexSep, 1)
        try:
            self.category = self.pathSteps[1]
            self.categoryIndex, self.categoryTitle = self.category.split(indexSep, 1)
        except IndexError:
            self.category = None
            self.categoryIndex = None
            self.categoryTitle = None
        try:
            self.id = self.pathSteps[2]
            self.idIndex, self.idTitle = self.id.split(indexSep, 1)
        except IndexError:
            self.id = None
            self.idIndex = None
            self.idTitle = None

        # Admin Directory
        if self.dirDepth == 2 and adminTitle in self.categoryTitle:
            self.isAdminDir = True
        else:
            self.isAdminDir = False

        # Standard Zero Directories
        if self.dirDepth == 1:
            self.requiresAdditionalDirs = True
            self.zeroDirPath = join(self.area, f'{self.areaIndex}0{indexSep}{self.areaTitle}{adminSep}{adminTitle}')
            self.associatedDirs = [self.zeroDirPath]
            zeroIndexPrepend, zeroTitle = self.zeroDirPath.split('/', 1)[-1].split(indexSep,1)
            self.zeroDirs = []
            for i in range(len(standardZeroTitles)):
                if standardZeroTitles[i]:
                    standardZeroName = f'{zeroIndexPrepend}.0{i}{indexSep}{zeroTitle}{szSep}{standardZeroTitles[i]}'
                    self.zeroDirs.append(join(self.zeroDirPath, standardZeroName))
            for j in self.zeroDirs:
                self.associatedDirs.append(j)

        elif self.dirDepth == 2:
            self.requiresAdditionalDirs = True
            if sz_useAltMethod:
                self.zeroDirPath = join(self.area, f'{self.areaIndex}0{indexSep}{self.areaTitle}{adminSep}{adminTitle}')
            else:
                self.zeroDirPath = self.pathRelative
            self.associatedDirs = [self.zeroDirPath]
            self.zeroDirs = []
            for k in range(len(standardZeroTitles)):
                if standardZeroTitles[k]:
                    if sz_useAltMethod:
                        zeroIndex = self.zeroDirPath.split('/', 1)[-1].split(indexSep,1)[0] + '.' + self.categoryIndex[1] + str(k)
                    else:
                        zeroIndex = self.categoryIndex + '.0' + str(k)
                    zeroTitle = f'{zeroIndex}{indexSep}{self.categoryTitle}{szSep}{standardZeroTitles[k]}'
                    self.zeroDirs.append(join(self.zeroDirPath, zeroTitle))
                    self.associatedDirs.append(join(self.zeroDirPath, zeroTitle))

        elif self.dirDepth == 3:
            self.requiresAdditionalDirs = False
            self.zeroDirPath = None
            self.zeroDirs = []
            self.associatedDirs = []

    def makeDirs(self):
        dirsToMake = [self.pathInFs]
        if self.requiresAdditionalDirs:
            for dir in self.associatedDirs:
                dirsToMake.append(join(src, dir))
                dirsToMake.append(join(dst, dir))

        print('DEBUG CLASS: dirsToMake:')
        for i in dirsToMake:
            print(i)
        for dir in dirsToMake:
            print('DEBUG CLASS: dir', dir)
            if not exists(dir):
                mkdir(dir)



# ----------------------------------------------------------------------------------------------------------------------
# ----- Testing --------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    print()
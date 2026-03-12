from os.path import isdir, join
from env import src, dst, indexSep, adminTitle, adminSep, sz_useAltMethod


class JDir:
    pathToJdexDir = src
    pathToFsDir = dst

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
        self.pathInJDex = join(self.pathToJdexDir, self.pathRelative)
        self.pathInFs = join(self.pathToFsDir, self.pathRelative)
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
        if self.dirDepth == 3:
            self.zeroDir = None
        # Areas & Categories use same SZ Dir using alt method
        elif self.dirDepth == 1 or sz_useAltMethod:
            self.zeroDir = join(self.area, f'{self.areaIndex}0{indexSep}{self.areaTitle}{adminSep}{adminTitle}')
        # Categories if SZ alt method is not used
        else:
            self.zeroDir = self.pathRelative








# ----------------------------------------------------------------------------------------------------------------------
# ----- Testing --------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# foo = JDir('1_food')
foo = JDir('1_food/11_fruit')
# foo = JDir('1_food/11_fruit/11.01_apple')


# print(foo.pathRelative)
# print(foo.pathSteps)
# print(foo.pathInJDex)
# print(foo.pathInFs)
# print(foo.dirDepth)
# print(foo.area, foo.areaIndex, foo.areaTitle)
# print(foo.category, foo.categoryIndex, foo.categoryTitle)
# print(foo.id, foo.idIndex, foo.idTitle)
print(foo.isAdminDir)
print(foo.zeroDir)
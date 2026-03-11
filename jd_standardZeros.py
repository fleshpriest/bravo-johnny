'''
No direct usage.
Referenced by other scripts to determine correct locations & file names for standard zero directories
'''


from env import src, dst, sep, sz_altMethod, adminTitle, sz_Titles
from sys_utils import convertFsTree


def sz_getPathToZero (pathToDir: str) -> tuple[str]:
    # expects relative path to dir; example: '1_food/11_fruit/11.01_apple'

    # function requires a list, hence this hack
    pathSteps = convertFsTree([pathToDir], 'relativeList')[0]
    output = []

    # Prepare this data for alt method of SZ Category management
    areaIndex, areaTitle = pathSteps[0].split(sep, 1)
    dirName = f'{areaIndex}0{sep}{areaTitle}{sep}{adminTitle}'
    sz_catDir = pathSteps[0] + '/' + dirName

    # ID level dirs are not associated with an admin folder
    if len(pathSteps) == 3:
        return ()

    # Ignore 0_admin folder, manually managed by the user
    elif len(pathSteps) == 1:
        if areaIndex == '0':
            return ()
        else:
            output.append(sz_catDir)

    # Category level dirs vary depending on user preference
    elif len(pathSteps) == 2:
        catIndex, catTite = pathSteps[1].split(sep, 1)

        if sz_altMethod:
            sz_idPrepend = f'{sz_catDir}/{catIndex[1]}0.{catIndex[1]}'
        else:
            sz_idPrepend = f'{pathToDir}/{catIndex}.0'

        for i in range(len(sz_Titles)):
            # ignore blanks left for reserved system expansion (5:7)
            if sz_Titles[i]:
                sz_idTitle = f'{i}{sep}{catTite}{sep}{sz_Titles[i]}'
                sz_idDir = sz_idPrepend + sz_idTitle
                output.append(sz_idDir)

    return tuple(output)


if __name__ == '__main__':
    exit()
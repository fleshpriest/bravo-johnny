from env import src, dst, indexSep
from os import listdir, makedirs
from os.path import isdir, exists, join
# from jd_standardZeros import *



# def makeDirAndZeros (path: str, rootDst: str) -> None:
#     # path expects relative path to dir, rootDst expects full filepath
#
#     pathsToMake = [join(rootDst, path)]
#     for i in sz_getPathToZero(path):
#         pathsToMake.append(join(rootDst, i))
#
#     for dir in pathsToMake:
#         if not exists(dir):
#             # TODO: will make parent directories as needed, change in future to prevent file systemm errors
#             makedirs(dir)
#
#     return
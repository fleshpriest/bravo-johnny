'''
Modify the variables in this file & rename to env.py
'''


# ----------------------------------------------------------------------------------------------------------------------
# ----- Paths ----------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


# NOTE: use full paths to directory starting at root directory

# path to the root directory of the jdex
src = '/path/to/obsidianVault/'

# path to root directory of JD file system (where your areas are located)
dst = '/path/to/jdRoot/'

# path to file for storing the JDex structure as text
jdexFilePath = '/path/to/obsidianVault/jdex.md'


# ----------------------------------------------------------------------------------------------------------------------
# ----- Directory Naming -----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


'''
Directory names are constructed in the following way:
AC.ID + indexSep + dirName + adminSep + adminTitle + szSep + szTitle
ie... 11.01_fruit_admin_jdex
'''

# seperator used between JD Index & Label. ie...
#            sep = '_' -> '31.03_cat'
indexSep = '_'

# title used to designate admin directories for category level 0 lables. ie...
#           adminTitle = 'admin' -> 1_food/10_food_admin
adminTitle = 'admin'

# seperator between directory label & adminTitle
# Todo: integrate
adminSep = '_'

# standard zero titles, empty elements 5:7 are intentional
# appends to the standard zero directory names
sz_Titles = ('jdex',     # 0
             'inbox',    # 1
             'tasks',    # 2
             'template', # 3
             'links',    # 4
             '',         # 5, reserved for expansion
             '',         # 6, reserved for expansion
             '',         # 7, reserved for expansion
             'someday',  # 8
             'archive')  # 9

# seperator between directory label & standard zero title
# todo: integrate
szSep = '_'


# ----------------------------------------------------------------------------------------------------------------------
# ----- Standard Zeros -------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


# True:  standard zeros stored in the category level admin folder. ie... 1_food/10_food_admin/10.21_vegetables_inbox
# False: standard zeros stored in their associated category.       ie... 1_food/12_vegetables/12.01_vegetables_inbox
sz_useAltMethod = True


# ----------------------------------------------------------------------------------------------------------------------
# ----- Auto Generated JDex --------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


# True = runs automatically when new directories are created, False = manual run only
autoGenerateJdexFile = False

# if jdexFileUseTabs = False, spaces will be used instead
jdexFileTabsPreferred = True
jdexFileSpacePerTab = 4

# prepends directory name with the following text in the JDex text file
jdexFileMarker = '- '


# ----------------------------------------------------------------------------------------------------------------------
# ----- Do not Modify Beyond This Point --------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


from os.path import normpath

src = normpath(src)
dst = normpath(dst)
jdexFilePath = normpath(jdexFilePath)
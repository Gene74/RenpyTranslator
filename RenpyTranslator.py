# Librarys

import sys
import getopt
import os
import re


# Methods

def getNumberOfTranslations():
    return len(translation_informations)

def hasTranslations():
    return getNumberOfTranslations() > 0

def getFullTranslationPath(file_name):
    return path_translation_files + file_name

def getFullScriptPath(file_name):
    return path_script_files + file_name


def readTranslations(file_name):
    translation_file = getFullTranslationPath(file_name)
    try:
        f = open(translation_file, "r", encoding="utf-8")
    except:
        print("Error ->", translation_file, "does not exist!")
        return False
    else:
        first_string = ''
        first_line_nr = 0
        
        line_nr = 0
        for line in f.readlines():
            line_nr += 1
            text = re.search("(\".*?\")",line)

            if text != None:
                text = text.group(1)
                if first_string == '' or line_nr > first_line_nr + 1:
                    first_string = text
                    first_line_nr = line_nr

                elif line_nr == first_line_nr + 1:
                    translation_informations[first_string] = text
                    reverse_translation_informations[text] = first_string
                    first_string = ''
                    first_line_nr = 0

                else:
                    first_string = ''
                    first_line_nr = 0

            else:
                continue
        f.close()
        return True


def translate(file_name, create_backups, reverse_translation):
    if not hasTranslations():
        return False
    
    # Read all lines
    script_file = getFullScriptPath(file_name)
    try:
        f = open(script_file, "r", encoding="utf-8")
    except:
        print("Error ->", script_file, "does not exist!")
        return False
    else:
        data = ''
        for line in f:
            data += line
        f.close()

    # Reverse the Translation?
    if not reverse_translation:
        t_informations = translation_informations
    else:
        t_informations = reverse_translation_informations

    # Proceed with the translation
    for key in t_informations:
        old_string = key
        new_string = t_informations[key]
        data = data.replace(old_string, new_string)

    # Backup the original file
    if create_backups:
        backup_file_name = script_file
        while os.path.isfile(backup_file_name):
            backup_file_name += ".bak"
        try:
            os.rename(script_file, backup_file_name)
        except:
            print("Error -> An exception occured while proceeding file", backup_file_name)
            return False
    else:
        try:
            os.remove(script_file)
        except:
            print("Error -> Couldn't delete original file", script_file)
            return False

    # Save the translated file
    translated_file = open(script_file, "w", encoding="utf-8")
    translated_file.write(data)
    translated_file.close()
    return True


def usage():
    print("usage: RenpyTranslator.py [-h] -t <path> -s <path> [-r] [-n]")
    print("     -h ... this help text")
    print("     -t ... directory with translation files")
    print("     -s ... directory with script files")
    print("     -r ... optional, reverse translation")
    print("     -n ... dont create backups")
    print()
    print("example: RenpyTranslator.py -t ./game -s ./game/tl/english")
    print()
    return


# MAIN PROGRAM START

print()
print("-" * 80)
print("RENPY-TRANSLATOR (created by Gene74 in 2018)")
print("-" * 80)

# Folders
path_translation_files = ''
path_script_files = ''

# Translation Informations
translation_informations = {}           # All found translation pairs
reverse_translation_informations = {}   # All found translation pairs reversed

# Flags
reverse_translation = False
create_backup_files = True

#Read Arguments
if len(sys.argv) < 5:
    print("\nNot enough arguments, see usage below:\n")
    usage()
    sys.exit(0)
    
try:
    opts, args = getopt.getopt(sys.argv[1:],"ht:s:rn")

except getopt.GetoptError:
    usage()
    sys.exit(0)

for opt, arg in opts:

    if opt == '-h':
        usage()
        sys.exit(0)

    elif opt == '-t':
        path_translation_files = arg
        if not path_translation_files.endswith("/"):
            path_translation_files += "/"
        if not os.path.isdir(path_translation_files):
            print("Path to translation files '" + path_translation_files + "' -> could not be found!")
            sys.exit(0)

    elif opt == '-s':
        path_script_files = arg
        if not path_script_files.endswith("/"):
            path_script_files += "/"
        if not os.path.isdir(path_script_files):
            print("Path to script files '" + path_script_files + "' -> could not be found!")
            sys.exit(0)

    elif opt == '-r':
        reverse_translation = True

    elif opt == '-n':
        create_backup_files = False


if path_translation_files == '' or path_script_files == '':
    usage()
    sys.exit(0)


# File Counters
translation_files = 0
translated_files = 0
non_translated_files = 0

# Read translation files
print()
print("reading translation files:")
print("--------------------------")

for filename in os.listdir(path_translation_files):
    if filename.endswith(".rpy"):
        print(getFullTranslationPath(filename), "...", end='')
        translation_files += 1
        if readTranslations(filename):
            print(" OK")
        else:
            print(" FAIL")
            

# Continue with translation?
if translation_files == 0:
    print("There was no translation file found in path '" + path_translation_files + "'")
    sys.exit(0)

elif not hasTranslations():
    print("No translation informations were found in translation files in path '" + path_translation_files + "'")
    sys.exit(0)

else:
    # Translate script files
    print()
    print("translate script files:")
    print("-----------------------")

    for filename in os.listdir(path_script_files):
        if filename.endswith(".rpy"):
            print(getFullScriptPath(filename), "...", end='')
            if translate(filename, create_backup_files, reverse_translation):
                print(" OK")
                translated_files += 1
            else:
                print(" FAIL")
                non_translated_files += 1

    print()
    print("-" * 80)
    print("translated files    :", str(translated_files))
    print("non-translated files:", str(non_translated_files))
    print("-" * 80)
    print()

# PROGRAM END
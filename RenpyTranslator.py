# Librarys
import sys
import getopt
import os
import re


# Translation Class
class TranslationFile:

    file_name = ''                          # This filename is the same in both directories
    path_translation_files = ''             # Directory with translation files
    path_script_files = ''                  # Directory with files to translate
    translation_informations = {}           # All found translation pairs
    reverse_translation_informations = {}   # All found translation pairs reversed

    def __init__(self, file_name, path_translation_files, path_script_files):
        self.file_name = file_name
        self.path_translation_files = path_translation_files
        self.path_script_files = path_script_files

    def getNumberOfTranslations(self):
        return len(self.translation_informations)

    def hasTranslations(self):
        return self.getNumberOfTranslations() > 0

    def getFullTranslationPath(self):
        return self.path_translation_files + self.file_name

    def getFullScriptPath(self):
        return self.path_script_files + self.file_name

    def readTranslations(self):
        translation_file = self.getFullTranslationPath()
        try:
            f = open(translation_file, "r", encoding="utf-8")
        except:
            print("Error -> File", translation_file, "does not exist!")
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
                        self.translation_informations[first_string] = text
                        self.reverse_translation_informations[text] = first_string
                        first_string = ''
                        first_line_nr = 0

                    else:
                        first_string = ''
                        first_line_nr = 0

                else:
                    continue
            f.close()
            return True

    def translate(self, reverseTranslation):
        if self.getNumberOfTranslations() == 0:
            return False
        
        # Read all lines
        script_file = self.getFullScriptPath()
        try:
            f = open(script_file, "r", encoding="utf-8")
        except:
            print("Error -> File", script_file, "does not exist!")
            return False
        else:
            data = ''
            for line in f:
                data += line
            f.close()

        # Reverse the Translation?
        if not reverseTranslation:
            t_informations = self.translation_informations
        else:
            t_informations = self.reverse_translation_informations

        # Proceed with the translation
        for key in t_informations:
            old_string = key
            new_string = t_informations[key]
            data = data.replace(old_string, new_string)

        # Backup the original file
        backup_file_name = script_file
        while os.path.isfile(backup_file_name):
            backup_file_name += ".bak"
        try:
            os.rename(script_file, backup_file_name)
        except:
            print("Error -> An exception occured while proceeding file", backup_file_name)
            return False

        # Save the translated file
        translated_file = open(script_file, "w", encoding="utf-8")
        translated_file.write(data)
        translated_file.close()
        return True

    def printAll(self):
        print(self.translation_informations)


# print out help text
def usage():
    print("usage: RenpyTranslator.py [-h] -t <path> -s <path> [-r]")
    print("     -h ... this help text")
    print("     -t ... directory with translation files")
    print("     -s ... directory with script files")
    print("     -r ... optional, reverse translation")
    print()
    print("example: RenpyTranslator.py -t ./game/ -s ./game/tl/english/")
    print()
    return


# MAIN PROGRAM START

# Folder with translation files
path_translation_files = ''

# Folder with script files
path_script_files = ''

# Should the translation be reversed?
reverse_translation = False

#Read Arguments
if len(sys.argv) < 5:
    print("\nNot enough arguments, see usage below:\n")
    usage()
    sys.exit(0)
    
try:
    opts, args = getopt.getopt(sys.argv[1:],"ht:s:r")

except getopt.GetoptError:
    usage()
    sys.exit(0)

for opt, arg in opts:

    if opt == '-h':
        usage()
        sys.exit(0)

    elif opt == '-t':
        path_translation_files = arg

        if not os.path.isdir(path_translation_files):
            print("Path to translation files '" + path_translation_files + "' -> could not be found!")
            sys.exit(0)

    elif opt == '-s':
        path_script_files = arg

        if not os.path.isdir(path_script_files):
            print("Path to script files '" + path_script_files + "' -> could not be found!")
            sys.exit(0)

    elif opt == '-r':
        reverse_translation = True

if path_translation_files == '' or path_script_files == '':
    usage()
    sys.exit(0)


# Read files
checked_files = 0
translated_files = 0
non_translated_files = 0

print()
print("----------------------------------------------------")
print("processing files ...")

for filename in os.listdir(path_translation_files):

    if filename.endswith(".rpy"):
        checked_files += 1
        translation_file = TranslationFile(filename, path_translation_files, path_script_files)

        if translation_file.readTranslations() and translation_file.hasTranslations():

            if translation_file.translate(reverse_translation):
                print(path_script_files+filename, "-> translated successfully")
                translated_files += 1

            else:
                print(path_script_files+filename, "-> was not translated")
                non_translated_files += 1


if checked_files == 0:
    print("There was no translation file found in path '" + path_translation_files + "'")
    sys.exit(0)

else:
    print("----------------------------------------------------")
    print("translated files    :", str(translated_files))
    print("non-translated files:", str(non_translated_files))
    print("----------------------------------------------------")
    print()

# PROGRAM END
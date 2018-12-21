import sys
import os
import TranslationFile


# Folder with files
pathFiles = "./files/"

# Folder with files with translation informations
pathTranslations = "./translations/"

# Should the translation be reversed?
reverseTranslation = False
if len(sys.argv) > 0:
    if sys.argv[0] == "-r":
        reverseTranslation = True


# Read files
for filename in os.listdir(pathTranslations):
    if filename.endswith(".rpy"):
        tf = TranslationFile.TranslationFile(filename, pathTranslations, pathFiles)
        if tf.readTranslations() and tf.hasTranslations():
            if tf.translate(reverseTranslation):
                print(filename, "-> translated successfully")
            else:
                print(filename, "-> was not translated")

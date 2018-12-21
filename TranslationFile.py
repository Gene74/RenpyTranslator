import os
import sys
import re
import TranslationInformation


class TranslationFile:

    fileName = ''                   # This filename is the same in both directories
    translationPath = ''            # Directory with translation files
    filePath = ''                   # Directory with files to translate
    translationInformations = {}    # All found translation pairs
    revInformations = {}            # All found translation pairs reversed


    def __init__(self, fileName, translationPath, filePath):
        self.fileName = fileName
        self.translationPath = translationPath
        self.filePath = filePath


    def getNumberOfTranslations(self):
        return len(self.translationInformations)


    def hasTranslations(self):
        return self.getNumberOfTranslations() > 0


    def getFullTranslationPath(self):
        return self.translationPath + self.fileName


    def getFullFilePath(self):
        return self.filePath + self.fileName


    def readTranslations(self):
        path = self.getFullTranslationPath()
        try:
            f = open(path, "r", encoding="utf-8")
        except:
            print("Error -> File", path, "does not exist!")
            return False
        else:
            firstString = ''
            firstLineNr = 0
            
            lineNr = 0
            for line in f.readlines():
                lineNr += 1
                text = re.search("(\".*?\")",line)

                if text != None:
                    text = text.group(1)
                    if firstString == '' or lineNr > firstLineNr + 1:
                        firstString = text
                        firstLineNr = lineNr

                    elif lineNr == firstLineNr + 1:
                        self.translationInformations[firstString] = text
                        self.revInformations[text] = firstString
                        firstString = ''
                        firstLineNr = 0

                    else:
                        firstString = ''
                        firstLineNr = 0

                else:
                    continue
            f.close()
            return True


    def translate(self, reverseTranslation):
        if self.getNumberOfTranslations() == 0:
            return False
        
        # Read all lines
        path = self.getFullFilePath()
        try:
            f = open(path, "r", encoding="utf-8")
        except:
            print("Error -> File", path, "does not exist!")
            return False
        else:
            data = ''
            for line in f:
                data += line
            f.close()

        # Reverse the Translation?
        if not reverseTranslation:
            informations = self.translationInformations
        else:
            informations = self.revInformations

        # Proceed with the translation
        for key in informations:
            oldString = key
            newString = informations[key]
            data = data.replace(oldString, newString)

        # Backup the original file
        backup = path
        while os.path.isfile(backup):
            backup += ".bak"
        try:
            os.rename(path, backup)
        except:
            print("Error -> An exception occured while proceeding file", backup)
            return False

        # Save the translated file
        tf = open(path, "w", encoding="utf-8")
        tf.write(data)
        tf.close()
        return True


    def printAll(self):
        print(self.translationInformations)

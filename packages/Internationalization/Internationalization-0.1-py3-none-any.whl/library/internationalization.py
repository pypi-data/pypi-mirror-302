import os
import json

class Internationalization:
    appNameMapping = {
        'QT': 'QTLauncher',
        'PR': 'Picarro',
        'TL': 'TestLauncher'
    }

    def __init__(self, appName, language='EN', additionalLanguageFilePath=None):
        self.appName = appName
        self.language = language.lower()
        self.localeDict = {}
        # self.defaultDict = {}

        projectBasePath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

        fullAppName = self.appNameMapping.get(self.appName)

        self.basePath = os.path.join(projectBasePath, 'library', fullAppName)

        self.loadLanguageFiles(additionalLanguageFilePath)

    def loadLanguageFiles(self, additionalLanguageFilePath):
        localeFilePath = os.path.join(self.basePath, f"language_{self.language}.json")
        # defaultFilePath = os.path.join(self.basePath, "language_en.json")

        self.localeDict = self.getDataFromFile(localeFilePath)
        # self.defaultDict = self.getDataFromFile(defaultFilePath)

        if additionalLanguageFilePath:
            additionalDict = self.getDataFromFile(additionalLanguageFilePath)
            if additionalDict:
                self.localeDict.update(additionalDict)

    def getDataFromFile(self, filePath):
        """Reads JSON data from a file and returns it as a dictionary."""
        if not os.path.exists(filePath):
            return None
        with open(filePath, "r", encoding='utf-8') as fileObj:
            return json.load(fileObj)

    def getLocaleText(self, key):
        """Returns the localized text for the given key."""
        if self.localeDict is None:
            return key

        textToReturn = self.localeDict.get(key)

        if textToReturn is None:
            return key

        return textToReturn

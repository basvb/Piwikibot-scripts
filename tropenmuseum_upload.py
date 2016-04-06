#!/usr/bin/python
# -*- coding: utf-8  -*-
import sys
sys.path.append("..")
from scripts.upload import UploadRobot #stated to be unresolved, but works fine
import pandas as pd

def load_metadata():
    '''
    This function loads the metadata from the given csv-file.
    '''
    location_metadata='D:/Wikipedia/Tropenmuseum/tropenmuseum_metadata.csv'
    metadata=pd.read_csv(location_metadata)
    return metadata

def upload_file(file_location, description, filename):
    '''
    Given a description, file_location and filename this function uploads the file at the file location using the
    description using the filename given as filename on Commons.
    '''
    url=file_location
    bot = UploadRobot(url, description=description, useFilename=filename, keepFilename=True, verifyDescription=False)
    bot.run()

def main():
    '''
    The main loop
    First the metadata is loaded and some variables are defined.
    Then for each file:
    First the source URL gets defined
    then the destination file name gets defined
    then a long part of the code defines what ends up in the descriptions with a lot of checks and dependencies on
    whether data exists

    after this is done the upload function is called to upload the file using the determined source, description
    and file name
    '''

    metadata=load_metadata()
    file_folder='D:/Wikipedia/Tropenmuseum/Tropenmuseum_afbeeldingen/'
    begin=20 #to define the beginning and end by hand if some files are already uploaded
    end=metadata.shape[0] #either all files or a specified ending index to stop at.
    for i in range(begin, end): #for each file
        #define the url where the file can be found:
        url=file_folder + str(metadata.loc[i]['ObjectNumber']) + '.jpg'

        #define the title to use on Commons:
        #If an English title is available use it (otherwise Dutch)
        # and if the orginal title is longer than 70 characters it gets shortened to 65 characters
        if not pd.isnull(metadata.loc[i]['TitleEN']):
            if len(metadata.loc[i]['TitleEN'])<70:
                filename=metadata.loc[i]['TitleEN']
            else:
                filename=metadata.loc[i]['TitleEN'][:65] + '...'
        else:
            if len(metadata.loc[i]['TitleNL'])<70:
                filename=metadata.loc[i]['TitleNL']
            else:
                filename=metadata.loc[i]['TitleNL'][:65] + '...'
        filename+=' - Collectie stichting Nationaal Museum van Wereldculturen - ' +metadata.loc[i]['ObjectNumber'] + '.jpg'

        #start with defining the description, mostly self-explanatory and not useful to explain for other uploads.
        description='=={{int:filedesc}}==\n\n{{Photograph\n' #first lines
        description+='| photographer     = ' + metadata.loc[i]['Photographer'] + '\n' #add the photographer-line
        description+='| title            = '
        if not pd.isnull(metadata.loc[i]['TitleNL']):
            description+='{{nl|' + metadata.loc[i]['TitleNL'] + '}}'
        if not pd.isnull(metadata.loc[i]['TitleEN']):
            description+='{{en|' + metadata.loc[i]['TitleEN'] + '}}'
        description+='\n| description      = '
        if not pd.isnull(metadata.loc[i]['Description']):
            description+= '{{nl|' + metadata.loc[i]['Description'] + '\n'
        else:
            description+= '{{nl|'
        if not pd.isnull(metadata.loc[i]['Religion']):
            description+='\'\'\'Religie:\'\'\' ' + metadata.loc[i]['Religion'] + '\n'
        if not pd.isnull(metadata.loc[i]['Culture']):
            description+='\'\'\'Cultuur:\'\'\' ' + metadata.loc[i]['Culture'] + '\n'
        if not pd.isnull(metadata.loc[i]['IndigenousName']):
            description+='\'\'\'Inheemse naam:\'\'\' ' + metadata.loc[i]['IndigenousName'] + '\n'
        if not pd.isnull(metadata.loc[i]['OnderwerpNL']):
            description+='\'\'\'Onderwerp:\'\'\' ' + metadata.loc[i]['OnderwerpNL'] + '\n'
        description+='}}\n'
        if not pd.isnull(metadata.loc[i]['SubjectEN']):
            description+='{{en|\'\'\'Subject:\'\'\' ' + metadata.loc[i]['SubjectEN'] + '}}\n'
        if not pd.isnull(metadata.loc[i]['RelatedPersons']):
            description+='| depicted people  = ' + metadata.loc[i]['RelatedPersons'] + '\n'
        if not pd.isnull(metadata.loc[i]['RelatedLocations']):
            description+='| depicted place   = ' + metadata.loc[i]['RelatedLocations'] + '\n'
        description+='| date             = ' + metadata.loc[i]['Date'] + '\n| medium           = '
        if not pd.isnull(metadata.loc[i]['MateriaalNL']):
            description+='{{nl|' + metadata.loc[i]['MateriaalNL'] + '}}'
        if not pd.isnull(metadata.loc[i]['MaterialEN']):
            description+='{{en|' + metadata.loc[i]['MaterialEN'] + '}}'
        description+='\n| dimensions       = ' + metadata.loc[i]['Dimensions'] + '\n'
        if not pd.isnull(metadata.loc[i]['RelatedInstitutions']):
            description+='| institution     = ' + metadata.loc[i]['RelatedInstitutions'] + '\n'
        if not pd.isnull(metadata.loc[i]['Credits']):
            description+='| credit line      = ' + metadata.loc[i]['Credits'] + '\n'
        description+='| accession number = ' + metadata.loc[i]['ObjectNumber'] + '\n'
        description+='| source           = {{KIT-ccid|' + str(metadata.loc[i]['ObjectID']) + '}}{{Expedition Wikipedia}}\n'
        description+='| permission       = ' + metadata.loc[i]['License'] + '\n}}\n\n'
        #from here on categories
        description+='[[Category:Files from the Nationaal Museum van Wereldculturen]]\n'

        if not pd.isnull(metadata.loc[i]['Commonscat1']):
            description+='[[Category:' + metadata.loc[i]['Commonscat1'] + ']]\n'
        if not pd.isnull(metadata.loc[i]['Commonscat2']):
            description+='[[Category:' + metadata.loc[i]['Commonscat2'] + ']]\n'

        upload_file(url, description, filename)

if __name__ == "__main__":
    main()

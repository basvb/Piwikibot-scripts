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
        description+='[[Category:Files from the Nationaal Museum van Wereldculturen]]\n'

        if not pd.isnull(metadata.loc[i]['Commonscat1']):
            description+='[[Category:' + metadata.loc[i]['Commonscat1'] + ']]\n'
        if not pd.isnull(metadata.loc[i]['Commonscat2']):
            description+='[[Category:' + metadata.loc[i]['Commonscat2'] + ']]\n'
        if metadata.loc[i]['ObjectNumber'] in ['TM-60009978', 'TM-60010004', 'TM-60010015', 'TM-60010060', 'TM-60010061', 'TM-60010062',
                                               'TM-60010081', 'TM-60010111', 'TM-60010162', 'TM-60010163', 'TM-60014986', 'TM-60014987', 'TM-60014998', ]:
            if metadata.loc[i]['ObjectNumber'] in ['TM-60009978']:
                filename='Expeditielid J.W. van Nouhuys bij een boom in de rivier Ingsim - Collectie stichting Nationaal Museum van Wereldculturen - TM-60009978.jpg'

            if metadata.loc[i]['ObjectNumber'] in ['TM-60010004']:
                filename='Een Papua in een kano op het Sentani-meer - Collectie stichting Nationaal Museum van Wereldculturen - TM-60010004.jpg'

            if metadata.loc[i]['ObjectNumber'] in ['TM-60010015']:
                filename='Paalwoningen bij Poejo in het Sentani-meer - Collectie stichting Nationaal Museum van Wereldculturen - TM-60010015.jpg'

            if metadata.loc[i]['ObjectNumber'] in ['TM-60010060']:
                filename='Prauwen met Papua\'s in de Humboldt-baai bij de Zeemeeuw - Collectie stichting Nationaal Museum van Wereldculturen - TM-60010060.jpg'

            if metadata.loc[i]['ObjectNumber'] in ['TM-60010061']:
                filename='Prauwen met Papua\'s in de Humboldt-baai  bij het vertrek van h... - Collectie stichting Nationaal Museum van Wereldculturen - TM-60010061.jpg'

            if metadata.loc[i]['ObjectNumber'] in ['TM-60010062']:
                filename='Prauwen met Papua\'s in de Humboldt-baai bij het vertrek van h... - Collectie stichting Nationaal Museum van Wereldculturen - TM-60010062.jpg'

            if metadata.loc[i]['ObjectNumber'] in ['TM-60010081']:
                filename='Gezicht op een onderneming bij de ambtswoning van assistent-r... - Collectie stichting Nationaal Museum van Wereldculturen - TM-60010081.jpg'

            if metadata.loc[i]['ObjectNumber'] in ['TM-60010111']:
                filename='Portret van een groep Papua\'s bij Joka aan het Sentani-meer - Collectie stichting Nationaal Museum van Wereldculturen - TM-60010111.jpg'

            if metadata.loc[i]['ObjectNumber'] in ['TM-60010163']:
                filename='Portret van een Papua familie voor hun huis - Collectie stichting Nationaal Museum van Wereldculturen - TM-60010163.jpg'

            if metadata.loc[i]['ObjectNumber'] in ['TM-60014986']:
                filename='Portret van een groep Papua\'s bij Joka aan het Sentani-meer - Collectie stichting Nationaal Museum van Wereldculturen - TM-60014986.jpg'

            if metadata.loc[i]['ObjectNumber'] in ['TM-60014987']:
                filename='Portret van de korano\'s van Tobadi en Ajapo bij Joka aan het ... - Collectie stichting Nationaal Museum van Wereldculturen - TM-60014987.jpg'

            if metadata.loc[i]['ObjectNumber'] in ['TM-60014998']:
                filename='Expeditielid L.F. de Beaufort met Papua\'s bij Joka aan het Se... - Collectie stichting Nationaal Museum van Wereldculturen - TM-60014998.jpg'

            upload_file(url, description, filename)
        #upload_file(url, description, filename)


if __name__ == "__main__":
    main()

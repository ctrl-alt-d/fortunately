# -*- coding: utf-8 -*- 

import os   #work with paths
import sys  #IO
import unicodecsv  #unicode csv on python 2.7 
import logging     
import urllib   #download images
from PIL import Image   #resize images
from appy.pod.renderer import Renderer   #render documents

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

logging.info('**start**')

#initialize global vars
PROJECT_DIR = os.path.dirname(__file__)
location = lambda x: os.path.join(PROJECT_DIR, x)

#TODO: guess from filesystem
KNOWLEDGE_AREA = [ location(x) for x in
                     ( r'cards/computers/basic_computer', 
                       r'cards/computers/database', 
                       r'cards/computers/networking', 
                       r'cards/computers/developing', 
                       r'cards/computers/operating_system', 
                       r'cards/law/international',
                     ) 
                    ]

#improve: work with several templates.
MASTERCARD_TEMPLATE =  location( r'cards/mastercards/row_x_3_modelA.odt' )

TMP_DIR = location( r'tmp' )

SIZE = 240, 145

ERROR_IMAGE = r'http://4.bp.blogspot.com/-yUsv10OBHSA/U3uJFpzuMzI/AAAAAAAADjU/9_RAscdDA_4/s1600/error+404+54411+error-404.jpg'
if True:    #imatge a posar si no es pot utilitzar la del fitxer
    url = ERROR_IMAGE
    logging.info('url: ' + url)
    local_file = location( os.path.join( 'tmp/', url.rsplit('/',1)[1] ) ).lower()
    urllib.urlretrieve(url, local_file)
    im = Image.open(local_file)
    im.thumbnail(SIZE, Image.ANTIALIAS)
    im.save(local_file)
    ERROR_IMAGE_LOCAL_FILE = local_file 

logging.info('main loop')
for card_to_generate in KNOWLEDGE_AREA:

    csv_path = os.path.join(card_to_generate, 'cards.csv' )

    logging.info( csv_path )
    try:    
        file=open(csv_path, "rb")
    except IOError:
        logging.warning( 'fitxer [{0}] no trobat'.format( csv_path ) )
        continue
    reader = unicodecsv.DictReader(file, encoding='utf-8')

    logging.info( 'opened, reading rows' )
    cards = list(  reader )
    
    #downloading images
    if not os.path.exists( TMP_DIR ):
        os.makedirs( TMP_DIR )
    for card in cards:        
        #internet url
        url = card['picture']
        logging.info('url: ' + url)
        local_file = location( os.path.join( 'tmp/', url.rsplit('/',1)[1] ) ).lower()
        urllib.urlretrieve(url, local_file)
        #resizing
        try:
            im = Image.open(local_file)
            im.thumbnail(SIZE, Image.ANTIALIAS)
            im.save(local_file)
        except:
            loca_file = ERROR_IMAGE_LOCAL_FILE                    
            logging.warning( 'bad image: ' + url )
        
        #setting local path            
        card['picture'] = local_file
    
    report_data = {
                        'cards': cards,
                   }

    logging.info( 'ready to render' )
    target_file = os.path.join(card_to_generate, 'bin_cards/cards.odt' ) 
    renderer = Renderer(MASTERCARD_TEMPLATE , report_data, target_file, overwriteExisting=True )
    renderer.run()
    logging.info( 'finished' )
    
logging.info('**end**')

    
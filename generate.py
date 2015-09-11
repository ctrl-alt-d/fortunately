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

CARDS_TO_GENERATE = [ location(x) for x in
                     ( r'cards/computers/basic_computer', 
                       r'cards/computers/database', 
                       r'cards/law/international',
                     ) 
                    ]

MASTERCARD_TEMPLATE =  location( r'cards/mastercards/row_x_3_modelA.odt' )
TMP_DIR = location( r'tmp' )

logging.info('main loop')
for card_to_generate in CARDS_TO_GENERATE:

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
    for card in cards:
        url = card['picture']
        local_file = location( os.path.join( 'tmp/', url.rsplit('/',1)[1] ) ).lower()
        urllib.urlretrieve(url, local_file)
        im = Image.open(local_file)        
        size = 240, 145
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(local_file)
                    
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

    
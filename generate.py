# -*- coding: utf-8 -*- 

import os
import sys
import unicodecsv
from appy.pod.renderer import Renderer
import logging
import codecs


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
    
    print cards

    report_data = {
                        'cards': cards,
                   }

    logging.info( 'ready to render' )
    target_file = os.path.join(card_to_generate, 'bin_cards/cards.odt' ) 
    renderer = Renderer(MASTERCARD_TEMPLATE , report_data, target_file, overwriteExisting=True )
    renderer.run()
    logging.info( 'finished' )
        
            
    
logging.info('**end**')    
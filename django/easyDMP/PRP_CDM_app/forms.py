from PRP_CDM_app.models import *

class FormsDefinition:

    class LageForm:
        lab = 'LAGE'
        content = [
            Administration,
            lageSample,
        ]

        exclude = { 'Administration':
                   ['sr_id',
                   'user_id',
                   'lab_id',
                   ],
                   'lageSample':
                   ['sr_id',
                   'user_id',
                   ],
                   }

    class LameForm:
        lab = 'LAME'
        content = [
            Administration,
            lageSample,
        ]
        
        exclude = { 'Administration':
                   ['sr_id',
                   'user_id',
                   'lab_id',
                   'experimentabstract',
                   ],
                   'lageSample':
                   ['sr_id',
                   'user_id',
                   'expected_date_of_delivery',
                   'is_quality',
                   'is_buffer_used',
                   'is_volume_in_uL',
                   ],
                   }

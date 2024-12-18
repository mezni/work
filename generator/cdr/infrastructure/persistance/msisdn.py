from tinydb import TinyDB, Query
import random
from typing import List, Optional
from entities.value_objects.msisdn import MSISDN
from entities.repositories.msisdn import MSISDNRepository

class TinyDBMSISDNRepository(MSISDNRepository):
    def __init__(self, db_file: str = 'db.json'):
        self.db = TinyDB(db_file)
        self.msisdn_table = self.db.table('_default')

    def get_random(self) -> Optional['MSISDN']:
        msisdns = self.msisdn_table.all()
        if msisdns:
            random_record = random.choice(msisdns)
            return MSISDN(random_record['msisdn'])
        return None
from infrastructure.persistance.msisdn import TinyDBMSISDNRepository
db_file = 'db.json'  
msisdn_repo = TinyDBMSISDNRepository(db_file)
random_msisdn = msisdn_repo.get_random()
print(random_msisdn)
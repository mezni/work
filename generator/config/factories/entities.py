import random
from ..entities.customer import Customer
from ..entities.bearer import Bearer
from ..entities.qos import QoS

class EntityFactory:
    @staticmethod
    def generate_qos() -> QoS:
        gbr = random.randint(100, 1000)
        mbr = random.randint(1000, 10000)
        return QoS(gbr, mbr)

    @staticmethod
    def create_bearer(bearer_id: int, bearer_type: str) -> Bearer:
        qos = EntityFactory.generate_qos()
        return Bearer(bearer_id, bearer_type, qos)

    @staticmethod
    def create_customer(msisdn: str, imei: str, imsi: str) -> Customer:
        return Customer(msisdn, imei, imsi)

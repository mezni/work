from value_objects import QoS
class Customer:
    def __init__(self, customer_type: str, msisdn: str, imsi: str, imei: str):
        """
        Initializes a Customer entity with customer_type, MSISDN, IMSI, and IMEI.

        Args:
            customer_type (str): Type of customer (e.g., "regular", "premium").
            msisdn (str): The MSISDN as a string.
            imsi (str): The IMSI as a string.
            imei (str): The IMEI as a string.
        """
        self.customer_type = customer_type
        self.msisdn = msisdn  
        self.imsi = imsi  
        self.imei = imei 

    def __str__(self):
        return f"Customer(customer_type={self.customer_type}, msisdn={self.msisdn}, imsi={self.imsi}, imei={self.imei})"

    def __eq__(self, other):
        if not isinstance(other, Customer):
            return False
        return self.msisdn == other.msisdn and self.imsi == other.imsi and self.imei == other.imei

    def __hash__(self):
        return hash((self.customer_type, self.msisdn, self.imsi, self.imei))


    def to_dict(self):
        return {
            "customer_type": self.customer_type,
            "msisdn": str(self.msisdn),  
            "imsi": str(self.imsi),      
            "imei": str(self.imei)      
        }


class Node:
    def __init__(self, network_type: str, rnc_id: str = None, lac: str = None, cell_id: str = None, tac: str = None, gNB_ID: str = None,
                 NR_Cell_ID: str = None, MSC_Address: str = None, SGSN_Address: str = None, GGSN_Address: str = None,
                 plmn: str = "", SGW_Address: str = None, PGW_Address: str = None, MME_Address: str = None):
        """
        Initializes a Node entity with relevant parameters based on network type.
        """
        self.network_type = network_type
        self.plmn = plmn
        self.rnc_id = rnc_id
        self.lac = lac
        self.cell_id = cell_id
        self.tac = tac
        self.gNB_ID = gNB_ID
        self.NR_Cell_ID = NR_Cell_ID
        self.MSC_Address = MSC_Address
        self.SGSN_Address = SGSN_Address
        self.GGSN_Address = GGSN_Address
        self.SGW_Address = SGW_Address
        self.PGW_Address = PGW_Address
        self.MME_Address = MME_Address

    def __str__(self):
        return f"Node(network_type={self.network_type}, rnc_id={self.rnc_id}, lac={self.lac}, cell_id={self.cell_id}, " \
               f"tac={self.tac}, gNB_ID={self.gNB_ID}, NR_Cell_ID={self.NR_Cell_ID}, MSC_Address={self.MSC_Address}, " \
               f"SGSN_Address={self.SGSN_Address}, GGSN_Address={self.GGSN_Address}, plmn={self.plmn}, " \
               f"SGW_Address={self.SGW_Address}, PGW_Address={self.PGW_Address}, MME_Address={self.MME_Address})"

    def to_dict(self):
        """
        Converts the Node object to a dictionary representation, omitting keys with None values.

        Returns:
            dict: A dictionary representing the Node object.
        """
        return {k: v for k, v in vars(self).items() if v not in [None, "", [], {}]}


class Bearer:
    def __init__(self, bearer_id: int, bearer_type: str, qos: QoS):
        if not self._validate(bearer_id, bearer_type, qos):
            raise ValueError(f"Invalid Bearer parameters: ID={bearer_id}, Type={bearer_type}, QoS={qos}")
        
        self.bearer_id = bearer_id
        self.bearer_type = bearer_type
        self.qos = qos

    def _validate(self, bearer_id: int, bearer_type: str, qos: QoS) -> bool:
        if not isinstance(bearer_id, int) or bearer_id <= 0:
            raise ValueError(f"Bearer ID must be a positive integer, got: {bearer_id}")
        if not isinstance(bearer_type, str) or not bearer_type:
            raise ValueError(f"Bearer Type must be a non-empty string, got: {bearer_type}")
        if not isinstance(qos, QoS):
            raise ValueError(f"QoS must be an instance of QoS class, got: {type(qos)}")
        return True

    def __repr__(self):
        return f"Bearer(ID={self.bearer_id}, Type={self.bearer_type}, QoS={self.qos})"

    def to_dict(self):
        return {
            "Bearer_ID": self.bearer_id,
            "Bearer_Type": self.bearer_type,
            "QoS": self.qos.to_dict()  # Ensure the QoS is converted to a dict
        }

    def apply_qos(self, qos: QoS):
        if not isinstance(qos, QoS):
            raise ValueError(f"Invalid QoS object: {qos}")
        self.qos = qos

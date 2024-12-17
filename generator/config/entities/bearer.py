from .qos import QoS

class Bearer:
    def __init__(self, bearer_id: int, bearer_type: str, qos: QoS):
        self.bearer_id = bearer_id
        self.bearer_type = bearer_type
        self.qos = qos

    def __repr__(self):
        return f"Bearer(ID={self.bearer_id}, Type={self.bearer_type}, QoS={self.qos})"

    def to_dict(self):
        return {
            "Bearer_ID": self.bearer_id,
            "Bearer_Type": self.bearer_type,
            "QoS": self.qos.to_dict()
        }

    def apply_qos(self, qos: QoS):
        self.qos = qos

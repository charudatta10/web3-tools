from datetime import datetime
import json


from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


class Transaction:
    def __init__(self, sender, recipient, amount, signature=None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = str(datetime.now())
        self.signature = signature

    def get_dict(self):
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'timestamp': self.timestamp,
            'signature': self.signature
        }

    @staticmethod
    def from_dict(data):
        return Transaction(
            sender=data['sender'],
            recipient=data['recipient'],
            amount=data['amount'],
            signature=data.get('signature')
        )

    def sign_transaction(self, private_key):
        message = json.dumps(self.get_dict(), sort_keys=True)
        self.signature = private_key.sign(
            message.encode("utf-8"),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        ).hex()

    def verify_transaction(self, sender_wallet, recipient_wallet):
        if not sender_wallet or not recipient_wallet:
            return False, "Sender or recipient wallet does not exist."
        if sender_wallet.balance < self.amount:
            return False, "Insufficient balance."
        if sender_wallet.address != self.sender:
            return False, "Invalid sender address."
        if not self.signature:
            return False, "Missing signature."
        message = json.dumps(self.get_dict(), sort_keys=True)
        try:
            signature = bytes.fromhex(self.signature)
            sender_wallet.public_key.verify(
                signature,
                message.encode("utf-8"),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True, "Transaction verified."
        except Exception as e:
            return False, f"Invalid signature: {str(e)}"

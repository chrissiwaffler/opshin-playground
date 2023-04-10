from blockfrost import ApiUrls
from pycardano import BlockFrostChainContext, Address, PaymentVerificationKey, PaymentSigningKey, plutus_script_hash, TransactionBuilder, PlutusV2Script, Network, TransactionOutput, datum_hash
from gift import CancelDatum
from config import blockfrost_project_id

# build a chain context
context = BlockFrostChainContext(blockfrost_project_id, base_url=ApiUrls.preview.value)

# create the script address
with open("build/gift/script.cbor", "r") as f:
    script_hex = f.read()
gift_script = PlutusV2Script(bytes.fromhex(script_hex))

script_hash = plutus_script_hash(gift_script)
network = Network.TESTNET
script_address = Address(script_hash, network=network)
print(f"created address for script: {script_address}")

# giver/locker sends funds to the script address
# attach the public key hash of a receiver address as datum to the utxo
# use the datatype defined in the contract, that also uses PlutusData
payment_vkey = PaymentVerificationKey.load("keys/key1/payment.vkey")
payment_skey = PaymentSigningKey.load("keys/key1/payment.skey")
giver_address = Address(payment_vkey.hash(), network=network)

payment_vkey_2 = PaymentVerificationKey.load("keys/key2/payment.vkey")
taker_address = Address(payment_vkey_2.hash(), network=network)

builder = TransactionBuilder(context)
builder.add_input_address(giver_address)

datum = CancelDatum(payment_vkey_2.hash().to_primitive())
builder.add_output(
    TransactionOutput(script_address, 50000000, datum_hash=datum_hash(datum))
)

# build, sign and submit the transaction
signed_tx = builder.build_and_sign([payment_skey], giver_address)
tx_hash = context.submit_tx(signed_tx.to_cbor())
print(f"submitted the transaction with tx_hash: {tx_hash}")
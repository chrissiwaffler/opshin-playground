from blockfrost import ApiUrls
from pycardano import BlockFrostChainContext, Address, PaymentVerificationKey, PaymentSigningKey, plutus_script_hash, TransactionBuilder, PlutusData, Redeemer, PlutusV2Script, Network, TransactionOutput
from gift import CancelDatum
from config import blockfrost_project_id

context = BlockFrostChainContext(blockfrost_project_id, base_url=ApiUrls.preview.value)
network = Network.TESTNET

with open("build/gift/script.cbor", "r") as f:
    script_hex = f.read()
gift_script = PlutusV2Script(bytes.fromhex(script_hex))
script_hash = plutus_script_hash(gift_script)

payment_vkey_2 = PaymentVerificationKey.load("keys/key2/payment.vkey")
payment_skey_2 = PaymentSigningKey.load("keys/key2/payment.skey")
taker_address = Address(payment_vkey_2.hash(), network=network)

# After running `deploy_gift.py`, 
# copy the script address and replace it with the existing one.
script_address = "addr_test1wqfcx5785es6k2hfpgsrfkpwzsln632uz3g7dhwumvcwphs58xm00"

# Taker/unlocker sends a transaction to consume 
# the funds locked in the gift smart contract.
# here we specify the redeemer tag as spend 
# and pass in no special redeemer, as it is being ignored by the contract.
redeemer = Redeemer(PlutusData()) # Plutus equivalent of none

utxo_to_spend = context.utxos(str(script_address))[0]

builder = TransactionBuilder(context)

# Add info on the UTxO to spend, Plutus script, actual datum and the redeemer.
# Specify the amount of funds to take.
datum = CancelDatum(payment_vkey_2.hash().to_primitive())
builder.add_script_input(utxo_to_spend, gift_script, datum, redeemer)

take_output = TransactionOutput(taker_address, 25123456)
builder.add_output(take_output)

# Taker/Unlocker provides collateral. 
# IN this scenario, the provided UTXO is consumed instead of fees
# A UTXO Provided for collateral must only have ada, no other native assets
non_nft_utxo = None
for utxo in context.utxos(str(taker_address)):
    # multi_asset should be empty for collateral utxo
    if not utxo.output.amount.multi_asset:
        non_nft_utxo = utxo
        break

builder.collaterals.append(non_nft_utxo)

# Don't forget to add the taker as a *required* signer, 
# so the contact knows that they will sign the transaction
builder.required_signers = [payment_vkey_2.hash()]
signed_tx = builder.build_and_sign([payment_skey_2], taker_address)

tx_hash = context.submit_tx(signed_tx.to_cbor())
print(f"submitted the transaction with tx_hash: {tx_hash}")
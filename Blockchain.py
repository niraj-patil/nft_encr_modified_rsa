from web3 import Web3
import os
from dotenv import load_dotenv

def mint_nft(address:str,uri:str):
    load_dotenv()

    w3=Web3(Web3.HTTPProvider("https://goerli.infura.io/v3/139b52a3df5343b2b4f134d8b673e9ad"))
    contact_address=os.getenv("CONTRACT_ADDRESS")
    contract_abi=os.getenv("CONTRACT_ABI")
    limited_access=w3.eth.contract(address=contact_address,abi=contract_abi)
    account_address=os.getenv('ACCOUNT')
    w3.eth.default_account=account_address
    private_key=os.getenv('ACCOUNT_PRIVATE_KEY')

    transaction = limited_access.functions.awardItem(address,uri).build_transaction()
    transaction.update({ 'gas' : 1000000 })
    transaction.update({ 'nonce' : w3.eth.get_transaction_count(account_address) })
    signed_tx = w3.eth.account.sign_transaction(transaction, private_key)
    txn_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)



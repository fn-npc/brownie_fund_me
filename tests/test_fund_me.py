from brownie import network, accounts, exceptions
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fund_me
import pytest


def test_can_fund_and_withdraw():
    # Arrange
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100

    # Act1
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    # Assert1 - want to check if our account to amt funded is being recorded correctly
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee

    # Act2
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    # Assert2 - want to check if our mappings is being updated on withdrawal
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    # so the process is you do the function where you expect it to break, read the error, and make sense of it
    # if it's what you expect, then that's good enough, but you could always raise an exception to handle it if you want
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})

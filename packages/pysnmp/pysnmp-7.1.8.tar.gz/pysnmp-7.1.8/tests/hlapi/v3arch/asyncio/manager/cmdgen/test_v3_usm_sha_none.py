import pytest
from pysnmp.hlapi.v3arch.asyncio import *
from pysnmp.proto.errind import UnknownUserName, WrongDigest
from tests.agent_context import AGENT_PORT, AgentContextManager


@pytest.mark.asyncio
async def test_usm_sha_none():
    async with AgentContextManager():
        snmpEngine = SnmpEngine()
        authData = UsmUserData(
            "usr-sha-none",
            "authkey1",
            authProtocol=USM_AUTH_HMAC96_SHA,
        )
        errorIndication, errorStatus, errorIndex, varBinds = await get_cmd(
            snmpEngine,
            authData,
            await UdpTransportTarget.create(("localhost", AGENT_PORT), retries=0),
            ContextData(),
            ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
        )

        assert errorIndication is None
        assert errorStatus == 0
        assert len(varBinds) == 1
        assert varBinds[0][0].prettyPrint() == "SNMPv2-MIB::sysDescr.0"
        isinstance(varBinds[0][1], OctetString)

        snmpEngine.close_dispatcher()


@pytest.mark.asyncio
async def test_usm_sha_none_wrong_auth():
    async with AgentContextManager():
        snmpEngine = SnmpEngine()
        authData = UsmUserData(
            "usr-sha-none",
            "authkey1",
            authProtocol=USM_AUTH_HMAC96_MD5,  # wrongly use usmHMACMD5AuthProtocol
        )
        errorIndication, errorStatus, errorIndex, varBinds = await get_cmd(
            snmpEngine,
            authData,
            await UdpTransportTarget.create(("localhost", AGENT_PORT), retries=0),
            ContextData(),
            ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
        )

        assert isinstance(errorIndication, WrongDigest)
        assert str(errorIndication) == "Wrong SNMP PDU digest"

        snmpEngine.close_dispatcher()


@pytest.mark.asyncio
async def test_usm_sha_none_wrong_user():
    async with AgentContextManager():
        snmpEngine = SnmpEngine()
        authData = UsmUserData(
            "usr-sha-none-not-exist",
            "authkey1",
            authProtocol=USM_AUTH_HMAC96_SHA,
        )
        errorIndication, errorStatus, errorIndex, varBinds = await get_cmd(
            snmpEngine,
            authData,
            await UdpTransportTarget.create(("localhost", AGENT_PORT), retries=0),
            ContextData(),
            ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
        )

        assert isinstance(errorIndication, UnknownUserName)
        assert str(errorIndication) == "Unknown USM user"

        snmpEngine.close_dispatcher()

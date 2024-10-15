#
# This file is part of pysnmp software.
#
# Copyright (c) 2005-2020, Ilya Etingof <etingof@gmail.com>
# License: https://www.pysnmp.com/pysnmp/license.html
#
# PySNMP MIB module SNMP-USER-BASED-SM-MIB (https://www.pysnmp.com/pysnmp)
# ASN.1 source http://mibs.pysnmp.com:80/asn1/SNMP-USER-BASED-SM-MIB
# Produced by pysmi-0.1.3 at Tue Apr 18 00:48:12 2017
# On host grommit.local platform Darwin version 16.4.0 by user ilya
# Using Python version 3.4.2 (v3.4.2:ab2c023a9432, Oct  5 2014, 20:42:22)
#
OctetString, Integer, ObjectIdentifier = mibBuilder.import_symbols(
    "ASN1", "OctetString", "Integer", "ObjectIdentifier"
)
(NamedValues,) = mibBuilder.import_symbols("ASN1-ENUMERATION", "NamedValues")
(
    ValueRangeConstraint,
    SingleValueConstraint,
    ValueSizeConstraint,
    ConstraintsIntersection,
    ConstraintsUnion,
) = mibBuilder.import_symbols(
    "ASN1-REFINEMENT",
    "ValueRangeConstraint",
    "SingleValueConstraint",
    "ValueSizeConstraint",
    "ConstraintsIntersection",
    "ConstraintsUnion",
)
(
    SnmpAdminString,
    snmpAuthProtocols,
    snmpPrivProtocols,
    SnmpEngineID,
) = mibBuilder.import_symbols(
    "SNMP-FRAMEWORK-MIB",
    "SnmpAdminString",
    "snmpAuthProtocols",
    "snmpPrivProtocols",
    "SnmpEngineID",
)
ObjectGroup, ModuleCompliance, NotificationGroup = mibBuilder.import_symbols(
    "SNMPv2-CONF", "ObjectGroup", "ModuleCompliance", "NotificationGroup"
)
(
    MibScalar,
    MibTable,
    MibTableRow,
    MibTableColumn,
    Counter64,
    Gauge32,
    iso,
    Counter32,
    NotificationType,
    Bits,
    Unsigned32,
    MibIdentifier,
    Integer32,
    TimeTicks,
    IpAddress,
    ModuleIdentity,
    snmpModules,
    ObjectIdentity,
) = mibBuilder.import_symbols(
    "SNMPv2-SMI",
    "MibScalar",
    "MibTable",
    "MibTableRow",
    "MibTableColumn",
    "Counter64",
    "Gauge32",
    "iso",
    "Counter32",
    "NotificationType",
    "Bits",
    "Unsigned32",
    "MibIdentifier",
    "Integer32",
    "TimeTicks",
    "IpAddress",
    "ModuleIdentity",
    "snmpModules",
    "ObjectIdentity",
)
(
    DisplayString,
    AutonomousType,
    RowStatus,
    StorageType,
    TextualConvention,
    RowPointer,
    TestAndIncr,
) = mibBuilder.import_symbols(
    "SNMPv2-TC",
    "DisplayString",
    "AutonomousType",
    "RowStatus",
    "StorageType",
    "TextualConvention",
    "RowPointer",
    "TestAndIncr",
)
snmpUsmMIB = ModuleIdentity((1, 3, 6, 1, 6, 3, 15))
if mibBuilder.loadTexts:
    snmpUsmMIB.setRevisions(
        (
            "2002-10-16 00:00",
            "1999-01-20 00:00",
            "1997-11-20 00:00",
        )
    )
if mibBuilder.loadTexts:
    snmpUsmMIB.setLastUpdated("200210160000Z")
if mibBuilder.loadTexts:
    snmpUsmMIB.setOrganization("SNMPv3 Working Group")
if mibBuilder.loadTexts:
    snmpUsmMIB.setContactInfo(
        "WG-email: snmpv3@lists.tislabs.com Subscribe: majordomo@lists.tislabs.com In msg body: subscribe snmpv3 Chair: Russ Mundy Network Associates Laboratories postal: 15204 Omega Drive, Suite 300 Rockville, MD 20850-4601 USA email: mundy@tislabs.com phone: +1 301-947-7107 Co-Chair: David Harrington Enterasys Networks Postal: 35 Industrial Way P. O. Box 5004 Rochester, New Hampshire 03866-5005 USA EMail: dbh@enterasys.com Phone: +1 603-337-2614 Co-editor Uri Blumenthal Lucent Technologies postal: 67 Whippany Rd. Whippany, NJ 07981 USA email: uri@lucent.com phone: +1-973-386-2163 Co-editor: Bert Wijnen Lucent Technologies postal: Schagen 33 3461 GL Linschoten Netherlands email: bwijnen@lucent.com phone: +31-348-480-685 "
    )
if mibBuilder.loadTexts:
    snmpUsmMIB.setDescription(
        "The management information definitions for the SNMP User-based Security Model. Copyright (C) The Internet Society (2002). This version of this MIB module is part of RFC 3414; see the RFC itself for full legal notices. "
    )
usmMIBObjects = MibIdentifier((1, 3, 6, 1, 6, 3, 15, 1))
usmMIBConformance = MibIdentifier((1, 3, 6, 1, 6, 3, 15, 2))
usmNoAuthProtocol = ObjectIdentity((1, 3, 6, 1, 6, 3, 10, 1, 1, 1))
if mibBuilder.loadTexts:
    usmNoAuthProtocol.setStatus("current")
if mibBuilder.loadTexts:
    usmNoAuthProtocol.setDescription("No Authentication Protocol.")
usmHMACMD5AuthProtocol = ObjectIdentity((1, 3, 6, 1, 6, 3, 10, 1, 1, 2))
if mibBuilder.loadTexts:
    usmHMACMD5AuthProtocol.setStatus("current")
if mibBuilder.loadTexts:
    usmHMACMD5AuthProtocol.setDescription(
        "The HMAC-MD5-96 Digest Authentication Protocol."
    )
if mibBuilder.loadTexts:
    usmHMACMD5AuthProtocol.setReference(
        "- H. Krawczyk, M. Bellare, R. Canetti HMAC: Keyed-Hashing for Message Authentication, RFC2104, Feb 1997. - Rivest, R., Message Digest Algorithm MD5, RFC1321. "
    )
usmHMACSHAAuthProtocol = ObjectIdentity((1, 3, 6, 1, 6, 3, 10, 1, 1, 3))
if mibBuilder.loadTexts:
    usmHMACSHAAuthProtocol.setStatus("current")
if mibBuilder.loadTexts:
    usmHMACSHAAuthProtocol.setDescription(
        "The HMAC-SHA-96 Digest Authentication Protocol."
    )
if mibBuilder.loadTexts:
    usmHMACSHAAuthProtocol.setReference(
        "- H. Krawczyk, M. Bellare, R. Canetti, HMAC: Keyed-Hashing for Message Authentication, RFC2104, Feb 1997. - Secure Hash Algorithm. NIST FIPS 180-1. "
    )
usmNoPrivProtocol = ObjectIdentity((1, 3, 6, 1, 6, 3, 10, 1, 2, 1))
if mibBuilder.loadTexts:
    usmNoPrivProtocol.setStatus("current")
if mibBuilder.loadTexts:
    usmNoPrivProtocol.setDescription("No Privacy Protocol.")
usmDESPrivProtocol = ObjectIdentity((1, 3, 6, 1, 6, 3, 10, 1, 2, 2))
if mibBuilder.loadTexts:
    usmDESPrivProtocol.setStatus("current")
if mibBuilder.loadTexts:
    usmDESPrivProtocol.setDescription("The CBC-DES Symmetric Encryption Protocol.")
if mibBuilder.loadTexts:
    usmDESPrivProtocol.setReference(
        "- Data Encryption Standard, National Institute of Standards and Technology. Federal Information Processing Standard (FIPS) Publication 46-1. Supersedes FIPS Publication 46, (January, 1977; reaffirmed January, 1988). - Data Encryption Algorithm, American National Standards Institute. ANSI X3.92-1981, (December, 1980). - DES Modes of Operation, National Institute of Standards and Technology. Federal Information Processing Standard (FIPS) Publication 81, (December, 1980). - Data Encryption Algorithm - Modes of Operation, American National Standards Institute. ANSI X3.106-1983, (May 1983). "
    )


class KeyChange(TextualConvention, OctetString):
    description = "Every definition of an object with this syntax must identify a protocol P, a secret key K, and a hash algorithm H that produces output of L octets. The object's value is a manager-generated, partially-random value which, when modified, causes the value of the secret key K, to be modified via a one-way function. The value of an instance of this object is the concatenation of two components: first a 'random' component and then a 'delta' component. The lengths of the random and delta components are given by the corresponding value of the protocol P; if P requires K to be a fixed length, the length of both the random and delta components is that fixed length; if P allows the length of K to be variable up to a particular maximum length, the length of the random component is that maximum length and the length of the delta component is any length less than or equal to that maximum length. For example, usmHMACMD5AuthProtocol requires K to be a fixed length of 16 octets and L - of 16 octets. usmHMACSHAAuthProtocol requires K to be a fixed length of 20 octets and L - of 20 octets. Other protocols may define other sizes, as deemed appropriate. When a requester wants to change the old key K to a new key keyNew on a remote entity, the 'random' component is obtained from either a true random generator, or from a pseudorandom generator, and the 'delta' component is computed as follows: - a temporary variable is initialized to the existing value of K; - if the length of the keyNew is greater than L octets, then: - the random component is appended to the value of the temporary variable, and the result is input to the the hash algorithm H to produce a digest value, and the temporary variable is set to this digest value; - the value of the temporary variable is XOR-ed with the first (next) L-octets (16 octets in case of MD5) of the keyNew to produce the first (next) L-octets (16 octets in case of MD5) of the 'delta' component. - the above two steps are repeated until the unused portion of the keyNew component is L octets or less, - the random component is appended to the value of the temporary variable, and the result is input to the hash algorithm H to produce a digest value; - this digest value, truncated if necessary to be the same length as the unused portion of the keyNew, is XOR-ed with the unused portion of the keyNew to produce the (final portion of the) 'delta' component. For example, using MD5 as the hash algorithm H: iterations = (lenOfDelta - 1)/16; /* integer division */ temp = keyOld; for (i = 0; i < iterations; i++) { temp = MD5 (temp || random); delta[i*16 .. (i*16)+15] = temp XOR keyNew[i*16 .. (i*16)+15]; } temp = MD5 (temp || random); delta[i*16 .. lenOfDelta-1] = temp XOR keyNew[i*16 .. lenOfDelta-1]; The 'random' and 'delta' components are then concatenated as described above, and the resulting octet string is sent to the recipient as the new value of an instance of this object. At the receiver side, when an instance of this object is set to a new value, then a new value of K is computed as follows: - a temporary variable is initialized to the existing value of K; - if the length of the delta component is greater than L octets, then: - the random component is appended to the value of the temporary variable, and the result is input to the hash algorithm H to produce a digest value, and the temporary variable is set to this digest value; - the value of the temporary variable is XOR-ed with the first (next) L-octets (16 octets in case of MD5) of the delta component to produce the first (next) L-octets (16 octets in case of MD5) of the new value of K. - the above two steps are repeated until the unused portion of the delta component is L octets or less, - the random component is appended to the value of the temporary variable, and the result is input to the hash algorithm H to produce a digest value; - this digest value, truncated if necessary to be the same length as the unused portion of the delta component, is XOR-ed with the unused portion of the delta component to produce the (final portion of the) new value of K. For example, using MD5 as the hash algorithm H: iterations = (lenOfDelta - 1)/16; /* integer division */ temp = keyOld; for (i = 0; i < iterations; i++) { temp = MD5 (temp || random); keyNew[i*16 .. (i*16)+15] = temp XOR delta[i*16 .. (i*16)+15]; } temp = MD5 (temp || random); keyNew[i*16 .. lenOfDelta-1] = temp XOR delta[i*16 .. lenOfDelta-1]; The value of an object with this syntax, whenever it is retrieved by the management protocol, is always the zero length string. Note that the keyOld and keyNew are the localized keys. Note that it is probably wise that when an SNMP entity sends a SetRequest to change a key, that it keeps a copy of the old key until it has confirmed that the key change actually succeeded. "
    status = "current"


usmStats = MibIdentifier((1, 3, 6, 1, 6, 3, 15, 1, 1))
usmStatsUnsupportedSecLevels = MibScalar(
    (1, 3, 6, 1, 6, 3, 15, 1, 1, 1), Counter32()
).setMaxAccess("read-only")
if mibBuilder.loadTexts:
    usmStatsUnsupportedSecLevels.setStatus("current")
if mibBuilder.loadTexts:
    usmStatsUnsupportedSecLevels.setDescription(
        "The total number of packets received by the SNMP engine which were dropped because they requested a securityLevel that was unknown to the SNMP engine or otherwise unavailable. "
    )
usmStatsNotInTimeWindows = MibScalar(
    (1, 3, 6, 1, 6, 3, 15, 1, 1, 2), Counter32()
).setMaxAccess("read-only")
if mibBuilder.loadTexts:
    usmStatsNotInTimeWindows.setStatus("current")
if mibBuilder.loadTexts:
    usmStatsNotInTimeWindows.setDescription(
        "The total number of packets received by the SNMP engine which were dropped because they appeared outside of the authoritative SNMP engine's window. "
    )
usmStatsUnknownUserNames = MibScalar(
    (1, 3, 6, 1, 6, 3, 15, 1, 1, 3), Counter32()
).setMaxAccess("read-only")
if mibBuilder.loadTexts:
    usmStatsUnknownUserNames.setStatus("current")
if mibBuilder.loadTexts:
    usmStatsUnknownUserNames.setDescription(
        "The total number of packets received by the SNMP engine which were dropped because they referenced a user that was not known to the SNMP engine. "
    )
usmStatsUnknownEngineIDs = MibScalar(
    (1, 3, 6, 1, 6, 3, 15, 1, 1, 4), Counter32()
).setMaxAccess("read-only")
if mibBuilder.loadTexts:
    usmStatsUnknownEngineIDs.setStatus("current")
if mibBuilder.loadTexts:
    usmStatsUnknownEngineIDs.setDescription(
        "The total number of packets received by the SNMP engine which were dropped because they referenced an snmpEngineID that was not known to the SNMP engine. "
    )
usmStatsWrongDigests = MibScalar(
    (1, 3, 6, 1, 6, 3, 15, 1, 1, 5), Counter32()
).setMaxAccess("read-only")
if mibBuilder.loadTexts:
    usmStatsWrongDigests.setStatus("current")
if mibBuilder.loadTexts:
    usmStatsWrongDigests.setDescription(
        "The total number of packets received by the SNMP engine which were dropped because they didn't contain the expected digest value. "
    )
usmStatsDecryptionErrors = MibScalar(
    (1, 3, 6, 1, 6, 3, 15, 1, 1, 6), Counter32()
).setMaxAccess("read-only")
if mibBuilder.loadTexts:
    usmStatsDecryptionErrors.setStatus("current")
if mibBuilder.loadTexts:
    usmStatsDecryptionErrors.setDescription(
        "The total number of packets received by the SNMP engine which were dropped because they could not be decrypted. "
    )
usmUser = MibIdentifier((1, 3, 6, 1, 6, 3, 15, 1, 2))
usmUserSpinLock = MibScalar(
    (1, 3, 6, 1, 6, 3, 15, 1, 2, 1), TestAndIncr()
).setMaxAccess("read-write")
if mibBuilder.loadTexts:
    usmUserSpinLock.setStatus("current")
if mibBuilder.loadTexts:
    usmUserSpinLock.setDescription(
        "An advisory lock used to allow several cooperating Command Generator Applications to coordinate their use of facilities to alter secrets in the usmUserTable. "
    )
usmUserTable = MibTable(
    (1, 3, 6, 1, 6, 3, 15, 1, 2, 2),
)
if mibBuilder.loadTexts:
    usmUserTable.setStatus("current")
if mibBuilder.loadTexts:
    usmUserTable.setDescription(
        "The table of users configured in the SNMP engine's Local Configuration Datastore (LCD). To create a new user (i.e., to instantiate a new conceptual row in this table), it is recommended to follow this procedure: 1) GET(usmUserSpinLock.0) and save in sValue. 2) SET(usmUserSpinLock.0=sValue, usmUserCloneFrom=templateUser, usmUserStatus=createAndWait) You should use a template user to clone from which has the proper auth/priv protocol defined. If the new user is to use privacy: 3) generate the keyChange value based on the secret privKey of the clone-from user and the secret key to be used for the new user. Let us call this pkcValue. 4) GET(usmUserSpinLock.0) and save in sValue. 5) SET(usmUserSpinLock.0=sValue, usmUserPrivKeyChange=pkcValue usmUserPublic=randomValue1) 6) GET(usmUserPulic) and check it has randomValue1. If not, repeat steps 4-6. If the new user will never use privacy: 7) SET(usmUserPrivProtocol=usmNoPrivProtocol) If the new user is to use authentication: 8) generate the keyChange value based on the secret authKey of the clone-from user and the secret key to be used for the new user. Let us call this akcValue. 9) GET(usmUserSpinLock.0) and save in sValue. 10) SET(usmUserSpinLock.0=sValue, usmUserAuthKeyChange=akcValue usmUserPublic=randomValue2) 11) GET(usmUserPulic) and check it has randomValue2. If not, repeat steps 9-11. If the new user will never use authentication: 12) SET(usmUserAuthProtocol=usmNoAuthProtocol) Finally, activate the new user: 13) SET(usmUserStatus=active) The new user should now be available and ready to be used for SNMPv3 communication. Note however that access to MIB data must be provided via configuration of the SNMP-VIEW-BASED-ACM-MIB. The use of usmUserSpinlock is to avoid conflicts with another SNMP command generator application which may also be acting on the usmUserTable. "
    )
usmUserEntry = MibTableRow(
    (1, 3, 6, 1, 6, 3, 15, 1, 2, 2, 1),
).setIndexNames(
    (0, "SNMP-USER-BASED-SM-MIB", "usmUserEngineID"),
    (0, "SNMP-USER-BASED-SM-MIB", "usmUserName"),
)
if mibBuilder.loadTexts:
    usmUserEntry.setStatus("current")
if mibBuilder.loadTexts:
    usmUserEntry.setDescription(
        "A user configured in the SNMP engine's Local Configuration Datastore (LCD) for the User-based Security Model. "
    )
usmUserEngineID = MibTableColumn((1, 3, 6, 1, 6, 3, 15, 1, 2, 2, 1, 1), SnmpEngineID())
if mibBuilder.loadTexts:
    usmUserEngineID.setStatus("current")
if mibBuilder.loadTexts:
    usmUserEngineID.setDescription(
        "An SNMP engine's administratively-unique identifier. In a simple agent, this value is always that agent's own snmpEngineID value. The value can also take the value of the snmpEngineID of a remote SNMP engine with which this user can communicate. "
    )
usmUserName = MibTableColumn(
    (1, 3, 6, 1, 6, 3, 15, 1, 2, 2, 1, 2),
    SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(1, 32)),
)
if mibBuilder.loadTexts:
    usmUserName.setStatus("current")
if mibBuilder.loadTexts:
    usmUserName.setDescription(
        "A human readable string representing the name of the user. This is the (User-based Security) Model dependent security ID. "
    )
usmUserSecurityName = MibTableColumn(
    (1, 3, 6, 1, 6, 3, 15, 1, 2, 2, 1, 3), SnmpAdminString()
).setMaxAccess("read-only")
if mibBuilder.loadTexts:
    usmUserSecurityName.setStatus("current")
if mibBuilder.loadTexts:
    usmUserSecurityName.setDescription(
        "A human readable string representing the user in Security Model independent format. The default transformation of the User-based Security Model dependent security ID to the securityName and vice versa is the identity function so that the securityName is the same as the userName. "
    )
usmUserCloneFrom = MibTableColumn(
    (1, 3, 6, 1, 6, 3, 15, 1, 2, 2, 1, 4), RowPointer()
).setMaxAccess("read-create")
if mibBuilder.loadTexts:
    usmUserCloneFrom.setStatus("current")
if mibBuilder.loadTexts:
    usmUserCloneFrom.setDescription(
        "A pointer to another conceptual row in this usmUserTable. The user in this other conceptual row is called the clone-from user. When a new user is created (i.e., a new conceptual row is instantiated in this table), the privacy and authentication parameters of the new user must be cloned from its clone-from user. These parameters are: - authentication protocol (usmUserAuthProtocol) - privacy protocol (usmUserPrivProtocol) They will be copied regardless of what the current value is. Cloning also causes the initial values of the secret authentication key (authKey) and the secret encryption key (privKey) of the new user to be set to the same values as the corresponding secrets of the clone-from user to allow the KeyChange process to occur as required during user creation. The first time an instance of this object is set by a management operation (either at or after its instantiation), the cloning process is invoked. Subsequent writes are successful but invoke no action to be taken by the receiver. The cloning process fails with an 'inconsistentName' error if the conceptual row representing the clone-from user does not exist or is not in an active state when the cloning process is invoked. When this object is read, the ZeroDotZero OID is returned. "
    )
usmUserAuthProtocol = MibTableColumn(
    (1, 3, 6, 1, 6, 3, 15, 1, 2, 2, 1, 5),
    AutonomousType().clone((1, 3, 6, 1, 6, 3, 10, 1, 1, 1)),
).setMaxAccess("read-create")
if mibBuilder.loadTexts:
    usmUserAuthProtocol.setStatus("current")
if mibBuilder.loadTexts:
    usmUserAuthProtocol.setDescription(
        "An indication of whether messages sent on behalf of this user to/from the SNMP engine identified by usmUserEngineID, can be authenticated, and if so, the type of authentication protocol which is used. An instance of this object is created concurrently with the creation of any other object instance for the same user (i.e., as part of the processing of the set operation which creates the first object instance in the same conceptual row). If an initial set operation (i.e. at row creation time) tries to set a value for an unknown or unsupported protocol, then a 'wrongValue' error must be returned. The value will be overwritten/set when a set operation is performed on the corresponding instance of usmUserCloneFrom. Once instantiated, the value of such an instance of this object can only be changed via a set operation to the value of the usmNoAuthProtocol. If a set operation tries to change the value of an existing instance of this object to any value other than usmNoAuthProtocol, then an 'inconsistentValue' error must be returned. If a set operation tries to set the value to the usmNoAuthProtocol while the usmUserPrivProtocol value in the same row is not equal to usmNoPrivProtocol, then an 'inconsistentValue' error must be returned. That means that an SNMP command generator application must first ensure that the usmUserPrivProtocol is set to the usmNoPrivProtocol value before it can set the usmUserAuthProtocol value to usmNoAuthProtocol. "
    )
usmUserAuthKeyChange = MibTableColumn(
    (1, 3, 6, 1, 6, 3, 15, 1, 2, 2, 1, 6), KeyChange().clone(hexValue="")
).setMaxAccess("read-create")
if mibBuilder.loadTexts:
    usmUserAuthKeyChange.setStatus("current")
if mibBuilder.loadTexts:
    usmUserAuthKeyChange.setDescription(
        "An object, which when modified, causes the secret authentication key used for messages sent on behalf of this user to/from the SNMP engine identified by usmUserEngineID, to be modified via a one-way function. The associated protocol is the usmUserAuthProtocol. The associated secret key is the user's secret authentication key (authKey). The associated hash algorithm is the algorithm used by the user's usmUserAuthProtocol. When creating a new user, it is an 'inconsistentName' error for a set operation to refer to this object unless it is previously or concurrently initialized through a set operation on the corresponding instance of usmUserCloneFrom. When the value of the corresponding usmUserAuthProtocol is usmNoAuthProtocol, then a set is successful, but effectively is a no-op. When this object is read, the zero-length (empty) string is returned. The recommended way to do a key change is as follows: 1) GET(usmUserSpinLock.0) and save in sValue. 2) generate the keyChange value based on the old (existing) secret key and the new secret key, let us call this kcValue. If you do the key change on behalf of another user: 3) SET(usmUserSpinLock.0=sValue, usmUserAuthKeyChange=kcValue usmUserPublic=randomValue) If you do the key change for yourself: 4) SET(usmUserSpinLock.0=sValue, usmUserOwnAuthKeyChange=kcValue usmUserPublic=randomValue) If you get a response with error-status of noError, then the SET succeeded and the new key is active. If you do not get a response, then you can issue a GET(usmUserPublic) and check if the value is equal to the randomValue you did send in the SET. If so, then the key change succeeded and the new key is active (probably the response got lost). If not, then the SET request probably never reached the target and so you can start over with the procedure above. "
    )
usmUserOwnAuthKeyChange = MibTableColumn(
    (1, 3, 6, 1, 6, 3, 15, 1, 2, 2, 1, 7), KeyChange().clone(hexValue="")
).setMaxAccess("read-create")
if mibBuilder.loadTexts:
    usmUserOwnAuthKeyChange.setStatus("current")
if mibBuilder.loadTexts:
    usmUserOwnAuthKeyChange.setDescription(
        "Behaves exactly as usmUserAuthKeyChange, with one notable difference: in order for the set operation to succeed, the usmUserName of the operation requester must match the usmUserName that indexes the row which is targeted by this operation. In addition, the USM security model must be used for this operation. The idea here is that access to this column can be public, since it will only allow a user to change his own secret authentication key (authKey). Note that this can only be done once the row is active. When a set is received and the usmUserName of the requester is not the same as the umsUserName that indexes the row which is targeted by this operation, then a 'noAccess' error must be returned. When a set is received and the security model in use is not USM, then a 'noAccess' error must be returned. "
    )
usmUserPrivProtocol = MibTableColumn(
    (1, 3, 6, 1, 6, 3, 15, 1, 2, 2, 1, 8),
    AutonomousType().clone((1, 3, 6, 1, 6, 3, 10, 1, 2, 1)),
).setMaxAccess("read-create")
if mibBuilder.loadTexts:
    usmUserPrivProtocol.setStatus("current")
if mibBuilder.loadTexts:
    usmUserPrivProtocol.setDescription(
        "An indication of whether messages sent on behalf of this user to/from the SNMP engine identified by usmUserEngineID, can be protected from disclosure, and if so, the type of privacy protocol which is used. An instance of this object is created concurrently with the creation of any other object instance for the same user (i.e., as part of the processing of the set operation which creates the first object instance in the same conceptual row). If an initial set operation (i.e. at row creation time) tries to set a value for an unknown or unsupported protocol, then a 'wrongValue' error must be returned. The value will be overwritten/set when a set operation is performed on the corresponding instance of usmUserCloneFrom. Once instantiated, the value of such an instance of this object can only be changed via a set operation to the value of the usmNoPrivProtocol. If a set operation tries to change the value of an existing instance of this object to any value other than usmNoPrivProtocol, then an 'inconsistentValue' error must be returned. Note that if any privacy protocol is used, then you must also use an authentication protocol. In other words, if usmUserPrivProtocol is set to anything else than usmNoPrivProtocol, then the corresponding instance of usmUserAuthProtocol cannot have a value of usmNoAuthProtocol. If it does, then an 'inconsistentValue' error must be returned. "
    )
usmUserPrivKeyChange = MibTableColumn(
    (1, 3, 6, 1, 6, 3, 15, 1, 2, 2, 1, 9), KeyChange().clone(hexValue="")
).setMaxAccess("read-create")
if mibBuilder.loadTexts:
    usmUserPrivKeyChange.setStatus("current")
if mibBuilder.loadTexts:
    usmUserPrivKeyChange.setDescription(
        "An object, which when modified, causes the secret encryption key used for messages sent on behalf of this user to/from the SNMP engine identified by usmUserEngineID, to be modified via a one-way function. The associated protocol is the usmUserPrivProtocol. The associated secret key is the user's secret privacy key (privKey). The associated hash algorithm is the algorithm used by the user's usmUserAuthProtocol. When creating a new user, it is an 'inconsistentName' error for a set operation to refer to this object unless it is previously or concurrently initialized through a set operation on the corresponding instance of usmUserCloneFrom. When the value of the corresponding usmUserPrivProtocol is usmNoPrivProtocol, then a set is successful, but effectively is a no-op. When this object is read, the zero-length (empty) string is returned. See the description clause of usmUserAuthKeyChange for a recommended procedure to do a key change. "
    )
usmUserOwnPrivKeyChange = MibTableColumn(
    (1, 3, 6, 1, 6, 3, 15, 1, 2, 2, 1, 10), KeyChange().clone(hexValue="")
).setMaxAccess("read-create")
if mibBuilder.loadTexts:
    usmUserOwnPrivKeyChange.setStatus("current")
if mibBuilder.loadTexts:
    usmUserOwnPrivKeyChange.setDescription(
        "Behaves exactly as usmUserPrivKeyChange, with one notable difference: in order for the Set operation to succeed, the usmUserName of the operation requester must match the usmUserName that indexes the row which is targeted by this operation. In addition, the USM security model must be used for this operation. The idea here is that access to this column can be public, since it will only allow a user to change his own secret privacy key (privKey). Note that this can only be done once the row is active. When a set is received and the usmUserName of the requester is not the same as the umsUserName that indexes the row which is targeted by this operation, then a 'noAccess' error must be returned. When a set is received and the security model in use is not USM, then a 'noAccess' error must be returned. "
    )
usmUserPublic = MibTableColumn(
    (1, 3, 6, 1, 6, 3, 15, 1, 2, 2, 1, 11),
    OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 32)).clone(hexValue=""),
).setMaxAccess("read-create")
if mibBuilder.loadTexts:
    usmUserPublic.setStatus("current")
if mibBuilder.loadTexts:
    usmUserPublic.setDescription(
        "A publicly-readable value which can be written as part of the procedure for changing a user's secret authentication and/or privacy key, and later read to determine whether the change of the secret was effected. "
    )
usmUserStorageType = MibTableColumn(
    (1, 3, 6, 1, 6, 3, 15, 1, 2, 2, 1, 12), StorageType().clone("nonVolatile")
).setMaxAccess("read-create")
if mibBuilder.loadTexts:
    usmUserStorageType.setStatus("current")
if mibBuilder.loadTexts:
    usmUserStorageType.setDescription(
        "The storage type for this conceptual row. Conceptual rows having the value 'permanent' must allow write-access at a minimum to: - usmUserAuthKeyChange, usmUserOwnAuthKeyChange and usmUserPublic for a user who employs authentication, and - usmUserPrivKeyChange, usmUserOwnPrivKeyChange and usmUserPublic for a user who employs privacy. Note that any user who employs authentication or privacy must allow its secret(s) to be updated and thus cannot be 'readOnly'. If an initial set operation tries to set the value to 'readOnly' for a user who employs authentication or privacy, then an 'inconsistentValue' error must be returned. Note that if the value has been previously set (implicit or explicit) to any value, then the rules as defined in the StorageType Textual Convention apply. It is an implementation issue to decide if a SET for a readOnly or permanent row is accepted at all. In some contexts this may make sense, in others it may not. If a SET for a readOnly or permanent row is not accepted at all, then a 'wrongValue' error must be returned. "
    )
usmUserStatus = MibTableColumn(
    (1, 3, 6, 1, 6, 3, 15, 1, 2, 2, 1, 13), RowStatus()
).setMaxAccess("read-create")
if mibBuilder.loadTexts:
    usmUserStatus.setStatus("current")
if mibBuilder.loadTexts:
    usmUserStatus.setDescription(
        "The status of this conceptual row. Until instances of all corresponding columns are appropriately configured, the value of the corresponding instance of the usmUserStatus column is 'notReady'. In particular, a newly created row for a user who employs authentication, cannot be made active until the corresponding usmUserCloneFrom and usmUserAuthKeyChange have been set. Further, a newly created row for a user who also employs privacy, cannot be made active until the usmUserPrivKeyChange has been set. The RowStatus TC [RFC2579] requires that this DESCRIPTION clause states under which circumstances other objects in this row can be modified: The value of this object has no effect on whether other objects in this conceptual row can be modified, except for usmUserOwnAuthKeyChange and usmUserOwnPrivKeyChange. For these 2 objects, the value of usmUserStatus MUST be active. "
    )
usmMIBCompliances = MibIdentifier((1, 3, 6, 1, 6, 3, 15, 2, 1))
usmMIBGroups = MibIdentifier((1, 3, 6, 1, 6, 3, 15, 2, 2))
usmMIBCompliance = ModuleCompliance((1, 3, 6, 1, 6, 3, 15, 2, 1, 1)).setObjects(
    ("SNMP-USER-BASED-SM-MIB", "usmMIBBasicGroup")
)
if mibBuilder.loadTexts:
    usmMIBCompliance.setDescription(
        "The compliance statement for SNMP engines which implement the SNMP-USER-BASED-SM-MIB. "
    )
usmMIBBasicGroup = ObjectGroup((1, 3, 6, 1, 6, 3, 15, 2, 2, 1)).setObjects(
    ("SNMP-USER-BASED-SM-MIB", "usmStatsUnsupportedSecLevels"),
    ("SNMP-USER-BASED-SM-MIB", "usmStatsNotInTimeWindows"),
    ("SNMP-USER-BASED-SM-MIB", "usmStatsUnknownUserNames"),
    ("SNMP-USER-BASED-SM-MIB", "usmStatsUnknownEngineIDs"),
    ("SNMP-USER-BASED-SM-MIB", "usmStatsWrongDigests"),
    ("SNMP-USER-BASED-SM-MIB", "usmStatsDecryptionErrors"),
    ("SNMP-USER-BASED-SM-MIB", "usmUserSpinLock"),
    ("SNMP-USER-BASED-SM-MIB", "usmUserSecurityName"),
    ("SNMP-USER-BASED-SM-MIB", "usmUserCloneFrom"),
    ("SNMP-USER-BASED-SM-MIB", "usmUserAuthProtocol"),
    ("SNMP-USER-BASED-SM-MIB", "usmUserAuthKeyChange"),
    ("SNMP-USER-BASED-SM-MIB", "usmUserOwnAuthKeyChange"),
    ("SNMP-USER-BASED-SM-MIB", "usmUserPrivProtocol"),
    ("SNMP-USER-BASED-SM-MIB", "usmUserPrivKeyChange"),
    ("SNMP-USER-BASED-SM-MIB", "usmUserOwnPrivKeyChange"),
    ("SNMP-USER-BASED-SM-MIB", "usmUserPublic"),
    ("SNMP-USER-BASED-SM-MIB", "usmUserStorageType"),
    ("SNMP-USER-BASED-SM-MIB", "usmUserStatus"),
)
if mibBuilder.loadTexts:
    usmMIBBasicGroup.setDescription(
        "A collection of objects providing for configuration of an SNMP engine which implements the SNMP User-based Security Model. "
    )
mibBuilder.export_symbols(
    "SNMP-USER-BASED-SM-MIB",
    usmUserStorageType=usmUserStorageType,
    PYSNMP_MODULE_ID=snmpUsmMIB,
    usmUserTable=usmUserTable,
    KeyChange=KeyChange,
    usmUserStatus=usmUserStatus,
    usmStatsNotInTimeWindows=usmStatsNotInTimeWindows,
    usmMIBGroups=usmMIBGroups,
    usmHMACSHAAuthProtocol=usmHMACSHAAuthProtocol,
    usmUserPrivKeyChange=usmUserPrivKeyChange,
    usmUserPublic=usmUserPublic,
    usmUserAuthProtocol=usmUserAuthProtocol,
    snmpUsmMIB=snmpUsmMIB,
    usmNoAuthProtocol=usmNoAuthProtocol,
    usmUserAuthKeyChange=usmUserAuthKeyChange,
    usmUserOwnAuthKeyChange=usmUserOwnAuthKeyChange,
    usmUserPrivProtocol=usmUserPrivProtocol,
    usmStatsUnknownUserNames=usmStatsUnknownUserNames,
    usmUserEngineID=usmUserEngineID,
    usmMIBConformance=usmMIBConformance,
    usmDESPrivProtocol=usmDESPrivProtocol,
    usmUser=usmUser,
    usmMIBCompliance=usmMIBCompliance,
    usmUserCloneFrom=usmUserCloneFrom,
    usmUserEntry=usmUserEntry,
    usmMIBBasicGroup=usmMIBBasicGroup,
    usmStatsUnsupportedSecLevels=usmStatsUnsupportedSecLevels,
    usmMIBObjects=usmMIBObjects,
    usmNoPrivProtocol=usmNoPrivProtocol,
    usmStatsWrongDigests=usmStatsWrongDigests,
    usmUserOwnPrivKeyChange=usmUserOwnPrivKeyChange,
    usmHMACMD5AuthProtocol=usmHMACMD5AuthProtocol,
    usmUserSecurityName=usmUserSecurityName,
    usmStatsUnknownEngineIDs=usmStatsUnknownEngineIDs,
    usmUserSpinLock=usmUserSpinLock,
    usmStats=usmStats,
    usmUserName=usmUserName,
    usmMIBCompliances=usmMIBCompliances,
    usmStatsDecryptionErrors=usmStatsDecryptionErrors,
)

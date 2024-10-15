#
# This file is part of pysnmp software.
#
# Copyright (c) 2005-2020, Ilya Etingof <etingof@gmail.com>
# License: https://www.pysnmp.com/pysnmp/license.html
#
# PySNMP MIB module SNMP-NOTIFICATION-MIB (https://www.pysnmp.com/pysnmp)
# ASN.1 source http://mibs.pysnmp.com:80/asn1/SNMP-NOTIFICATION-MIB
# Produced by pysmi-0.1.3 at Tue Apr 18 00:41:37 2017
# On host grommit.local platform Darwin version 16.4.0 by user ilya
# Using Python version 3.4.2 (v3.4.2:ab2c023a9432, Oct  5 2014, 20:42:22)
#
OctetString, Integer, ObjectIdentifier = mibBuilder.import_symbols(
    "ASN1", "OctetString", "Integer", "ObjectIdentifier"
)
(NamedValues,) = mibBuilder.import_symbols("ASN1-ENUMERATION", "NamedValues")
(
    ValueRangeConstraint,
    ConstraintsIntersection,
    SingleValueConstraint,
    ValueSizeConstraint,
    ConstraintsUnion,
) = mibBuilder.import_symbols(
    "ASN1-REFINEMENT",
    "ValueRangeConstraint",
    "ConstraintsIntersection",
    "SingleValueConstraint",
    "ValueSizeConstraint",
    "ConstraintsUnion",
)
(SnmpAdminString,) = mibBuilder.import_symbols("SNMP-FRAMEWORK-MIB", "SnmpAdminString")
snmpTargetParamsName, SnmpTagValue = mibBuilder.import_symbols(
    "SNMP-TARGET-MIB", "snmpTargetParamsName", "SnmpTagValue"
)
NotificationGroup, ObjectGroup, ModuleCompliance = mibBuilder.import_symbols(
    "SNMPv2-CONF", "NotificationGroup", "ObjectGroup", "ModuleCompliance"
)
(
    TimeTicks,
    IpAddress,
    Integer32,
    snmpModules,
    MibScalar,
    MibTable,
    MibTableRow,
    MibTableColumn,
    Bits,
    Counter32,
    Gauge32,
    Unsigned32,
    MibIdentifier,
    iso,
    ModuleIdentity,
    ObjectIdentity,
    NotificationType,
    Counter64,
) = mibBuilder.import_symbols(
    "SNMPv2-SMI",
    "TimeTicks",
    "IpAddress",
    "Integer32",
    "snmpModules",
    "MibScalar",
    "MibTable",
    "MibTableRow",
    "MibTableColumn",
    "Bits",
    "Counter32",
    "Gauge32",
    "Unsigned32",
    "MibIdentifier",
    "iso",
    "ModuleIdentity",
    "ObjectIdentity",
    "NotificationType",
    "Counter64",
)
DisplayString, TextualConvention, RowStatus, StorageType = mibBuilder.import_symbols(
    "SNMPv2-TC", "DisplayString", "TextualConvention", "RowStatus", "StorageType"
)
snmpNotificationMIB = ModuleIdentity((1, 3, 6, 1, 6, 3, 13))
if mibBuilder.loadTexts:
    snmpNotificationMIB.setRevisions(
        (
            "2002-10-14 00:00",
            "1998-08-04 00:00",
            "1997-07-14 00:00",
        )
    )
if mibBuilder.loadTexts:
    snmpNotificationMIB.setLastUpdated("200210140000Z")
if mibBuilder.loadTexts:
    snmpNotificationMIB.setOrganization("IETF SNMPv3 Working Group")
if mibBuilder.loadTexts:
    snmpNotificationMIB.setContactInfo(
        "WG-email: snmpv3@lists.tislabs.com Subscribe: majordomo@lists.tislabs.com In message body: subscribe snmpv3 Co-Chair: Russ Mundy Network Associates Laboratories Postal: 15204 Omega Drive, Suite 300 Rockville, MD 20850-4601 USA EMail: mundy@tislabs.com Phone: +1 301-947-7107 Co-Chair: David Harrington Enterasys Networks Postal: 35 Industrial Way P. O. Box 5004 Rochester, New Hampshire 03866-5005 USA EMail: dbh@enterasys.com Phone: +1 603-337-2614 Co-editor: David B. Levi Nortel Networks Postal: 3505 Kesterwood Drive Knoxville, Tennessee 37918 EMail: dlevi@nortelnetworks.com Phone: +1 865 686 0432 Co-editor: Paul Meyer Secure Computing Corporation Postal: 2675 Long Lake Road Roseville, Minnesota 55113 EMail: paul_meyer@securecomputing.com Phone: +1 651 628 1592 Co-editor: Bob Stewart Retired"
    )
if mibBuilder.loadTexts:
    snmpNotificationMIB.setDescription(
        "This MIB module defines MIB objects which provide mechanisms to remotely configure the parameters used by an SNMP entity for the generation of notifications. Copyright (C) The Internet Society (2002). This version of this MIB module is part of RFC 3413; see the RFC itself for full legal notices. "
    )
snmpNotifyObjects = MibIdentifier((1, 3, 6, 1, 6, 3, 13, 1))
snmpNotifyConformance = MibIdentifier((1, 3, 6, 1, 6, 3, 13, 3))
snmpNotifyTable = MibTable(
    (1, 3, 6, 1, 6, 3, 13, 1, 1),
)
if mibBuilder.loadTexts:
    snmpNotifyTable.setStatus("current")
if mibBuilder.loadTexts:
    snmpNotifyTable.setDescription(
        "This table is used to select management targets which should receive notifications, as well as the type of notification which should be sent to each selected management target."
    )
snmpNotifyEntry = MibTableRow(
    (1, 3, 6, 1, 6, 3, 13, 1, 1, 1),
).setIndexNames((1, "SNMP-NOTIFICATION-MIB", "snmpNotifyName"))
if mibBuilder.loadTexts:
    snmpNotifyEntry.setStatus("current")
if mibBuilder.loadTexts:
    snmpNotifyEntry.setDescription(
        "An entry in this table selects a set of management targets which should receive notifications, as well as the type of notification which should be sent to each selected management target. Entries in the snmpNotifyTable are created and deleted using the snmpNotifyRowStatus object."
    )
snmpNotifyName = MibTableColumn(
    (1, 3, 6, 1, 6, 3, 13, 1, 1, 1, 1),
    SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(1, 32)),
)
if mibBuilder.loadTexts:
    snmpNotifyName.setStatus("current")
if mibBuilder.loadTexts:
    snmpNotifyName.setDescription(
        "The locally arbitrary, but unique identifier associated with this snmpNotifyEntry."
    )
snmpNotifyTag = MibTableColumn(
    (1, 3, 6, 1, 6, 3, 13, 1, 1, 1, 2), SnmpTagValue()
).setMaxAccess("read-create")
if mibBuilder.loadTexts:
    snmpNotifyTag.setStatus("current")
if mibBuilder.loadTexts:
    snmpNotifyTag.setDescription(
        "This object contains a single tag value which is used to select entries in the snmpTargetAddrTable. Any entry in the snmpTargetAddrTable which contains a tag value which is equal to the value of an instance of this object is selected. If this object contains a value of zero length, no entries are selected."
    )
snmpNotifyType = MibTableColumn(
    (1, 3, 6, 1, 6, 3, 13, 1, 1, 1, 3),
    Integer32()
    .subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2)))
    .clone(namedValues=NamedValues(("trap", 1), ("inform", 2)))
    .clone("trap"),
).setMaxAccess("read-create")
if mibBuilder.loadTexts:
    snmpNotifyType.setStatus("current")
if mibBuilder.loadTexts:
    snmpNotifyType.setDescription(
        "This object determines the type of notification to be generated for entries in the snmpTargetAddrTable selected by the corresponding instance of snmpNotifyTag. This value is only used when generating notifications, and is ignored when using the snmpTargetAddrTable for other purposes. If the value of this object is trap(1), then any messages generated for selected rows will contain Unconfirmed-Class PDUs. If the value of this object is inform(2), then any messages generated for selected rows will contain Confirmed-Class PDUs. Note that if an SNMP entity only supports generation of Unconfirmed-Class PDUs (and not Confirmed-Class PDUs), then this object may be read-only."
    )
snmpNotifyStorageType = MibTableColumn(
    (1, 3, 6, 1, 6, 3, 13, 1, 1, 1, 4), StorageType().clone("nonVolatile")
).setMaxAccess("read-create")
if mibBuilder.loadTexts:
    snmpNotifyStorageType.setStatus("current")
if mibBuilder.loadTexts:
    snmpNotifyStorageType.setDescription(
        "The storage type for this conceptual row. Conceptual rows having the value 'permanent' need not allow write-access to any columnar objects in the row."
    )
snmpNotifyRowStatus = MibTableColumn(
    (1, 3, 6, 1, 6, 3, 13, 1, 1, 1, 5), RowStatus()
).setMaxAccess("read-create")
if mibBuilder.loadTexts:
    snmpNotifyRowStatus.setStatus("current")
if mibBuilder.loadTexts:
    snmpNotifyRowStatus.setDescription(
        "The status of this conceptual row. To create a row in this table, a manager must set this object to either createAndGo(4) or createAndWait(5)."
    )
snmpNotifyFilterProfileTable = MibTable(
    (1, 3, 6, 1, 6, 3, 13, 1, 2),
)
if mibBuilder.loadTexts:
    snmpNotifyFilterProfileTable.setStatus("current")
if mibBuilder.loadTexts:
    snmpNotifyFilterProfileTable.setDescription(
        "This table is used to associate a notification filter profile with a particular set of target parameters."
    )
snmpNotifyFilterProfileEntry = MibTableRow(
    (1, 3, 6, 1, 6, 3, 13, 1, 2, 1),
).setIndexNames((1, "SNMP-TARGET-MIB", "snmpTargetParamsName"))
if mibBuilder.loadTexts:
    snmpNotifyFilterProfileEntry.setStatus("current")
if mibBuilder.loadTexts:
    snmpNotifyFilterProfileEntry.setDescription(
        "An entry in this table indicates the name of the filter profile to be used when generating notifications using the corresponding entry in the snmpTargetParamsTable. Entries in the snmpNotifyFilterProfileTable are created and deleted using the snmpNotifyFilterProfileRowStatus object."
    )
snmpNotifyFilterProfileName = MibTableColumn(
    (1, 3, 6, 1, 6, 3, 13, 1, 2, 1, 1),
    SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(1, 32)),
).setMaxAccess("read-create")
if mibBuilder.loadTexts:
    snmpNotifyFilterProfileName.setStatus("current")
if mibBuilder.loadTexts:
    snmpNotifyFilterProfileName.setDescription(
        "The name of the filter profile to be used when generating notifications using the corresponding entry in the snmpTargetAddrTable."
    )
snmpNotifyFilterProfileStorType = MibTableColumn(
    (1, 3, 6, 1, 6, 3, 13, 1, 2, 1, 2), StorageType().clone("nonVolatile")
).setMaxAccess("read-create")
if mibBuilder.loadTexts:
    snmpNotifyFilterProfileStorType.setStatus("current")
if mibBuilder.loadTexts:
    snmpNotifyFilterProfileStorType.setDescription(
        "The storage type for this conceptual row. Conceptual rows having the value 'permanent' need not allow write-access to any columnar objects in the row."
    )
snmpNotifyFilterProfileRowStatus = MibTableColumn(
    (1, 3, 6, 1, 6, 3, 13, 1, 2, 1, 3), RowStatus()
).setMaxAccess("read-create")
if mibBuilder.loadTexts:
    snmpNotifyFilterProfileRowStatus.setStatus("current")
if mibBuilder.loadTexts:
    snmpNotifyFilterProfileRowStatus.setDescription(
        "The status of this conceptual row. To create a row in this table, a manager must set this object to either createAndGo(4) or createAndWait(5). Until instances of all corresponding columns are appropriately configured, the value of the corresponding instance of the snmpNotifyFilterProfileRowStatus column is 'notReady'. In particular, a newly created row cannot be made active until the corresponding instance of snmpNotifyFilterProfileName has been set."
    )
snmpNotifyFilterTable = MibTable(
    (1, 3, 6, 1, 6, 3, 13, 1, 3),
)
if mibBuilder.loadTexts:
    snmpNotifyFilterTable.setStatus("current")
if mibBuilder.loadTexts:
    snmpNotifyFilterTable.setDescription(
        "The table of filter profiles. Filter profiles are used to determine whether particular management targets should receive particular notifications. When a notification is generated, it must be compared with the filters associated with each management target which is configured to receive notifications, in order to determine whether it may be sent to each such management target. A more complete discussion of notification filtering can be found in section 6. of [SNMP-APPL]."
    )
snmpNotifyFilterEntry = MibTableRow(
    (1, 3, 6, 1, 6, 3, 13, 1, 3, 1),
).setIndexNames(
    (0, "SNMP-NOTIFICATION-MIB", "snmpNotifyFilterProfileName"),
    (1, "SNMP-NOTIFICATION-MIB", "snmpNotifyFilterSubtree"),
)
if mibBuilder.loadTexts:
    snmpNotifyFilterEntry.setStatus("current")
if mibBuilder.loadTexts:
    snmpNotifyFilterEntry.setDescription(
        "An element of a filter profile. Entries in the snmpNotifyFilterTable are created and deleted using the snmpNotifyFilterRowStatus object."
    )
snmpNotifyFilterSubtree = MibTableColumn(
    (1, 3, 6, 1, 6, 3, 13, 1, 3, 1, 1), ObjectIdentifier()
)
if mibBuilder.loadTexts:
    snmpNotifyFilterSubtree.setStatus("current")
if mibBuilder.loadTexts:
    snmpNotifyFilterSubtree.setDescription(
        "The MIB subtree which, when combined with the corresponding instance of snmpNotifyFilterMask, defines a family of subtrees which are included in or excluded from the filter profile."
    )
snmpNotifyFilterMask = MibTableColumn(
    (1, 3, 6, 1, 6, 3, 13, 1, 3, 1, 2),
    OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 16)).clone(hexValue=""),
).setMaxAccess("read-create")
if mibBuilder.loadTexts:
    snmpNotifyFilterMask.setStatus("current")
if mibBuilder.loadTexts:
    snmpNotifyFilterMask.setDescription(
        "The bit mask which, in combination with the corresponding instance of snmpNotifyFilterSubtree, defines a family of subtrees which are included in or excluded from the filter profile. Each bit of this bit mask corresponds to a sub-identifier of snmpNotifyFilterSubtree, with the most significant bit of the i-th octet of this octet string value (extended if necessary, see below) corresponding to the (8*i - 7)-th sub-identifier, and the least significant bit of the i-th octet of this octet string corresponding to the (8*i)-th sub-identifier, where i is in the range 1 through 16. Each bit of this bit mask specifies whether or not the corresponding sub-identifiers must match when determining if an OBJECT IDENTIFIER matches this family of filter subtrees; a '1' indicates that an exact match must occur; a '0' indicates 'wild card', i.e., any sub-identifier value matches. Thus, the OBJECT IDENTIFIER X of an object instance is contained in a family of filter subtrees if, for each sub-identifier of the value of snmpNotifyFilterSubtree, either: the i-th bit of snmpNotifyFilterMask is 0, or the i-th sub-identifier of X is equal to the i-th sub-identifier of the value of snmpNotifyFilterSubtree. If the value of this bit mask is M bits long and there are more than M sub-identifiers in the corresponding instance of snmpNotifyFilterSubtree, then the bit mask is extended with 1's to be the required length. Note that when the value of this object is the zero-length string, this extension rule results in a mask of all-1's being used (i.e., no 'wild card'), and the family of filter subtrees is the one subtree uniquely identified by the corresponding instance of snmpNotifyFilterSubtree."
    )
snmpNotifyFilterType = MibTableColumn(
    (1, 3, 6, 1, 6, 3, 13, 1, 3, 1, 3),
    Integer32()
    .subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2)))
    .clone(namedValues=NamedValues(("included", 1), ("excluded", 2)))
    .clone("included"),
).setMaxAccess("read-create")
if mibBuilder.loadTexts:
    snmpNotifyFilterType.setStatus("current")
if mibBuilder.loadTexts:
    snmpNotifyFilterType.setDescription(
        "This object indicates whether the family of filter subtrees defined by this entry are included in or excluded from a filter. A more detailed discussion of the use of this object can be found in section 6. of [SNMP-APPL]."
    )
snmpNotifyFilterStorageType = MibTableColumn(
    (1, 3, 6, 1, 6, 3, 13, 1, 3, 1, 4), StorageType().clone("nonVolatile")
).setMaxAccess("read-create")
if mibBuilder.loadTexts:
    snmpNotifyFilterStorageType.setStatus("current")
if mibBuilder.loadTexts:
    snmpNotifyFilterStorageType.setDescription(
        "The storage type for this conceptual row. Conceptual rows having the value 'permanent' need not allow write-access to any columnar objects in the row."
    )
snmpNotifyFilterRowStatus = MibTableColumn(
    (1, 3, 6, 1, 6, 3, 13, 1, 3, 1, 5), RowStatus()
).setMaxAccess("read-create")
if mibBuilder.loadTexts:
    snmpNotifyFilterRowStatus.setStatus("current")
if mibBuilder.loadTexts:
    snmpNotifyFilterRowStatus.setDescription(
        "The status of this conceptual row. To create a row in this table, a manager must set this object to either createAndGo(4) or createAndWait(5)."
    )
snmpNotifyCompliances = MibIdentifier((1, 3, 6, 1, 6, 3, 13, 3, 1))
snmpNotifyGroups = MibIdentifier((1, 3, 6, 1, 6, 3, 13, 3, 2))
snmpNotifyBasicCompliance = ModuleCompliance(
    (1, 3, 6, 1, 6, 3, 13, 3, 1, 1)
).setObjects(
    ("SNMP-TARGET-MIB", "snmpTargetBasicGroup"),
    ("SNMP-NOTIFICATION-MIB", "snmpNotifyGroup"),
)
if mibBuilder.loadTexts:
    snmpNotifyBasicCompliance.setDescription(
        "The compliance statement for minimal SNMP entities which implement only SNMP Unconfirmed-Class notifications and read-create operations on only the snmpTargetAddrTable."
    )
snmpNotifyBasicFiltersCompliance = ModuleCompliance(
    (1, 3, 6, 1, 6, 3, 13, 3, 1, 2)
).setObjects(
    ("SNMP-TARGET-MIB", "snmpTargetBasicGroup"),
    ("SNMP-NOTIFICATION-MIB", "snmpNotifyGroup"),
    ("SNMP-NOTIFICATION-MIB", "snmpNotifyFilterGroup"),
)
if mibBuilder.loadTexts:
    snmpNotifyBasicFiltersCompliance.setDescription(
        "The compliance statement for SNMP entities which implement SNMP Unconfirmed-Class notifications with filtering, and read-create operations on all related tables."
    )
snmpNotifyFullCompliance = ModuleCompliance((1, 3, 6, 1, 6, 3, 13, 3, 1, 3)).setObjects(
    ("SNMP-TARGET-MIB", "snmpTargetBasicGroup"),
    ("SNMP-TARGET-MIB", "snmpTargetResponseGroup"),
    ("SNMP-NOTIFICATION-MIB", "snmpNotifyGroup"),
    ("SNMP-NOTIFICATION-MIB", "snmpNotifyFilterGroup"),
)
if mibBuilder.loadTexts:
    snmpNotifyFullCompliance.setDescription(
        "The compliance statement for SNMP entities which either implement only SNMP Confirmed-Class notifications, or both SNMP Unconfirmed-Class and Confirmed-Class notifications, plus filtering and read-create operations on all related tables."
    )
snmpNotifyGroup = ObjectGroup((1, 3, 6, 1, 6, 3, 13, 3, 2, 1)).setObjects(
    ("SNMP-NOTIFICATION-MIB", "snmpNotifyTag"),
    ("SNMP-NOTIFICATION-MIB", "snmpNotifyType"),
    ("SNMP-NOTIFICATION-MIB", "snmpNotifyStorageType"),
    ("SNMP-NOTIFICATION-MIB", "snmpNotifyRowStatus"),
)
if mibBuilder.loadTexts:
    snmpNotifyGroup.setDescription(
        "A collection of objects for selecting which management targets are used for generating notifications, and the type of notification to be generated for each selected management target."
    )
snmpNotifyFilterGroup = ObjectGroup((1, 3, 6, 1, 6, 3, 13, 3, 2, 2)).setObjects(
    ("SNMP-NOTIFICATION-MIB", "snmpNotifyFilterProfileName"),
    ("SNMP-NOTIFICATION-MIB", "snmpNotifyFilterProfileStorType"),
    ("SNMP-NOTIFICATION-MIB", "snmpNotifyFilterProfileRowStatus"),
    ("SNMP-NOTIFICATION-MIB", "snmpNotifyFilterMask"),
    ("SNMP-NOTIFICATION-MIB", "snmpNotifyFilterType"),
    ("SNMP-NOTIFICATION-MIB", "snmpNotifyFilterStorageType"),
    ("SNMP-NOTIFICATION-MIB", "snmpNotifyFilterRowStatus"),
)
if mibBuilder.loadTexts:
    snmpNotifyFilterGroup.setDescription(
        "A collection of objects providing remote configuration of notification filters."
    )
mibBuilder.export_symbols(
    "SNMP-NOTIFICATION-MIB",
    PYSNMP_MODULE_ID=snmpNotificationMIB,
    snmpNotifyFilterProfileTable=snmpNotifyFilterProfileTable,
    snmpNotifyTag=snmpNotifyTag,
    snmpNotifyGroup=snmpNotifyGroup,
    snmpNotifyFilterProfileRowStatus=snmpNotifyFilterProfileRowStatus,
    snmpNotifyRowStatus=snmpNotifyRowStatus,
    snmpNotifyCompliances=snmpNotifyCompliances,
    snmpNotifyTable=snmpNotifyTable,
    snmpNotifyType=snmpNotifyType,
    snmpNotifyStorageType=snmpNotifyStorageType,
    snmpNotifyConformance=snmpNotifyConformance,
    snmpNotifyFilterMask=snmpNotifyFilterMask,
    snmpNotifyFilterProfileName=snmpNotifyFilterProfileName,
    snmpNotifyEntry=snmpNotifyEntry,
    snmpNotifyFullCompliance=snmpNotifyFullCompliance,
    snmpNotifyObjects=snmpNotifyObjects,
    snmpNotifyFilterEntry=snmpNotifyFilterEntry,
    snmpNotificationMIB=snmpNotificationMIB,
    snmpNotifyFilterRowStatus=snmpNotifyFilterRowStatus,
    snmpNotifyBasicFiltersCompliance=snmpNotifyBasicFiltersCompliance,
    snmpNotifyFilterGroup=snmpNotifyFilterGroup,
    snmpNotifyFilterProfileEntry=snmpNotifyFilterProfileEntry,
    snmpNotifyFilterTable=snmpNotifyFilterTable,
    snmpNotifyFilterSubtree=snmpNotifyFilterSubtree,
    snmpNotifyBasicCompliance=snmpNotifyBasicCompliance,
    snmpNotifyFilterStorageType=snmpNotifyFilterStorageType,
    snmpNotifyGroups=snmpNotifyGroups,
    snmpNotifyName=snmpNotifyName,
    snmpNotifyFilterProfileStorType=snmpNotifyFilterProfileStorType,
    snmpNotifyFilterType=snmpNotifyFilterType,
)

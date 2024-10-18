#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from datetime import datetime
import xml.etree.cElementTree as ET
import collections

import xmltodict

from edds_process.globals import SCOS_HEADER_BYTES, LOGGER, INPUT_STRFTIME

__all__ = ['parse_tcreport_xml',
           'yield_tcreport_xml',
           'parse_raw_xml',
           'yield_raw_xml',
           'count_packets',
           'xml_to_dict',
           'remove_scos_header']

# Expected fields and order of the tc report elements
TC_REPORT_KEYS = ['ExecutionTime', 'CommandName', 'RawBodyData',
                      'OnBoardAccState', 'ExecCompState', 'ExecCompPBState',
                      'SequenceName', 'uniqueID', 'Description',
                      'ReleaseTime', 'UplinkTime',
                      'ReleaseState','GroundState','UplinkState',
                      'OnBoardState', 'Apid',
                    ]

def parse_tcreport_xml(tcreport_xml, logger=LOGGER):
    """
    Parse an input EDDS tcreport XML file.

    :param tcreport_xml: input TcReport XML file to parse
    :param kwargs: keyword arguments to be passed to yield_tcreport_xml. (See yield_tcreport_xml docstring for input argument
    :return: Dictionary containing the content of tcreport (ExecutionTime used as keys)
    """

    tc_report = dict()
    for tcreport_content in yield_tcreport_xml(tcreport_xml, logger=logger):
        # save the data in the packet list
        name = tcreport_content.pop('CommandName')
        exec_time = tcreport_content.pop('ExecutionTime')
        tc_report[(name, exec_time)] = tcreport_content

    return tc_report


def yield_tcreport_xml(tcreport_xml,
                   logger=LOGGER):
    """
    Parse an input edds tcreport XML file.

    :param tcreport_xml: Path to the EDDS TcReport XML file
    :param logger: Define logger
    :return: Tc Report content.
    """

    with open(tcreport_xml, 'r') as xml_file:
        # loop without parsing on the document

        for event, elem in ET.iterparse(xml_file, ['end']):
            # Retrieve tag with Tc report list
            if elem.tag == 'PktTcReportListElement':

                tc_elem_list = dict()
                for tag in TC_REPORT_KEYS:

                    if tag == 'ExecutionTime':
                        value = datetime.strptime(elem.find('ExecutionTime').text, INPUT_STRFTIME)
                    elif tag == 'uniqueID':
                        value = None
                        for field in elem.findall('./CustomField'):
                            fieldname = field.find('FieldName').text
                            if fieldname == 'uniqueID':
                                value = field.find('Value').text
                                break
                    else:
                        if elem.find(tag) is not None:
                            value = elem.find(tag).text
                        else:
                            logger.warning(f'{tag} not found in {tcreport_xml}')
                            value = None

                    tc_elem_list[tag] = value

                yield tc_elem_list


def parse_raw_xml(raw_xml, **kwargs):
    """
    Parse an input EDDS raw XML file.

    :param raw_xml: input EDDS raw file to parse
    :param kwargs: keyword arguments to be passed to yield_raw_xml. (See yield_raw_xml docstring for input arguments)
    :return: list of raw binary packets
    """

    raw_binary_packets = []
    for packet_content in yield_raw_xml(raw_xml, kwargs):
        # save the data in the packet list
        raw_binary_packets.append(packet_content)

    return raw_binary_packets


def yield_raw_xml(raw_xml,
                    scos_header=SCOS_HEADER_BYTES,
                    logger=LOGGER):
    """
    Parse an input EDDS raw XML file.

    :param raw_xml: Path to the EDDS TmRaw or TcRaw XML file
    :param scos_header: Header offset bytes to remove
    :return: list of binary packets extracted from the input file.
    """

    with open(raw_xml, 'r') as xml_file:
        # loop without parsing on the document
        # get an iterable
        context = ET.iterparse(xml_file, events=('start', 'end'))

        is_first = True

        for event, elem in context:
            # get the root element
            if is_first:
                root = elem
                is_first = False
            if event == 'end' and elem.tag == 'PktRawResponseElement':

                # get packet ID
                packet_ID = elem.attrib['packetID']

                # get Packet node
                packet_node = elem.find('Packet')

                # only put in the database events with data inside
                if packet_node is None:
                    logger.debug(
                        "Packet {0} doesn't have data".format(packet_ID)
                    )
                    continue
                else:
                    packet_content = packet_node.text

                # if keyword is True, then remove scos2000 header (i.e., first 76 bytes)
                if scos_header:
                    packet_content = remove_scos_header(packet_content,
                                                        scos_header=scos_header)

                root.clear()

                # return current packet
                yield packet_content


def remove_scos_header(packet, scos_header=SCOS_HEADER_BYTES):
    """
    Remove SCOS2000 header from the input hexadecimal binary packet

    :param packet: hexa. binary packet with SCOS header to remove.
    :param scos_header: scos header in bytes to remove
    :return: hexa. packet without SCOS header
    """
    return bytearray.fromhex(packet)[scos_header:].hex().upper()


def xml_to_dict(xml_file,
                as_list=False,
                logger=LOGGER):
    """
    Convert input XML file into dictionary.

    :param xml_file: input XML file to convert
    :param as_list: If True, attempt to return only the
                    list of XML elements in the XML files.
                    Must be a valid DDS input file.
    :param logger: logger
    :return: dictionary or list containing XML element tree
    """
    output_xml = None

    with open(xml_file, 'r') as xml:
        xml_dict = xmltodict.parse(xml.read())

    if as_list:

        try:
            xml_dict = xml_dict['ns2:ResponsePart'] \
                ['Response']
        except:
            logger.error(f'{xml_file} is not a valid EDDS response XML file!')
            return output_xml

        # Try to get list of ParamSampleListElement from a Param DDS XML file
        if 'ParamResponse' in xml_dict:
            xml_list = xml_dict['ParamResponse'] \
                ['ParamSampleList']['ParamSampleListElement']

        # Try to get list of PktRawResponseElement from a TmRaw DDS XML file
        elif 'PktRawResponse' in xml_dict:
            xml_list = xml_dict['PktRawResponse'] \
                ['PktRawResponseElement']

        # Try to get list of PktTcReportListElement from a TcReport DDS XML file
        elif 'PktTcReportResponse' in xml_dict:
            xml_list = xml_dict['PktTcReportResponse'] \
                ['PktTcReportList']['PktTcReportListElement']
        else:
            logger.warning(f'Content of {xml_file} cannot be returned as a list of elements!')
            return output_xml

        if isinstance(xml_list, collections.OrderedDict):
            xml_list = [xml_list]
        output_xml = xml_list

    else:
        output_xml = xml_dict

    return output_xml


def count_packets(xml_file, file_type=None,
                  logger=LOGGER):
    """
    Return the number of packets in the input DDS XML file

    :param xml_file: input DDS XML file
    :param file_type: type of DDS data. Possible values are 'TMREPORT' or 'TMRAW'.
    :param logger: external logger can be passed here.
    :return: integer containing the number of packets found
    """

    # Initialize output counter
    counter = 0

    if file_type is None:
        logger.debug('Attempting to retrieve EDDS file type from the file name...')
        file_basename = os.path.basename(xml_file).upper()
        # Try to get Type of DDS file from the basename
        if 'TCREPORT' in file_basename or '_TC_' in file_basename:
            file_type = 'TCREPORT'
        elif 'TMRAW' in file_basename or '_TM_' in file_basename:
            file_type = 'TMRAW'
        else:
            logger.warning(f'Input DDS file is not valid: {xml_file}')
            return None
    else:
        file_type = file_type.upper()

    if file_type == 'TCREPORT':
        element_name = 'PktTcReportListElement'
    elif file_type == 'TMRAW':
        element_name = 'PktRawResponseElement'
    else:
        logger.warning(f'Input DDS file type is not valid: {file_type}')
        return []

    tree = ET.parse(xml_file)

    return len(tree.findall(f'.//{element_name}'))

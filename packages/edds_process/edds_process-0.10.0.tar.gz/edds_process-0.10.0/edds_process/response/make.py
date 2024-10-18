#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import xmltodict

from edds_process.globals import LOGGER

__all__ = ['make_tmraw_xml', 'make_tcreport_xml', 'make_param_xml']


def make_tmraw_xml(packets, output_file,
                   overwrite=False,
                   logger=LOGGER):
    """
    Create a MOC DDS TmRaw XML file with input binary packets.

    :param packets: List of packets to save into the DDS XML file (provided as hexadecimal strings)
    :param output_file: Path and name of the output DDS XML file
    :param overwrite: If True then replace existing output file, else abort output file production
    :return: True if output file has been successfully generated, False otherwise.
    """

    if os.path.isfile(output_file) and not overwrite:
        logger.warning(f'{output_file} already exists, skip output file production!')
        return output_file
    elif os.path.isfile(output_file) and overwrite:
        logger.debug(f'{output_file} already exists and will be replaced!')
    else:
        logger.debug(f'Writing {output_file} with {len(packets)} packet(s)')

    # Add DDS file header
    xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    xml += '<ns2:ResponsePart xmlns:ns2="http://edds.egos.esa/model">'
    xml += '<Response>'
    xml += '<PktRawResponse>'

    # Add packets
    for i, packet in enumerate(packets):
        # Write PktRawResponseElement tag and packetID attribute
        xml += f'<PktRawResponseElement packetID="{i + 1}">'
        # Write packet
        xml += f'<Packet>{packet}</Packet>'
        # Close PktRawResponseElement
        xml += f'</PktRawResponseElement>'

    # Add DDS file footer
    xml += '</PktRawResponse>'
    xml += '</Response>'
    xml += '</ns2:ResponsePart>'

    # write output EDDS TmRaw XML file
    logger.debug(f'Saving output EDDS TcReport XML file {output_file}')
    with open(output_file, 'w') as out_file:
        out_file.write(xml)

    return os.path.isfile(output_file)


def make_tcreport_xml(tcreport_list, output_file,
                      overwrite=False,
                      logger=LOGGER):
    """
    Create a MOC DDS TcReport XML file with input binary packets.

    :param tcreport_list: List of TcReport XML Elements to save into the DDS XML file (provided as dictionary)
    :param output_file: Path and name of the output DDS XML file
    :param overwrite: If True then replace existing output file, else abort output file production
    :return: True if output file has been successfully generated, False otherwise.
    """

    if os.path.isfile(output_file) and not overwrite:
        logger.warning(f'{output_file} already exists, skip output file production!')
        return output_file
    elif os.path.isfile(output_file) and overwrite:
        logger.debug(f'{output_file} already exists and will be replaced!')
    else:
        logger.debug(f'Writing {output_file} with {len(tcreport_list)} packet(s)')

    # Prepare input dictionary to be serialized by dicttoxml
    tcreport_data = {'Response':
                     {'PktTcReportResponse':
                      {'PktTcReportList':
                       {'PktTcReportListElement': tcreport_list}}}}

    # Build XML snippet from input tcreport element list
    tcreport_xml = xmltodict.unparse(tcreport_data)

    # Remove the first line (<?xml version="1.0" encoding="utf-8"?>)
    # automatically added by xmltodict.unparse() method
    tcreport_xml = tcreport_xml.split('\n')[1]

    # Add header and root parts
    tcreport_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' \
                   f'<ns2:ResponsePart xmlns:ns2="http://edds.egos.esa/model">' \
                   f'{tcreport_xml}</ns2:ResponsePart>'

    # Create output TcReport XML file
    logger.debug(f'Saving output EDDS TcReport XML file {output_file}')
    with open(output_file, 'w') as fw:
        fw.write(tcreport_xml)

    return os.path.isfile(output_file)


def make_param_xml(param_list, output_file,
                   overwrite=False,
                   logger=LOGGER):
    """
    Create a MOC DDS Param XML file with input ParamSampleListElement elements.

    :param param_list: List of ParamSampleListElement XML Elements
    to save into the DDS XML file (provided as dictionary)
    :param output_file: Path and name of the output DDS XML file
    :param overwrite: If True then replace existing output file, else abort output file production
    :return: True if output file has been successfully generated, False otherwise.
    """

    if os.path.isfile(output_file) and not overwrite:
        logger.warning(f'{output_file} already exists, skip output file production!')
        return output_file
    elif os.path.isfile(output_file) and overwrite:
        logger.debug(f'{output_file} already exists and will be replaced!')
    else:
        logger.debug(f'Writing {output_file} with {len(param_list)} element(s)')

    # Prepare input dictionary to be serialized by dicttoxml
    param_data = {'Response':
                  {'ParamResponse':
                   {'ParamSampleList':
                    {'ParamSampleListElement': param_list}}}}

    # Build XML snippet from input param element list
    param_xml = xmltodict.unparse(param_data)

    # Remove the first line (<?xml version="1.0" encoding="utf-8"?>)
    # automatically added by xmltodict.unparse() method
    param_xml = param_xml.split('\n')[1]

    # Add header and root parts
    param_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' \
        f'<ns2:ResponsePart xmlns:ns2="http://edds.egos.esa/model">' \
        f'{param_xml}</ns2:ResponsePart>'

    # Create output Param XML file
    logger.debug(f'Saving output EDDS Param XML file {output_file}')
    with open(output_file, 'w') as fw:
        fw.write(param_xml)

    return os.path.isfile(output_file)

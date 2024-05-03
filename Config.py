import os
import sys
import wx
import typing
import csv


class Config:
    # region Class Variables
    EQUIVALENTS = {}

    IPGS = ['570 A9', '570 X-19', 'evIPG-12G', 'evIPG-3G']

    LINK_TYPES = ['SD', 'HD', '3GA']
    LINK_LINE_SUPPORTED = {
        'SD': ['525i', '625i'],
        'HD': ['720p', '1080i', '1080sF', '1080p'],
        '3GA': ['720p', '1080i', '1080sF', '1080p']
    }
    FRAME_RATES_SUPPORTED = {
        '525i': ['59.94'],
        '625i': ['50'],
        '720p': ['23.98', '24', '25', '29.97', '30', '50', '59.94', '60'],
        '1080i': ['50', '59.94', '60'],
        '1080sF': ['23.98', '24', '25', '29.97', '30'],
        '1080p': ['23.98', '24', '25', '29.97', '30']
    }

    COLOUR_SPACE = ['YCbCr-422-10']

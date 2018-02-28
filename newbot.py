# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import os
import string
import urllib
import sys


class MurkinaParser:

    real_names = []
    other_names = []

    assari = []
    brygge = []
    delipharma = []
    ict = []
    macciavelli = []
    myssy = []
    tottisalmi = []

    def __init__(self, restaurant_name):
        self.init_files()
        # self.main(self.parse_restaurant_name(restaurant_name))

    def to_unicode(obj, encoding='utf-8'):
        if isinstance(obj, basestring):
            if not isinstance(obj, unicode):
                obj = unicode(obj, encoding)
        return obj
        # Parse restaurant names from file and store them to array
    def init_files(self):
        ravintola_file = open('raflojen_nimet', 'r').readlines()
        for name in ravintola_file:
            # self.to_unicode(name)
            # print '\xc3\xa4'  
            # if '\xc3\xa4' in name:
            #     self.real_names = name.replace('\xc3\xa4', 'a')
            #     print "ae'd"
            self.real_names = name.split(",")

        print(self.real_names)

        self.parse_other_names()

        # print self.real_names


    def parse_other_names(self):
        lempinimifile = open('lempinimet.txt', 'r').readlines()

        self.assari = lempinimifile[0].split(",")
        self.brygge = lempinimifile[1].split(",")
        self.delipharma = lempinimifile[2].split(",")
        self.ict = lempinimifile[3].split(",")
        self.macciavelli = lempinimifile[4].split(",")
        self.myssy = lempinimifile[5].split(",")
        self.tottisalmi = lempinimifile[6].split(",")
        self.galilei = lempinimifile[7].split(",")
        self.mantymaki = lempinimifile[8].split(",")

    def parse_restaurant_name(self, restaurant_name):
        restaurant_name = restaurant_name.lower()
        # Oikeat nimet
        for rname in self.real_names:
            if restaurant_name == rname.lower():
                return rname
        # Lempinimet
        for rname in self.assari:
            if restaurant_name == rname.lower():
                return self.real_names[0]

        for rname in self.brygge:
            if restaurant_name == rname.lower():
                return self.real_names[1]

        for rname in self.delipharma:
            if restaurant_name == rname.lower():
                return self.real_names[4]

        for rname in self.ict:
            if restaurant_name == rname.lower():
                return self.real_names[6]

        for rname in self.macciavelli:
            if restaurant_name == rname.lower():
                return self.real_names[8]

        for rname in self.myssy:
            if restaurant_name == rname.lower():
                return self.real_names[11]

        for rname in self.tottisalmi:
            if restaurant_name == rname.lower():
                return self.real_names[19]

        for rname in self.galilei:
            if restaurant_name == rname.lower():
                return self.real_names[22]
                
        for rname in self.mantymaki:
            if restaurant_name == rname.lower():
                return self.real_names[12]
        return None


        
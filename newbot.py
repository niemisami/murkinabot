# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import sys
import os
import string


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

        # Parse restaurant names from file and store them to array
    def init_files(self):
        ravintola_file = open('raflojen_nimet', 'r').readlines()
        for name in ravintola_file:
            if '\xc3\xa4' in name:
                self.real_names = name.replace('\xc3\xa4', 'a')
            self.real_names = self.real_names.split(",")
        print self.real_names

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
        self.mantymaki = lempinimifile[7].split(",")
        self.galilei = lempinimifile[8].split(",")

    def parse_restaurant_name(self, restaurant_name):
        print(restaurant_name)
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
        for rname in self.mantymaki:
            if restaurant_name == rname.lower():
                return self.real_names[12]
        for rnmame in self.galilei:
        	if restaurant_name == rname.lower():
        		return self.real_names[22]

    def main(self, restaurant_name):

        if restaurant_name is None:
            print "Ei sellaista ravintolaa ole"

        else:

            markup = urllib2.urlopen('http://murkinat.appspot.com').read()

            soup = BeautifulSoup(markup, "html.parser")

            restaurants = soup.find_all('div', class_="restaurant")

            f = open('temp.txt', 'w')
            errors = open('errors.txt', 'w')
            for restaurant in restaurants:

                names = restaurant.find('h3', class_="restaurantName")

                output = ""
                for name in names.stripped_strings:
                    try:

                        # print "%s ja %s" %(name, restaurant_name)
                        # print name.encode('utf-8')  == restaurant_name
                        # print
                        # name.encode('utf-8').replace(u"c2a0".decode('hex'), '
                        # ') == restaurant_name

                        # name = name.encode('hex', 'ignore')
                        # print name
                        # print "%s ja %s" %(name, restaurant_name)
                        # print name.strip() == restaurant_name.strip()
                        if name.encode('utf-8').replace(u"c2a0".decode('hex'), ' ') == restaurant_name:
                            output += name
                            # print name

                            meals = restaurant.find_all(
                                'table', class_="meals")

                            for meal in meals:
                                mealNames = meal.find_all(
                                    'td', class_="mealName")
                                for mealName in mealNames:
                                    try:
                                        output += mealName.string
                                    except UnicodeEncodeError:
                                        print "Unicode error"
                                        f.write("Error\n")

                            print output

                            break
                        # else:
                        # 	print "Nimi väärin?"

                        # print output

                            # irc.send( 'PRIVMSG %s :%s' % ( line[2], output.encode('utf-8')))

                    except UnicodeEncodeError as err:
                        # print 'Error'
                        f.write("Error\n")

                #irc.send( 'PRIVMSG %s :%s' % ( line[2], name.encode('utf-8')))

                    #irc.send( 'PRIVMSG %s :%s' % ( line[2], mealName.string.encode('utf-8')))

    def get_restaurants(self):
        if len(self.real_names) == 0:
            self.init_files
        return self.real_names


if __name__ == '__main__':
    murkinat = Murkinat(sys.argv[1])

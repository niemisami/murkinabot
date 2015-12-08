# -*- coding: utf-8 -*-

"""
muutama esimerkki komennoista
"""

import random
from bs4 import BeautifulSoup
import urllib2
from newbot import MurkinaParser
# tähän sanastoon lisätään komennot ja niitä vastaavat oliot

command_dict = {}


class Test:

    def main( self, irc, line ):

        irc.send( 'PRIVMSG %s :Hello world!' % line[2] )

command_dict[ ':!test' ] = Test()


class Join:

    def main( self, irc, line):

        irc.send( 'JOIN %s' % ( line[4] ) )

command_dict[ ':!join' ] = Join()


class Quit:

    def main( self, irc , line ):

        # määritellään komento vain pääkäyttäjille
        irc.send( 'PRIVMSG %s :%s, %s' % (line[2], line[0], "sammutetaan"))
        if line[0] in irc.users:

            irc.send( 'QUIT' )
            irc.socket.close()
            irc.done = 1

command_dict[ ':!quit' ] = Quit()


class Anagram:

    def main( self, irc, line):

        string = list( ' '.join( line[4:] ) )
        random.shuffle( string )
        string = ''.join( string )
        irc.send( 'PRIVMSG %s :%s' % ( line[2], string ) )

command_dict[ ':!anagram' ] = Anagram()

class Murkinat:

    def main( self, irc, line):


        parser = MurkinaParser()

        restaurant_name = parser.parse_restaurant_name(line[2])

        print restaurant_name

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
                        # print name.encode('utf-8').replace(u"c2a0".decode('hex'), ' ') == restaurant_name

                        # name = name.encode('hex', 'ignore')
                        # print name
                        # print "%s ja %s" %(name, restaurant_name)
                        # print name.strip() == restaurant_name.strip()
                        if name.encode('utf-8').replace(u"c2a0".decode('hex'), ' ') == restaurant_name:
                            f.write(name.encode('utf-8'))
                            output += name
                            # print name


                            meals = restaurant.find_all('table', class_="meals")

                            for meal in meals:
                                mealNames = meal.find_all('td', class_="mealName")
                                for mealName in mealNames:
                                    try:
                                        output += mealName.string
                                        f.write(mealName.string.encode('utf-8'))
                                    except UnicodeEncodeError:
                                        print "Unicode error"

                            print output

                            # irc.send( 'PRIVMSG %s :%s' % ( line[2], output.encode('utf-8')))
                            break
                        # else:
                        #   print "Nimi väärin?"

                        # print output




                    except UnicodeEncodeError as err:
                        # print 'Error'
                        f.write("Error")




command_dict[ ':!murkinat' ] = Murkinat()
# -*- coding: utf-8 -*-

"""
muutama esimerkki komennoista
"""

import random
import urllib2
from bs4 import BeautifulSoup
from newbot import MurkinaParser
from datetime import datetime
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
        if line[0] in irc.users:

            irc.send( 'PRIVMSG %s :%s, %s' % (line[2], line[0], "sammutetaan"))
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

        self.parser = MurkinaParser("")
        restaurant_name = self.parser.parse_restaurant_name(line[4])

        if line[4] == 'help' or line[4] == '-h':
            pass
            irc.sendWithDelay( 'PRIVMSG %s :%s' % ( line[2], "Hae Turun ravintoloiden ruokalistat kirjoittamalla !murkinat nimi (esim !murkinat ict)" ))
            irc.sendWithDelay( 'PRIVMSG %s :%s' % ( line[2], "Muut komennot:"))   
            irc.sendWithDelay( 'PRIVMSG %s :%s' % ( line[2], "Listaa avoimet ravintolat: !murkinat lista"))   
            irc.sendWithDelay( 'PRIVMSG %s :%s' % ( line[2], "Ehdottaa satunnaista avoinna olevaa ravintolaa: !murkinat random"))
        elif restaurant_name is None and line[4] != 'lista' and line[4] != 'random':
            print "Ei sellaista ravintolaa ole"
        else:
            open_restaurants = self.find_menu(irc,restaurant_name)
            if line[4] == 'random':
                self.find_menu(irc, self.get_random(open_restaurants))
            elif line[4] == "lista":
                irc.sendWithDelay( 'PRIVMSG %s :%s' % ( line[2], list_restaurants(open_restaurants)))
     



    def find_menu(self,irc,restaurant_name):
            markup = urllib2.urlopen('http://murkinat.appspot.com').read()
            soup = BeautifulSoup(markup, "html.parser")
            restaurants = soup.find_all('div', class_="restaurant")
            open_restaurants = []


            f = open('temp.txt', 'w')
            errors = open('errors.txt', 'w')
            for restaurant in restaurants:

                names = restaurant.find('h3', class_="restaurantName")

                output = ""
                for name in names.stripped_strings:
                    open_restaurants.append(name);
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

                            irc.sendWithDelay( 'PRIVMSG %s :%s' % ( line[2], name.encode('utf-8')))
                            print "%s ja %s" % (name,restaurant_name)
                            output += name
                            # print name


                            meals = restaurant.find_all('table', class_="meals")

                            for meal in meals:
                                mealNames = meal.find_all('td', class_="mealName")
                                for mealName in mealNames:
                                    try:
                                        for m in mealName.stripped_strings:
                                            f.write(m.encode('utf-8'))
                                            irc.sendWithDelay( 'PRIVMSG %s :%s' % ( line[2], m.encode('utf-8')))
                                    except UnicodeEncodeError:
                                        print "Unicode error"

                            self.log(line)
                            break

                    except UnicodeEncodeError as err:
                        # print 'Error'
                        f.write("Error")



    def log(self, line):
        with open("log.txt", 'a') as f:
            if len(line) > 4:
                f.write("%s@%s: %s\n" %(str(datetime.now()),line[0], line[4]))
            else:
              f.write("%s: empty" %(line[2]))

    def list_restaurants(self, restaurants):

        output = "Ravintolat: "
        for name in restaurants:
            if name != restaurants[len(restaurants)-1]:
                output += "%s, " %(name)
            else:
                output += name
        return output
                                    
    def get_random(self,restaurants):
        rnd = random.randint(0,len(restaurants))
        return restaurants[rnd]
        

class JuhannusKeneraattori:

    def main(self, irc, line):
        if len(line[4]) > 0: 
            jussinimet = ['Dallaspulla','Jeesus','Kossu','Huittisten','Amkkihomo','Onneksi olkoon Mikko','Läski','Kalanaama','Diplomi-Insinööri','Selfie','Homo','Hintti','Hupsu','Perse','Aasi','Aamukalja','Sammuja','Ripuli','Juhannussija','Vässykkä','Penseä','DJ-Sorslund','Hukkuja','Juliuksen mökin viimeinen hereillä oleva sankari joka on ollut ihan törkeässä kännissä koko viikonlopun','Pippelöijä','Forsman','Spagetti']
            nameArgs = ''
            for index, name in enumerate(line):
                if(index >= 4):
                    nameArgs += '%s ' % line[index] 
            juhannusnimi = "Juhannusnimesi on: %s" % random.choice(jussinimet) + "-" + nameArgs.title()
            # print "testi: " + nameArgs;
            irc.send( 'PRIVMSG %s :%s' % ( line[2], juhannusnimi))
        else:
            message = 'Kirjoita vielä nimesi, hintti'
            irc.send( 'PRIVMSG %s :%s' % ( line[2], message))







command_dict[ ':!murkinat' ] = Murkinat()

command_dict[ ':!juhannusnimi' ] = JuhannusKeneraattori()
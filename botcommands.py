# -*- coding: utf-8 -*-

import random
import urllib2
from bs4 import BeautifulSoup
from newbot import MurkinaParser
from datetime import datetime

# tähän sanastoon lisätään komennot ja niitä vastaavat oliot

command_dict = {}

class Test:
    def main(self, irc, line):
        irc.send('PRIVMSG %s :Hello world!' % line[2])

command_dict[ ':!test' ] = Test()


class Join:
    def main( self, irc, line):
        irc.send( 'JOIN %s' % ( line[4] ) )

command_dict[ ':!join' ] = Join()


class Quit:
    def main(self, irc, line):

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
        random.shuffle(string)
        string = ''.join(string)
        irc.send( 'PRIVMSG %s :%s' % ( line[2], string ) )

command_dict[ ':!anagram' ] = Anagram()

class Kolikko:
    def main( self, irc, line):
        replyTo = line[0][1:line[0].index('!')]
        cointoss = random.randint(0,1)
        result = "Klaava" if cointoss == 0 else "Kruuna"
        string = replyTo + ": " + result
        irc.send( 'PRIVMSG %s :%s' % (line[2], string) )

command_dict[ ':!kolikko' ] = Kolikko()

class Murkinat:

    def main( self, irc, line):

        self.parser = MurkinaParser("")
        self.websiteParser = WebsiteParser()
        self.irc_connection = irc
        self.irc_line = line

        commands = line[4:]
        
        self.murkinat(commands)

        # restaurant_name = self.parser.parse_restaurant_name(line[4])

        # if line[4] == 'help' or line[4] == '-h':
        #     pass
        #     irc.sendWithDelay( 'PRIVMSG %s :%s' % ( line[2], "Hae Turun ravintoloiden ruokalistat kirjoittamalla !murkinat nimi (esim !murkinat ict)" ))
        #     irc.sendWithDelay( 'PRIVMSG %s :%s' % ( line[2], "Muut komennot:"))   
        #     irc.sendWithDelay( 'PRIVMSG %s :%s' % ( line[2], "Listaa avoimet ravintolat: !murkinat lista"))   
        #     irc.sendWithDelay( 'PRIVMSG %s :%s' % ( line[2], "Ehdottaa satunnaista avoinna olevaa ravintolaa: !murkinat random"))
        # elif restaurant_name is None and line[4] != 'lista' and line[4] != 'random':
        #     print "Ei sellaista ravintolaa ole"
        # else:
        #     open_restaurants = self.find_menu(irc,restaurant_name)
        #     if line[4] == 'random':
        #         self.find_menu(irc, self.get_random(open_restaurants))
        #     elif line[4] == "lista":
        #         irc.sendWithDelay( 'PRIVMSG %s :%s' % ( line[2], list_restaurants(open_restaurants)))
     

    def murkinat(self,commands):

        command = commands[0]

        # command = "" #for testing
        # command = "help" #for testing
        # command = "joke" #for testing
        # command = "lista" #for testing
        # command = "random" #for testing
        # command = "mäntymäki" #for testing

        if command is None or len(command) == 0:
            self.received_empty_command() 

        elif command == "help" or command == "h":
            self.return_help()

            # Other commands require loading the murkinat site 
        else:
            command = command.lower()
            murkinat_site = self.load_murkinat_html()
            restaurant_container = self.websiteParser.parse_div_class_from(murkinat_site,"restaurant")

            if command == "lista":
                open_restaurants = self.return_open_restaurants(restaurant_container)
                self.send_irc(self.list_restaurants(open_restaurants))

            elif command == "random":
                random_name = self.return_random_restaurant(restaurant_container)
                print random_name

            else:
                index = 0
                # TODO continue:
                # commands = self.remove_duplicates(commands) 
                for command in commands:

                    restaurant_name = self.parser.parse_restaurant_name(command)
                    if restaurant_name is None:
                        self.return_wrong_name_error()
                    else: 
                        result = self.parse_menu(restaurant_container, restaurant_name)
                        if result:
                            # self.log()
                            print "cool"
                        else:  
                            self.send_irc("Ei olee")
                            print "not cool"
                    
                    if(index > 5): # No reason to get all the restaurants and pollute irc channel
                        break
                    index += 1


        ####Oikeat murkinametodit####
    def return_help(self):
    
        self.send_irc("Hae Turun ravintoloiden ruokalistat kirjoittamalla !murkinat nimi (esim !murkinat Ict)")
        self.send_irc("Muut komennot:")
        self.send_irc("!murkinat lista : Listaa avoimet ravintolat")
        self.send_irc("!murkinat random : Ehdottaa satunnaista avoinna olevaa ravintolaa")
        self.send_irc("!murkinat ict delica mikro: Listaa max 5 ravintolaa")

    def return_random_restaurant(self, restaurant_container):
        open_restaurants = self.return_open_restaurants(restaurant_container)
        # print open_restaurants
        random_name = self.websiteParser.get_random(open_restaurants)
        # print random_name
        self.parse_menu(restaurant_container, random_name)

    def return_wrong_name_error(self):
        self.send_irc("Oh noes! Tuntematon ravintola")

    def load_murkinat_html(self):
        return self.websiteParser.parse_website('http://murkinat.appspot.com')

    def return_open_restaurants(self, restaurant_container):
        return self.websiteParser.parse_class_from_soup_item(restaurant_container, "h3", "restaurantName")

    def list_restaurants(self, restaurants):
        output = "Avoimet ravintolat: "
        for name in restaurants:
            if name != restaurants[len(restaurants)-1]:
                output += "%s, " %(name)
            else:
                output += name
        return output

    def parse_menu(self, restaurant_container, restaurant_name):
        errors = open('errors.txt', 'w')
        for restaurant in restaurant_container:
            names = restaurant.find('h3', class_="restaurantName")
            for name in names.stripped_strings:
                try:
                    # print restaurant_name
                    # print name
                    restaurant_name = self.websiteParser.to_unicode(restaurant_name)
                    if u"\u00A0" in name:
                        name = name.replace(u"\u00A0", " ")    
                    # for c in name:
                    #         print ord(c)
                    # print ""
                    # for c in restaurant_name:
                    #         print ord(c)
                    if name == restaurant_name:

                        self.send_irc(name)
                        
                        meals = restaurant.find_all('table', class_="meals")


                        for meal in meals:
                            mealNames = meal.find_all('td', class_="mealName")
                            for mealName in mealNames:
                            
                                    for m in mealName.stripped_strings:
                                        self.send_irc(m)
                        return True #Success

                except UnicodeEncodeError as err:
                    print 'Error'
                    errors.write("Error")
        return False #Fail


        ###### IRC and logging methods######
    def send_irc(self, message):
        # print message
        self.irc_connection.sendWithDelay('PRIVMSG %s :%s' % (self.irc_line[2], message.encode('utf-8')))

    def log(self, line):
        with open("log.txt", 'a') as f:
            if len(self.irc_line) > 4:
                f.write("%s@%s: %s\r\n" %(str(datetime.now()),self.irc_line[0], self.irc_line[4]))
            else:
              f.write("%s: empty" %(self.irc_line[2]))

    def received_empty_command(self):
        self.send_irc("Tyhjä komento")


    def encode(self,encodable_text):
        # if '\xc3\xa4' in encodable_text.encode('utf-8'):
        #     print "khyl"
        #     return encodable_text.encode('utf-8').replace('\xc3\xa4', 'ä')
        if u'c2a0' in encodable_text:
            print "encoding "
            return encodable_text.replace('c2a0'.decode('hex'), ' ')
        return encodable_text

        # TODO 
    def remove_duplicates(self, item_list):
        for i in range(0,len(item_list)-1):
            for j in range(0, len(item_list)-1):
                pass
                # if i != j and item_list[i] == item_list[j]:
                #     print item_list[i]



class WebsiteParser:

    def __init__(self):
        pass

        #####BeautifulSoup helper methods########
    def parse_website(self, url):
        return urllib2.urlopen(url).read()

        # Returns BeautifulSoup item instances as an array. Class e.g "restaurant"
    def parse_div_class_from(self, html_form, class_name):
        return self.parse_class_from(html_form, 'div', class_name)
        # soup = BeautifulSoup(html_form, "html.parser")
        # #For example: restaurants = soup.find_all('div', class_="restaurant")
        # return soup.find_all('div', class_ = class_name)    

    def parse_class_from(self, html_form, element, class_name):
        soup = BeautifulSoup(html_form, "html.parser")
        #For example: restaurants = soup.find_all('div', class_="restaurant")
        return soup.find_all(element, class_ = class_name)

    def parse_all_elements(self, html_form, element_type):
        soup = BeautifulSoup(html_form, "html.parser")
        #For example: restaurants = soup.find_all('div', class_="restaurant")
        # for raw_item in soup.find_all(element_type):
        return soup.find_all(element_type)

        # Returns array of parsed Strings from html elments: element_type with class: class_name 
    def parse_class_from_soup_item(self, soup_item_array, element_type, class_name):
        parsed_items = []
        for parent_item in soup_item_array:
            raw_item = parent_item.find(element_type, class_ = class_name)
            for stripped_item in raw_item.stripped_strings:
                # stripped_item = self.to_unicode(stripped_item)
                parsed_items.append(stripped_item)
        return parsed_items


        ####Helper methods######
    def get_stripped_strings(self, soup_result_set):
        stripped_array = []
        for raw_item in soup_result_set:
            for item in raw_item.stripped_strings:
                stripped_array.append(item) 
        return stripped_array
        # return soup_result_set.stripped_strings
        # for stripped_result in soup_result_set:
            # print stripped_result.string

    def to_unicode(self,obj, encoding='utf-8'):
        if isinstance(obj, basestring):
            if not isinstance(obj, unicode):
                obj = unicode(obj, encoding)
        return obj

    def get_random(self,restaurants):
        rnd = random.randint(0,len(restaurants)-1)
        # print "%s length: %s" % (rnd, len(restaurants))
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
            message = 'Kirjoita vielä nimesi'
            irc.send( 'PRIVMSG %s :%s' % ( line[2], message))

class Jokes:

    def main(self, irc, line):
        self.websiteParser = WebsiteParser()
        self.irc_connection = irc
        self.irc_line = line
        if len(line) >= 5 and line[4] == "digit":  
            self.tell_digit_joke()
        else:   
            self.tell_joke()

    def tell_joke(self):
        rnd = random.randint(0,4)
        url = "http://www.gotlines.com/jokes/%d" % rnd
        # print url
        joke_site = self.websiteParser.parse_website(url)
        joke_containers = self.websiteParser.parse_div_class_from(joke_site, "line_box_text")
        jokes = self.websiteParser.parse_class_from_soup_item(joke_containers, "a", "linetext")
        joke = jokes[0]
        joke = self.websiteParser.get_random(jokes)
        self.send_irc(joke)  

    def tell_digit_joke(self):
        url = "http://wiki.digit.fi/Vitsiarkisto"
        joke_site = self.websiteParser.parse_website(url)
        joke_containers = self.websiteParser.parse_all_elements(joke_site, "p")
        jokes = self.websiteParser.get_stripped_strings(joke_containers)
        
        joke = ""
        # Site has few short lines or random characters so filter those out
        index = 0;
        while len(joke) < 5:
            joke = self.websiteParser.get_random(jokes)
        self.send_irc(joke)

    def send_irc(self, message):
        # print message
        self.irc_connection.sendWithDelay('PRIVMSG %s :%s' % (self.irc_line[2], message.encode('utf-8')))





command_dict[ ':!murkinat' ] = Murkinat()

command_dict[ ':!juhannusnimi' ] = JuhannusKeneraattori()

command_dict[ ':!vitshumor' ] = Jokes()

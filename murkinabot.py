# -*- coding: utf-8 -*-

"""
yksinkertainen ircbotti

komennot:
    !test
    !join
    !quit
    !anagram
    !murkinat
    !juhannusnimi
"""

import socket
import botcommands
from time import sleep


class Ircbot:

    def __init__(self ):

        # määritellään botille pääkäyttäjät

        self.users = [ ':samies!sakrnie@linux.utu.fi' ]

        # välttämättömiä tietoja

        self.server = 'irc.utu.fi'
        self.port = 6667
        self.username = 'murkis'
        self.realname = 'Murkinabotti'
        self.nick = 'murkinabot'

        # luodaan socket

        self.socket   = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # haetaan botille komennot

        self.commands = botcommands.command_dict

        # päälooppia toistettan kunnes done = 1

        self.done     = 0

        # kanava jolle botti halutaan
        self.channel  = '#trcfood'
        # self.channel  = '#murkinatesti'

    def send( self, string ):

        # tällä lähetetään viestejä

        self.socket.send( string + '\n' )

    def sendWithDelay( self, string):
        self.socket.send(string + '\n')
        sleep(0.3)

    def connect( self ):

        # yhdistetään serveriin ja läheteään omat tiedot

        self.socket.connect((self.server, self.port))
        self.send( 'NICK %s' % self.nick)
        self.send( 'USER %s a a :%s' % (self.username, self.realname))

        # liitytään kanavalle

        self.send( 'JOIN %s' % self.channel )

    def check( self, line ):

        print line
        line = line.split(' ')

        # vastataan pingiin muuten serveri katkaisee yhteyden

        if line[0] == 'PING':

             self.send( 'PONG :abc' )

        try:

            # vastataan komentoihin myös yksityiskeskutelussa

            if line[2][0] != '#':

                line[2] = line[0].split( '!' )[0][1:]

            # suoritetaan komennot jos niitä on tullut

            # line form :samies!sakrnie@linux.utu.fi PRIVMSG #murkinatesti :!murkinat ict
            # f = open('requests.txt', 'w')
            # kirjoitetaan tiedostoon kuka teki kyselyn ja millä parametrilla
            # f.write("%s: %s" %(line[1],line[2]))

            self.commands[ line[3] ].main( self , line )

        except:
            pass

    def testing(self):

        # Testaa seuraavia komentoja 
        # self.commands[":!murkinat"].main(self, ['a', 'b', 'c', 'd','Tottis', 'ict', 'perse', 'ict', 'mikro', 'maccis'])
        # self.commands[":!juhannisnimi"].main(self, ['a', 'b', 'c', 'd','Sami'])
        self.commands[":!vitshumor"].main(self, ['a', 'b', 'c', 'd','digit'])

    def mainloop( self ):

        buffer = ''

        while not self.done:

        # vastaanotetaan dataa

            buffer += self.socket.recv( 4096 )
            buffer = buffer.split( '\r\n' )

            for line in buffer[0:-1]:

                self.check( line )

            buffer = buffer[-1]

def main():

    irc = Ircbot()
    irc.connect()
    irc.mainloop()
    # irc.testing()

if __name__ == '__main__' : main()

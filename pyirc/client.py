from _socket import socket, AF_INET, SOCK_STREAM, SHUT_RDWR
import re
import threading
import logging
from Queue import Queue
import random, string
import replies
import sys, os

"""
IRC String Regex used for easily deciphering received messages.
Source:
https://mybuddymichael.com/writings/a-regular-expression-for-irc-messages.html
"""
_irc_re_string = "^(?:[:](\S+) )?(\S+)(?: (?!:)(.+?))?(?: [:](.+))?$"
_irc_regex = re.compile(_irc_re_string)

class Client():
    """
    pyIrc - Client
    
    Author:
        Theodoros Kyriazidis
    
    Description:
        Establishes a connection to the specified server
        and starts two threads: One that reads server output
        and one that reads user input and sends it to the server.
        
    Args:
        host (str): The hostname of the IRC Server. (default = "irc.freenode.net")
        port (int): The port number where the host listens for TCP connections. (default = 6667)
        nick (str): The nickname of the user. (default = "pyIrcNick")
        user (str): The username of the user. (default = "pyIrcUser")
        ident (str): The IDENT of the user. (default = "pyIrcIdent")
        realname (str, optional): The Real Name of the user (default = "...")
        print_raw_lines (int, optional): If set to 1, the client will not format the incoming server messages.
    """
    def __init__(self,
                 host = "irc.freenode.net",
                 port = 6667,
                 nick = "pyIrcNickName",
                 user = "pyIrcUser",
                 ident = "pyIrcIdent",
                 realname = "pyIrcRealName",
                 print_raw_lines = 0):
        
        self.read_buffer = ""
        if print_raw_lines == 1:
            print 'Raw Lines Mode is Enabled.'
        
        # Randomize the nickname to avoid nickname collisions on multiple instances of pyIrc with default nick
        if nick == "pyIrcNickName":
            nick = nick + self.randomword(5)
        
        # Initialize Connection
        self.connection = Connection()
        self.connection.connect(host, port)
        
        # Send NICK and USER commands to register
        self.connection.msg_nick([nick])
        self.connection.msg_user([user, ' 0 * ', realname])
        
        """ Uncomment these to test auto-joining a channel and sending a message. """
        #self.connection.msg_join(["#diktya"])
        #self.connection.msg_privmsg(["#diktya", "Automated"])
        
        # Initialize User Input Queue
        self.user_input = Queue()
        
        # Get whether user used print_raw_lines
        self.print_raw_lines = print_raw_lines
        
        # Start Thread that reads incoming messages
        self.readMsgThread = threading.Thread(target=self.read_from_socket)
        self.readMsgThread.start()
        
        # Start Thread that reads user input and sends it to the server
        self.readUserInputThread = threading.Thread(target=self.read_user_input(), args=(self.user_input,))
        self.readUserInputThread.start()

    # Returns a random word. Used for pyIrcNickName collisions only.
    def randomword(self, length):
        return ''.join(random.choice(string.lowercase) for i in range(length)) 
    
    def read_from_socket(self):
        print 'Started TCP socket listening...'
        """While this function is running, the client prints the server output to stdout."""
        #Do this forever:
        while 1:
            # Read 1024 bytes from the socket into read buffer
            self.read_buffer = self.read_buffer + self.connection.buffer_receive()
            # Split readbuffer into list by newline
            temp=self.read_buffer.split("\n")
            # Take the first entry in the readbuffer stack 
            self.read_buffer=temp.pop( )
        
            # Remove \r and split the line by character
            for line in temp:
                logging.info(line)
                if self.print_raw_lines == 0:
                    self.connection.parse_command(line)
                else:
                    print line
            
    def read_user_input(self):
        # Starts a thread that creates the Console
        self.consoleThread = threading.Thread(target=self.console, args=(self.user_input,))
        self.consoleThread.start()
        while 1:
            # Receive actions from the queue
            cmd = self.user_input.get()
            command = cmd.split(" ")[0]
            # Commands start with "/"
            if command.startswith("/"):
                # Remove / and keep the rest of the command
                command = command[1:]
                #Lowercase
                commandL = command.lower()
                # Find command and call action with params!
                if commandL in self.connection.msg_dict:
                    action = self.connection.msg_dict[commandL]
                    params = cmd.split(" ")[1:]
                    action(self.connection, params)
                else:
                    print 'Unknown command /' + command
            else:
                print 'Unknown command ' + command
            
    # Console
    def console(self, q):
        while 1:
            try:
                cmd = raw_input('')
                q.put(cmd)
                if cmd == '/forcequit':
                    self.connection.disconnect()
                    os._exit()
            except EOFError:
                break
                           
class Connection():
    """
    pyIrc - connection
    
    Author:
        Theodoros Kyriazidis
    
    Description:
        A class that contains a reference to the IRC Socket.
        
    Args:
        <none>
    """
    def __init__(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        print 'Socket created.'

    def connect(self, host, port):
        # socket.connect requires a tuple data structure
        self.sock.connect((host, port))
        print 'Attempting connection to ' + host + ":" + str(port)
        self.host = host
        self.port = port
        
    def send_string(self, string):
        """
        As specified in:
            RFC 2812
            Internet Relay Chat: Client Protocol
            Section 2.3 (page 6):
            
            IRC messages are always lines of characters terminated with a CR-LF
            (Carriage Return - Line Feed) pair, and these messages SHALL NOT
            exceed 512 characters in length, counting all characters including
            the trailing CR-LF.
        """
        # Remove all user-added \r\n (CR-LF) characters
        string.strip("\r")
        string.strip("\n")
        
        # Keep this to print it later
        strippedStr = string
        
        # Re-add \r\n (CR-LF) to the message
        string = string + "\r\n"
        
        # These messages SHALL NOT exceed 512 characters in length, counting all characters including the trailing CR-LF
        if len(string)>512:
            print "Message is too long and cannot be sent to the server."
        else:
            self.sock.send(string)
            print 'Sending to ' + self.host + ':' + str(self.port) + ' : ' + strippedStr
        
    def buffer_receive(self):
        # Receive max number of bytes!
        return self.sock.recv(1024)
    
    def parse_command(self, line):
        line = line.strip("\r\n")
        
        # Match Line to Regex
        group = _irc_regex.match(line).group
        
        # Assign matched strings to parameters
        sender = str(group(1))
        command = str(group(2))
        receiver = str(group(3))
        message = str(group(4))
        
        command_lower = command.lower()
        
        # Find appropriate event / reply / error or default
        if command_lower in replies.event_dict:
            action = replies.event_dict[command_lower]
            print action(sender, receiver, message)
        elif command_lower in replies.reply_dict:
            action = replies.reply_dict[command_lower]
            print action(sender, receiver, message)
        elif command_lower in replies.error_dict:
            action = replies.error_dict[command_lower]
            print action(sender, receiver, message)
        else:
            action = replies.on_default
            print action(command, sender, receiver, message)

        # Send automatic PONG response if the server PINGs us.
        if command == 'PING':
            self.msg_pong([message])

    def disconnect(self):
        self.sock.shutdown(SHUT_RDWR)
        self.sock.close()
        
    
    """Messages
    As specified in:
        RFC 2812
        Internet Relay Chat: Client Protocol
        Section 3 ('Messages')
        https://tools.ietf.org/html/rfc2812#section-3
    """
    
    """Connection Registration Messages
    As specified in:
        RFC 2812
        Internet Relay Chat: Client Protocol
        Section 3.1 ('Messages' / 'Connection Registration')
        https://tools.ietf.org/html/rfc2812#section-3.1
    """
    
    def msg_pass(self, params):
        """" Usage: PASS <password>
        Must be used before the USER command. """
        params_req = 1
        if len(params) > params_req:
            print 'Too many parameters for command PASS'
        elif len(params) < params_req:
            print 'Too few parameters for command PASS'
        else:
            self.send_string("PASS " + params[0])
        
    def msg_nick(self, params):
        """" Usage: NICK <nickname> """
        params_req = 1
        if len(params) > params_req:
            print 'Too many parameters for command NICK'
        elif len(params) < params_req:
            print 'Too few parameters for command NICK'
        else:
            self.send_string("NICK " + params[0])
        
    def msg_user(self, params):
        """" Usage: USER <user> <mode> <unused> :<realname> 
        <mode> is a numeric bitmask for the user's mode.
        e.g. Using a <mode> of '0 *' makes the user visible to users
        that aren't in the same channel as the user."""
        params_req = 3
        if len(params) > params_req:
            print 'Too many parameters for command USER'
        elif len(params) < params_req:
            print 'Too few parameters for command USER'
        else:
            self.send_string("USER " + params[0] + " " + params[1] + " :" + params[2])
        
    def msg_oper(self, params):
        """" Usage: OPER <name> <password> """
        params_req = 2
        if len(params) > params_req:
            print 'Too many parameters for command OPER'
        elif len(params) < params_req:
            print 'Too few parameters for command OPER'
        else:
            self.send_string("OPER " + params[0] + " " + params[1])
    
    def msg_mode(self, params):
        """" Usage: MODE <name> <( "+" / "-" ) ("i" / "w" / "o" / "O" / "r" )> """
        params_req = 2
        if len(params) > params_req:
            print 'Too many parameters for command MODE'
        elif len(params) < params_req:
            print 'Too few parameters for command MODE'
        else:
            self.send_string("MODE " + params[0] + " " + params[1])
        
    def msg_service(self, params):
        """" Usage: SERVICE <nickname> <reserved> <distribution> <type> <reserved> :<info> """
        params_req = 4
        if len(params) > params_req:
            print 'Too many parameters for command SERVICE'
        elif len(params) < params_req:
            print 'Too few parameters for command SERVICE'
        else:
            self.send_string("SERVICE " + params[0] + " " + params[1] + " " + params[2] + " :" + params[3])
        
    def msg_quit(self, params):
        """" Usage: QUIT :<quit message> """
        quit_message = " ".join(params)
        self.send_string("QUIT :" + quit_message)
    
    def msg_squit(self, params):
        """" Usage: SQUIT <server> :<comment>
        Terminates a Server with the <comment> parameter as its QUIT message.
        """
        params_req = 2
        if len(params) < params_req:
            print 'Too few parameters for command SQUIT'
        else:
            server_name = params[0]
            quit_message = " ".join(params[1:])
            self.send_string("SQUIT " + server_name + " :" +  quit_message)
    
    """Channel operations
    As specified in:
        RFC 2812
        Internet Relay Chat: Client Protocol
        Section 3.2 ('Messages' / 'Channel operations')
        https://tools.ietf.org/html/rfc2812#section-3.2
    """
    
    def msg_join(self, params):
        """ Usage: JOIN ( <target_channel> *( "," <target_channel> ) [ <key> *( "," <key> ) ] ) / "0"
            Channel Key defaults to blank.
        """
        params_min = 1
        params_max = 2
        if len(params) > params_max:
            print 'Too many parameters for command JOIN'
        elif len(params) < params_min:
            print 'Too few parameters for command JOIN'
        else:
            if len(params) == 1:
                self.send_string("JOIN " + params[0])
            else:
                self.send_string("JOIN " + params[0] + " " + params[1])
    
    def msg_part(self, params):
        """ Usage: <target_channel> *( "," <target_channel> ) [ <Part Message> ]"""
        params_min = 1
        if len(params) < params_min:
            print 'Too few parameters for command PART'
        else:
            if len(params) == 1:
                self.send_string("PART " + params[0])
            else:
                self.send_string("PART " + params[0] + " :" + " ".join(params[1:]))
            
    # Channel MODE command has been already defined in msg_mode
    
    def msg_topic(self, params):
        """ Usage: <channel> [ <topic> ]
            If change_topic is set to other than zero, the topic is changed.
            An empty new_topic clears the topic of the target channel.
        """
        params_min = 1
        if len(params) < params_min:
            print 'Too few parameters for command TOPIC'
        else:
            if len(params) == 1:
                self.send_string("TOPIC " + params[0])
            else:
                self.send_string("TOPIC " + params[0] + " :" + params[1])
            
    def msg_names(self, params):
        """ Usage: [ <channel> *( "," <channel> ) [ <target> ] ] """       
        params_min = 1
        params_max = 2
        if len(params) > params_max:
            print 'Too many parameters for command NAMES'
        elif len(params) < params_min:
            print 'Too few parameters for command NAMES'
        else:
            if len(params) == 1:
                self.send_string("NAMES " + params[0])
            else:
                self.send_string("NAMES " + params[0] + " " + params[1])
        
    def msg_list(self, params):
        """ Usage: [ <channel> *( "," <channel> ) [ <target> ] ] """       
        params_min = 1
        params_max = 2
        if len(params) > params_max:
            print 'Too many parameters for command LIST'
        elif len(params) < params_min:
            print 'Too few parameters for command LIST'
        else:
            if len(params) == 1:
                self.send_string("LIST " + params[0])
            else:
                self.send_string("LIST " + params[0] + " " + params[1])
        
    def msg_invite(self, params):
        params_req = 2
        if len(params) > params_req:
            print 'Too many parameters for command INVITE'
        elif len(params) < params_req:
            print 'Too few parameters for command INVITE'
        else:
            self.send_string("INVITE " + params[0] + " " + params[1])
        
    def msg_kick(self, params):
        params_min = 2
        if len(params) < params_min:
            print 'Too few parameters for command KICK'
        else:
            if len(params) == 2:
                self.send_string("KICK " + params[0] + " " + params[1])
            else:
                self.send_string("KICK " + params[0] + " " + params[1] + " :" + params[2:])
        
    """Sending messages
    As specified in:
        RFC 2812
        Internet Relay Chat: Client Protocol
        Section 3.3 ('Messages' / 'Sending messages')
        https://tools.ietf.org/html/rfc2812#section-3.3
    """    
    
    def msg_privmsg(self, params):
        """Usage: PRIVMSG <msgtarget> <text to be sent>"""
        params_min = 2
        if len(params) < params_min:
            print 'Too few parameters for command PRIVMSG'
        else:
            self.send_string("PRIVMSG " + params[0] + " :" + " ".join(params[1:]))
     
    def msg_notice(self, params):
        """Usage: NOTICE <msgtarget> <text to be sent>"""
        params_min = 2
        if len(params) < params_min:
            print 'Too few parameters for command NOTICE'
        else:
            self.send_string("NOTICE " + params[0] + " :" + " ".join(params[1:]))
        
    """Server queries and commands
    As specified in:
        RFC 2812
        Internet Relay Chat: Client Protocol
        Section 3.4 ('Messages' / 'Server queries and commands')
        https://tools.ietf.org/html/rfc2812#section-3.4
    """
    
    def msg_motd(self, params):
        """Usage: MOTD [ <target> ] """
        if len(params)<=0:
            self.send_string("MOTD")
        elif len(params)==1:
            self.send_string("MOTD " + params[0])
        else:
            print 'Too many parameters for command MOTD'
            
    def msg_lusers(self, params):
        """Usage: LUSERS [ <mask> [ <target> ] ] """
        if len(params)<=0:
            self.send_string("LUSERS")
        elif len(params)==1:
            self.send_string("LUSERS " + params[0])
        elif len(params)==2:
            self.send_string("LUSERS " + params[0] + " " + params[1])
        else:
            print 'Too many parameters for command LUSERS'
        
    def msg_version(self, params):
        """Usage: VERSION [ <target> ] """
        if len(params)<=0:
            self.send_string("VERSION")
        elif len(params)==1:
            self.send_string("VERSION " + params[0])
        else:
            print 'Too many parameters for command VERSION'
        
    def msg_stats(self, params):
        """Usage: STATS [ <query> [ <target> ] ] """
        if len(params)<=0:
            self.send_string("STATS")
        elif len(params)==1:
            self.send_string("STATS " + params[0])
        elif len(params)==2:
            self.send_string("STATS " + params[0] + " " + params[1])
        else:
            print 'Too many parameters for command LUSERS'
      
    def msg_links(self, params):    
        """Usage: LINKS [ [ <remote server> ] <server mask> ] """
        if len(params)<=0:
            self.send_string("LINKS")
        elif len(params)==1:
            self.send_string("LINKS " + params[0])
        elif len(params)==2:
            self.send_string("LINKS " + params[0] + " " + params[1])
        else:
            print 'Too many parameters for command LINKS'
        
    def msg_time(self, params):
        """Usage: TIME [ <target> ] """
        if len(params)<=0:
            self.send_string("TIME")
        elif len(params)==1:
            self.send_string("TIME " + params[0])
        else:
            print 'Too many parameters for command TIME'
        
    def msg_connect(self, params):
        """Usage: CONNECT <target server> <port> [ <remote server> ]"""
        params_min = 2
        params_max = 3
        if len(params) > params_max:
            print 'Too many parameters for command JOIN'
        elif len(params) < params_min:
            print 'Too few parameters for command JOIN'
        else:
            if len(params) == 2:
                self.send_string("CONNECT " + params[0] + " " + params[1])
            else:
                self.send_string("CONNECT " + params[0] + " " + params[1] + " " + params[2])
        
    def msg_trace(self, params):
        """Usage: TRACE [ <target> ] """
        if len(params)<=0:
            self.send_string("TRACE")
        elif len(params)==1:
            self.send_string("TRACE " + params[0])
        else:
            print 'Too many parameters for command TRACE'
    
    def msg_admin(self, params):
        """Usage: ADMIN [ <target> ] """
        if len(params)<=0:
            self.send_string("ADMIN")
        elif len(params)==1:
            self.send_string("ADMIN " + params[0])
        else:
            print 'Too many parameters for command ADMIN'
    
    def msg_info(self, params):
        """Usage: INFO [ <target> ] """
        if len(params)<=0:
            self.send_string("INFO")
        elif len(params)==1:
            self.send_string("INFO " + params[0])
        else:
            print 'Too many parameters for command INFO'
    
    """Service Query and Commands
    As specified in:
        RFC 2812
        Internet Relay Chat: Client Protocol
        Section 3.5 ('Messages' / 'Service Query and Commands')
        https://tools.ietf.org/html/rfc2812#section-3.5
    """
    
    def msg_servlist(self, params):
        """Usage: [ <mask> [ <type> ] ] """
        if len(params)<=0:
            self.send_string("SERVLIST")
        elif len(params)==1:
            self.send_string("SERVLIST " + params[0])
        elif len(params)==2:
            self.send_string("SERVLIST " + params[0] + " " + params[1])
        else:
            print 'Too many parameters for command SERVLIST'
        
    def msg_squery(self, params):
        """Usage: <servicename> <text> """
        params_min = 2
        if len(params) < params_min:
            print 'Too few parameters for command PRIVMSG'
        else:
            self.send_string("SQUERY " + params[0] + " :" + " ".join(params[1:]))
    
    """User based queries
    As specified in:
        RFC 2812
        Internet Relay Chat: Client Protocol
        Section 3.6 ('Messages' / 'User based queries')
        https://tools.ietf.org/html/rfc2812#section-3.6
    """   
      
    def msg_who(self, params):
        """ Usage: WHO [ <mask> [ "o" ] ]
        If the user writes anything as a second parameter it is interpreted as an 'o'. """
        if len(params)<=0:
            self.send_string("WHO")
        elif len(params)==1:
            self.send_string("WHO " + params[0])
        elif len(params)==2:
            self.send_string("WHO " + params[0] + " o ")
        else:
            print 'Too many parameters for command WHO'
            
    def msg_whois(self, params):
        """ Usage: WHOIS [ <target> ] <mask> *( "," <mask> ) """
        if len(params)<=0:
            print 'Too few parameters for command WHOIS'
        elif len(params)==1:
            self.send_string("WHOIS " + params[0])
        elif len(params)==2:
            self.send_string("WHOIS " + params[0] + " " + params[1])
        else:
            print 'Too many parameters for command WHOIS'
        
    def msg_whowas(self, params):
        """ Usage: WHOWAS <nickname> *( "," <nickname> ) [ <count> [ <target> ] ] """
        if len(params)<=0:
            print 'Too few parameters for command WHOWAS'
        elif len(params)==1:
            self.send_string("WHOWAS " + params[0])
        elif len(params)==2:
            self.send_string("WHOWAS " + params[0] + " " + params[1])
        elif len(params)==3:
            self.send_string("WHOWAS " + params[0] + " " + params[1] + " " + params[2])
        else:
            print 'Too many parameters for command WHOWAS'
    
    """Miscellaneous messages
    As specified in:
        RFC 2812
        Internet Relay Chat: Client Protocol
        Section 3.7 ('Messages' / 'Miscellaneous messages')
        https://tools.ietf.org/html/rfc2812#section-3.7
    """   
       
    def msg_kill(self, params):
        """Usage: <nickname> <comment>"""
        params_min = 2
        if len(params) < params_min:
            print 'Too few parameters for command KILL'
        else:
            self.send_string("KILL " + params[0] + " :" + " ".join(params[1:]))
        
    def msg_ping(self, params):
        """Usage: <server 1> [ <server 2> ]"""
        if len(params)<=0:
            print 'Too few parameters for command PING'
        elif len(params)==1:
            self.send_string("PING " + params[0])
        elif len(params)==2:
            self.send_string("PING " + params[0] + " " + params[1])
        else:
            print 'Too many parameters for command PING'
        
    def msg_pong(self, params):
        """Usage: <server 1> [ <server 2> ]"""
        if len(params)<=0:
            print 'Too few parameters for command PONG'
        elif len(params)==1:
            self.send_string("PONG " + params[0])
        elif len(params)==2:
            self.send_string("PONG " + params[0] + " " + params[1])
        else:
            print 'Too many parameters for command PONG'
        
    def msg_error(self, params):
        self.send_string("ERROR :" + " ".join(params))
        
    # Dict to associate user commands with functions
    msg_dict = {    'pass': msg_pass,
                    'nick': msg_nick,
                    'user': msg_user,
                    'oper': msg_oper,
                    'mode': msg_mode,
                    'service': msg_service,
                    'quit': msg_quit,
                    'squit': msg_squit,
                    'join': msg_join,
                    'part': msg_part,
                    'topic': msg_topic,
                    'names': msg_names,
                    'list': msg_list,
                    'invite': msg_invite,
                    'kick': msg_kick,
                    'privmsg': msg_privmsg,
                    'notice': msg_notice,
                    'motd': msg_motd,
                    'lusers': msg_lusers,
                    'version': msg_version,
                    'stats': msg_stats,
                    'links': msg_links,
                    'time': msg_time,
                    'connect': msg_connect,
                    'trace': msg_trace,
                    'admin': msg_admin,
                    'info': msg_info,
                    'servlist': msg_servlist,
                    'squery': msg_squery,
                    'who': msg_who,
                    'whois': msg_whois,
                    'whowas': msg_whowas,
                    'kill': msg_kill,
                    'ping': msg_ping,
                    'pong': msg_pong,
                    'error': msg_error}
        
import argparse
import client
from threading import Thread

# Argument parser! Python magic.
parser = argparse.ArgumentParser()

# Optional arguments to specify a different server, port, nickname etc.
parser.add_argument("-server", metavar='<address>', type=str, help="The IP or Host Address of the Server.", default='irc.freenode.net')
parser.add_argument("-port", metavar='<host port>', type=int, help="The port of the Server that is running an IRC Server", default=6667)
parser.add_argument("-nick", metavar='<nickname>', type=str, help="The nickname with which to connect.", default='pyIrcNickName')
parser.add_argument("-username", metavar='<username>', type=str, help="The username with which to connect.", default='pyIrcUser')
parser.add_argument("-ident", metavar='<ident>', type=str, help="The identity with which to connect.", default='pyIrcIdent')
parser.add_argument("-realname", metavar='<name>', type=str, help="The Real Name with which to connect.", default='pyIrcRealName')

parser.add_argument("-r", "--raw", help="Print raw lines as they are received from server (no formatting)", action="store_true")

args = parser.parse_args()
print "Initializing Client..."
__client = client.Client(host=args.server, port=args.port, nick=args.nick, user=args.username, ident=args.ident, realname=args.realname, print_raw_lines=int(args.raw))

from Queue import Queue
import logging

"""
    pyIrc - Replies
    
    Author:
        Theodoros Kyriazidis
    
    Description:
        A module that contains all replies that can be received by the client.
"""

def on_default(command, sender, receipient, message):
    return "[" + command + "] from <" + sender + "> to " + receipient + ": " +  message

def on_join(sender, receipient, message):
    return sender + " has joined " + receipient
    
def on_privmsg(sender, receipient, message):
    return "<" + sender + "> says to " + receipient + " : " + message
    
def on_error(sender, receipient, message):
    return 'Error from ' + sender + " to " + receipient + ": " + message
    
def on_notice(sender, receipient, message):
    return '[NOTICE] <' + sender + "> : " + message
    
def on_kick(sender, receipient, message):
    return on_default('KICK', sender,receipient,message)
    
def on_mode(sender, receipient, message):
    return on_default('MODE', sender,receipient,message)
    
def on_part(sender, receipient, message):
    return on_default('PART', sender,receipient,message)
    
def on_ping(sender, receipient, message):
    return on_default('PING', sender,receipient,message)
    
def on_quit(sender, receipient, message):
    return on_default('QUIT', sender,receipient,message)
    
def on_invite(sender, receipient, message):
    return on_default('INVITE', sender,receipient,message)
    
def on_pong(sender, receipient, message):
    return on_default('PONG', sender,receipient,message)
    
def on_topic(sender, receipient, message):
    return on_default('TOPIC', sender,receipient,message)
    
def on_nick(sender, receipient, message):
    return on_default('NICK',sender,receipient,message)
    
event_dict = { 
            'join': on_join,
            'privmsg': on_privmsg,
            'error': on_error,
            'notice': on_notice,
            'kick': on_kick,
            'mode': on_mode,
            'part': on_part,
            'ping': on_ping,
            'quit': on_quit,
            'invite': on_invite,
            'pong': on_pong,
            'topic': on_topic,
            'nick': on_nick
            }

"""Replies
    As specified in:
        RFC 2812
        Internet Relay Chat: Client Protocol
        Section 5 ('Replies')
        https://tools.ietf.org/html/rfc2812#section-5
    """
    
"""Command responses
    As specified in:
        RFC 2812
        Internet Relay Chat: Client Protocol
        Section 5.1 ('Replies' / 'Command responses')
        https://tools.ietf.org/html/rfc2812#section-5.1
"""

def RPL_WELCOME(sender, receipient, message):
    """ Reply Code 001 """
    return on_default('RPL_WELCOME', sender, receipient, message)
    #return "<" + sender + ">: " + message
    
def RPL_YOURHOST(sender, receipient, message):
    """ Reply Code 002 """
    return on_default('RPL_YOURHOST', sender, receipient, message)
    #return "<" + sender + ">: " + message
    
def RPL_CREATED(sender, receipient, message):
    """ Reply Code 003 """
    return on_default('RPL_CREATED', sender, receipient, message)
   # return "<" + sender + ">: " + message
    
def RPL_MYINFO(sender, receipient, message):
    """ Reply Code 004 """
    return on_default('RPL_MYINFO', sender, receipient, message)
    return "<" + sender + ">: " + message

def RPL_BOUNCE(sender, receipient, message):
    """ Reply Code 005 """
    return on_default('RPL_BOUNCE', sender, receipient, message)
    return "<" + sender + ">: " + message

def RPL_USERHOST(sender, receipient, message):
    """ Reply Code 302 """
    return "<" + sender + ">: " + message

def RPL_ISON(sender, receipient, message):
    """ Reply Code 303 """
    return "<" + sender + ">: " + message

def RPL_AWAY(sender, receipient, message):
    """ Reply Code 301 """
    return "<" + sender + ">: " + message

def RPL_UNAWAY(sender, receipient, message):
    """ Reply Code 305 """
    return "<" + sender + ">: " + message

def RPL_NOWAWAY(sender, receipient, message):
    """ Reply Code 306 """
    return "<" + sender + ">: " + message

def RPL_WHOISUSER(sender, receipient, message):
    """ Reply Code 311 """
    return "<" + sender + ">: " + message

def RPL_WHOISSERVER(sender, receipient, message):
    """ Reply Code 312 """
    return "<" + sender + ">: " + message

def RPL_WHOISOPERATOR(sender, receipient, message):
    """ Reply Code 313 """
    return "<" + sender + ">: " + message

def RPL_WHOISIDLE(sender, receipient, message):
    """ Reply Code 317 """
    return "<" + sender + ">: " + message

def RPL_ENDOFWHOIS(sender, receipient, message):
    """ Reply Code 318 """
    return "<" + sender + ">: " + message

def RPL_WHOISCHANNELS(sender, receipient, message):
    """ Reply Code 319 """
    return "<" + sender + ">: " + message

def RPL_WHOWASUSER(sender, receipient, message):
    """ Reply Code 314 """
    return "<" + sender + ">: " + message

def RPL_ENDOFWHOWAS(sender, receipient, message):
    """ Reply Code 369 """
    return "<" + sender + ">: " + message

def RPL_LIST(sender, receipient, message):
    """ Reply Code 322 """
    return "<" + sender + ">: " + message

def RPL_LISTEND(sender, receipient, message):
    """ Reply Code 323 """
    return "<" + sender + ">: " + message

def RPL_UNIQOPIS(sender, receipient, message):
    """ Reply Code 325 """
    return "<" + sender + ">: " + message

def RPL_CHANNELMODEIS(sender, receipient, message):
    """ Reply Code 324 """
    return "<" + sender + ">: " + message

def RPL_NOTOPIC(sender, receipient, message):
    """ Reply Code 331 """
    return "<" + sender + ">: " + message

def RPL_TOPIC(sender, receipient, message):
    """ Reply Code 332 """
    return "<" + sender + ">: " + message

def RPL_INVITING(sender, receipient, message):
    """ Reply Code 341 """
    return "<" + sender + ">: " + message

def RPL_SUMMONING(sender, receipient, message):
    """ Reply Code 342 """
    return "<" + sender + ">: " + message

def RPL_INVITELIST(sender, receipient, message):
    """ Reply Code 346 """
    return "<" + sender + ">: " + message

def RPL_ENDOFINVITELIST(sender, receipient, message):
    """ Reply Code 347 """
    return "<" + sender + ">: " + message

def RPL_EXCEPTLIST(sender, receipient, message):
    """ Reply Code 348 """
    return "<" + sender + ">: " + message

def RPL_ENDOFEXCEPTLIST(sender, receipient, message):
    """ Reply Code 349 """
    return "<" + sender + ">: " + message

def RPL_VERSION(sender, receipient, message):
    """ Reply Code 351 """
    return "<" + sender + ">: " + message

def RPL_WHOREPLY(sender, receipient, message):
    """ Reply Code 352 """
    return "<" + sender + ">: " + message

def RPL_ENDOFWHO(sender, receipient, message):
    """ Reply Code 315 """
    return "<" + sender + ">: " + message

def RPL_NAMREPLY(sender, receipient, message):
    """ Reply Code 353 """
    return "<" + sender + ">: " + message

def RPL_ENDOFNAMES(sender, receipient, message):
    """ Reply Code 366 """
    return "<" + sender + ">: " + message

def RPL_LINKS(sender, receipient, message):
    """ Reply Code 364 """
    return "<" + sender + ">: " + message

def RPL_ENDOFLINKS(sender, receipient, message):
    """ Reply Code 365 """
    return "<" + sender + ">: " + message

def RPL_BANLIST(sender, receipient, message):
    """ Reply Code 367 """
    return "<" + sender + ">: " + message

def RPL_ENDOFBANLIST(sender, receipient, message):
    """ Reply Code 368 """
    return "<" + sender + ">: " + message

def RPL_INFO(sender, receipient, message):
    """ Reply Code 371 """
    return "<" + sender + ">: " + message

def RPL_ENDOFINFO(sender, receipient, message):
    """ Reply Code 374 """
    return "<" + sender + ">: " + message

def RPL_MOTDSTART(sender, receipient, message):
    """ Reply Code 375 """
    return "<" + sender + ">: " + message

def RPL_MOTD(sender, receipient, message):
    """ Reply Code 372 """
    return "<" + sender + ">: " + message

def RPL_ENDOFMOTD(sender, receipient, message):
    """ Reply Code 376 """
    return "<" + sender + ">: " + message

def RPL_YOUREOPER(sender, receipient, message):
    """ Reply Code 381 """
    return "<" + sender + ">: " + message

def RPL_REHASHING(sender, receipient, message):
    """ Reply Code 382 """
    return "<" + sender + ">: " + message

def RPL_YOURESERVICE(sender, receipient, message):
    """ Reply Code 383 """
    return "<" + sender + ">: " + message

def RPL_TIME(sender, receipient, message):
    """ Reply Code 391 """
    return "<" + sender + ">: " + message

def RPL_USERSSTART(sender, receipient, message):
    """ Reply Code 392 """
    return "<" + sender + ">: " + message

def RPL_USERS(sender, receipient, message):
    """ Reply Code 393 """
    return "<" + sender + ">: " + message

def RPL_ENDOFUSERS(sender, receipient, message):
    """ Reply Code 394 """
    return "<" + sender + ">: " + message

def RPL_NOUSERS(sender, receipient, message):
    """ Reply Code 395 """
    return "<" + sender + ">: " + message

def RPL_TRACELINK(sender, receipient, message):
    """ Reply Code 200 """
    return "<" + sender + ">: " + message

def RPL_TRACECONNECTING(sender, receipient, message):
    """ Reply Code 201 """
    return "<" + sender + ">: " + message

def RPL_TRACEHANDSHAKE(sender, receipient, message):
    """ Reply Code 202 """
    return "<" + sender + ">: " + message

def RPL_TRACEUNKNOWN(sender, receipient, message):
    """ Reply Code 203 """
    return "<" + sender + ">: " + message

def RPL_TRACEOPERATOR(sender, receipient, message):
    """ Reply Code 204 """
    return "<" + sender + ">: " + message

def RPL_TRACEUSER(sender, receipient, message):
    """ Reply Code 205 """
    return "<" + sender + ">: " + message

def RPL_TRACESERVER(sender, receipient, message):
    """ Reply Code 206 """
    return "<" + sender + ">: " + message

def RPL_TRACESERVICE(sender, receipient, message):
    """ Reply Code 207 """
    return "<" + sender + ">: " + message

def RPL_TRACENEWTYPE(sender, receipient, message):
    """ Reply Code 208 """
    return "<" + sender + ">: " + message

def RPL_TRACECLASS(sender, receipient, message):
    """ Reply Code 209 """
    return "<" + sender + ">: " + message

def RPL_TRACERECONNECT(sender, receipient, message):
    """ Reply Code 210 """
    return "<" + sender + ">: " + message

def RPL_TRACELOG(sender, receipient, message):
    """ Reply Code 261 """
    return "<" + sender + ">: " + message

def RPL_TRACEEND(sender, receipient, message):
    """ Reply Code 262 """
    return "<" + sender + ">: " + message

def RPL_STATSLINKINFO(sender, receipient, message):
    """ Reply Code 211 """
    return "<" + sender + ">: " + message

def RPL_STATSCOMMANDS(sender, receipient, message):
    """ Reply Code 212 """
    return "<" + sender + ">: " + message

def RPL_ENDOFSTATS(sender, receipient, message):
    """ Reply Code 219 """
    return "<" + sender + ">: " + message

def RPL_STATSUPTIME(sender, receipient, message):
    """ Reply Code 242 """
    return "<" + sender + ">: " + message

def RPL_STATSOLINE(sender, receipient, message):
    """ Reply Code 243 """
    return "<" + sender + ">: " + message

def RPL_UMODEIS(sender, receipient, message):
    """ Reply Code 221 """
    return "<" + sender + ">: " + message

def RPL_SERVLIST(sender, receipient, message):
    """ Reply Code 234 """
    return "<" + sender + ">: " + message

def RPL_SERVLISTEND(sender, receipient, message):
    """ Reply Code 235 """
    return "<" + sender + ">: " + message

def RPL_LUSERCLIENT(sender, receipient, message):
    """ Reply Code 251 """
    return "<" + sender + ">: " + message

def RPL_LUSEROP(sender, receipient, message):
    """ Reply Code 252 """
    return "<" + sender + ">: " + message

def RPL_LUSERUNKNOWN(sender, receipient, message):
    """ Reply Code 253 """
    return "<" + sender + ">: " + message

def RPL_LUSERCHANNELS(sender, receipient, message):
    """ Reply Code 254 """
    return "<" + sender + ">: " + message

def RPL_LUSERME(sender, receipient, message):
    """ Reply Code 255 """
    return "<" + sender + ">: " + message

def RPL_ADMINME(sender, receipient, message):
    """ Reply Code 256 """
    return "<" + sender + ">: " + message

def RPL_ADMINLOC1(sender, receipient, message):
    """ Reply Code 257 """
    return "<" + sender + ">: " + message

def RPL_ADMINLOC2(sender, receipient, message):
    """ Reply Code 258 """
    return "<" + sender + ">: " + message

def RPL_ADMINEMAIL(sender, receipient, message):
    """ Reply Code 259 """
    return "<" + sender + ">: " + message

def RPL_TRYAGAIN(sender, receipient, message):
    """ Reply Code 263 """
    return "<" + sender + ">: " + message

reply_dict = {
            '001': RPL_WELCOME,
            '002': RPL_YOURHOST,
            '003': RPL_CREATED,
            '004': RPL_MYINFO,
            '005': RPL_BOUNCE,
            '302': RPL_USERHOST,
            '303': RPL_ISON,
            '301': RPL_AWAY,
            '305': RPL_UNAWAY,
            '306': RPL_NOWAWAY,
            '311': RPL_WHOISUSER,
            '312': RPL_WHOISSERVER,
            '313': RPL_WHOISOPERATOR,
            '317': RPL_WHOISIDLE,
            '318': RPL_ENDOFWHOIS,
            '319': RPL_WHOISCHANNELS,
            '314': RPL_WHOWASUSER,
            '369': RPL_ENDOFWHOWAS,
            '322': RPL_LIST,
            '323': RPL_LISTEND,
            '325': RPL_UNIQOPIS,
            '324': RPL_CHANNELMODEIS,
            '331': RPL_NOTOPIC,
            '332': RPL_TOPIC,
            '341': RPL_INVITING,
            '342': RPL_SUMMONING,
            '346': RPL_INVITELIST,
            '347': RPL_ENDOFINVITELIST,
            '348': RPL_EXCEPTLIST,
            '349': RPL_ENDOFEXCEPTLIST,
            '351': RPL_VERSION,
            '352': RPL_WHOREPLY,
            '315': RPL_ENDOFWHO,
            '353': RPL_NAMREPLY,
            '366': RPL_ENDOFNAMES,
            '364': RPL_LINKS,
            '365': RPL_ENDOFLINKS,
            '367': RPL_BANLIST,
            '368': RPL_ENDOFBANLIST,
            '371': RPL_INFO,
            '374': RPL_ENDOFINFO,
            '375': RPL_MOTDSTART,
            '372': RPL_MOTD,
            '376': RPL_ENDOFMOTD,
            '381': RPL_YOUREOPER,
            '382': RPL_REHASHING,
            '383': RPL_YOURESERVICE,
            '391': RPL_TIME,
            '392': RPL_USERSSTART,
            '393': RPL_USERS,
            '394': RPL_ENDOFUSERS,
            '395': RPL_NOUSERS,
            '200': RPL_TRACELINK,
            '201': RPL_TRACECONNECTING,
            '202': RPL_TRACEHANDSHAKE,
            '203': RPL_TRACEUNKNOWN,
            '204': RPL_TRACEOPERATOR,
            '205': RPL_TRACEUSER,
            '206': RPL_TRACESERVER,
            '207': RPL_TRACESERVICE,
            '208': RPL_TRACENEWTYPE,
            '209': RPL_TRACECLASS,
            '210': RPL_TRACERECONNECT,
            '261': RPL_TRACELOG,
            '262': RPL_TRACEEND,
            '211': RPL_STATSLINKINFO,
            '212': RPL_STATSCOMMANDS,
            '219': RPL_ENDOFSTATS,
            '242': RPL_STATSUPTIME,
            '243': RPL_STATSOLINE,
            '221': RPL_UMODEIS,
            '234': RPL_SERVLIST,
            '235': RPL_SERVLISTEND,
            '251': RPL_LUSERCLIENT,
            '252': RPL_LUSEROP,
            '253': RPL_LUSERUNKNOWN,
            '254': RPL_LUSERCHANNELS,
            '255': RPL_LUSERME,
            '256': RPL_ADMINME,
            '257': RPL_ADMINLOC1,
            '258': RPL_ADMINLOC2,
            '259': RPL_ADMINEMAIL,
            '263': RPL_TRYAGAIN
            }

"""Error Replies
    As specified in:
        RFC 2812
        Internet Relay Chat: Client Protocol
        Section 5.2 ('Replies' / 'Error Replies')
        https://tools.ietf.org/html/rfc2812#section-5.2
"""

def ERR_NOSUCHNICK(sender, receipient, message):
    """ Error Code 401 """
    return "ERROR from <" + sender + ">: " + message

def ERR_NOSUCHSERVER(sender, receipient, message):
    """ Error Code 402 """
    return "ERROR from <" + sender + ">: " + message

def ERR_NOSUCHCHANNEL(sender, receipient, message):
    """ Error Code 403 """
    return "ERROR from <" + sender + ">: " + message

def ERR_CANNOTSENDTOCHAN(sender, receipient, message):
    """ Error Code 404 """
    return "ERROR from <" + sender + ">: " + message

def ERR_TOOMANYCHANNELS(sender, receipient, message):
    """ Error Code 405 """
    return "ERROR from <" + sender + ">: " + message

def ERR_WASNOSUCHNICK(sender, receipient, message):
    """ Error Code 406 """
    return "ERROR from <" + sender + ">: " + message

def ERR_TOOMANYTARGETS(sender, receipient, message):
    """ Error Code 407 """
    return "ERROR from <" + sender + ">: " + message

def ERR_NOSUCHSERVICE(sender, receipient, message):
    """ Error Code 408 """
    return "ERROR from <" + sender + ">: " + message

def ERR_NOORIGIN(sender, receipient, message):
    """ Error Code 409 """
    return "ERROR from <" + sender + ">: " + message

def ERR_NORECIPIENT(sender, receipient, message):
    """ Error Code 411 """
    return "ERROR from <" + sender + ">: " + message

def ERR_NOTEXTTOSEND(sender, receipient, message):
    """ Error Code 412 """
    return "ERROR from <" + sender + ">: " + message

def ERR_NOTOPLEVEL(sender, receipient, message):
    """ Error Code 413 """
    return "ERROR from <" + sender + ">: " + message

def ERR_WILDTOPLEVEL(sender, receipient, message):
    """ Error Code 414 """
    return "ERROR from <" + sender + ">: " + message

def ERR_BADMASK(sender, receipient, message):
    """ Error Code 415 """
    return "ERROR from <" + sender + ">: " + message

def ERR_UNKNOWNCOMMAND(sender, receipient, message):
    """ Error Code 421 """
    return "ERROR from <" + sender + ">: " + message

def ERR_NOMOTD(sender, receipient, message):
    """ Error Code 422 """
    return "ERROR from <" + sender + ">: " + message

def ERR_NOADMININFO(sender, receipient, message):
    """ Error Code 423 """
    return "ERROR from <" + sender + ">: " + message

def ERR_FILEERROR(sender, receipient, message):
    """ Error Code 424 """
    return "ERROR from <" + sender + ">: " + message

def ERR_NONICKNAMEGIVEN(sender, receipient, message):
    """ Error Code 431 """
    return "ERROR from <" + sender + ">: " + message

def ERR_ERRONEUSNICKNAME(sender, receipient, message):
    """ Error Code 432 """
    return "ERROR from <" + sender + ">: " + message

def ERR_NICKNAMEINUSE(sender, receipient, message):
    """ Error Code 433 """
    return "ERROR from <" + sender + ">: " + message

def ERR_NICKCOLLISION(sender, receipient, message):
    """ Error Code 436 """
    return "ERROR from <" + sender + ">: " + message

def ERR_UNAVAILRESOURCE(sender, receipient, message):
    """ Error Code 437 """
    return "ERROR from <" + sender + ">: " + message

def ERR_USERNOTINCHANNEL(sender, receipient, message):
    """ Error Code 441 """
    return "ERROR from <" + sender + ">: " + message

def ERR_NOTONCHANNEL(sender, receipient, message):
    """ Error Code 442 """
    return "ERROR from <" + sender + ">: " + message

def ERR_USERONCHANNEL(sender, receipient, message):
    """ Error Code 443 """
    return "ERROR from <" + sender + ">: " + message

def ERR_NOLOGIN(sender, receipient, message):
    """ Error Code 444 """
    return "ERROR from <" + sender + ">: " + message

def ERR_SUMMONDISABLED(sender, receipient, message):
    """ Error Code 445 """
    return "ERROR from <" + sender + ">: " + message

def ERR_USERSDISABLED(sender, receipient, message):
    """ Error Code 446 """
    return "ERROR from <" + sender + ">: " + message

def ERR_NOTREGISTERED(sender, receipient, message):
    """ Error Code 451 """
    return "ERROR from <" + sender + ">: " + message

def ERR_NEEDMOREPARAMS(sender, receipient, message):
    """ Error Code 461 """
    return "ERROR from <" + sender + ">: " + message

def ERR_ALREADYREGISTRED(sender, receipient, message):
    """ Error Code 462 """
    return "ERROR from <" + sender + ">: " + message

def ERR_NOPERMFORHOST(sender, receipient, message):
    """ Error Code 463 """
    return "ERROR from <" + sender + ">: " + message

def ERR_PASSWDMISMATCH(sender, receipient, message):
    """ Error Code 464 """
    return "ERROR from <" + sender + ">: " + message

def ERR_YOUREBANNEDCREEP(sender, receipient, message):
    """ Error Code 465 """
    return "ERROR from <" + sender + ">: " + message

def ERR_YOUWILLBEBANNED(sender, receipient, message):
    """ Error Code 466 """
    return "ERROR from <" + sender + ">: " + message

def ERR_KEYSET(sender, receipient, message):
    """ Error Code 467 """
    return "ERROR from <" + sender + ">: " + message

def ERR_CHANNELISFULL(sender, receipient, message):
    """ Error Code 471 """
    return "ERROR from <" + sender + ">: " + message

def ERR_UNKNOWNMODE(sender, receipient, message):
    """ Error Code 472 """
    return "ERROR from <" + sender + ">: " + message

def ERR_INVITEONLYCHAN(sender, receipient, message):
    """ Error Code 473 """
    return "ERROR from <" + sender + ">: " + message

def ERR_BANNEDFROMCHAN(sender, receipient, message):
    """ Error Code 474 """
    return "ERROR from <" + sender + ">: " + message

def ERR_BADCHANNELKEY(sender, receipient, message):
    """ Error Code 475 """
    return "ERROR from <" + sender + ">: " + message

def ERR_BADCHANMASK(sender, receipient, message):
    """ Error Code 476 """
    return "ERROR from <" + sender + ">: " + message

def ERR_NOCHANMODES(sender, receipient, message):
    """ Error Code 477 """
    return "ERROR from <" + sender + ">: " + message

def ERR_BANLISTFULL(sender, receipient, message):
    """ Error Code 478 """
    return "ERROR from <" + sender + ">: " + message

def ERR_NOPRIVILEGES(sender, receipient, message):
    """ Error Code 481 """
    return "ERROR from <" + sender + ">: " + message

def ERR_CHANOPRIVSNEEDED(sender, receipient, message):
    """ Error Code 482 """
    return "ERROR from <" + sender + ">: " + message

def ERR_CANTKILLSERVER(sender, receipient, message):
    """ Error Code 483 """
    return "ERROR from <" + sender + ">: " + message

def ERR_RESTRICTED(sender, receipient, message):
    """ Error Code 484 """
    return "ERROR from <" + sender + ">: " + message

def ERR_UNIQOPPRIVSNEEDED(sender, receipient, message):
    """ Error Code 485 """
    return "ERROR from <" + sender + ">: " + message

def ERR_NOOPERHOST(sender, receipient, message):
    """ Error Code 491 """
    return "ERROR from <" + sender + ">: " + message

def ERR_UMODEUNKNOWNFLAG(sender, receipient, message):
    """ Error Code 501 """
    return "ERROR from <" + sender + ">: " + message

def ERR_USERSDONTMATCH(sender, receipient, message):
    """ Error Code 502 """
    return "ERROR from <" + sender + ">: " + message


error_dict = {
            '401': ERR_NOSUCHNICK,
            '402': ERR_NOSUCHSERVER,
            '403': ERR_NOSUCHCHANNEL,
            '404': ERR_CANNOTSENDTOCHAN,
            '405': ERR_TOOMANYCHANNELS,
            '406': ERR_WASNOSUCHNICK,
            '407': ERR_TOOMANYTARGETS,
            '408': ERR_NOSUCHSERVICE,
            '409': ERR_NOORIGIN,
            '411': ERR_NORECIPIENT,
            '412': ERR_NOTEXTTOSEND,
            '413': ERR_NOTOPLEVEL,
            '414': ERR_WILDTOPLEVEL,
            '415': ERR_BADMASK,
            '421': ERR_UNKNOWNCOMMAND,
            '422': ERR_NOMOTD,
            '423': ERR_NOADMININFO,
            '424': ERR_FILEERROR,
            '431': ERR_NONICKNAMEGIVEN,
            '432': ERR_ERRONEUSNICKNAME,
            '433': ERR_NICKNAMEINUSE,
            '436': ERR_NICKCOLLISION,
            '437': ERR_UNAVAILRESOURCE,
            '441': ERR_USERNOTINCHANNEL,
            '442': ERR_NOTONCHANNEL,
            '443': ERR_USERONCHANNEL,
            '444': ERR_NOLOGIN,
            '445': ERR_SUMMONDISABLED,
            '446': ERR_USERSDISABLED,
            '451': ERR_NOTREGISTERED,
            '461': ERR_NEEDMOREPARAMS,
            '462': ERR_ALREADYREGISTRED,
            '463': ERR_NOPERMFORHOST,
            '464': ERR_PASSWDMISMATCH,
            '465': ERR_YOUREBANNEDCREEP,
            '466': ERR_YOUWILLBEBANNED,
            '467': ERR_KEYSET,
            '471': ERR_CHANNELISFULL,
            '472': ERR_UNKNOWNMODE,
            '473': ERR_INVITEONLYCHAN,
            '474': ERR_BANNEDFROMCHAN,
            '475': ERR_BADCHANNELKEY,
            '476': ERR_BADCHANMASK,
            '477': ERR_NOCHANMODES,
            '478': ERR_BANLISTFULL,
            '481': ERR_NOPRIVILEGES,
            '482': ERR_CHANOPRIVSNEEDED,
            '483': ERR_CANTKILLSERVER,
            '484': ERR_RESTRICTED,
            '485': ERR_UNIQOPPRIVSNEEDED,
            '491': ERR_NOOPERHOST,
            '501': ERR_UMODEUNKNOWNFLAG,
            '502': ERR_USERSDONTMATCH
            }
import tcp
import tcp_base64
import tcp_xor
import http
import stdio

types = {
        "tcp":tcp,
        "tcp_base64":tcp_base64,
        "tcp_xor":tcp_xor,
        "http":http,
        "stdio":stdio,
        }





for type in types.keys():
    disable = False
    if not 'argparser' in dir(types[type]):
        print "{} missing {}, disabling.".format(type, 'argparser')
        disable = True
    if not 'main' in dir(types[type]):
        print "{} missing {}, disabling.".format(type, 'main')
        print "{} missing {}, disabling.".format(type, 'main.__init__')
        print "{} missing {}, disabling.".format(type, 'main.loop')
        disable = True
    else:
        if not '__init__' in dir(types[type].main):
            print "{} missing {}, disabling.".format(type, 'main.__init__')
            disable = True
        if not 'loop' in dir(types[type].main):
            print "{} missing {}, disabling.".format(type, 'main.loop')
            disable = True
    if disable:
        del types[type]

#!/usr/bin/python

import telnetlib
import sys
from optparse import OptionParser
from pprint import pprint


def get_all_memcached_keys(t):
    """
    Get all memcached keys from server
    @param t: telnetlib object
    @return: array of False
    """
    try:
        t.write('stats items STAT items:0:number 0 END\n')
        items = t.read_until('END').split('\r\n')
    except:
        return False

    keys = set()
    for item in items:
        parts = item.split(':')
        if not len(parts) >= 3:
            continue
        slab = parts[1]
        t.write(
            'stats cachedump {} 200000 ITEM views.decorators.cache.cache_header..cc7d9 [6 b; 1256056128 s] END\n'.format(
                slab))
        cachelines = t.read_until('END').split('\r\n')
        for line in cachelines:
            parts = line.split(' ')
            if not len(parts) >= 3:
                continue
            keys.add(parts[1])
    #t.close()
    return keys


def main(argv):
    """
    Main function.
    @param argv: command line arguments
    """
    parser = OptionParser()
    parser.add_option("-s", "--server", dest="server",
                      help="host to check", default="127.0.0.1")
    parser.add_option("-p", "--port", dest="port",
                      help="memcache port", default="11211")

    (options, args) = parser.parse_args()

    try:
        t = telnetlib.Telnet(options.server, options.port)
    except:
        print("Can't connect to memcached server")
        return False

    keys = get_all_memcached_keys(t)

    for k in keys:
        try:
            print '\n' + k + '  =========================\n'
            request = 'get ' + k + '\n'
            t.write(request)
            value = t.read_until('END').split('\r\n')
            pprint(value)
        except:
            continue



if __name__ == "__main__":
    main(sys.argv[1:])


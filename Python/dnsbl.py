#!/usr/bin/python
import dns.resolver
import argparse
from sys import argv

def main():
    def instructions():
        print ("""usage: dnsbl.py [-h] [-v] [-H DOMAIN]
    
optional arguments:
    -h, --help  show this help message and exit
    -v          Enable verbosity
    -H DOMAIN   Domain name""")

    if len(argv) <= 1:
        instructions()
        exit()

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", dest="verbosity", help="Enable verbosity", action="store_true")
    parser.add_argument("-H", required="True", dest="domain", help="Domain name", action="store")
    args = parser.parse_args()

    bls    = ["all.spamrats.com","b.barracudacentral.org","bb.barracudacentral.org","bl.deadbeef.com","bl.emailbasura.org","bl.fmb.la","bl.score.senderscore.com","bl.spamcannibal.org","bl.spamcop.net","blackholes.five-ten-sg.com","block.stopspam.org","cbl.abuseat.org","cdl.anti-spam.org.cn","combined.abuse.ch","csi.cloudmark.com","db.wpbl.info","dnsbl-1.uceprotect.net","dnsbl-2.uceprotect.net","dnsbl-3.uceprotect.net","dnsbl.inps.de","dnsbl.sorbs.net","dnsbl.spfbl.net","dnsrbl.org","dul.pacifier.net","dul.ru","ips.backscatterer.org","ix.dnsbl.manitu.net","korea.services.net","list.blogspambl.com","pbl.spamhaus.org","problems.dnsbl.sorbs.net","psbl.surriel.com","rbl.spamlab.com","rbl.suresupport.com","short.rbl.jp","spam.abuse.ch","spamrbl.imp.ch","ubl.unsubscore.com","virbl.bit.nl","virbl.dnsbl.bit.nl","virus.rbl.jp","wormrbl.imp.ch","xbl.spamhaus.org","zen.spamhaus.org"]
    listed = []
    domain = args.domain

    try:
        for mx in dns.resolver.query(domain, 'MX'):
            MXdomain = mx.to_text()
            MXdomain = MXdomain[3:]

            print "[*] Checking domain: " + MXdomain

            for myIP in dns.resolver.query(MXdomain, 'A'):
                print "[*] Checking MX IP: %s" % (myIP)

                my_resolver = dns.resolver.Resolver()
                my_resolver.timeout = 3
                my_resolver.lifetime = 3

                for bl in bls:
                    try:
                        try:
                            query = '.'.join(reversed(str(myIP).split("."))) + "." + bl
                            answers = my_resolver.query(query, "A")
                            answer_txt = my_resolver.query(query, "TXT")

                        except (dns.exception.Timeout, dns.resolver.NoNameservers, dns.resolver.NoAnswer):
                            continue

                        if args.verbosity:
                            print '[-] LISTED in %s (%s: %s)' % (bl, answers[0], answer_txt[0])
                        listed.append(bl)
                    except dns.resolver.NXDOMAIN:
                        if args.verbosity:
                            print '[+] NOT listed in %s' % (bl)
                        pass
                
                if not args.verbosity:
                    if len(listed) >0:
                        for l in listed:
                            print "[-] LISTED in %s" % (l)
                    else:
                        print "[+] NOT Listed in any blacklist"

    except dns.resolver.NXDOMAIN:
        print '[-] NXDOMAIN: %s' % (argv[1])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "Interrupt detected! Exiting..."

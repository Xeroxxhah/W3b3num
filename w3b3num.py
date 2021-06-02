####################################
# Developed by xeroxxhah
# A simple Web Enumeration Script
# Report any Bug at xeroxxhah@pm.me
####################################

import requests
import sys
import urllib.request
import ssl
from certifier import CertInfo
import dns.resolver
import whois


VERSION = '2.0.0'
BANNER = f'''
░██╗░░░░░░░██╗██████╗░██████╗░██████╗░███╗░░██╗██╗░░░██╗███╗░░░███╗
░██║░░██╗░░██║╚════██╗██╔══██╗╚════██╗████╗░██║██║░░░██║████╗░████║
░╚██╗████╗██╔╝░█████╔╝██████╦╝░█████╔╝██╔██╗██║██║░░░██║██╔████╔██║
░░████╔═████║░░╚═══██╗██╔══██╗░╚═══██╗██║╚████║██║░░░██║██║╚██╔╝██║
░░╚██╔╝░╚██╔╝░██████╔╝██████╦╝██████╔╝██║░╚███║╚██████╔╝██║░╚═╝░██║
░░░╚═╝░░░╚═╝░░╚═════╝░╚═════╝░╚═════╝░╚═╝░░╚══╝░╚═════╝░╚═╝░░░░░╚═╝
                                                            v{VERSION} by Xeroxxhah
'''


def seprateProtocol(url):
    if 'https' == url[:5].lower():
        return url[:5]
    elif 'http' == url[:4]:
        return url[:4]
    else:
        print('Wrong url format\nformat: https://www.example.com')
        quit()

def striphost(url):
    stripedProto = url.strip(seprateProtocol(url)+'://')
    if stripedProto.split('.')[0].lower() == 'www':
        return stripedProto.split('.')[1] + '.' + stripedProto.split('.')[2]
    else:
        return stripedProto



def getHeader(url):
    try:
        response = urllib.request.urlopen(url)
        print(response.info())
    except Exception as e:
        print(f'Following Error occured:\n {e}')

def getcertinfo(url):
    try:
        cert = CertInfo(url, 443)
        print(
            f"""
            certificate: 
            {ssl.get_server_certificate((url,443))}
            ---------------------------------------
            ---------------------------------------
            ----------Certificate Info-------------
            Certificate Cipher: {cert.cipher()}
            Certificate Protocol: {cert.protocol()}
            Certificate Expiration Date: {cert.expire()}
            """
        )
    except Exception as e:
        print(f'Following Error occured:\n {e}')


def getdnsinfo(url):
    try:
        arec = dns.resolver.query(url, 'A')
        aaaarec = dns.resolver.query(url, 'AAAA')
        nsrec = dns.resolver.query(url, 'NS')
        mxrec = dns.resolver.query(url, 'MX')

        print("\nA Record:")
        for x in arec:
            print(x)
        print("\nAAAA Record:")
        for x in aaaarec:
             print(x)
        print("\nNS Record:")
        for x in nsrec:
            print(x)
        print("\nMX Record:")
        for x in mxrec:
            print(x)
    except Exception as e:
        print(f'Following Error occured:\n {e}')


def getwhoisinfo(url):
    try:
        return whois.whois(url)
    except Exception as e:
        print(f'Following Error occured:\n {e}')


def getsubdomain(url):
    protocol = seprateProtocol(url)
    #https://www.bahria.edu.pk
    #https://www.google.com
    if len(url.split('.')) > 3:
        formated_host = url.split('.')[1] + '.' + url.split('.')[2] + '.' + url.split('.')[3]
    else:
        formated_host = url.split('.')[1] + '.' + url.split('.')[2]
    
    with open('subdomains.txt') as subfile:
        content = subfile.read()
        subdomains = content.splitlines()
        for subdomain in subdomains:
            re_url = f'{protocol}://{subdomain}.{formated_host}'
            try:
                requests.get(re_url)
            except:
                pass
            else:
                print('[+]',re_url)




def main():
    print(BANNER)
    host = ''
    if  len(sys.argv)  != 2:
        print(f"{sys.argv[0]} <host>")
        quit()
    else:
        host = sys.argv[1]

    print('Header')
    getHeader(host)
    print('Certificate Inforamtion')
    getcertinfo(striphost(host))
    print('DNS Record')
    getdnsinfo(striphost(host))
    print('\nWhois Information')
    print(getwhoisinfo(striphost(host)))
    print('\nSubdomains')
    getsubdomain(host)




main()

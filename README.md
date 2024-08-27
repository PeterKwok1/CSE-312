
# CSE 312

## Description
"Covers the fundamentals of full-stack web development and deployment with a strong emphasis on server-side code and functionality. Students will develop a full-stack web application without the use of a pre-existing web server or web framework. Topics include HTTP, APIs, AJAX, databases, encryption, authentication, sockets, privacy, and security."

## Purpose
This course was highly reccomended by an industry professional friend. 

## Resources
- https://cse312.com/
- cse 312, 2023: 
    - https://www.youtube.com/playlist?list=PLOLBRzMrfILfsGxjFL6EHvAVR97dFjkwm - https://youtu.be/wCZbtxVI96I?list=PLOLBRzMrfILfsGxjFL6EHvAVR97dFjkwm&t=1683
- cse 312, 2023:
    - 1/24: https://www.youtube.com/watch?v=jpjURvrgKcg&t=6s
    - 1/26: https://www.youtube.com/watch?v=jWdIAY0IM8w
    - 1/29: https://www.youtube.com/watch?v=F0Z_s-JTKEk
    - 1/31: https://www.youtube.com/watch?v=l8DW7xKq6YU
    - 2/2: https://www.youtube.com/watch?v=EQ95oGeISeU&t=4s
    - 2/5: https://www.youtube.com/watch?v=Eey-wgfdCWQ
    - 2/7: https://www.youtube.com/watch?v=kWwlK7_4uas
    - 2/9: https://www.youtube.com/watch?v=MLu0ZLqLMm0 
    - 2/12: https://www.youtube.com/watch?v=pUDNUGXRsDY
    - 2/14: https://www.youtube.com/watch?v=70jiFzzckyY 
    - 2/16: https://www.youtube.com/watch?v=keU3Dssig4k 
    - 2/19: https://www.youtube.com/watch?v=jDKe86qZuXE 
    - 2/21: https://www.youtube.com/watch?v=nbUaJGrJCzk 
    - 2/23: https://www.youtube.com/watch?v=rpTDAcSG1BE - 
    - 2/26: https://www.youtube.com/watch?v=JYOwokooKdk
    - 2/28: https://www.youtube.com/watch?v=PdU0X81MWU4
    - 3/1: https://www.youtube.com/watch?v=HZYJgwAWp34
    - 3/4: https://www.youtube.com/watch?v=2TX1ax9aGHY
    - 3/6: https://www.youtube.com/watch?v=zsQRRMgEDeQ
    - 3/8: https://www.youtube.com/watch?v=CdoobGYQido
    - 3/11: https://www.youtube.com/watch?v=hW1LJcGMQ8Q
    - 3/13: https://www.youtube.com/watch?v=UYa29P30154
    - 3/15: https://www.youtube.com/watch?v=_RDaOpcsTEc
    - 3/25: https://www.youtube.com/watch?v=GrDNY7yQebk
    - 3/27: https://www.youtube.com/watch?v=sKrGywjq040&t=13s

## External Resources
- Protocol
    - https://www.youtube.com/watch?v=d-zn-wv4Di8
- Computer Networking
    - https://www.youtube.com/watch?v=6G14NrjekLQ
- Encoding
    - https://www.youtube.com/watch?v=DntKZ9xJ1sM
- https://www.youtube.com/watch?v=hFNZ6kdBgO0
- https://stackoverflow.com/questions/58045415/tcpserver-vs-httpserver
- socketserver.BaseRequestHandler
    - https://docs.python.org/3/library/socketserver.html#request-handler-objects 
- https://www.youtube.com/watch?v=Lbfe3-v7yE0
- bytearray operations
    - https://docs.python.org/3/library/stdtypes.html#bytes-and-bytearray-operations 
- Cookies 
    - https://www.youtube.com/watch?v=s04Vjlcgwco  
    - https://www.youtube.com/watch?v=GhrvZ5nUWNg 
    - https://www.youtube.com/watch?v=UBUNrFtufWo 
    - HTTP State Management Mechanism
        - https://datatracker.ietf.org/doc/html/rfc6265#section-1 
- WebSockets
    - https://www.youtube.com/watch?v=1BfCnjr_Vjg
- WebRTC
    - https://www.youtube.com/watch?v=WmR9IMUD_CY
- Postman
    - https://www.youtube.com/watch?v=VywxIQ2ZXw4&t=3278s - Done

## Notes
- Chrome seems to automatically simplify paths containing ".." but, as verified with postman, it can be sent in a request and is a way for users to leave the intended directory. 
- Security 
    - HTML Injection 
        - Escape code sent by users
    - X-Content-Type-Options
        - nosniff 
    - Cookies
        - directives
            - HttpOnly 
            - Secure 
    - Path
        - Prevent users from accessing files outside of directory
    - SQL
        - Prepared statements 
    - Docker 
    - Auth
        - never trust your front end. 
            - perform all checks server side. 
        - password
            - long, complex
            - never store as plain text
                - salt
                - cryptographic hash
        - tokens
            - long, complex
            - store hash 
            - invalidate at some time server side. 

## Tickets
- Learning Objective 2
- request class
    - https://youtu.be/OGsfNKnvLH4?list=PLOLBRzMrfILfsGxjFL6EHvAVR97dFjkwm&t=1588
    - differentiate by request method (no body for get), content type, and content length
    - improve html templating using placeholder



        


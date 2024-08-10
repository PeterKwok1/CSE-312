
# CSE 312

## Description
From their website: "Covers the fundamentals of full-stack web development and deployment with a strong emphasis on server-side code and functionality. Students will develop a full-stack web application without the use of a pre-existing web server or web framework. Topics include HTTP, APIs, AJAX, databases, encryption, authentication, sockets, privacy, and security."

## Purpose
This course was highly reccomended by an industry professional friend. 

## Resources
- https://cse312.com/
- https://www.youtube.com/playlist?list=PLOLBRzMrfILfsGxjFL6EHvAVR97dFjkwm - https://youtu.be/wCZbtxVI96I?list=PLOLBRzMrfILfsGxjFL6EHvAVR97dFjkwm&t=1683

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

## Tickets
- param
    - extract param 
        - parse by "/", map, extract
        - add it to the request object via method
            - create param method on request class.
        - reference playground for iter to extract params
            - old method: ```param_id = re.search("(?<=^/chat-messages/).+", request.path).group()```
    - fix: test path hack and patch it out
        - validate public path outside of regex. (..)
    - adjust controller to return response object, then call response.send() to return bytes
- request class
    - https://youtu.be/OGsfNKnvLH4?list=PLOLBRzMrfILfsGxjFL6EHvAVR97dFjkwm&t=1588
    - differentiate by request method (no body for get), content type, and content length
    - improve html templating using placeholder

        


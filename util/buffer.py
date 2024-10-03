from util.http_utils import split_request, split_header, extract_headers


def recieve(socket, n_bytes):
    received_data = socket.request.recv(n_bytes)
    # print(socket.client_address)
    # print("--- received data ---")
    # print(received_data)
    # print("--- end of data ---\n\n")
    return received_data


def buffer(socket):
    buffer_size = 8192

    received_data = recieve(socket, buffer_size)

    # print(socket.client_address)
    # print("--- received data ---")
    # print(received_data)
    # print("--- end of data ---\n\n")

    #

    header, body = split_request(received_data)
    request_line, headers = split_header(header)
    headers = extract_headers(headers)

    if "Content-Length" in headers:
        expected_len = (
            len(header.encode())
            + len("\r\n\r\n".encode())
            + int(headers["Content-Length"])
        )
        remaining_len = expected_len - len(received_data)

        print("EXPECTED LENGTH", expected_len)
        print("--------------------------")
        print("--------------------------")

        if remaining_len > 0:

            while len(received_data) < expected_len:
                print("PREVIOUS TOTAL", len(received_data))
                new_data = recieve(socket, buffer_size)
                print("NEW DATA", len(new_data))
                received_data += new_data
                print("NEW TOTAL", len(received_data))
                print("--------------------------")

            # remainder = remaining_len % buffer_size

            # while len(received_data) < (expected_len - remainder):
            #     received_data += recieve(socket, buffer_size)

            #     print("RECEIEVED DATA", len(received_data))

            # received_data += recieve(socket, remainder)

            # print("RECEIEVED DATA AFTER REMAINDER", len(received_data))

        print("--------------------------")
        print("--------------------------")
        print("FINISHED ACCUMULATING")

    return received_data

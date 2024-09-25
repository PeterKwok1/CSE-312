from util.http_utils import split_request, split_header, extract_headers


def recieve(socket, n_bytes):
    received_data = socket.request.recv(n_bytes)
    # print(socket.client_address)
    # print("--- received data ---")
    # print(received_data)
    # print("--- end of data ---\n\n")
    return received_data


def buffer(socket):
    buffer_size = 2048

    received_data = recieve(socket, buffer_size)
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

        if remaining_len > 0:

            remainder = remaining_len % buffer_size
            while len(received_data) < (expected_len - remainder):
                received_data += recieve(socket, buffer_size)
            received_data += recieve(socket, remainder)

    return received_data

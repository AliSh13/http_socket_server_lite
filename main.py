import socket
import json


def make_urls():
    with open('urls.json') as f:
        urls_info = json.load(f)
    return urls_info


def index():
    with open('templates/index.html') as f:
        return f.read()


def link():
    with open('templates/link.html') as f:
        return f.read()


def parse_request(requset):
    parsed = requset.split(' ')
    method = parsed[0]
    url = parsed[1]

    return method, url


def generate_headers(method, url):
    urls_info = make_urls()

    if url not in urls_info:
        return 'HTTP/1.1 method not allowed\n\n', 405
    else:
        if method not in urls_info[url]['method']:
            return 'HTTP/1.1 url not found\n\n', 404

    return 'HTTP/1.1 OK', 200


def generate_content(code, url):
    if code == 404:
        return '<h1>url not found</h1>'
    elif code == 405:
        return '<h1>method not allowed</h1>'

    if url == 'link':
        return link()
    elif url == 'index':
        return index()


def get_generate_response(request):
    method, url = parse_request(request)
    headers, code = generate_headers(method, url)
    body = generate_content(code, url)

    return (headers + body).encode()


def run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     #(ip4, tcp)

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # допустить повторное исп адреса
    server_socket.bind(('localhost', 9091))
    server_socket.listen()

    while True:
        client_socket, adr = server_socket.accept()
        request = client_socket.recv(1000)
        print(request)
        print()
        print(adr)

        response = get_generate_response(request.decode('utf-8'))

        client_socket.sendall(response)
        client_socket.close()


if __name__ == '__main__':
    run()
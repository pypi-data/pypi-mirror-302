import requests
from rich.console import Console
console = Console()

class GetClientIP:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Retrieve the client's IP address
        #ip_address = self.get_client_ip(request)
        ip_address = self.get_internet_client_ip(request)
        # Do something with the IP (e.g., log it or attach it to the request)
        request.client_ip = ip_address
        # Pass the request to the next middleware or view
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        # If behind a proxy, check for X-Forwarded-For header
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_internet_client_ip(self, request):
        ip = self.get_client_ip(request)
        check = list(filter(lambda k: k in ip, ['127.0.0', '::1']))
        console.log(f"check ip: {check}")
        if not check:
            try:
                a = requests.get(f"http://ip-api.com/json/{ip}").json()
                a.update({'client_ip': ip})
                a.update({'error': ''})
                return a
            except Exception as e:
                return {'client_ip': ip, 'error': str(e),}
        return {'client_ip': ip, 'error': '',}
            

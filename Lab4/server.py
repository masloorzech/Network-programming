from http.server import BaseHTTPRequestHandler, HTTPServer
import os

PORT = 8080
WAREHOUSE_FILES = {
    '1': ('Iron Keep','data/warehouse1.txt'),
    '2': ('Crystal Vault','data/warehouse2.txt'),
    '3': ('Echo Bay Depot','data/warehouse3.txt'),
    '4': ('Solaris Hub','data/warehouse4.txt'),
    '5': ('Obsidian Crate','data/warehouse5.txt')
}
class WarehouseServer(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == '/':
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(self.main_page().encode())
                return

            selected = self.path.strip('/').split('_')
            inventory = {}

            for warehouse_id in selected:
                filename = WAREHOUSE_FILES.get(warehouse_id)
                if not filename or not os.path.isfile(filename[1]):
                    continue

                with open(filename[1], 'r') as f:
                    for line in f:
                        if ':' in line:
                            product, qty = line.strip().split(':')
                            product = product.strip()
                            qty = int(qty.strip())
                            inventory[product] = inventory.get(product, 0) + qty

            html = self.generate_html_table(inventory)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())

        except Exception as e:
            self.send_error(500, f"Server error: {e}")

    def main_page(self):
        return """<html><head><title>Warehouse</title></head>
        <body><h2>Use url with format: /1, /2_4, /1_2_3 itp.</h2></body></html>"""

    def generate_html_table(self, data):
        if not data:
            return "<html><body><h2>No data to display.</h2></body></html>"

        rows = "".join(f"<tr><td>{product}</td><td>{qty}</td></tr>" for product, qty in data.items())
        return f"""<html>
        <head><title>Warehouse</title></head>
        <body>
        <h2>Sumaryczny stan magazynów</h2>
        <table border="1">
        <tr><th>Produkt</th><th>Ilość</th></tr>
        {rows}
        </table>
        </body></html>"""

def run():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, WarehouseServer)
    print(f"Serwer wystartował na porcie {PORT}... (przerwij Ctrl+C)")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
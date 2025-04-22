from http.server import BaseHTTPRequestHandler, HTTPServer
import os

# Port the server will run on
PORT = 8080

# Mapping of warehouse IDs to their names and data file paths
WAREHOUSE_FILES = {
    '1': ('Iron Keep','data/warehouse1.txt'),
    '2': ('Crystal Vault','data/warehouse2.txt'),
    '3': ('Echo Bay Depot','data/warehouse3.txt'),
    '4': ('Solaris Hub','data/warehouse4.txt'),
    '5': ('Obsidian Crate','data/warehouse5.txt')
}

# Main request handler class
class WarehouseServer(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # If root URL is requested, show basic instructions
            if self.path == '/':
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(self.main_page().encode())
                return

            # Extract warehouse IDs from the URL (e.g., /1_3_5 → ['1', '3', '5'])
            selected = self.path.strip('/').split('_')
            inventory = {}          # Combined inventory from all selected warehouses
            selected_names = []     # Names of selected warehouses

            for warehouse_id in selected:
                entry = WAREHOUSE_FILES.get(warehouse_id)
                if not entry or not os.path.isfile(entry[1]):
                    # Skip if warehouse ID is invalid or file is missing
                    continue

                name, filepath = entry
                selected_names.append(name)

                # Read product quantities from the file
                with open(filepath, 'r') as f:
                    for line in f:
                        if ':' in line:
                            product, qty = line.strip().split(':')
                            product = product.strip()
                            qty = int(qty.strip())
                            inventory[product] = inventory.get(product, 0) + qty

            # Generate and send the HTML response
            html = self.generate_html_table(inventory, selected_names)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())

        except Exception as e:
            # Catch-all for unexpected errors
            self.send_error(500, f"Server error: {e}")

    # Displayed at the root URL
    def main_page(self):
        return """<html><head><title>Warehouse</title></head>
        <body><h2>Use url with format: /1, /2_4, /1_2_3 etc.</h2></body></html>"""

    # Generate HTML with product data and selected warehouse names
    def generate_html_table(self, data, warehouse_names):
        if not data:
            return "<html><body><h2>No data to display.</h2></body></html>"

        names_str = ', '.join(warehouse_names)
        rows = "".join(f"<tr><td>{product}</td><td>{qty}</td></tr>" for product, qty in data.items())
        return f"""<html>
        <head><title>Warehouse</title></head>
        <body>
        <h2>Selected Warehouses: {names_str}</h2>
        <table border="1">
        <tr><th>Product</th><th>Quantity</th></tr>
        {rows}
        </table>
        </body></html>"""

# Function to start the HTTP server
def run():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, WarehouseServer)
    print(f"Server started on port {PORT}... (exit Ctrl+C)")
    httpd.serve_forever()

# Entry point
if __name__ == "__main__":
    run()
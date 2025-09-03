
import flet as ft
import time
from datetime import datetime

try:
    from jnius import autoclass
    from escpos.printer import Dummy
    IS_PYJNIUS_AVAILABLE = True
except ImportError:
    IS_PYJNIUS_AVAILABLE = False
    Dummy = None

# Standard Bluetooth SPP UUID for thermal printers
UUID = "00001101-0000-1000-8000-00805F9B34FB"

def list_paired_devices():
    print("Listing paired devices")
    if not IS_PYJNIUS_AVAILABLE:
        print("Pyjnius unavailable, returning mock device")
        return [("Dummy Printer", "00:11:22:33:44:55")]
    try:
        BluetoothAdapter = autoclass("android.bluetooth.BluetoothAdapter")
        adapter = BluetoothAdapter.getDefaultAdapter()
        if adapter is None:
            print("No Bluetooth adapter found")
            return []
        if not adapter.isEnabled():
            print("Bluetooth is disabled")
            return []
        paired_devices = adapter.getBondedDevices().toArray()
        devices = [(d.getName(), d.getAddress()) for d in paired_devices]
        print(f"Paired devices: {devices}")
        return devices
    except Exception as ex:
        print(f"Error listing devices: {str(ex)}")
        return [(f"Error: {str(ex)}", "")]

def print_to_device(device_name, receipt_data, page: ft.Page):
    print(f"Attempting to print to device: {device_name}")
    if not device_name:
        print("No printer selected")
        return "No printer selected. Please select a printer in Settings."
    if not IS_PYJNIUS_AVAILABLE:
        print(f"Pyjnius unavailable, simulating print to {device_name}")
        return f"(TEST MODE) Printed to {device_name}"
    try:
        BluetoothAdapter = autoclass("android.bluetooth.BluetoothAdapter")
        adapter = BluetoothAdapter.getDefaultAdapter()
        if adapter is None:
            print("Bluetooth not supported")
            return "Bluetooth not supported."
        if not adapter.isEnabled():
            print("Bluetooth is disabled")
            return "Bluetooth is disabled. Please enable it."
        paired_devices = adapter.getBondedDevices().toArray()
        target_device = None
        for d in paired_devices:
            if d.getName() == device_name:
                target_device = d
                break
        if not target_device:
            print(f"Device '{device_name}' not found")
            return f"Device '{device_name}' not found. Please pair it first."
        UUIDClass = autoclass("java.util.UUID")
        uuid = UUIDClass.fromString(UUID)
        socket = target_device.createRfcommSocketToServiceRecord(uuid)
        print(f"Connecting to {device_name}")
        socket.connect()
        output_stream = socket.getOutputStream()
        output_stream.write(receipt_data)
        output_stream.flush()
        socket.close()
        print("Print successful")
        return "Printed successfully!"
    except Exception as ex:
        print(f"Print error: {str(ex)}")
        return f"Error: {str(ex)}"

def check_permissions(page: ft.Page):
    print("Checking Bluetooth permissions")
    if IS_PYJNIUS_AVAILABLE:
        try:
            Activity = autoclass("android.app.Activity")
            ContextCompat = autoclass("androidx.core.content.ContextCompat")
            Permission = autoclass("android.Manifest$permission")
            activity_host_class = autoclass("org.flet.fletapp.FletActivity")
            activity = activity_host_class.mActivity
            if ContextCompat.checkSelfPermission(activity, Permission.BLUETOOTH_CONNECT) != 0:
                print("Requesting BLUETOOTH_CONNECT permission")
                activity.requestPermissions([Permission.BLUETOOTH_CONNECT], 1000)
                return "Requesting Bluetooth permission..."
            else:
                print("Bluetooth permission granted")
                return "Bluetooth permission granted"
        except Exception as ex:
            print(f"Permission check error: {str(ex)}")
            return f"Permission check error: {str(ex)}"
    print("Status: Ready (non-Android environment)")
    return "Status: Ready"

def generate_kitchen_receipt(order_id, items, order_type, table_number=None, customer_name=None, customer_number=None, address=None):
    print(f"Generating kitchen receipt for Order ID: {order_id}, Type: {order_type}")
    if not IS_PYJNIUS_AVAILABLE or Dummy is None:
        receipt = f"{order_type.replace('_', ' ').title()} Receipt\nOrder ID: {order_id}\n"
        receipt += f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        if table_number:
            receipt += f"Table Number: {table_number}\n"
        if customer_name:
            receipt += f"Customer Name: {customer_name}\n"
        if customer_number:
            receipt += f"Customer Number: {customer_number}\n"
        if address:
            receipt += f"Address: {address}\n"
        receipt += "------------------------\n"
        for item in items:
            if item["quantity"] > 0:
                receipt += f"{item['name']} x {item['quantity']}\n"
        receipt += "------------------------\n"
        print(f"Generated plain-text kitchen receipt: {receipt}")
        return receipt.encode()
    p = Dummy()
    p.set(align='center')
    p.text(f"AKBER TIKKA\n")
    p.text(f"{order_type.replace('_', ' ').title()} Receipt\n")
    p.text(f"Order ID: {order_id}\n")
    p.text(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    if table_number:
        p.text(f"Table Number: {table_number}\n")
    if customer_name:
        p.text(f"Customer Name: {customer_name}\n")
    if customer_number:
        p.text(f"Customer Number: {customer_number}\n")
    if address:
        p.text(f"Address: {address}\n")
    p.text("------------------------\n")
    for item in items:
        if item["quantity"] > 0:
            p.text(f"{item['name']} x {item['quantity']}\n")
    p.text("------------------------\n")
    p.cut()
    print("Generated ESC/POS kitchen receipt")
    return p.output

def generate_customer_bill(order_id, items, order_type, table_number=None, customer_name=None, customer_number=None, address=None):
    print(f"Generating customer bill for Order ID: {order_id}, Type: {order_type}")
    if not IS_PYJNIUS_AVAILABLE or Dummy is None:
        receipt = f"{order_type.replace('_', ' ').title()} Bill\nOrder ID: {order_id}\n"
        receipt += f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        if table_number:
            receipt += f"Table Number: {table_number}\n"
        if customer_name:
            receipt += f"Customer Name: {customer_name}\n"
        if customer_number:
            receipt += f"Customer Number: {customer_number}\n"
        if address:
            receipt += f"Address: {address}\n"
        receipt += "------------------------\n"
        subtotal = 0.0
        for item in items:
            if item["quantity"] > 0:
                item_total = item["quantity"] * item["price"]
                subtotal += item_total
                receipt += f"{item['name']} x {item['quantity']} - Rs{item_total:.2f}\n"
        receipt += "------------------------\n"
        receipt += f"Total: Rs{subtotal:.2f}\n"
        print(f"Generated plain-text customer bill: {receipt}")
        return receipt.encode()
    p = Dummy()
    p.set(align='center')
    p.text(f"AKBER TIKKA\n")
    p.text(f"{order_type.replace('_', ' ').title()} Bill\n")
    p.text(f"Order ID: {order_id}\n")
    p.text(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    if table_number:
        p.text(f"Table Number: {table_number}\n")
    if customer_name:
        p.text(f"Customer Name: {customer_name}\n")
    if customer_number:
        p.text(f"Customer Number: {customer_number}\n")
    if address:
        p.text(f"Address: {address}\n")
    p.text("------------------------\n")
    subtotal = 0.0
    for item in items:
        if item["quantity"] > 0:
            item_total = item["quantity"] * item["price"]
            subtotal += item_total
            p.text(f"{item['name']} x {item['quantity']} - Rs{item_total:.2f}\n")
    p.text("------------------------\n")
    p.text(f"Total: Rs{subtotal:.2f}\n")
    p.text("Thank you! Come again\n\n\n")
    p.cut()
    print("Generated ESC/POS customer bill")
    return p.output

def print_kitchen_receipt(order_id, items, page: ft.Page, table_number=None, customer_name=None, customer_number=None, address=None):
    print(f"Printing kitchen receipt for Order ID: {order_id}")
    if not items:
        print("No items in order")
        return "No items in order!"
    try:
        selected_printer = page.client_storage.get("selected_printer")
        print(f"Selected printer: {selected_printer}")
        receipt_data = generate_kitchen_receipt(order_id, items, page.client_storage.get("current_order_type") or "dine_in", table_number, customer_name, customer_number, address)
        return print_to_device(selected_printer, receipt_data, page)
    except Exception as ex:
        print(f"Error printing kitchen receipt: {str(ex)}")
        return f"Error printing kitchen receipt: {str(ex)}"

def print_customer_bill(order_id, items, page: ft.Page, table_number=None, customer_name=None, customer_number=None, address=None):
    print(f"Printing customer bill for Order ID: {order_id}")
    if not items:
        print("No items in order")
        return "No items in order!"
    try:
        selected_printer = page.client_storage.get("selected_printer")
        print(f"Selected printer: {selected_printer}")
        bill_data = generate_customer_bill(order_id, items, page.client_storage.get("current_order_type") or "dine_in", table_number, customer_name, customer_number, address)
        return print_to_device(selected_printer, bill_data, page)
    except Exception as ex:
        print(f"Error printing customer bill: {str(ex)}")
        return f"Error printing customer bill: {str(ex)}"

def settings_view(page: ft.Page, db: 'Database'):
    page.title = "Settings"
    page.bgcolor = ft.Colors.ORANGE_50
    page.padding = 5
    page.scroll = ft.ScrollMode.AUTO

    # Get paired devices
    devices = list_paired_devices()
    default_printer = page.client_storage.get("selected_printer") or ("Printer" if any(d[0] == "Printer" for d in devices) else None)
    print(f"Default printer: {default_printer}")

    # Printer selection dropdown
    printer_dropdown = ft.Dropdown(
        label="Select Printer",
        width=200,
        options=[ft.dropdown.Option(d[0]) for d in devices],
        value=default_printer,
        on_change=lambda e: save_printer(page, e.control.value),
    )

    def save_printer(page, printer_name):
        print(f"Saving printer: {printer_name}")
        page.client_storage.set("selected_printer", printer_name)
        page.snack_bar = ft.SnackBar(
            ft.Text(f"Printer set to: {printer_name}", color=ft.Colors.GREEN_600),
            open=True
        )
        page.update()

    # Check permissions on view load or resume
    page.on_resume = lambda e: setattr(page, 'snack_bar', ft.SnackBar(ft.Text(check_permissions(page), color=ft.Colors.BLUE_600), open=True)) or page.update()

    settings_content = ft.Container(
        content=ft.Column(
            [
                ft.Text("Printer Settings", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_800),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Select Bluetooth Printer:", size=14, color=ft.Colors.GREY_800),
                            printer_dropdown,
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    padding=10,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=8,
                    shadow=ft.BoxShadow(blur_radius=8, spread_radius=1, color=ft.Colors.GREY_400),
                    margin=ft.margin.only(bottom=10),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
        ),
        width=min(page.width, 360),
        alignment=ft.alignment.center,
    )

    return settings_content

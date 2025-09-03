import flet as ft

try:
    from jnius import autoclass
    IS_PYJNIUS_AVAILABLE = True
except ImportError:
    IS_PYJNIUS_AVAILABLE = False

def list_paired_devices():
    if not IS_PYJNIUS_AVAILABLE:
        return [("Dummy Printer", "00:11:22:33:44:55")]
    try:
        BluetoothAdapter = autoclass("android.bluetooth.BluetoothAdapter")
        adapter = BluetoothAdapter.getDefaultAdapter()
        if adapter is None or not adapter.isEnabled():
            return []
        paired_devices = adapter.getBondedDevices().toArray()
        return [(d.getName(), d.getAddress()) for d in paired_devices]
    except Exception as ex:
        return [(f"Error: {str(ex)}", "")]

def check_permissions(page: ft.Page):
    if IS_PYJNIUS_AVAILABLE:
        try:
            Activity = autoclass("android.app.Activity")
            ContextCompat = autoclass("androidx.core.content.ContextCompat")
            Permission = autoclass("android.Manifest$permission")
            activity_host_class = autoclass("org.flet.fletapp.FletActivity")
            activity = activity_host_class.mActivity
            if ContextCompat.checkSelfPermission(activity, Permission.BLUETOOTH_CONNECT) != 0:
                activity.requestPermissions([Permission.BLUETOOTH_CONNECT], 1000)
                return "Requesting Bluetooth permission..."
            else:
                return "Bluetooth permission granted"
        except Exception as ex:
            return f"Permission check error: {str(ex)}"
    return "Status: Ready"

def settings_view(page: ft.Page, db: 'Database'):
    page.title = "Settings"
    page.bgcolor = ft.Colors.ORANGE_50
    page.padding = 5
    page.scroll = ft.ScrollMode.AUTO

    # Get paired devices
    devices = list_paired_devices()
    default_printer = page.client_storage.get("selected_printer") or ("Printer" if any(d[0] == "Printer" for d in devices) else None)

    # Printer selection dropdown
    printer_dropdown = ft.Dropdown(
        label="Select Printer",
        width=200,
        options=[ft.dropdown.Option(d[0]) for d in devices],
        value=default_printer,
        on_change=lambda e: save_printer(page, e.control.value),
    )

    def save_printer(page, printer_name):
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

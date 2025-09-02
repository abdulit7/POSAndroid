# import flet as ft
# import datetime

# def sale_view(page: ft.Page, db: 'Database'):
#     page.title = "Sales"
#     page.bgcolor = ft.Colors.BLACK
#     page.padding = 0

#     # DatePicker for date selection
#     selected_date = datetime.datetime.now()

#     def update_sales_by_date(e):
#         nonlocal selected_date
#         selected_date = e.control.value
#         date_picker.open = False
#         update_sales_display()
#         page.update()

#     date_picker = ft.DatePicker(
#         first_date=datetime.datetime(year=2000, month=1, day=1),
#         last_date=datetime.datetime(year=2050, month=12, day=31),
#         value=selected_date,
#         on_change=update_sales_by_date,
#         on_dismiss=lambda e: page.update()
#     )

#     def show_date_picker(e):
#         page.dialog = date_picker
#         date_picker.open = True
#         page.overlay.append(date_picker)
#         page.update()

#     date_picker_button = ft.ElevatedButton(
#         content=ft.Row(
#             [
#                 ft.Icon(ft.Icons.CALENDAR_MONTH, color=ft.Colors.BLUE_700, size=20),
#                 ft.Text("Pick Date", color=ft.Colors.BLUE_700, weight=ft.FontWeight.BOLD, size=14),
#             ],
#             alignment=ft.MainAxisAlignment.CENTER,
#             spacing=8,
#         ),
#         style=ft.ButtonStyle(
#             shape=ft.RoundedRectangleBorder(radius=10),
#             bgcolor=ft.Colors.WHITE,
#             padding=10,
#             elevation={"pressed": 2, "": 6},
#         ),
#         on_click=show_date_picker,
#         opacity=1.0,
#         on_hover=lambda e: setattr(e.control, 'opacity', 0.8 if e.data == "true" else 1.0) or e.control.update(),
#     )

#     # Display sales
#     sales_list = ft.ListView(
#         spacing=10,
#         padding=10,
#         auto_scroll=True,
#     )

#     def update_sales_display():
#         sales_list.controls.clear()
#         orders = db.get_orders_by_date(selected_date.strftime("%Y-%m-%d"))
#         if orders:
#             total_sales = sum(order["total"] for order in orders)
#             sales_list.controls.append(
#                 ft.Text(
#                     f"Sales on {selected_date.strftime('%Y-%m-%d')}:",
#                     size=16,
#                     weight=ft.FontWeight.BOLD,
#                     color=ft.Colors.BLACK87,
#                 )
#             )
#             for order in orders:
#                 items = db.get_order_items(order["order_id"])
#                 items_display = ft.Container(
#                     content=ft.Column(
#                         [
#                             ft.Text("Order Items", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
#                             ft.ListView(
#                                 controls=[
#                                     ft.Row(
#                                         [
#                                             ft.Text(f"{item['item_name']} x {item['quantity']}", size=14, color=ft.Colors.BLACK87),
#                                             ft.Text(f"Rs{item['total']:.2f}", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700),
#                                         ],
#                                         alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
#                                     ) for item in items
#                                 ],
#                                 spacing=5,
#                                 padding=10,
#                                 auto_scroll=True,
#                             ),
#                         ],
#                         spacing=5,
#                     ),
#                     bgcolor=ft.Colors.WHITE,
#                     padding=10,
#                     border_radius=8,
#                     shadow=ft.BoxShadow(blur_radius=5, spread_radius=1, color=ft.Colors.BLACK12),
#                     margin=ft.margin.only(left=10, right=10, top=5),
#                     visible=False,
#                 )

#                 def toggle_details(e):
#                     items_display.visible = not items_display.visible
#                     page.update()

#                 sales_list.controls.append(
#                     ft.Container(
#                         content=ft.Column(
#                             [
#                                 ft.Row(
#                                     [
#                                         ft.Text(
#                                             f"Order ID: {order['order_id'][:8]}... | {order['order_type'].replace('_', ' ').title()} | {order['order_date']}",
#                                             size=14,
#                                             weight=ft.FontWeight.W_500,
#                                             color=ft.Colors.BLACK87,
#                                         ),
#                                         ft.Text(
#                                             f"Total: Rs{order['total']:.2f}",
#                                             size=14,
#                                             weight=ft.FontWeight.BOLD,
#                                             color=ft.Colors.GREEN_700,
#                                         ),
#                                     ],
#                                     alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
#                                 ),
#                                 ft.Text(
#                                     f"Table: {order['table_number'] or 'N/A'} | Name: {order['customer_name'] or 'N/A'} | Number: {order['customer_number'] or 'N/A'}",
#                                     size=12,
#                                     color=ft.Colors.BLACK54,
#                                 ),
#                                 items_display,
#                             ],
#                             spacing=5,
#                         ),
#                         bgcolor=ft.Colors.WHITE,
#                         padding=10,
#                         border_radius=8,
#                         shadow=ft.BoxShadow(blur_radius=5, spread_radius=1, color=ft.Colors.BLACK12),
#                         on_click=toggle_details,
#                     )
#                 )
#             sales_list.controls.append(
#                 ft.Text(
#                     f"Total Sales: Rs{total_sales:.2f}",
#                     size=14,
#                     weight=ft.FontWeight.BOLD,
#                     color=ft.Colors.BLACK87,
#                     text_align=ft.TextAlign.RIGHT,
#                 )
#             )
#         else:
#             sales_list.controls.append(
#                 ft.Container(
#                     content=ft.Text(
#                         "No sales for this date",
#                         size=14,
#                         color=ft.Colors.BLACK54,
#                         text_align=ft.TextAlign.CENTER,
#                     ),
#                     padding=10,
#                 )
#             )
#         page.update()

#     # Initial display
#     update_sales_display()

#     # Gradient background
#     background = ft.Container(
#         gradient=ft.LinearGradient(
#             begin=ft.Alignment(-1, -1),
#             end=ft.Alignment(1, 1),
#             colors=[ft.Colors.ORANGE_200, ft.Colors.ORANGE_400, ft.Colors.ORANGE_600],
#         ),
#         expand=True,
#     )

#     # Main content container
#     sales_content = ft.Container(
#         content=ft.Column(
#             [
#                 ft.Container(
#                     content=ft.Text(
#                         "Sales by Date",
#                         size=24,
#                         weight=ft.FontWeight.BOLD,
#                         color=ft.Colors.WHITE,
#                         font_family="Roboto",
#                         text_align=ft.TextAlign.CENTER,
#                     ),
#                     shadow=ft.BoxShadow(
#                         blur_radius=8,
#                         spread_radius=1,
#                         color=ft.Colors.BLACK26,
#                     ),
#                     padding=8,
#                 ),
#                 date_picker_button,
#                 ft.Container(
#                     content=sales_list,
#                     bgcolor=ft.Colors.WHITE,
#                     border_radius=10,
#                     padding=10,
#                     shadow=ft.BoxShadow(
#                         blur_radius=15,
#                         spread_radius=3,
#                         color=ft.Colors.BLACK26,
#                     ),
#                     margin=ft.margin.symmetric(horizontal=10, vertical=20),
#                     height=400,
#                 ),
#                 # ft.ElevatedButton(
#                 #     content=ft.Row(
#                 #         [
#                 #             ft.Icon(ft.Icons.ARROW_BACK, color=ft.Colors.BLUE_700, size=20),
#                 #             ft.Text("Back to Dashboard", color=ft.Colors.BLUE_700, weight=ft.FontWeight.BOLD, size=14),
#                 #         ],
#                 #         alignment=ft.MainAxisAlignment.CENTER,
#                 #         spacing=8,
#                 #     ),
#                 #     style=ft.ButtonStyle(
#                 #         shape=ft.RoundedRectangleBorder(radius=10),
#                 #         bgcolor=ft.Colors.WHITE,
#                 #         padding=10,
#                 #         elevation={"pressed": 2, "": 6},
#                 #     ),
#                 #     on_click=lambda e: page.go("/dashboard"),
#                 #     opacity=1.0,
#                 #     on_hover=lambda e: setattr(e.control, 'opacity', 0.8 if e.data == "true" else 1.0) or e.control.update(),
#                 # ),
#             ],
#             alignment=ft.MainAxisAlignment.CENTER,
#             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#             spacing=10,
#         ),
#         width=min(page.width, 370),
#         alignment=ft.alignment.center,
#     )

#     # Stack the gradient background and content
#     return ft.Stack(
#         [
#             background,
#             sales_content,
#         ],
#         expand=True,
#     )



import flet as ft
import datetime

def sale_view(page: ft.Page, db: 'Database'):
    page.title = "Sales"
    page.bgcolor = ft.Colors.BLACK
    page.padding = 0

    # DatePicker for date selection
    selected_date = datetime.datetime.now()

    def update_sales_by_date(e):
        nonlocal selected_date
        selected_date = e.control.value
        date_picker.open = False
        update_sales_display()
        page.update()

    date_picker = ft.DatePicker(
        first_date=datetime.datetime(year=2000, month=1, day=1),
        last_date=datetime.datetime(year=2050, month=12, day=31),
        value=selected_date,
        on_change=update_sales_by_date,
        on_dismiss=lambda e: page.update()
    )

    def show_date_picker(e):
        page.dialog = date_picker
        date_picker.open = True
        page.overlay.append(date_picker)
        page.update()

    date_picker_button = ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.CALENDAR_MONTH, color=ft.Colors.BLUE_700, size=20),
                ft.Text("Pick Date", color=ft.Colors.BLUE_700, weight=ft.FontWeight.BOLD, size=14),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        ),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            bgcolor=ft.Colors.WHITE,
            padding=10,
            elevation={"pressed": 2, "": 6},
        ),
        on_click=show_date_picker,
        opacity=1.0,
        on_hover=lambda e: setattr(e.control, 'opacity', 0.8 if e.data == "true" else 1.0) or e.control.update(),
    )

    # Display sales
    sales_list = ft.ListView(
        spacing=10,
        padding=10,
        auto_scroll=True,
    )

    def update_sales_display():
        sales_list.controls.clear()
        orders = db.get_orders_by_date(selected_date.strftime("%Y-%m-%d"))
        if orders:
            total_sales = sum(order["total"] for order in orders)
            sales_list.controls.append(
                ft.Text(
                    f"Sales on {selected_date.strftime('%Y-%m-%d')}:",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK87,
                )
            )
            for order in orders:
                items = db.get_order_items(order["order_id"])
                items_display = ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Order Items", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
                            ft.ListView(
                                controls=[
                                    ft.Row(
                                        [
                                            ft.Text(
                                                f"{item['item_name']} x {item['quantity']}",
                                                size=10,
                                                color=ft.Colors.BLACK87,
                                                max_lines=1,
                                            ),
                                            ft.Text(
                                                f"Rs{item['total']:.2f}",
                                                size=10,
                                                weight=ft.FontWeight.BOLD,
                                                color=ft.Colors.GREEN_700,
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    ) for item in items
                                ],
                                spacing=5,
                                padding=5,
                                auto_scroll=True,
                            ),
                        ],
                        spacing=5,
                    ),
                    bgcolor=ft.Colors.WHITE,
                    padding=5,
                    border_radius=8,
                    shadow=ft.BoxShadow(blur_radius=5, spread_radius=1, color=ft.Colors.BLACK12),
                    margin=ft.margin.only(left=5, right=5, top=5),
                    width=340,
                    visible=False,
                )

                def toggle_details(e):
                    items_display.visible = not items_display.visible
                    page.update()

                sales_list.controls.append(
                    ft.GestureDetector(
                        content=ft.Container(
                            content=ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Text(
                                                f"Order ID: {order['order_id'][:8]}... | {order['order_type'].replace('_', ' ').title()} | {order['order_date']}",
                                                size=12,
                                                weight=ft.FontWeight.W_500,
                                                color=ft.Colors.BLACK87,
                                                max_lines=1,
                                            ),
                                            ft.Text(
                                                f"Rs{order['total']:.2f}",
                                                size=12,
                                                weight=ft.FontWeight.BOLD,
                                                color=ft.Colors.GREEN_700,
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    ),
                                    ft.Text(
                                        f"Table: {order['table_number'] or 'N/A'} | Name: {order['customer_name'] or 'N/A'} | Number: {order['customer_number'] or 'N/A'}",
                                        size=10,
                                        color=ft.Colors.BLACK54,
                                        max_lines=1,
                                    ),
                                    items_display,
                                ],
                                spacing=5,
                            ),
                            bgcolor=ft.Colors.WHITE,
                            padding=10,
                            border_radius=8,
                            shadow=ft.BoxShadow(blur_radius=5, spread_radius=1, color=ft.Colors.BLACK12),
                            width=340,
                        ),
                        on_tap=toggle_details,
                        on_hover=lambda e: setattr(e.control.content, 'opacity', 0.8 if e.data == "true" else 1.0) or e.control.content.update(),
                    )
                )
            sales_list.controls.append(
                ft.Text(
                    f"Total Sales: Rs{total_sales:.2f}",
                    size=14,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK87,
                    text_align=ft.TextAlign.RIGHT,
                )
            )
        else:
            sales_list.controls.append(
                ft.Container(
                    content=ft.Text(
                        "No sales for this date",
                        size=14,
                        color=ft.Colors.BLACK54,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    padding=10,
                    width=340,
                )
            )
        page.update()

    # Initial display
    update_sales_display()

    # Gradient background
    background = ft.Container(
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=[ft.Colors.ORANGE_200, ft.Colors.ORANGE_400, ft.Colors.ORANGE_600],
        ),
        expand=True,
    )

    # Main content container
    sales_content = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Text(
                        "Sales by Date",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                        font_family="Roboto",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    shadow=ft.BoxShadow(
                        blur_radius=8,
                        spread_radius=1,
                        color=ft.Colors.BLACK26,
                    ),
                    padding=8,
                ),
                date_picker_button,
                ft.Container(
                    content=sales_list,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=10,
                    padding=10,
                    shadow=ft.BoxShadow(
                        blur_radius=15,
                        spread_radius=3,
                        color=ft.Colors.BLACK26,
                    ),
                    margin=ft.margin.symmetric(horizontal=10, vertical=20),
                    height=400,
                    width=340,
                ),
                # ft.ElevatedButton(
                #     content=ft.Row(
                #         [
                #             ft.Icon(ft.Icons.ARROW_BACK, color=ft.Colors.BLUE_700, size=20),
                #             ft.Text("Back to Dashboard", color=ft.Colors.BLUE_700, weight=ft.FontWeight.BOLD, size=14),
                #         ],
                #         alignment=ft.MainAxisAlignment.CENTER,
                #         spacing=8,
                #     ),
                #     style=ft.ButtonStyle(
                #         shape=ft.RoundedRectangleBorder(radius=10),
                #         bgcolor=ft.Colors.WHITE,
                #         padding=10,
                #         elevation={"pressed": 2, "": 6},
                #     ),
                #     on_click=lambda e: page.go("/dashboard"),
                #     opacity=1.0,
                #     on_hover=lambda e: setattr(e.control, 'opacity', 0.8 if e.data == "true" else 1.0) or e.control.update(),
                # ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        width=min(page.width, 360),
        alignment=ft.alignment.center,
    )

    # Stack the gradient background and content
    return ft.Stack(
        [
            background,
            sales_content,
        ],
        expand=True,
    )
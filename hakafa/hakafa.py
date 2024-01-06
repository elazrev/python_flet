import flet as ft
from flet import TextField, Checkbox, ElevatedButton, TextButton, Text, Row, Column
from flet_core.control_event import ControlEvent
import customers as table
import time
import json


def main(page: ft.Page) -> None:
    page.title = 'HaKafa'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 410
    page.window_height = 500
    page.window_resizable = False
    page.scroll = ft.ScrollMode.ALWAYS
    page.rtl = True
    page.snack_bar = ft.SnackBar(
        content=ft.Text("Hello, world!"),
        action="Alright!",
    )




    # Setups Fields
    text_user_first_name: TextField = TextField(label='שם פרטי', text_align=ft.TextAlign.RIGHT, width=200)
    text_user_last_name: TextField = TextField(label='שם משפחה', text_align=ft.TextAlign.RIGHT, width=200)
    text_user_phone_number: TextField = TextField(label='מספר טלפון', text_align=ft.TextAlign.RIGHT, width=200,
                                                  keyboard_type=ft.KeyboardType.PHONE)
    add_user_phone_number: TextField = TextField(label='מספר טלפון', text_align=ft.TextAlign.RIGHT, width=200,
                                                 keyboard_type=ft.KeyboardType.PHONE)

    button_submit: ElevatedButton = ElevatedButton(text='מעבר למאזן', width=200, disabled=True)
    button_add_costumer: ElevatedButton = ElevatedButton(text='לקוח חדש')
    button_submit_customer: ElevatedButton = ElevatedButton(text='הכנס לקוח חדש', width=200, disabled=True)
    button_list_customers: ElevatedButton = ElevatedButton(text='רשימת לקוחות')
    home_button: ft.IconButton = ft.IconButton(icon=ft.icons.HOME, disabled=True)
    main_button: ft.IconButton = ft.IconButton(icon=ft.icons.EXIT_TO_APP_SHARP, icon_color=ft.colors.RED_ACCENT, tooltip='exit')
    list_button: ft.IconButton = ft.IconButton(icon=ft.icons.LIST_ALT_SHARP, disabled=True)
    request_center: ft.ElevatedButton = ft.ElevatedButton(text='בקשות', width=200)
    text_send_request: TextField = ft.TextField(label="בקשה חדשה", text_align=ft.TextAlign.RIGHT, width=200)
    send_request_btn: ElevatedButton = ft.ElevatedButton(text='שלח',
                                                         bgcolor=ft.colors.GREEN_300,
                                                         disabled=True,
                                                         )


    def exit_btn(e):
        text_user_phone_number = None
        list_button.disabled = True
        home_button.disabled = True
        home_button.icon_color = None
        start_page(e)

    def validate(e: ControlEvent) -> None:
        if text_user_phone_number.value:
            button_submit.disabled = False
        else:
            button_submit.disabled = True

        page.update()

    def validate_add(e: ControlEvent) -> None:
        if all([text_user_first_name.value, text_user_last_name.value, add_user_phone_number.value]):
            button_submit_customer.disabled = False
        else:
            button_submit_customer.disabled = True

        page.update()

    def validate_request(e: ControlEvent) -> None:
        if text_send_request.value:
            if len(text_send_request.value) >= 2:
                send_request_btn.disabled = False
                send_request_btn.data = text_send_request.value
            page.update()

    def start_page(e: ControlEvent) -> None:
        page.clean()

        page.add(
            Row(
                controls=[
                    Column(
                        [
                            text_user_phone_number,
                            button_submit
                        ]
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,

            )
        )

    def first_page(e: ControlEvent) -> None:
        if text_user_phone_number:
            home_button.disabled = False
            home_button.icon_color = ft.colors.CYAN

        if text_user_phone_number.value == '1111':
            list_button.disabled = False
            page.clean()
            page.add(
                Row(
                    [
                    ],
                    alignment=ft.MainAxisAlignment.END
                ),
                Row(
                    controls=[Text(value=f"ברוך הבא מנהל!", size=20)],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                Row(controls=[button_add_costumer, button_list_customers], alignment=ft.MainAxisAlignment.CENTER),
                Row(controls=[request_center], alignment=ft.MainAxisAlignment.CENTER),


            )
        else:
            if table.get_name(text_user_phone_number.value):
                balance = table.get_balance(text_user_phone_number.value)["balance"]
                page.clean()
                page.add(
                    Row(
                        [
                        ],
                        alignment=ft.MainAxisAlignment.END
                    ),
                    Row(
                        controls=[Text(value=f"ברוך הבא {table.get_name(text_user_phone_number.value)[0]}", size=20)],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    Row(
                        controls=[Text(value=f"המאזן שלך הינו", size=15, color=ft.colors.BLUE_800)],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    Row(
                        controls=[Text(value=f"{table.get_balance(text_user_phone_number.value)['balance']}", size=15,
                                       color=ft.colors.GREEN if int(table.get_balance(text_user_phone_number.value)["balance"]) >= 0
                                       else ft.colors.RED)],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    Row(
                        controls=[Text(value=f"תאריך עריכה", size=10)],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    Row(
                        controls=[Text(value=f"{table.get_balance(text_user_phone_number.value)['update_date']}", size=10)],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                [
                                    ft.ListTile(
                                        leading=ft.Icon(ft.icons.MESSAGE),
                                        title=ft.Text("בקשות לתשלום"),
                                    ),
                                    ft.Row(
                                        [
                                         text_send_request,
                                         ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                    ft.Row(
                                        [
                                            send_request_btn,
                                            #request_list_dialog,
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                                    ),
                                ]
                            ),
                            width=400,
                            padding=10,
                        )
                    )
                )
            else:
                home_button.disabled = True
                home_button.icon_color = None
                page.clean()
                page.add(
                    Row(
                        controls=[
                            Column(
                                [
                                    Text(
                                        value="אינך מחובר למערכת, נסה שנית"
                                    ),
                                    main_button,
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    )
                )

    def send_request(e):
        new_comment = e.control.data
        print(new_comment)
        table.add_comment(text_user_phone_number.value, new_comment)
        print('done!')

    def add_customer(e: ControlEvent) -> None:
        page.clean()
        page.add(
            Row(
                [
                ],
                alignment=ft.MainAxisAlignment.END
            ),
            Row(
                controls=[
                    Column(
                        [
                            text_user_first_name,
                            text_user_last_name,
                            add_user_phone_number,
                            button_submit_customer
                        ]
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )

        )

    def added(e: ControlEvent) -> None:
        table.add_customer(add_user_phone_number.value, text_user_first_name.value, text_user_last_name.value)
        page.clean()
        page.add(
            Row(
                [
                ],
                alignment=ft.MainAxisAlignment.END
            ),
            Row(
                controls=[
                    Column(
                        [Text(value=f'נוסף בהצלחה!\n{text_user_first_name.value}')],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ], alignment=ft.MainAxisAlignment.CENTER
            )
        )
        time.sleep(2)
        customers_list(e)

    def delete_page(e):
        page.clean()
        page.add(
            Row(
                [

                ],
                alignment=ft.MainAxisAlignment.END
            ),
            Row(
                controls=[
                    Row(
                        [Text(value=f'האם ברצונך למחוק את\n'
                                    f'{e.control.data["first_name"]} {e.control.data["last_name"]}')],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ], alignment=ft.MainAxisAlignment.CENTER
            ),
            Row(
                controls=[
                    Row(
                        [
                            ElevatedButton(text='כן',
                                           color=ft.colors.RED,
                                           on_click=delete_customer,
                                           data=e.control.data),
                            ElevatedButton(text='בטל',
                                           color=ft.colors.BLUE_800,
                                           on_click=customers_list),
                         ]
                    )
                ], alignment=ft.MainAxisAlignment.CENTER
            )
        )

    def delete_customer(e):

        try:
            print(f"you selected phone number = {e.control.data['phone']}")
            table.remove_customer(e.control.data['phone'])
            print("Successes")
            customers_list(e)

        except Exception as e:
            print(e)
            print("Error")

    def customer_page(e: ControlEvent) -> None:

        balance = json.loads(e.control.data['balance'])['balance']
        update_date = json.loads(e.control.data['balance'])['update_date']
        done_btn = ft.ElevatedButton(text="סיום",
                                      color=ft.colors.WHITE,
                                      bgcolor=ft.colors.GREEN_300,
                                      data=e.control.data,
                                      opacity=75)
        if update_date is None:
            update_date = "לא נערך"

        text_balance = ft.TextField(value=balance,
                                    text_align=ft.TextAlign.RIGHT,
                                    width=100,
                                    color=ft.colors.GREEN if int(balance) >= 0
                                    else ft.colors.RED)

        def minus_click(e):
            text_balance.value = str(int(text_balance.value) - 1)
            page.update()

        def plus_click(e):
            text_balance.value = str(int(text_balance.value) + 1)
            page.update()

        def done(e):
            try:

                int(text_balance.value) * 1
                table.change_balance(phone_number=e.control.data['phone'], new_balance=text_balance.value)
                customers_list(e)
            except Exception as er:
                page.snack_bar = ft.SnackBar(
                    content=Text('משהו השתבש, נסה שוב'),
                    open=True
                )
                error_msg = "ערך לא חוקי!", er
                print(error_msg)
                text_balance.value = balance
                page.update()

        page.clean()
        page.add(
            Row(
                [

                ],
                alignment=ft.MainAxisAlignment.END
            ),
            Row(
                controls=[Text(value=f"{e.control.data['first_name']} {e.control.data['last_name']}", size=20)],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            Row(
                controls=[Text(value=f"{e.control.data['phone']}", size=14, color=ft.colors.GREY)],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            Row(
                controls=[Text(value=f"יתרה", size=15, color=ft.colors.BLUE_800)],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            Row(
                controls=[
                    Text(f"נערך לאחרונה ב {update_date}")
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            Row(
                [
                    ft.IconButton(ft.icons.REMOVE, on_click=minus_click, data=e.control.data),
                    text_balance,
                    ft.IconButton(ft.icons.ADD, on_click=plus_click, data=e.control.data),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            Row(
                controls=[
                    done_btn
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
        )
        done_btn.on_click = done
        page.update()

    def customers_list(e: ControlEvent) -> None:

        search_bar = TextField(label='חיפוש', text_size=13)

        customer_lst = table.customers_list()

        page.clean()
        page.add(
            Row(
                [ft.Text(value="רשימת לקוחות", size=20)],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            Row(
                [
                    Column(
                        [search_bar]
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
                )
            )


        r = ft.DataTable(
            column_spacing=5,
            divider_thickness=3,
            columns=[
                ft.DataColumn(ft.Text("שם פרטי")),
                ft.DataColumn(ft.Text("שם משפחה")),
                ft.DataColumn(ft.Text("מאזן"), numeric=True),
                ft.DataColumn(ft.Text("פעולות"), numeric=False),
            ],
        )

        page.add(Row([r], alignment=ft.MainAxisAlignment.CENTER))

        for customer in customer_lst:
            phone = customer['phone']
            balance = table.get_balance(phone)['balance']

            r.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.TextButton(
                            customer['first_name'],
                            data=customer,
                            on_click=customer_page)),
                        ft.DataCell(ft.Text(customer['last_name'])),
                        ft.DataCell(ft.Text(balance, color=ft.colors.RED if int(balance) < 0
                        else ft.colors.GREEN)),
                        ft.DataCell(
                            Row(
                                spacing=0,
                                controls=[

                                    ft.IconButton(
                                        icon=ft.icons.CREATE_OUTLINED,
                                        tooltip="עריכה",
                                        #on_click=customer_page(e,(customer[0]).first()),
                                        disabled=True,
                                        icon_size=12,
                                        data=customer,
                                    ),
                                    ft.IconButton(
                                        ft.icons.DELETE_OUTLINE,
                                        tooltip="מחק",
                                        on_click=delete_page,
                                        icon_size=12,
                                        icon_color=ft.colors.RED_200,
                                        data=customer,
                                    ),
                                ]
                            )
                        ),
                    ]
                )
            )
            page.update()

    # checkbox_signup.on_change = validate
    text_user_first_name.on_change = validate_add
    text_user_last_name.on_change = validate_add
    text_user_phone_number.on_change = validate
    add_user_phone_number.on_change = validate_add
    button_submit.on_click = first_page
    button_add_costumer.on_click = add_customer
    button_submit_customer.on_click = added
    home_button.on_click = first_page
    main_button.on_click = exit_btn
    button_list_customers.on_click = customers_list
    list_button.on_click = customers_list
    text_send_request.on_change = validate_request
    send_request_btn.on_click = send_request


    #NavBar
    page.appbar = ft.AppBar(
        leading=main_button,
        leading_width=40,
        title=ft.Text("הקפה בקפה"),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            list_button,
            home_button,
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="אודותינו"),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(text="פריט"),
                ],

            ),
        ],
    )

    # Render the page signup page
    page.add(
        Row(
            controls=[
                Column(
                    [
                        # text_user_first_name,
                        # text_user_last_name,
                        text_user_phone_number,
                        # checkbox_signup,
                        button_submit
                    ]
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )


if __name__ == "__main__":
    ft.app(target=main)  # , view=ft.AppView.WEB_BROWSER)

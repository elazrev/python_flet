import flet as ft
from flet import TextField, ElevatedButton, TextButton, Text, Row, Column
from flet_core.control_event import ControlEvent
import customers as table
import time
import json


# The app for management of deaths and customers for Merav!
def main(page: ft.Page) -> None:
    page.title = 'HaKafa'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.SYSTEM
    # page.window_width = 410
    # page.window_height = 500
    page.window_resizable = True
    page.scroll = ft.ScrollMode.ALWAYS
    page.rtl = True
    page.snack_bar = ft.SnackBar(content=Text('ערב טוב'), action="סבבה")

    # Setup buttons and fields
    """navbar buttons"""
    home_button: ft.IconButton = ft.IconButton(
        icon=ft.icons.HOME,
        disabled=True,
        tooltip='Home',
        visible=False
    )
    main_button: ft.IconButton = ft.IconButton(
        icon=ft.icons.EXIT_TO_APP_SHARP,
        icon_color=ft.colors.RED_ACCENT,
        disabled=True,
        tooltip='Exit',
        visible=False
    )
    list_button: ft.IconButton = ft.IconButton(
        icon=ft.icons.LIST_ALT_SHARP,
        disabled=True,
        visible=False,
    )

    """login page"""
    text_user_phone_number: TextField = TextField(
        label='קוד גישה',
        text_align=ft.TextAlign.RIGHT,
        width=200,
        keyboard_type=ft.KeyboardType.PHONE,
        password=True

    )
    button_submit: ElevatedButton = ElevatedButton(
        text='כניסה',
        width=200,
        disabled=True)

    """home page"""
    # Client
    text_new_request: TextField = TextField(
        label='בקשה חדשה',
        width=190,
        text_align=ft.TextAlign.RIGHT
    )
    submit_request_btn: ElevatedButton = ft.ElevatedButton(
        text='שלח',
        bgcolor=ft.colors.YELLOW_600,
        disabled=True,
        color=ft.colors.WHITE
    )
    client_request_list: ElevatedButton = ft.ElevatedButton(
        text='בקשות בהמתנה',
        bgcolor=ft.colors.GREEN_100,
        disabled=False,
        color=ft.colors.WHITE
    )

    # Manager
    add_customer_btn: ElevatedButton = ElevatedButton(text='לקוח חדש')
    list_customers_btn: ElevatedButton = ElevatedButton(text='רשימת לקוחות')
    manager_request_list: ElevatedButton = ElevatedButton(text='בקשות')

    """add client page"""
    add_client_first_name: TextField = TextField(
        label='שם פרטי',
        text_align=ft.TextAlign.RIGHT,
        width=200
    )
    add_client_last_name: TextField = TextField(
        label='שם משפחה',
        text_align=ft.TextAlign.RIGHT,
        width=200
    )
    add_client_phone_number: TextField = TextField(
        label='מספר טלפון',
        text_align=ft.TextAlign.RIGHT,
        width=200,
        keyboard_type=ft.KeyboardType.PHONE
    )
    submit_add_btn: ElevatedButton = ElevatedButton(
        text='הכנס לקוח חדש',
        width=200,
        disabled=True
    )
    """Client Page View"""
    comments_list_btn: ElevatedButton = ElevatedButton(
        text="רשימת בקשות לקוח",
        width=200,
        disabled=True
    )

    # Validations and actions

    def login_validate(e: ControlEvent) -> None:
        """validates if the field is full"""
        if text_user_phone_number.value:
            button_submit.disabled = False
        else:
            button_submit.disabled = True

        # Update page for enable button
        page.update()

    def add_user_validate(e: ControlEvent) -> None:
        """validates if the fields are full"""
        if all(
                [
                    add_client_first_name.value,
                    add_client_last_name.value,
                    add_client_phone_number.value
                ]
        ):
            submit_add_btn.disabled = False
        else:
            submit_add_btn.disabled = True

        page.update()

    def request_validate(e: ControlEvent) -> None:
        if text_new_request.value:
            if len(text_new_request.value) >= 2:
                submit_request_btn.disabled = False
        page.update()

    def exit_actions(e: ControlEvent) -> None:
        """disables all none relevant buttons"""
        text_user_phone_number.value = None
        list_button.visible = False
        home_button.disabled = True
        home_button.visible = False
        main_button.visible = False
        button_submit.disabled = True
        text_new_request.value = None
        login_page(e)

    """ App Pages Area"""

    # Login Page:
    def login_page(e: ControlEvent) -> None:
        page.route = '/login'
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
                alignment=ft.MainAxisAlignment.CENTER
            )
        )

    # Welcome_Page
    def home_page(e: ControlEvent) -> None:
        page.route = '/home'
        page.clean()
        home_button.disabled = False
        home_button.icon_color = ft.colors.CYAN_ACCENT
        main_button.visible = True
        main_button.disabled = False

        # Manager Interface
        if text_user_phone_number.value == '1111':
            home_button.visible = True
            list_button.disabled = False
            list_button.visible = True
            page.add(
                Row(
                    [
                    ],
                    alignment=ft.MainAxisAlignment.END
                ),
                Row(
                    controls=[
                        Text(
                            value=f"ברוך הבא מנהל!",
                            size=20
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                Row(
                    controls=[
                        add_customer_btn,
                        list_customers_btn
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                Row(
                    controls=[
                        manager_request_list
                    ],
                    alignment=ft.MainAxisAlignment.CENTER),
            )
            page.update()
        else:
            # Client Interface
            if table.get_name(text_user_phone_number.value):
                # Pull comments by phone number
                try:
                    comments_list = table.customer_comment_list(text_user_phone_number.value)
                except Exception as e:
                    print(e)
                    comments_list = [{}]
                lst = ft.DataTable(
                    column_spacing=8,
                    divider_thickness=4,
                    columns=[
                        ft.DataColumn(Text("תוכן")),
                        ft.DataColumn(Text("תאריך")),
                    ]
                )

                dlg = ft.AlertDialog(
                    content=Row(
                        [
                            lst
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                )
                try:
                    for comment in comments_list:
                        text = comment['text']
                        time = comment['timestamp']

                        lst.rows.append(
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(
                                        Text(
                                            text
                                        )
                                    ),
                                    ft.DataCell(
                                        Text(
                                            time
                                        )
                                    )
                                ]
                            )
                        )
                        page.update()

                except Exception as e:
                    print(e)

                def new_comment(e):
                    try:
                        submit_request_btn.data = text_new_request.value
                        comment_text = e.control.data

                        table.add_comment(
                            phone_number=text_user_phone_number.value,
                            comment_text=comment_text
                        )

                        page.snack_bar.content = Text('נוסף בהצלחה')
                        page.snack_bar.open = True
                        page.update()
                        text_new_request.value = None
                        home_page(e)
                    except Exception as e:
                        print(e)

                def open_dlg(e):
                    page.dialog = dlg
                    dlg.open = True
                    page.update()

                client_request_list.on_click = open_dlg
                text_new_request.on_change = request_validate
                submit_request_btn.on_click = new_comment

                balance: dict = table.get_balance(text_user_phone_number.value)
                first_name: str = f'{table.get_name(text_user_phone_number.value)[0]}'
                last_name: str = f'{table.get_name(text_user_phone_number.value)[1]}'
                page.clean()
                page.add(
                    Row(
                        [
                        ],
                        alignment=ft.MainAxisAlignment.END
                    ),
                    Row(
                        controls=[
                            Text(
                                value=f"{first_name} {last_name}\nשלום!",
                                size=20,
                                text_align=ft.TextAlign.CENTER
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    Row(
                        controls=[
                            Text(
                                value=f"המאזן שלך הינו",
                                size=15,
                                color=ft.colors.BLUE_800
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    Row(
                        controls=[
                            Text(
                                value=f"{balance['balance']}",
                                size=15,
                                color=ft.colors.GREEN if int(balance["balance"]) >= 0 else ft.colors.RED,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    Row(
                        controls=[
                            Text(
                                value=f"תאריך עריכה",
                                size=10
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    Row(
                        controls=[
                            Text(
                                value=f"{balance['update_date']}",
                                size=10
                            )
                        ],
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
                                            text_new_request,
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                    ft.Row(
                                        [
                                            submit_request_btn,
                                            client_request_list
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                ]
                            ),
                            width=400,
                            padding=10,
                        )
                    )
                )
                page.update()
            else:

                main_button.visible = True

                def new_customer_request_view(e: ControlEvent) -> None:
                    page.route = "/new_request"

                    def successes_req(e) -> None:
                        try:
                            import time
                            table.add_new_request(
                                add_client_phone_number.value,
                                add_client_first_name.value,
                                add_client_last_name.value
                            )
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
                                            [Text(value=f'נוסף בהצלחה!\n{add_client_first_name.value}')],
                                            alignment=ft.MainAxisAlignment.CENTER
                                        )
                                    ], alignment=ft.MainAxisAlignment.CENTER
                                )
                            )

                            time.sleep(2)
                            login_page(e)

                        except Exception as e:
                            #raise e
                            print(e)
                            add_client_phone_number.value = None
                            page.snack_bar = ft.SnackBar(content=Text('something went wrong'), action="OK", open=True)
                            page.update()
                    main_button.disabled = False
                    submit_add_btn.text = "בקשה חדשה"
                    submit_add_btn.on_click = successes_req
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
                                        add_client_first_name,
                                        add_client_last_name,
                                        add_client_phone_number,
                                        submit_add_btn
                                    ]
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    )
                    page.update()

                home_button.visible = False
                home_button.disabled = True
                main_button.disabled = True
                page.add(
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                [
                                    ft.ListTile(
                                        title=ft.Text(
                                            "הקוד שהזנת לא קיים במערכת...",
                                            color=ft.colors.BLACK45
                                        ),

                                    ),
                                    ft.Row(
                                        [
                                            ft.IconButton(
                                                icon=ft.icons.BACKSPACE,
                                                on_click=login_page,
                                                tooltip="חזרה להתחברות"

                                            )
                                            # request_list_dialog,
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                    ft.Row(
                                        [
                                            ft.ElevatedButton(
                                                "להרשמה",
                                                on_click=new_customer_request_view
                                            )
                                            # request_list_dialog,
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                ]
                            ),
                            width=400,
                            padding=10,
                        )
                    )
                )
                page.update()

    # Customers List
    def customers_list_view(e: ControlEvent) -> None:
        page.route = '/list_view'

        def delete_customer(e):
            try:
                table.remove_customer(e.control.data['phone'])
                customers_list_view(e)
                page.update()

            except Exception as e:
                page.snack_bar.content = 'לא ניתן למחוק'
                page.snack_bar.open = True
                page.update()
                customers_list_view(e)

        def delete_page_view(e) -> None:
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
                                               on_click=customers_list_view),
                            ]
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER
                )
            )

        def edit_customer(e):
            pass

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
            column_spacing=9,
            divider_thickness=2,
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
                        ft.DataCell(
                            ft.TextButton(
                                customer['first_name'],
                                data=customer,
                                on_click=customer_page_view)),
                        ft.DataCell(ft.Text(customer['last_name'])),
                        ft.DataCell(ft.Text(balance, color=ft.colors.RED if int(balance) < 0
                        else ft.colors.GREEN)),
                        ft.DataCell(
                            Row(
                                spacing=0,
                                controls=[
                                    ft.IconButton(
                                        ft.icons.EMOJI_EMOTIONS_OUTLINED if not table.request_bool(
                                            phone) else ft.icons.WARNING_AMBER,
                                        tooltip="אין בקשות פתוחות" if not table.request_bool(
                                            phone) else "יש בקשות פתוחות",

                                        icon_size=12,
                                        icon_color=ft.colors.GREEN if not table.request_bool(
                                            phone) else ft.colors.BROWN_100,
                                        data=customer,
                                    ),
                                    ft.IconButton(
                                        ft.icons.DELETE_OUTLINE,
                                        tooltip="מחק",
                                        on_click=delete_page_view,
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
        page.update()

    # Specific Customer view
    def customer_page_view(e: ControlEvent) -> None:
        data = e.control.data
        comments_list_btn.disabled = True

        lst = ft.DataTable(
            column_spacing=5,
            divider_thickness=2,
            horizontal_lines=ft.BorderSide(width=3),
            columns=[
                ft.DataColumn(Text("תוכן")),
                ft.DataColumn(Text("תאריך")),
                ft.DataColumn(Text("מחק")),
            ]
        )

        dlg = ft.AlertDialog(
            content=Row(
                [
                    lst
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                width=250,
            )
        )
        if table.request_bool(e.control.data['phone']):
            comments_list_btn.disabled = False
            page.update()
            # list of comments for customer
            try:
                comments_list = table.customer_comment_list(e.control.data['phone'])
            except Exception as e:
                print(e)
                comments_list = []

            dlg.open = False
            comment_index = -1

            def dlg_close(e):
                page.dialog = dlg
                dlg.open = False
                page.update()

            def delete_comment(e):
                phone = e.control.data[0]
                index = e.control.data[1]
                table.delete_comment(phone, index)
                e.control.data = data
                dlg_close(e)
                page.update()
                customer_page_view(e)

            page.update()

            try:
                for comment in comments_list:
                    comment_index += 1
                    text = comment['text']
                    time_stamp = comment['timestamp']
                    lst.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(
                                    Text(
                                        text,
                                        size=10
                                    )
                                ),
                                ft.DataCell(
                                    Text(
                                        time_stamp,
                                        size=9,
                                        color=ft.colors.GREY
                                    )
                                ),
                                ft.DataCell(
                                    ft.IconButton(
                                        icon=ft.icons.DELETE_SWEEP,
                                        data=(e.control.data['phone'], comment_index, text),
                                        on_click=delete_comment
                                    )

                                ),
                            ]
                        )
                    )
                    page.update()

            except Exception as e:

                print(e)

        else:
            dlg.open = False

        def open_dlg(e):
            page.dialog = dlg
            dlg.open = True
            page.update()

        comments_list_btn.on_click = open_dlg
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

        def coins(e):
            text_balance.value = str(int(text_balance.value) + int(e.control.data))
            page.update()

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
                customers_list_view(e)
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
                [
                    comments_list_btn
                ],
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

        coins_lst = [-6, -7, -8, -15, -16, -20, -25, -30, -37, -40, -45]
        coins_grid = ft.GridView(
            expand=5,
            runs_count=3,
            max_extent=60,
            child_aspect_ratio=0.6,
            spacing=2,
            run_spacing=4,
        )
        for coin in coins_lst:
            coins_grid.controls.append(
                ft.ElevatedButton(
                    content=ft.Column(
                        [
                            Text(f"{coin}", size=9)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    data=str(coin),
                    on_long_press=coins,
                    bgcolor=ft.colors.YELLOW_50,
                    opacity=75,
                    tooltip=f"{coin}",
                    style=ft.ButtonStyle(shape=ft.CircleBorder(), padding=20),
                )
            )

        page.add(
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.ListTile(
                                leading=ft.Icon(ft.icons.PAYMENTS),
                                title=ft.Text("תשלומים נפוצים"),

                            ),
                            ft.Row(
                                [
                                    coins_grid
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                        ]
                    ),
                    width=400,
                    padding=10,
                )
            )
        )
        page.route = f'/customer/{e.control.data["first_name"]}'

        done_btn.on_click = done
        page.update()

    # New Customer
    def new_customer_view(e: ControlEvent) -> None:
        page.route = "/new_customer"
        submit_add_btn.text = "הכנס לקוח חדש"

        def successes(e) -> None:
            try:
                table.add_customer(
                    add_client_phone_number.value,
                    add_client_first_name.value,
                    add_client_last_name.value
                )
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
                                [Text(value=f'נוסף בהצלחה!\n{add_client_first_name.value}')],
                                alignment=ft.MainAxisAlignment.CENTER
                            )
                        ], alignment=ft.MainAxisAlignment.CENTER
                    )
                )
                time.sleep(2)
                customers_list_view(e)
            except Exception as e:
                print(e)
                add_client_phone_number.value = None
                page.snack_bar = ft.SnackBar(content=Text('something went wrong'), action="OK", open=True)
                page.update()

        submit_add_btn.on_click = successes
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
                            add_client_first_name,
                            add_client_last_name,
                            add_client_phone_number,
                            submit_add_btn
                        ]
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
        page.update()

    def unfinished_requests_view(e: ControlEvent) -> None:
        page.route = "/requests"
        requests_list = table.get_requests_list()

        def delete_click(e):
            try:
                phone = e.control.data['phone']
                table.delete_request(phone)
                page.update()
                page.snack_bar.content = Text('נמחק בהצלחה!')
                page.snack_bar.open = True
                page.update()
                unfinished_requests_view(e)
            except Exception as e:
                print(e)


        def save_click(e):
            try:
                phone = e.control.data["phone"]
                first_name = e.control.data["first_name"]
                last_name = e.control.data["last_name"]
                table.add_customer(phone, first_name, last_name)
                table.delete_request(phone)
                page.snack_bar.content = Text(f"{first_name} נוסף בהצלחה!!")
                page.snack_bar.open = True
                customers_list_view(e)
            except Exception as e:
                print(e)

        page.clean()
        page.add(
            Row(
                [ft.Text(value="רשימת בקשות", size=20)],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        )

        r = ft.DataTable(
            column_spacing=9,
            divider_thickness=2,
            columns=[
                ft.DataColumn(ft.Text("שם פרטי")),
                ft.DataColumn(ft.Text("שם משפחה")),
                ft.DataColumn(ft.Text("טלפון")),
                ft.DataColumn(ft.Text("אשר | מחק")),
            ],
        )

        page.add(Row([r], alignment=ft.MainAxisAlignment.CENTER))

        for customer in requests_list:
            phone = customer['phone']

            r.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.TextButton(
                                customer['first_name'],
                                data=customer,
                                on_click=customer_page_view)),
                        ft.DataCell(ft.Text(customer['last_name'])),
                        ft.DataCell(ft.Text(customer['phone'])),
                        ft.DataCell(
                            Row(
                                spacing=0,
                                controls=[
                                    ft.IconButton(
                                        ft.icons.DATA_SAVER_ON_ROUNDED,
                                        tooltip="שמור",
                                        icon_size=15,
                                        icon_color=ft.colors.GREEN_500,
                                        data=customer,
                                        on_click=save_click
                                    ),
                                    ft.IconButton(
                                        ft.icons.DELETE_OUTLINE,
                                        tooltip="מחק",
                                        icon_size=15,
                                        icon_color=ft.colors.RED_200,
                                        data=customer,
                                        on_click=delete_click
                                    ),
                                ]
                            )
                        ),
                    ]
                )
            )
            page.update()
        page.update()

    def route_change(route):
        # print(f"New route: {route}")
        pass

    # Buttons functionality management
    text_user_phone_number.on_change = login_validate
    button_submit.on_click = home_page
    main_button.on_click = exit_actions
    home_button.on_click = home_page
    list_button.on_click = customers_list_view

    """Client View buttons and fields"""

    """Manager views buttons and fields"""
    list_customers_btn.on_click = customers_list_view
    manager_request_list.on_click = unfinished_requests_view
    add_customer_btn.on_click = new_customer_view
    add_client_first_name.on_change = add_user_validate
    add_client_last_name.on_change = add_user_validate
    add_client_phone_number.on_change = add_user_validate

    page.on_route_change = route_change


    # NavBar
    page.appbar = ft.AppBar(
        leading=main_button,
        leading_width=40,
        title=ft.Text(f"הקפה בקפה "),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            list_button,
            home_button,
            ft.PopupMenuButton(icon=ft.icons.COFFEE_SHARP,
                               items=[
                                   ft.PopupMenuItem(),
                                   ft.PopupMenuItem(text="אודותינו"),
                                   ft.PopupMenuItem(text="Update check"),  # divider

                               ],

                               ),
        ],
    )

    # Rendering Login Page
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
            alignment=ft.MainAxisAlignment.CENTER
        )
    )


ft.app(main)  # view=ft.AppView.WEB_BROWSER)
# if __name__ == "__main__":
#   ft.app(target=main)

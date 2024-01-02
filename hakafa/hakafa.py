import flet as ft
from flet import TextField, Checkbox, ElevatedButton, TextButton, Text, Row, Column
from flet_core.control_event import ControlEvent
import customers as table


def main(page: ft.Page) -> None:
    page.title = 'HaKafa'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 410
    page.window_height = 500
    page.window_resizable = False
    page.scroll = ft.ScrollMode.ALWAYS



    # Setups Fields
    text_user_first_name: TextField = TextField(label='שם פרטי', text_align=ft.TextAlign.RIGHT, width=200)
    text_user_last_name: TextField = TextField(label='שם משפחה', text_align=ft.TextAlign.RIGHT, width=200)
    text_user_phone_number: TextField = TextField(label='מספר טלפון', text_align=ft.TextAlign.RIGHT, width=200,
                                                  keyboard_type=ft.KeyboardType.PHONE)
    add_user_phone_number: TextField = TextField(label='מספר טלפון', text_align=ft.TextAlign.RIGHT, width=200,
                                                 keyboard_type=ft.KeyboardType.PHONE)
    # checkbox_signup:  Checkbox = Checkbox(label='זה אני!', width=200, value=False, opacity=0.75, active_color=ft.colors.GREEN)
    button_submit: ElevatedButton = ElevatedButton(text='מעבר למאזן', width=200, disabled=True)
    button_add_costumer: ElevatedButton = ElevatedButton(text='לקוח חדש')
    button_submit_customer: ElevatedButton = ElevatedButton(text='הכנס לקוח חדש', width=200, disabled=True)
    button_list_customers: ElevatedButton = ElevatedButton(text='רשימת לקוחות')
    home_button: ft.IconButton = ft.IconButton(icon=ft.icons.HOME, icon_color=ft.colors.CYAN)
    main_button: ft.IconButton = ft.IconButton(icon=ft.icons.EXIT_TO_APP_SHARP, icon_color=ft.colors.RED_ACCENT,
                                               on_click=page.logout())

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

    def start_page(e: ControlEvent) -> None:
        page.clean()
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

    def first_page(e: ControlEvent) -> None:
        # print(f"{text_user_first_name.value} {text_user_last_name.value}")
        # print(f"{text_user_phone_number.value}")
        if text_user_phone_number.value == '1111':
            page.clean()
            page.add(
                Row(
                    [
                        home_button,
                        main_button
                    ],
                    alignment=ft.MainAxisAlignment.END
                ),
                Row(
                    controls=[Text(value=f"ברוך הבא מנהל!", size=20)],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                Row(controls=[button_add_costumer, button_list_customers], alignment=ft.MainAxisAlignment.CENTER)

            )
        else:
            if table.get_name(text_user_phone_number.value):
                phone = text_user_phone_number.value
                page.clean()
                page.add(
                    Row(
                        [
                            home_button,
                            main_button
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
                        controls=[Text(value=f"{table.get_name(text_user_phone_number.value)[2]}", size=15,
                                       color=ft.colors.GREEN if table.get_name(text_user_phone_number.value)[2] >= 0
                                       else ft.colors.RED)],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                )
            else:
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
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                )

    def add_customer(e: ControlEvent) -> None:
        page.clean()
        page.add(
            Row(
                [
                    home_button,
                    main_button
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
                    home_button,
                    main_button
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

    def delete_customer(e):

        try:
            print(f"you selected phone number = {e.control.data['phone']}")
            table.remove_customer(e.control.data['phone'])
            print("Successes")
            page.update()

        except Exception as e:
            print(e)
            print("Error")

    def customer_page(e: ControlEvent) -> None:
        page.clean()
        page.add(
            Row(
                [
                    home_button,
                    main_button
                ],
                alignment=ft.MainAxisAlignment.END
            ),
            Row(
                controls=[
                    Column(
                        [
                            Text(value=f'{e.control.data["first_name"]} {e.control.data["last_name"]}', size=20),
                            Text(value=f'יתרה:', size=20),
                            Text(value=f"{e.control.data['balance']}", size=15,
                                 color=ft.colors.GREEN if e.control.data['balance'] >= 0
                                 else ft.colors.RED),

                        ],

                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ], alignment=ft.MainAxisAlignment.CENTER
            )
        )
        page.update()

    def customers_list(e: ControlEvent) -> None:
        customer_lst = table.customers_list()

        page.clean()
        page.add(
            Row(
                [
                    home_button,
                    main_button
                ],
                alignment=ft.MainAxisAlignment.END
            ),
            Row(
                [ft.Text(value="רשימת לקוחות", size=12)],
                alignment=ft.MainAxisAlignment.CENTER,
            ), )
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

            r.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.TextButton(
                            customer['first_name'],
                            data=customer,
                            on_click=customer_page)),
                        ft.DataCell(ft.Text(customer['last_name'])),
                        ft.DataCell(ft.Text(customer['balance'], color=ft.colors.RED if int(customer['balance']) < 0
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
                                        on_click=delete_customer,
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
            print(e.control)
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
    main_button.on_click = start_page
    button_list_customers.on_click = customers_list


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

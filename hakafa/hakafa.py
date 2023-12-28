import flet as ft
from flet import TextField, Checkbox, ElevatedButton, TextButton, Text, Row, Column
from flet_core.control_event import ControlEvent
import customers as table


def main(page: ft.Page) -> None:
    page.title = 'HaKafa'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 400
    page.window_height = 400
    page.window_resizable = False

    # Setups Fields
    text_user_first_name: TextField = TextField(label='שם פרטי', text_align=ft.TextAlign.RIGHT, width=200)
    text_user_last_name: TextField = TextField(label='שם משפחה', text_align=ft.TextAlign.RIGHT, width=200)
    text_user_phone_number: TextField = TextField(label='מספר טלפון', text_align=ft.TextAlign.RIGHT, width=200, keyboard_type=ft.KeyboardType.PHONE)
    add_user_phone_number: TextField = TextField(label='מספר טלפון', text_align=ft.TextAlign.RIGHT, width=200, keyboard_type=ft.KeyboardType.PHONE)
    checkbox_signup:  Checkbox = Checkbox(label='זה אני!', width=200, value=False, opacity=0.75, active_color=ft.colors.GREEN)
    button_submit: ElevatedButton = ElevatedButton(text='מעבר למאזן', width=200, disabled=True)
    button_add_costumer: ElevatedButton = ElevatedButton(text='לקוח חדש')
    button_submit_customer: ElevatedButton = ElevatedButton(text='הכנס לקוח חדש', width=200, disabled=True)
    button_list_customers: ElevatedButton = ElevatedButton(text='רשימת לקוחות')
    home_button: ft.IconButton = ft.IconButton(icon=ft.icons.HOME, icon_color=ft.colors.CYAN)
    main_button: ft.IconButton = ft.IconButton(icon=ft.icons.EXIT_TO_APP_SHARP, icon_color=ft.colors.RED_ACCENT, on_click=page.logout())

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
                            checkbox_signup,
                            button_submit
                        ]
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )

    def first_page(e: ControlEvent) -> None:
        #print(f"{text_user_first_name.value} {text_user_last_name.value}")
        #print(f"{text_user_phone_number.value}")
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
                    controls=[Text(value=f"ברוך הבא {text_user_first_name.value}", size=20)],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                Row(
                    controls=[Text(value=f"המאזן שלך הינו", size=15, color=ft.colors.BLUE_800)],
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
                ],alignment=ft.MainAxisAlignment.CENTER
            )
        )

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
            ),
            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("First name")),
                    ft.DataColumn(ft.Text("Last name")),
                    ft.DataColumn(ft.Text("Age"), numeric=True),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text("John")),
                            ft.DataCell(ft.Text("Smith")),
                            ft.DataCell(ft.Text("43")),
                        ],
                    ),
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text("Jack")),
                            ft.DataCell(ft.Text("Brown")),
                            ft.DataCell(ft.Text("19")),
                        ],
                    ),
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text("Alice")),
                            ft.DataCell(ft.Text("Wong")),
                            ft.DataCell(ft.Text("25")),
                        ],
                    ),
                ],
            )

        )

    checkbox_signup.on_change = validate
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
                     #text_user_first_name,
                     #text_user_last_name,
                     text_user_phone_number,
                     checkbox_signup,
                     button_submit
                    ]
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

if __name__ == "__main__":
    ft.app(target=main) #, view=ft.AppView.WEB_BROWSER)


import asyncio
import random
import flet as ft

from api import ServerManager, get_reactive_ips, get_banned_ips
from database_handler import ban, unban


def create_row_ui(ip: str, on_banned=None, on_unbanned=None):
    if on_banned:
        return ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(
                                    f"IP:    {ip}",
                                    weight="bold",
                                    bgcolor="lightgray",
                                    selectable=True,
                                    max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                ),
                            ],
                            expand=True,
                        ),
                        ft.Column(
                            controls=[
                                ft.IconButton(
                                    icon=ft.Text(
                                        "Ban", size=20, weight="bold", color="red"
                                    ),
                                    on_click=on_banned,
                                )
                            ]
                        ),
                    ]
                ),
            ),
            bgcolor="#201E1E",
        )
    else:
        return ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(
                                    f"IP:    {ip}",
                                    weight="bold",
                                    bgcolor="lightgray",
                                    selectable=True,
                                    max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                ),
                            ],
                            expand=True,
                        ),
                        ft.Column(
                            controls=[
                                ft.IconButton(
                                    icon=ft.Text(
                                        "Unban",
                                        size=20,
                                        weight="bold",
                                        color="green",
                                    ),
                                    on_click=on_unbanned,
                                )
                            ]
                        ),
                    ]
                ),
            ),
            bgcolor="#201E1E",
        )


async def main(page: ft.Page):
    page.title = "Pt.Server"
    page.window_prevent_close = True
    page.keep_on_top = True
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#000000"
    page.padding = 10

    page.is_working = False

    async def keep_alive_heartbeat():
        while True:
            await asyncio.sleep(15)

    page.run_task(keep_alive_heartbeat)

    status_text = ft.Text(
        "🟢 Server Active\n(Double tap anywhere to exit saver)",
        color="#00FF00",
        size=16,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    saver_container = ft.Container(
        content=status_text,
        alignment=ft.Alignment.CENTER,
        expand=True,
    )

    saver_view = ft.GestureDetector(
        content=saver_container,
        on_double_tap=lambda e: page.run_task(toggle_screensaver, False),
        visible=False,
        expand=True,
    )

    async def anti_burn_in_loop():
        alignments = [
            ft.Alignment.TOP_LEFT,
            ft.Alignment.TOP_RIGHT,
            ft.Alignment.CENTER,
            ft.Alignment.BOTTOM_LEFT,
            ft.Alignment.BOTTOM_RIGHT,
            ft.Alignment.TOP_CENTER,
            ft.Alignment.BOTTOM_CENTER,
        ]
        while True:
            await asyncio.sleep(10)
            if saver_view.visible:
                saver_container.alignment = random.choice(alignments)
                page.update()

    page.run_task(anti_burn_in_loop)

    reactive_list = ft.ListView(expand=False, height=180, spacing=10)
    banned_list = ft.ListView(expand=False, height=180, spacing=10)

    async def reload(e=None):
        current_reactive = get_reactive_ips()
        current_banned = get_banned_ips()

        reactive_list.controls.clear()
        banned_list.controls.clear()

        for ip in list(current_reactive):
            reactive_list.controls.append(
                create_row_ui(
                    ip,
                    on_banned=lambda e, i_p=ip: page.run_task(handle_ban, i_p),
                )
            )

        for ip in list(current_banned):
            banned_list.controls.append(
                create_row_ui(
                    ip,
                    on_unbanned=lambda e, i_p=ip: page.run_task(
                        handle_unban, i_p
                    ),
                )
            )

        page.update()

    async def handle_ban(ip: str):
        await ban(ip, get_banned_ips())
        if ip in get_reactive_ips():
            get_reactive_ips().remove(ip)
        await reload()

    async def handle_unban(ip: str):
        await unban(ip, get_banned_ips())
        await reload()

    async def handle_server(e=None):
        start_button.disabled = True
        page.update()

        if not page.is_working:
            ServerManager.launch_server()
            start_style.bgcolor = ft.Colors.RED_700
            start_text.value = "Stop"
            page.is_working = True
            await toggle_screensaver(True)
        else:
            ServerManager.close_server()
            start_style.bgcolor = ft.Colors.GREEN_700
            start_text.value = "Start"
            page.is_working = False

        start_button.disabled = False
        page.update()

    async def toggle_screensaver(enable: bool):
        main_content.visible = not enable
        saver_view.visible = enable
        page.padding = 0 if enable else 10
        page.update()

    start_text = ft.Text("Start", size=20, color="white", weight="bold")
    start_style = ft.ButtonStyle(
        bgcolor=ft.Colors.GREEN_700,
        shape=ft.RoundedRectangleBorder(radius=12),
        padding=15,
        alignment=ft.Alignment.CENTER,
    )
    start_button = ft.Button(
        content=start_text, on_click=handle_server, style=start_style, expand=True
    )

    refresh_text = ft.Text("Refresh", size=20, color="white", weight="bold")
    refresh_style = ft.ButtonStyle(
        bgcolor=ft.Colors.BLUE_700,
        shape=ft.RoundedRectangleBorder(radius=12),
        padding=15,
        alignment=ft.Alignment.CENTER,
    )
    refresh_button = ft.Button(
        content=refresh_text, on_click=reload, style=refresh_style, expand=True
    )

    saver_btn_text = ft.Text("Saver Mode", size=20, color="white", weight="bold")
    saver_btn_style = ft.ButtonStyle(
        bgcolor=ft.Colors.GREY_800,
        shape=ft.RoundedRectangleBorder(radius=12),
        padding=15,
        alignment=ft.Alignment.CENTER,
    )
    saver_button = ft.Button(
        content=saver_btn_text,
        on_click=lambda e: page.run_task(toggle_screensaver, True),
        style=saver_btn_style,
        expand=True,
    )

    main_content = ft.Column(
        controls=[
            ft.Row([saver_button, refresh_button], spacing=8),
            ft.Row([start_button], spacing=8),
            ft.Divider(color="blue", thickness=3),
            ft.Text("Reactive IPs:", size=18, weight="bold", color="white"),
            reactive_list,
            ft.Divider(color="blue", thickness=3),
            ft.Text("Banned IPs:", size=18, weight="bold", color="white"),
            banned_list,
        ],
        scroll="adaptive",
        expand=True,
    )

    page.add(saver_view, main_content)
    await reload()


if __name__ == "__main__":
    ft.run(main)
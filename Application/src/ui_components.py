import flet as ft

def create_row_ui(bed_val : str, name_val : str, national_id_val : str, specialist_val : str, diet_val : str, res_val : str, diagnosis_val : str, consultation_val : str, on_delete, on_edit):
        
        return ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(f"Bed no. :    {bed_val}", weight="bold", bgcolor="lightgray", selectable=True, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                                ft.Text(f"Pt.Name :    {name_val}", weight="bold", bgcolor="lightgray", selectable=True, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                                ft.Text(f"NID     :    {national_id_val}", weight="bold", bgcolor="lightgray", selectable=True, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                                ft.Text(f"SP      :    {specialist_val}", weight="bold", bgcolor="lightgray", selectable=True, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                                ft.Text(f"Diet    :    {diet_val}", weight="bold", bgcolor="lightgray", selectable=True, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                                ft.Text(f"RES     :    {res_val}", weight="bold", bgcolor="lightgray", selectable=True, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                                ft.Text(f"Dx      :    {diagnosis_val}", weight="bold", bgcolor="lightgray", selectable=True, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                                ft.Text(f"Cx      :    {consultation_val}", weight="bold", bgcolor="lightgray", selectable=True, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS)
                            ],
                            expand=True 
                        ),
                        ft.Column(controls =[
                        ft.IconButton(
                            icon=ft.Text("Delete", size=20, weight="bold", color="red"), 
                            on_click=on_delete 
                        ),
                        ft.IconButton(
                            icon=ft.Text("Edit", size=20, weight="bold", color="blue"), 
                            on_click=on_edit
                        )])
                    ]
                )
            ), bgcolor="#201E1E"#, key=bed_val
        )
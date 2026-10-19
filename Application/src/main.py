import ui_components as ui
import utils 
import io
import os
import sys

import flet as ft
import httpx
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


SERVER_URL = u"http://127.0.0.1:2011"

class NetworkManager:
    _client: httpx.AsyncClient | None = None

    @classmethod
    def get_client(cls) -> httpx.AsyncClient:
        """ Create a client if not exists or uses the exist client and return it """
        if cls._client is None or cls._client.is_closed:
            cls._client = httpx.AsyncClient()
        return cls._client

    @classmethod
    async def close(cls):
        """ Close the client when the program is turn off """
        if cls._client and not cls._client.is_closed:
            await cls._client.aclose()

# --------  MAIN PAGE ---------
async def main(page: ft.Page):
#---------- INITIALIZING PAGE  -------------------
    page.title = "Pt.info" 
    page.horizontal_alignment = ft.CrossAxisAlignment.START
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.scroll = "adaptive"
    page.bgcolor = "#0d2f54" 
    page.theme_mode = ft.ThemeMode.DARK

#-----Variables--------- 
    page.editing_bed_id = None # A global Variables to can enable editing later
    share = ft.Share()
# -----  files  ------

#------------- INITIALIZING DATA -----------
    input_bg = ft.Colors.with_opacity(0.3, ft.Colors.BLACK)
    text_color = ft.Colors.WHITE 
    border_co = "#0C58D3" 

    bed_num = ft.TextField(label="Bed Number (Bed no.)", border_color=border_co, border_width=2, bgcolor=input_bg, color=text_color, on_change=lambda e, : clear_bed_error(), enable_interactive_selection=True)
    name_input = ft.TextField(label="Patient Name (Pt.Name)", border_color=border_co, border_width=2, bgcolor=input_bg, color=text_color, on_change=lambda e, : clear_name_error()) 
    nid_input = ft.TextField(label="National ID (NID)", cursor_color="blue", border_color=border_co, border_width=2, bgcolor=input_bg, color=text_color, input_filter=ft.NumbersOnlyInputFilter())
    sp_input = ft.TextField(label="Specialist (SP)", cursor_color="blue", border_color=border_co, border_width=2, bgcolor=input_bg, color=text_color)
    diet_input = ft.TextField(label="Diet", cursor_color="blue", border_color=border_co, border_width=2, bgcolor=input_bg, color=text_color)  
    res_input = ft.TextField(label="Respiration System (RES)", cursor_color="blue", border_color=border_co, border_width=2, bgcolor=input_bg, color=text_color)
    dx_input = ft.TextField(label="Diagnosis (Dx)", cursor_color="blue", border_color=border_co, border_width=2, bgcolor=input_bg, color=text_color)
    cx_input = ft.TextField(label="Consultation (Cx)", cursor_color="blue", border_color=border_co, border_width=2, bgcolor=input_bg, color=text_color)

    data_list = ft.ListView(expand=True)
    
#-------------- Sub Functions -------------------------
    def show_snack_bar(message : str, bg_color : ft.Colors) -> None: 
        page.show_dialog(ft.SnackBar(content=ft.Text(message, color=ft.Colors.WHITE, weight="bold"),bgcolor=bg_color,duration=2300))
        page.update()


    async def do_sharing_file() -> None:
        try:
            client = NetworkManager.get_client()
            response = await client.get(f"{SERVER_URL}/Patients")
            if response.status_code == 200:
                raw_data: list[list[str]] = response.json()
            else:
                show_snack_bar(f"Failed to load data for PDF. status code: {response.status_code}", ft.Colors.RED_700)

        except Exception as e:
            show_snack_bar(f"Failed to load data for PDF. {e}", ft.Colors.RED_700)
            return

        if not raw_data:
            show_snack_bar("No data available to share!", ft.Colors.AMBER_700)
            return
        
        if getattr(sys, "frozen", False):
            BASE_DIR = os.path.dirname(sys.executable)
        else:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        FONT_PATH = os.path.join(BASE_DIR, "Amiri-Regular.ttf")

        pdfmetrics.registerFont(TTFont("ArabicFont", FONT_PATH))

        def process_arabic_text(text: str, max_width: float = None,
                        font_name: str = "ArabicFont", font_size: float = 9) -> str:
            if not text:
                return ""

            reshaped = arabic_reshaper.reshape(text)

            if max_width is None:
                return get_display(reshaped)

            words = reshaped.split(" ")
            lines, current = [], ""
            for word in words:
                test = f"{current} {word}".strip()
                if pdfmetrics.stringWidth(get_display(test), font_name, font_size) <= max_width:
                    current = test
                else:
                    if current:
                        lines.append(current)
                    current = word
            if current:
                lines.append(current)

            return "<br/>".join(get_display(line) for line in lines)
        
        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=letter,
            title="Patients Table",
            leftMargin=36,
            rightMargin=36,
            topMargin=36,
            bottomMargin=36,
        )
        elements = []

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Heading1"],
            fontName="ArabicFont", 
            fontSize=16,
            spaceAfter=15,
            textColor=colors.HexColor("#1A365D"),
            alignment=1,  
        )
        cell_style = ParagraphStyle(
            "TableCell",
            parent=styles["Normal"],
            fontName="ArabicFont", 
            fontSize=9,
            leading=11,
            alignment=2,
            wordWrap="RTL", 
        )

        title_text = process_arabic_text("Patients Information Table")
        elements.append(Paragraph(f"<b>{title_text}</b>", title_style))
        elements.append(Spacer(1, 10))

        formatted_data = []

        headers = [
            "Bed No.",
            "Name",
            "NID",
            "Specialist",
            "Diet",
            "RES",
            "Dx",
            "Cx",
        ]

        formatted_data.append([
            Paragraph(f"<b>{process_arabic_text(col)}</b>", cell_style)
            for col in headers
        ])

        col_widths = [40, 105, 65, 65, 60, 60, 70, 75]

        for row in raw_data:
            if row:
                formatted_data.append([
                    Paragraph(
                        process_arabic_text(str(val), max_width=col_widths[i] - 12),
                        cell_style,
                    )
                    for i, val in enumerate(row)
                ])

        pdf_table = Table(formatted_data, colWidths=col_widths, hAlign="CENTER")
        pdf_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2B6CB0")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("TOPPADDING", (0, 0), (-1, 0), 8),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"), 
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.white, colors.HexColor("#F7FAFC")],
                ),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
                ("TOPPADDING", (0, 1), (-1, -1), 6),
            ])
        )

        elements.append(pdf_table)
        doc.build(elements)
        pdf_buffer.seek(0)

        file = ft.ShareFile.from_bytes(
            data=pdf_buffer.getvalue(),
            mime_type="application/pdf",
            name="Report.pdf",
        )
        await share.share_files(
            files=[file],
            text="Patients Report",
        )

    def edit_button(bed_val, name_val, national_id_val, specialist_val, diet_val, res_val, diagnosis_val, consultation_val) -> None:

        page.editing_bed_id = bed_val.strip().upper()

        bed_num.value = bed_val
        name_input.value = name_val
        nid_input.value = national_id_val
        sp_input.value = specialist_val
        diet_input.value = diet_val
        res_input.value = res_val
        dx_input.value = diagnosis_val
        cx_input.value = consultation_val

        save_text.value = 'Change' 
        save_style.bgcolor = ft.Colors.BLUE_700

        page.update()


    def clear_bed_error() -> None:
        if bed_num.error:
            bed_num.error = None; page.update()
        
    def clear_name_error() -> None:
        if name_input.error:
                name_input.error = None; page.update()


#------------MAIN Functions--------------------------------

    async def load_data(e=None) -> None: # load data that in CSV file
        data_list.controls.clear()
        try :
            client = NetworkManager.get_client()
            response = await client.get(f"{SERVER_URL}/Patients")
            if response.status_code == 200:
                for row in response.json():
                    if row:
                        row_ui = ui.create_row_ui(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], lambda e, i=row[0]: page.run_task(delete_data, i), lambda e, r= row : edit_button(*r))
                        data_list.controls.append(row_ui)
            elif response.status_code == 403:
                show_snack_bar('Your IP has been banned', ft.Colors.RED_700)
            else:
                show_snack_bar(f"Server error status code: ({response.status_code}).", ft.Colors.RED_700)

        # except ValueError:...
        except Exception as e:
            print(e)
            show_snack_bar(f'An error occurred while load data. Exiting from the app and enter later. Info = {e}', ft.Colors.RED_700)

    
    async def add_data() -> None: # Connect with save button and refresh data when the user press it
        """"  check if bed name field and name field is empty or not and upload data to CSV file or change it  """
        if not bed_num.value :
            bed_num.error = "This field is required"; page.update()
            return
        if not name_input.value :
            name_input.error = "This field is required"; page.update()
            return
        
        """  For better UX  """
        bed_num.value = bed_num.value.strip().upper()
        name_input.value = name_input.value.strip().title()
        nid_input.value = nid_input.value.strip()
        sp_input.value = sp_input.value.strip().title()
        diet_input.value = utils.clear_shortcut_inputs(diet_input.value)
        res_input.value = utils.clear_shortcut_inputs(res_input.value)
        dx_input.value = utils.clear_shortcut_inputs(dx_input.value)
        cx_input.value = utils.clear_shortcut_inputs(cx_input.value)
        
        save_button.disabled = True # protection from double presses on the button
        page.update() # Flet do Automatically update when the function is end but this chang is happens and end in this function.
                        #  Consequently, user cannot see the change without this manually update

        try :
            """ Checks if this upload is overwrite on previous data or append a new data """
            if page.editing_bed_id:
                client = NetworkManager.get_client()
                body = {
                    "Bed_Number" : bed_num.value,
                    "Name" : name_input.value,
                    "NID" : nid_input.value if nid_input.value else "",
                    "Specialist" : sp_input.value if sp_input.value else "",
                    "Diet" : diet_input.value if diet_input.value else "",
                    "Respiration_System" : res_input.value if res_input.value else "",
                    "Diagnosis" : dx_input.value if dx_input.value else "",
                    "Consultation" : cx_input.value if cx_input.value else ""
                }
                response = await client.put(f"{SERVER_URL}/Patients", json=body)

                if response.status_code == 404:
                    bed_num.error = "Cannot change the bed in edit mode"
                    show_snack_bar("Cannot change the bed in edit mode", ft.Colors.RED_700)
                elif response.status_code == 403:
                    show_snack_bar('Your IP have been banned', ft.Colors.RED_700)
                elif response.status_code == 204:
                    show_snack_bar("Changed successfully", ft.Colors.GREEN_700)
                else:
                    show_snack_bar(f"Server error ({response.status_code}), \n Info = {response.json()}", ft.Colors.RED_700)
                page.editing_bed_id = None
                del body, response
            else:
                client = NetworkManager.get_client()
                body = {
                    "Bed_Number" : bed_num.value,
                    "Name" : name_input.value,
                    "NID" : nid_input.value if nid_input.value else "",
                    "Specialist" : sp_input.value if sp_input.value else "",
                    "Diet" : diet_input.value if diet_input.value else "",
                    "Respiration_System" : res_input.value if res_input.value else "",
                    "Diagnosis" : dx_input.value if dx_input.value else "",
                    "Consultation" : cx_input.value if cx_input.value else ""
                }
                response = await client.post(f"{SERVER_URL}/Patients", json=body)
                if response.status_code == 409:
                    bed_num.error = "This bed is in use"
                    show_snack_bar("This bed is in use!", ft.Colors.RED_700)
                elif response.status_code == 403:
                    show_snack_bar('Your IP have been banned', ft.Colors.RED_700)
                elif response.status_code == 201:
                    show_snack_bar("Saved successfully", ft.Colors.GREEN_700)
                else:
                    show_snack_bar(f"Server error ({response.status_code}),\n Info = {response.json()}", ft.Colors.RED_700)
                del response, body

        except Exception as er :
            show_snack_bar(f'An error occurred while saving data. Try again later {er}', ft.Colors.RED_700)

        finally :
            bed_num.value = ""
            name_input.value = ""
            nid_input.value = ""
            sp_input.value = ""
            diet_input.value = ""
            res_input.value = ""
            dx_input.value = ""
            cx_input.value = ""

            clear_bed_error(); clear_name_error()
            save_style.bgcolor = ft.Colors.GREEN_700
            save_text.value = "Save"
            await load_data()
            save_button.disabled=False; page.update() # Even if error occurred, save button will be enable to use again

    async def delete_data(id_to_delete: str) -> None:
        try :
            client = NetworkManager.get_client()
            response = await client.delete(f"{SERVER_URL}/Patients", params={"bed_number" : id_to_delete})

            if response.status_code == 403:
                show_snack_bar('Your IP have been banned', ft.Colors.RED_700)
            elif response.status_code == 204:
                await load_data()
                show_snack_bar('Has deleted successfully', ft.Colors.GREEN_700);
            else:
                show_snack_bar(f"Server error ({response.status_code}, \n Info = {response.json()})", ft.Colors.RED_700)
            del response

        except Exception as e:
            show_snack_bar(f'An error occurred while deleting data. Try again later {e}', ft.Colors.RED_700)
            return
    
#-----------------  Buttons  ---------------------------------
    save_text = ft.Text('Save', size=23, color='white', weight='bold') # The text out of the button object due to can change it to be the editing button and return to be the save button easely
    
    save_style = ft.ButtonStyle(bgcolor=ft.Colors.GREEN_700, shape=ft.RoundedRectangleBorder(radius=15), padding=20) # The same ^
    
    save_button = ft.Button(content=save_text, on_click=lambda e : page.run_task(add_data), style=save_style, expand=True)

    paint_button = ft.Button(
        content=ft.Text('Share', size=20, weight='bold'),
        style=ft.ButtonStyle(bgcolor="#121010", side=ft.BorderSide(width=2, color=ft.Colors.BLUE_700),
        shape=ft.RoundedRectangleBorder(radius=15), padding=20), expand=True, on_click=lambda e, : page.run_task(do_sharing_file)
    )

    refresh_text = ft.Text("Refresh", size=23, color="white", weight="bold")
    refresh_style = ft.ButtonStyle(
        bgcolor=ft.Colors.BLUE_700,
        shape=ft.RoundedRectangleBorder(radius=15),
        padding=20,
        alignment=ft.Alignment.CENTER,
    )
    refresh_button = ft.Button(
        content=refresh_text, on_click=load_data, style=refresh_style, expand=True
    )
    
#----------------------  LOAD DATA ON THE PAGE  -----------------------

    label_re = ft.Text("* Required", color=ft.Colors.YELLOW_ACCENT_700, size=11, weight='bold')

    page.add(
        ft.Text("Add new data :", size=20, weight="bold", color="white"),
        label_re,
        bed_num,
        label_re,
        name_input,
        nid_input,
        sp_input,
        diet_input,
        res_input,
        dx_input,
        cx_input,
        ft.Row([save_button, paint_button], spacing=10, expand=True),
        ft.Row([refresh_button], spacing=10, expand=True),
        ft.Divider(color="blue", thickness=10),
        # search_input,
        ft.Text("Saved data :", size=20, weight="bold", color="white"),
        data_list 
    )

    await load_data(); page.update()
# -----------  START RUNNING  ------------
if __name__ == '__main__' :
    ft.run(main)
<<<<<<< HEAD
    NetworkManager.close()
=======
    NetworkManager.close()
>>>>>>> master

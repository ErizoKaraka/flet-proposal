import flet as ft
from flet import *
import asyncio
import flet.canvas as cv
import time
import json
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart
import datetime
import matplotlib.dates as mdates

tepe = 0
osi = 0
pulsi = 0
fall = 0
enviar = 0
pulsi_n1 = 0
tepe_n1 = 0
osi_n1 = 0
pulsi_n2 = 0
tepe_n2 = 0
osi_n2 = 0

def main (page:Page):

    def info_go(e):
        global camtemp
        camtemp = True
        page.go("/info")

    page.fonts = {
        "phil": "./assets/ChauPhilomeneOne-Regular.ttf"
    }

    gris = "#A6A6A6"
    color_i="#222222"

    lista_contactos = []

    def fondito(e):
        if e.data == "true":
            e.control.bgcolor=colors.BLACK26
            page.update()
        else:
            e.control.bgcolor=""
            page.update()

    def graphOp(e, op):
        if op == 0:
            graph_temperatura.visible = False
            graph_pulso.visible = True
            graph_oxigeno.visible = False
            page.update()
        elif op == 1:
            graph_temperatura.visible = False
            graph_pulso.visible = False
            graph_oxigeno.visible = True
            page.update()


        elif op == 2:
            graph_temperatura.visible = True
            graph_pulso.visible = False
            graph_oxigeno.visible = False
            page.update()

    page.bgcolor = colors.BLACK

    contactos = Column(
        controls=[
        ]
    )

    nombre_c= TextField(
        label="Nombre",
        border=ft.InputBorder.UNDERLINE,
        max_length=20
        )
            
    num = TextField(
        label="Numero",
        border=ft.InputBorder.UNDERLINE,
        value="+",
        max_length=20
        )

    no_user = Row(
        controls=[
            Text("Datos erroneos, intenta de nuevo", font_family="phil")
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        visible=False
    )

    pb = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(
                content= ft.Image(
                    "./assets/corazon.png",
                    height=40,
                    width=40,
                ),
                on_click=lambda e: graphOp(e, 0)
            ),
            ft.PopupMenuItem(
                content= ft.Image(
                    "./assets/ox.png",
                    height=40,
                    width=40,
                ),
                on_click=lambda e: graphOp(e, 1)
            ),
            ft.PopupMenuItem(
                content= ft.Image(
                    "./assets/tl.png",
                    height=40,
                    width=40,
                ),
                on_click=lambda e: graphOp(e, 2)
            ),
        ]
    )

    agregar = Container(
                border_radius=10,
                width=120,
                on_click=lambda _: page.go("/contactos/agregar"),
                content=Row(
                    controls=[
                        ft.Image(
                                fit=ImageFit.COVER,
                                height=40,
                                width=40,
                                src="./assets/agregar.png"
                        ),
                        Text("AÑADIR", size=20, font_family="phil")
                    ]
                ),
                on_hover=fondito
            )

    perfil = Container(
        alignment=alignment.bottom_center,
        width=20,
        height=20,
        content= ft.Image(src="./assets/contacto.jpg"),
        on_click=lambda _: page.go("/valores")
    )

    corazon =Container(
        padding=0,
        height=100,
        width=100,
        content=ft.Image(
        height=100,
        width=150,
        src="./assets/corazon.png"
        )
    )

    oxig =Container(
        padding=0,
        height=80,
        width=100,
        content=ft.Image(
        height=100,
        width=150,
        src="./assets/ox.png"
        )
    )

    term =Container(
        padding=0,
        height=80,
        width=100,
        content=ft.Image(
        height=100,
        width=150,
        src="./assets/tl.png"
        )
    )

    nombre = Container(
        width=220,
        content=TextField(label="Usuario", border=InputBorder.UNDERLINE)
    )
    
    contraseña = Container(
        width=220,
        content=TextField(label="Contraseña", border=InputBorder.UNDERLINE, password=True, can_reveal_password=True)
    )

    text_icon = Row(
        spacing=75,
        alignment=MainAxisAlignment.CENTER,
        controls=[
            Text("CONTACTOS", color="black", font_family="phil", size=10),Text("  MEDICION", color="black", font_family="phil", size=10),Text("ESTADISTICAS", color="black", font_family="phil", size=10)
        ]
    )

    med_icon = ft.IconButton(
        icon=ft.icons.MONITOR_HEART,
        icon_color=color_i,
        icon_size=30,
        on_click=lambda _: page.go("/mediciones")
    )

    cont_icon = ft.IconButton(
        icon=ft.icons.CALL_SHARP,
        icon_color=color_i,
        icon_size=30,
        on_click=lambda _: page.go("/contactos")
    )

    info_i = ft.IconButton(
        icon=ft.icons.AUTO_GRAPH_ROUNDED,
        icon_color=color_i,
        icon_size=30,
        on_click=info_go
    )

    iconos = Row(
        spacing=90,
        alignment=MainAxisAlignment.CENTER,
        controls=[
            cont_icon, med_icon,info_i
        ]
    )

    icons_t = Container(
        height=15,
        content=text_icon
    )

    icons_r=Container(
        height=40,
        content=iconos
    )

    class tabs(BottomAppBar):
        def __init__(self):
            super().__init__()
            self.shape=ft.NotchShape.CIRCULAR,
            self.bgcolor="white",
            self.height=80
            self.content = Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        icons_r,icons_t
                    ]
                )

    class grafico(ft.Container):
        def __init__(self, variable):
            super().__init__()
            self.fig, self.ax = plt.subplots()
            self.content = MatplotlibChart(self.fig, expand=False)
            plt.grid(color='gray', linestyle='--', linewidth=0.5)
            self.height = 300
            self.width = 500
            self.variable = variable
            self.df = pd.DataFrame(columns=["fecha"])
        def did_mount(self):
            self.running = True
            self.page.run_task(self.update_grafico)
        def will_unmount(self): 
            self.running = False
        async def update_grafico(self):
            if self.variable == 0:
                while self.running:
                    self.update()
                    new_row = pd.Series({"temperatura":int(tepe), "fecha":datetime.datetime.now()})
                    self.df = pd.concat([self.df, new_row.to_frame().T])
                    self.ax.plot(self.df['fecha'], self.df['temperatura'], color='b')
                    self.ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
                    self.ax.set_title("Gráfico de Temperatura") 
                    self.ax.set_ylabel("Temperatura (°C)")  
                    await asyncio.sleep(10)
            elif self.variable == 1:
                while self.running:
                    self.update()
                    new_rowo = pd.Series({"oxigeno":int(osi), "fecha":datetime.datetime.now()})
                    self.df = pd.concat([self.df, new_rowo.to_frame().T])
                    self.ax.plot(self.df['fecha'], self.df['oxigeno'], color='b')
                    self.ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
                    self.ax.set_title("Gráfico de Oxigeno") 
                    self.ax.set_ylabel("Oxígeno (%)")  
                    await asyncio.sleep(10)
            elif self.variable == 2:
                while self.running:
                    self.update()
                    new_rowp = pd.Series({"pulso":int(pulsi), "fecha":datetime.datetime.now()})
                    self.df = pd.concat([self.df, new_rowp.to_frame().T])
                    self.ax.plot(self.df['fecha'], self.df['pulso'], color='b')
                    self.ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
                    self.ax.set_title("Gráfico de Pulso")  
                    self.ax.set_ylabel("Pulso (ppm)")  
                    await asyncio.sleep(10)             
             
    class alertacaida(ft.Container):
        def __init__(self):
            super().__init__()
            self.height = 60
            self.border = ft.border.all(color="black")
            self.border_radius = 10
            self.bgcolor = "#C9CBC9"
            self.visible = False
            self.content = ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    Text("Caida detectada", font_family="phil", color="#FF000B", size=30)
                ]                
            )
        
        def did_mount(self):
            self.running = True
            self.page.run_task(self.update_cai)
        def will_unmount(self):
            self.running = False
    
        async def update_cai(self):
            global fall
            while self.running:
                if int(fall) == 1:
                    self.visible = True
                    self.update()
                elif int(fall) == 0:
                    self.visible = False
                    self.update()
                self.update()
                await asyncio.sleep(10)

    class valor_medio1(ft.TextField):
        def __init__(self, medida):
            super().__init__()
            self.border=ft.InputBorder.UNDERLINE
            self.input_filter=ft.NumbersOnlyInputFilter()
            self.width = 30
            if medida == "pulso":
                self.value = pulsi_n1
            elif medida == "ox":
                self.value = osi_n1
            elif medida == "temp":
                self.value = tepe_n1

    class valor_medio2(ft.TextField):
        def __init__(self, medida):
            super().__init__()
            self.border=ft.InputBorder.UNDERLINE
            self.input_filter=ft.NumbersOnlyInputFilter()
            self.width = 30
            if medida == "pulso":
                self.value = pulsi_n2
            elif medida == "ox":
                self.value = osi_n2
            elif medida == "temp":
                self.value = tepe_n2
            
    class contacto(ft.Row):
        def __init__(self, name, num):
            super().__init__()
            lista_contactos.append(f"{num}")
            self.alignment = ft.MainAxisAlignment.CENTER
            self.editarbuton = Container(
                            on_click=self.editar,
                            padding=0,
                            border_radius=20,
                            on_hover=fondito,
                            content=ft.Image(
                            fit=ImageFit.COVER,
                            height=60,
                            width=60,
                            src="./assets/editar.png",
                            visible=True
                            )
                        )
            self.name = ft.Text(value=name, font_family="phil", size=20)
            self.num = ft.Text(value=num, font_family="phil", size=20)
            self.save_contact=ft.IconButton(icon="save", visible=False, icon_size=50, icon_color="black", on_click=self.save, hover_color=colors.BLACK26)
            self.name_edit = TextField(
                value=name, 
                visible=False, 
                width=150, 
                height=50,
                border_width=3,
                max_length=20,
                focused_border_color="black",
                text_style=ft.TextStyle(font_family="phil"),
                content_padding=ft.Padding(
                    left=5, top=3, right=5, bottom=3
                    )
                )
            self.num_edit= TextField(
                value=num, 
                visible=False, 
                width=150, 
                height=50,
                border_width=3,
                max_length=20,
                focused_border_color="black",
                text_style=ft.TextStyle(font_family="phil"), 
                content_padding=ft.Padding(
                    left=5, top=3, right=5, bottom=3
                    )
                )    
            self.controls = [
                        Container(
                            padding=0,
                            content=ft.Image(
                            fit=ImageFit.COVER,
                            height=90,
                            width=90,
                            src="./assets/cont.png"
                            )
                        ),
                        Column(
                            wrap=True,
                            controls=[
                                  self.name,self.name_edit, self.num, self.num_edit
                                ]
                            ),
                        self.editarbuton, self.save_contact
                    ]
            
        def editar(self, e):
            self.name.visible = False
            self.num.visible = False
            self.editarbuton.visible = False
            self.name_edit.visible = True
            self.num_edit.visible = True
            self.save_contact.visible = True
            self.update()
        def save(self, e):
            self.name.visible = True
            self.num.visible = True
            self.editarbuton.visible = True
            self.name_edit.visible = False
            self.num_edit.visible = False
            self.save_contact.visible = False
            delnum = self.num.value
            lista_contactos.remove(delnum)
            self.name.value = self.name_edit.value
            self.num.value = self.num_edit.value
            lista_contactos.append(self.num.value)
            self.update()
        
    class num_pul(ft.Text):
        def __init__(self, font, size):
            super().__init__()
            self.font_family=font
            self.size=size
        
        def did_mount(self):
            self.running = True
            self.page.run_task(self.update_pul)
        def will_unmount(self):
            self.running = False

        async def update_pul(self):
            global pulsi
            global pulsi_n1
            global pulsi_n2
            while self.running:
                self.value = f"{pulsi}"
                self.update()
                await asyncio.sleep(10)
                
    class num_ox(ft.Text):
        def __init__(self, font, size):
            super().__init__()
            self.font_family=font
            self.size=size
        
        def did_mount(self):
            self.running = True
            self.page.run_task(self.update_ox)
        def will_unmount(self):
            self.running = False
    
        async def update_ox(self):
            global osi
            global osi_n1
            global osi_n2
            while self.running:
                self.value = f"{osi}"
                self.update()
                await asyncio.sleep(10)
                
    class num_temp(ft.Text):
        def __init__(self, font, size):
            super().__init__()
            self.font_family=font
            self.size=size
        
        def did_mount(self):
            self.running = True
            self.page.run_task(self.update_temp)
        def will_unmount(self):
            self.running = False
    
        async def update_temp(self):
            global tepe
            global tepe_n1
            global tepe_n2
            while self.running:
                self.value = f"{tepe}"
                self.update()
                await asyncio.sleep(10)
                
    class circuloestado3(cv.Canvas):
        def __init__(self):
            super().__init__()
            self.stroke_paint = ft.Paint(stroke_width=3, style=ft.PaintingStyle.STROKE)
            self.fill_paint = ft.Paint(style=ft.PaintingStyle.FILL)
            self.shapes = [
                cv.Circle(-90, 0, 20, self.fill_paint),
                cv.Circle(-90, 0, 20, self.stroke_paint)
            ]

        def did_mount(self):
            self.running = True
            self.page.run_task(self.update_colorox)

        def will_unmount(self):
            self.running = False

        async def update_colorox(self):
            while self.running:
                    if int(osi) <= int(valor_oxin1.value) or int(osi)>= int(valor_oxin2.value):
                        self.fill_paint.color = colors.RED
                    else:
                        self.fill_paint.color = colors.GREEN_400
                    self.update()
                    await asyncio.sleep(20)
            
    class circuloestado2(cv.Canvas):
        def __init__(self):
            super().__init__()
            self.stroke_paint = ft.Paint(stroke_width=3, style=ft.PaintingStyle.STROKE)
            self.fill_paint = ft.Paint(style=ft.PaintingStyle.FILL)
            self.shapes = [
                cv.Circle(-35, 0, 20, self.fill_paint),
                cv.Circle(-35, 0, 20, self.stroke_paint)
            ]

        def did_mount(self):
            self.running = True
            self.page.run_task(self.update_colortemp)

        def will_unmount(self):
            self.running = False

        async def update_colortemp(self):
            while self.running:
                    if float(tepe) <= float(valor_tempn1.value) or float(tepe) >= float(valor_tempn2.value):
                        self.fill_paint.color = colors.RED
                    else:
                        self.fill_paint.color = colors.GREEN_400
                    self.update()
                    await asyncio.sleep(20)
            
    class circuloestado(cv.Canvas):
        def __init__(self):
            super().__init__()
            self.stroke_paint = ft.Paint(stroke_width=3, style=ft.PaintingStyle.STROKE)
            self.fill_paint = ft.Paint(style=ft.PaintingStyle.FILL)
            self.shapes = [
                cv.Circle(-90, 0, 20, self.fill_paint),
                cv.Circle(-90, 0, 20, self.stroke_paint)
            ]

        def did_mount(self):
            self.running = True
            self.page.run_task(self.update_colorpul)

        def will_unmount(self):
            self.running = False

        async def update_colorpul(self):
            while self.running:
                    if int(pulsi) <= int(valor_puln1.value) or int(pulsi) >= int(valor_puln2.value):
                        self.fill_paint.color = colors.RED
                    else:
                        self.fill_paint.color = colors.GREEN_400
                    self.update()
                    await asyncio.sleep(20)

    class container_main(ft.Container):
        def __init__(self, content):
            super().__init__()
            self.content = content
            self.height = page.height - 20
            self.width = page.width - 20
            self.bgcolor = gris
            self.border_radius = 15
            self.padding = 20

    class col_p(ft.Column):
        def __init__(self, controls, horizontal_alignment,alignment, scroll):
            super().__init__()
            self.horizontal_alignment=horizontal_alignment
            self.alignment=alignment
            self.controls = controls
            self.scroll = scroll

    valor_tempn1 = valor_medio1("temp")
    valor_tempn2 = valor_medio1("temp")
    valor_oxin1 = valor_medio1("ox")
    valor_oxin2 = valor_medio2("ox")
    valor_puln1 = valor_medio1("pulso")
    valor_puln2 = valor_medio2("pulso")

    graph_temperatura = grafico(0)
    graph_oxigeno = grafico(1)
    graph_pulso = grafico(2)
    

    def route_change(e):
        page.views.clear()
        page.views.append(
            View(
                "/",
                bgcolor="black",
                horizontal_alignment=CrossAxisAlignment.CENTER,
                vertical_alignment=MainAxisAlignment.CENTER,
                controls=
                [
                    container_main(
                        col_p(
                            [
                                Row(controls=[
                                    ],
                                    wrap=True
                                ),
                                Divider(color="transparent", height=70),
                                Container(
                                    padding=15,
                                    width=300,
                                    height=400,
                                    border_radius=10,
                                    bgcolor="#C9CBC9",
                                    content=ft.Column(
                                        controls=[
                                            Row(controls=[
                                                Text("Iniciar sesión",size=30, font_family="phil")
                                                ],
                                                alignment=ft.MainAxisAlignment.CENTER
                                            ),
                                            Divider(color="transparent",height=20),
                                            nombre,
                                            Divider(color="transparent",height=10),
                                            contraseña,
                                            Divider(color="transparent",height=20),
                                            no_user,
                                            ElevatedButton(text="Confirmar", on_click=mediciones)
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    )
                                ),
                            ], ft.CrossAxisAlignment.CENTER,ft.MainAxisAlignment.START, False
                        )
                    )
                ]
            )
        )
        if page.route == "/mediciones":
            page.views.clear()
            page.views.append(
                View(
                    "/mediciones",
                    scroll=ft.ScrollMode.AUTO,
                    bottom_appbar=tabs(),
                    bgcolor="black",
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    vertical_alignment=MainAxisAlignment.CENTER,
                    controls=
                    [
                        container_main(
                            col_p(
                                
                                [
                                    Row(
                        wrap = False,
                        controls=[
                            Text(f"{nombre.content.value}", size=40, font_family="phil"), perfil
                        ]
                    ),
                    ft.Divider(
                        height=20,
                        color="#6C6A73"
                    ),
                    Container(
                        padding=1,
                        border_radius=10,
                        height=120,
                        bgcolor="#6C6A73",
                        content=Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                corazon, Row(
                                    controls=[
                                        num_pul("phil", 40), circuloestado(), Text("PPM          ",size=20, font_family="phil")
                                    ]
                                )
                            ]
                        )
                    ),
                    ft.Divider(
                        height=30,
                        color="transparent"
                    ),
                    Container(
                        height=120,
                        border_radius=10,
                        padding=1,
                        bgcolor="#6C6A73",
                        content=Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                term, Row(
                                    controls=[
                                        circuloestado2(),num_temp("phil", 40), Text("°C", size=40, font_family="phil"), Text("      ")
                                    ]
                                )
                             ]
                        )
                    ),
                    ft.Divider(
                        height=30,
                        color="transparent"
                    ),
                    Container(
                        padding=1,
                        border_radius=10,
                        height=120,
                        bgcolor="#6C6A73",
                        content=Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                oxig, Row(
                                    controls=[
                                        num_ox("phil", 40),circuloestado3(), Text("%        ", font_family="phil", size = 30)
                                    ]
                                )
                            ]
                        )
                    ),
                    alertacaida()
                                ],
                                ft.CrossAxisAlignment.START,ft.MainAxisAlignment.CENTER,  ft.ScrollMode.AUTO
                            )
                        ),
                    ],
                )
            )
        if page.route == "/contactos":
            
            page.views.clear()
            page.views.append(
                View(
                    "/contactos",
                    scroll=ft.ScrollMode.AUTO,
                    bgcolor="black",
                    bottom_appbar=tabs(),
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    vertical_alignment=MainAxisAlignment.CENTER,
                    controls=[
                        container_main(
                            col_p(
                                [
                                    Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        controls=[
                                            Text("MIS CONTACTOS", size=30, font_family="phil")
                                        ]
                                    ),
                                    ft.Divider(color="transparent"),
                                    contactos, agregar,
                                ], ft.CrossAxisAlignment.CENTER,ft.MainAxisAlignment.START, False
                            )
                        )
                    ]
                )
            )
            
        if page.route == "/contactos/agregar":
            page.views.clear()
            page.views.append(
                View(
                    "/contactos/agregar",
                    scroll=ft.ScrollMode.AUTO,
                    bgcolor="black",
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    vertical_alignment=MainAxisAlignment.CENTER,
                    controls=[
                        container_main(
                            col_p(
                                [
                                    ft.Divider(color="transparent", height=30),
                    ft.Image(
                                fit=ImageFit.COVER,
                                height=100,
                                width=100,
                                src="./assets/cont.png"
                        ),
                        ft.Divider(color="transparent", height=50),
                        nombre_c,
                        ft.Divider(color="transparent", height=50), 
                        num,
                        ft.Divider(color="transparent"),
                        Row(
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                            controls=[
                                ElevatedButton(
                                    text="Aceptar",
                                    color="black",
                                    on_click=añadcontacto
                                ), 
                                ElevatedButton(
                                    text="Cancelar",
                                    color="black",
                                    on_click=lambda _: page.go("/contactos")
                                    )
                                ]
                            )
                                ],
                                ft.CrossAxisAlignment.CENTER,
                                ft.MainAxisAlignment.CENTER,
                                ft.ScrollMode.AUTO
                            )
                        )
                    ]
                )
            )
            
        if page.route == "/info":
            graph_temperatura.visible = True
            graph_pulso.visible = False
            graph_oxigeno.visible = False
            
            page.views.clear()
            page.views.append(
                View(
                    "/info",
                    scroll=ft.ScrollMode.AUTO,
                    bgcolor="black",
                    bottom_appbar=tabs(),
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    vertical_alignment=MainAxisAlignment.CENTER,
                    controls=[
                        container_main(
                            col_p(
                                [
                                    Row(
                                        controls=[
                                            pb
                                        ]
                                    ),
                                    graph_temperatura,
                                    graph_oxigeno,
                                    graph_pulso
                                ], ft.CrossAxisAlignment.CENTER, ft.MainAxisAlignment, ft.ScrollMode.AUTO
                            )
                        )
                    ]
                )
            )

        if page.route == "/valores":
            page.views.clear()
            page.views.append(
                View(
                    "/valores",
                    scroll=ft.ScrollMode.AUTO,
                    bgcolor=gris,
                    bottom_appbar=tabs(),
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    vertical_alignment=MainAxisAlignment.CENTER,
                    controls=[
                        container_main(
                            col_p(
                                [   
                                    Row(
                                        wrap = False,
                                        controls=[
                                            Text(f"{nombre.content.value}", size=40, font_family="phil")
                                        ]
                                    ),
                                    Divider(
                                        color="#6C6A73"
                                    ),
                                    Row(
                                        controls=[
                                            Text(
                                                "Configuración de rango normal de datos vitales", font_family="phil", size=20
                                            )
                                        ],
                                        wrap=True
                                    ),
                                    Container(
                                        height=350,
                                        bgcolor="#6C6A73",
                                        padding=20,
                                        border_radius=10,
                                        content=Column(
                                            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                            controls=[
                                                Row(
                                                    controls=[
                                                        Text(
                                                            "Pulso", font_family="phil", size = 30
                                                        ),
                                                        valor_puln1,Text("PPM -", font_family="phil", size=20), valor_puln2, Text("PPM", font_family="phil", size=20)
                                                    ],
                                                    alignment= ft.MainAxisAlignment.CENTER,
                                                    wrap=True,
                                                ),
                                                ft.Divider(height=30, color="transparent"),
                                                Row(
                                                    controls=[
                                                        Text(
                                                            "Temp.", font_family="phil", size = 30
                                                        ),
                                                        valor_tempn1,Text("C° -", font_family="phil", size=20), valor_tempn2, Text("C°", font_family="phil", size=20)
                                                    ],
                                                    alignment= ft.MainAxisAlignment.CENTER,
                                                    wrap=True,
                                                ),
                                                Divider(height=30, color="transparent"),
                                                Row(
                                                    controls=[
                                                        Text(
                                                            "Ox.", font_family="phil", size = 30
                                                        ),
                                                        valor_oxin1,Text("% -", font_family="phil", size=20), valor_oxin2, Text("%", font_family="phil", size=20)
                                                    ],
                                                    alignment= ft.MainAxisAlignment.CENTER,
                                                    wrap=True,
                                                ),
                                                ElevatedButton("Aceptar", on_click=aceptar_val),
                                            ]
                                        )
                                    )
                                ],
                                ft.CrossAxisAlignment.CENTER,
                                ft.MainAxisAlignment, 
                                ft.ScrollMode.AUTO
                            )
                        )
                    ]
                )
            )
        
        page.update()

    def añadcontacto(e):
        nuevocontacto = contacto(nombre_c.value, num.value)
        contactos.controls.append(nuevocontacto)
        nombre_c.value=""
        num.value="+"
        page.go("/contactos")

    def mediciones(e):
        page.go("/mediciones")
        time.sleep(10)

    def aceptar_val(e):
        global osi_n1
        global osi_n2
        global tepe_n1
        global tepe_n2
        global pulsi_n1
        global pulsi_n2
        osi_n1 = valor_oxin1.value
        osi_n2  = valor_oxin2.value
        tepe_n1 = valor_tempn1.value
        tepe_n2 = valor_tempn2.value
        pulsi_n1 = valor_puln1.value
        pulsi_n2 = valor_puln2.value

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)
ft.app(target=main)

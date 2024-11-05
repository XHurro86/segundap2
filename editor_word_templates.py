import flet as ft
import shutil
import zipfile 
import os

# Definición de los campos de texto con estilo
fecha_facturacion = ft.TextField(label='Fecha Facturación',
                            hint_text="Fecha Facturación", 
                            width=300,
                            autofocus=True,
                            text_align='center',
                            border_radius=12,
                            focused_border_color=ft.colors.BLACK)

numero_factura = ft.TextField(label='Número Factura',
                            hint_text='Número Factura', 
                            width=300, 
                            text_align='center',
                            border_radius=12,
                            focused_border_color=ft.colors.BLACK)

nombre_cliente = ft.TextField(label='Nombre Cliente',
                            hint_text='Nombre Cliente', 
                            width=300, 
                            border_radius=12,
                            focused_border_color=ft.colors.BLACK)

direccion_cliente = ft.TextField(label='Dirección Cliente',
                            hint_text='Dirección Cliente', 
                            width=300, 
                            border_radius=12,
                            focused_border_color=ft.colors.BLACK12)

item_name_1 = ft.TextField(label='Item 1',
                            hint_text='Item 1', 
                            width=300, 
                            border_radius=12,
                            focused_border_color=ft.colors.BLACK12)

item_name_2 = ft.TextField(label='Item 2',
                            hint_text='Item 2', 
                            width=300, 
                            border_radius=12,
                            focused_border_color=ft.colors.BLACK12)

quantity_item_1 = ft.TextField(label='Cantidad Item 1',
                            value='0', 
                            text_align='center',
                            width=150,
                            border_radius=12,
                            focused_border_color=ft.colors.BLACK12)

quantity_item_2 = ft.TextField(label='Cantidad Item 2',
                            value='0', 
                            text_align='center',
                            width=150,
                            border_radius=12,
                            focused_border_color=ft.colors.BLACK12)

price_item_1 = ft.TextField(label='Precio Item 1',
                            value='0', 
                            text_align='center',
                            width=150,
                            border_radius=12,
                            focused_border_color=ft.colors.BLACK12)

price_item_2 = ft.TextField(label='Precio Item 2',
                            value='0', 
                            text_align='center',
                            width=150,
                            border_radius=12,
                            focused_border_color=ft.colors.BLACK12)

# Dialogo de Factura Generada
dialogo = ft.AlertDialog(title=ft.Text("Factura Generada"), 
                         on_dismiss=lambda e: print("Cerrado"))

# Función para generar la factura
def generar_factura(datos):
    shutil.copytree('plantilla', 'documento_tmp')

    with open('document.xml', 'r') as file:
        data = file.read()
        for key, value in datos.items():
            data = data.replace(key, value)

    with open('documento_tmp/word/document.xml', 'w') as file:
        file.write(data)

    with zipfile.ZipFile('factura.docx', 'w') as zipf:
        for root, dirs, files in os.walk('documento_tmp'):
            for file in files:
                zipf.write(os.path.join(root, file), 
                           os.path.relpath(os.path.join(root, file), 
                           'documento_tmp'))
                
    shutil.rmtree('documento_tmp')

# Función para limpiar los campos de texto
def limpiar_campos(page):
    # Restablece todos los campos a sus valores predeterminados
    fecha_facturacion.value = ''
    numero_factura.value = ''
    nombre_cliente.value = ''
    direccion_cliente.value = ''
    item_name_1.value = ''
    item_name_2.value = ''
    quantity_item_1.value = '0'
    quantity_item_2.value = '0'
    price_item_1.value = '0'
    price_item_2.value = '0'
    # Actualiza la página para reflejar los cambios
    page.update()

# Función principal
def main(page: ft.Page):
    page.scroll = "always"
    page.window_width = 700
    
    # Cambiar el color de fondo de la página
    page.bgcolor = ft.colors.INDIGO_800
    # Título principal
    titulo = ft.Text('Creación de Factura', style=ft.TextThemeStyle.HEADLINE_MEDIUM, color=ft.colors.GREEN_ACCENT)

    # Función que recoge los datos y genera la factura
    def obtener_datos(e):
        data_factura = {
            '%FECHA%' : fecha_facturacion.value,
            '%FACTURA%' : numero_factura.value,
            '%NOMBRE%' : nombre_cliente.value,
            '%DIRECCION%' : direccion_cliente.value,
            '%ITEM1%' : item_name_1.value,
            '%QITEM1%' : quantity_item_1.value,
            '%PITEM1%' : price_item_1.value,
            '%ITEM2%' : item_name_2.value,
            '%QITEM2%' : quantity_item_2.value,
            '%PITEM2%' : price_item_2.value,
            '%TITEM1%' : str(int(quantity_item_1.value) * int(price_item_1.value)),
            '%TITEM2%' : str(int(quantity_item_2.value) * int(price_item_2.value)),
            '%TOTAL%' : str((int(quantity_item_1.value) * int(price_item_1.value)) + (int(quantity_item_2.value) * int(price_item_2.value)))
        }
        generar_factura(data_factura)
        page.dialog = dialogo
        dialogo.open = True
        page.update()

    # Botón "Generar Factura"
    generar_btn = ft.ElevatedButton('Generar Factura', on_click=obtener_datos)

    # Botón "Limpiar"
    limpiar_btn = ft.ElevatedButton('Limpiar', on_click=lambda e: limpiar_campos(page), bgcolor=ft.colors.RED_400, color=ft.colors.WHITE)

    # Estilo del diseño, con espaciado y alineación adecuada
    page.add(
        titulo,
        ft.Column(
            controls=[
                ft.Row(controls=[fecha_facturacion, numero_factura], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(controls=[nombre_cliente, direccion_cliente], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(controls=[item_name_1, quantity_item_1, price_item_1], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(controls=[item_name_2, quantity_item_2, price_item_2], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(controls=[generar_btn, limpiar_btn], alignment=ft.MainAxisAlignment.CENTER)
            ], 
            spacing=20,  
            alignment=ft.MainAxisAlignment.CENTER
        )
    )


ft.app(target=main)

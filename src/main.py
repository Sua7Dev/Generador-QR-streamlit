import streamlit as st
import qrcode
from PIL import Image
from io import BytesIO
import random
import datetime

# Valores por defecto para las opciones de personalización
DEFAULT_FILL_COLOR = "#262626"
DEFAULT_BACK_COLOR = "#FFFFFF"
DEFAULT_BOX_SIZE = 8
DEFAULT_BORDER = 2
DEFAULT_URL = "https://youtu.be/xvFZjo5PgG0?si=VSdPrOL2gzcUuZM9"

numero_random = random.randint(1111, 9999)
numero_string = str(numero_random)
fecha_actual = datetime.datetime.now().strftime("%d-%m-%Y")
nombre_junto = "QR " + numero_string + " " + fecha_actual + ".png"

def generate_qr_code(data, fill_color="black", back_color="white", box_size=8, border=2):
    """
    Genera un código QR con estilo personalizado.

    Args:
        data (str): La URL o texto a codificar en el QR.
        fill_color (str): Color de los módulos del QR.
        back_color (str): Color de fondo del QR.
        box_size (int): Tamaño de cada "caja" o módulo del QR.
        border (int): Ancho del borde alrededor del QR.

    Returns:
        PIL.Image.Image: Objeto de imagen del código QR.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    return img

def display_qr_code(image):
    """
    Muestra el código QR en Streamlit.

    Args:
        image (PIL.Image.Image): Objeto de imagen del código QR.
    """
    # Convertir la imagen PIL a bytes para que st.image la pueda renderizar correctamente
    buf = BytesIO()
    image.save(buf, format="PNG")
    byte_im = buf.getvalue()
    st.image(byte_im, width="content") #, caption="Tu Código QR"


# Función para restablecer los valores
def reset_personalization():
    st.session_state.fill_color_key = DEFAULT_FILL_COLOR
    st.session_state.back_color_key = DEFAULT_BACK_COLOR
    st.session_state.box_size_key = DEFAULT_BOX_SIZE
    st.session_state.border_key = DEFAULT_BORDER
    st.session_state.url_input_key = DEFAULT_URL # También restablecemos la URL si lo deseas

def main():
    st.set_page_config(page_title="Generador de Códigos QR", layout="wide", page_icon=":material/qr_code:")

    # Inicializar session_state si no existen
    if "fill_color_key" not in st.session_state:
        st.session_state.fill_color_key = DEFAULT_FILL_COLOR
    if "back_color_key" not in st.session_state:
        st.session_state.back_color_key = DEFAULT_BACK_COLOR
    if "box_size_key" not in st.session_state:
        st.session_state.box_size_key = DEFAULT_BOX_SIZE
    if "border_key" not in st.session_state:
        st.session_state.border_key = DEFAULT_BORDER
    if "url_input_key" not in st.session_state:
        st.session_state.url_input_key = DEFAULT_URL

    col_izq, col_der = st.columns([5, 5])
    with col_izq:
        st.title("Generador de Códigos QR", anchor=False)
        with st.form("my_form"):
            url_input = st.text_input("Ingresa la URL o texto aquí", 
                                      value=st.session_state.url_input_key, key="url_input_key")
            generar_boton = st.form_submit_button("Generar QR", icon=":material/qr_code_2_add:", type="primary")        
        with st.expander("Personaliza tu QR", expanded=True, icon=":material/instant_mix:"):
            _, col1, col2, _ = st.columns([2, 3, 3, 2])
            with col1:
                fill_color = st.color_picker("Color del QR", value=st.session_state.fill_color_key, key="fill_color_key")
            with col2:
                back_color = st.color_picker("Color de Fondo", value=st.session_state.back_color_key, key="back_color_key")
            box_size = st.slider("Tamaño del Módulo", min_value=5, max_value=20, value=st.session_state.box_size_key, key="box_size_key")
            border = st.slider("Ancho del Borde", min_value=0, max_value=10, value=st.session_state.border_key, key="border_key")

            # Botón de Restablecer
            st.button(
                "Restablecer Opciones",
                on_click=reset_personalization,
                icon=":material/refresh:",
                help="Restablece todas las opciones de personalización a sus valores iniciales."
            )

    def download_qr_button(image, filename=nombre_junto):
        """
        Crea un botón para descargar el código QR.

        Args:
            image (PIL.Image.Image): Objeto de imagen del código QR.
            filename (str): Nombre del archivo de descarga.
        """
        buf = BytesIO()
        image.save(buf, format="PNG")
        byte_im = buf.getvalue()
        st.download_button(
            width=box_size * 30,
            icon=":material/download:",
            label="Descargar QR",
            data=byte_im,
            file_name=filename,
            mime="image/png"
        )

    with col_der:
        if generar_boton:
            if url_input:
                qr_image = generate_qr_code(url_input, fill_color, back_color, box_size, border)
                st.toast("¡Código QR generado con éxito!")
                display_qr_code(qr_image)
                _, col_relleno = st.columns([0.1, 8.8])
                with col_relleno:
                    download_qr_button(qr_image)
            else:
                st.warning("Por favor, introduce una URL o texto para generar el QR.")

    st.markdown("---")
    col_mensajefinal_izq, col_mensajefinal_der, _ = st.columns([3, 3, 10]) 
    with col_mensajefinal_izq:
        st.markdown("Desarrollado con ❤️ por [@Sua7Dev](https://github.com/Sua7Dev)")
    with col_mensajefinal_der:
        seleccion = st.feedback("thumbs")
        if seleccion is not None:
            st.markdown("¡Gracias por tu opinion!")

if __name__ == "__main__":
    main()
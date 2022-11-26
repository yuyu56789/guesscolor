import colorsys
import csv
import numpy as np
from PIL import Image
import streamlit as st
from streamlit_cropper import st_cropper


# NOTE: This must be the first command in your app, and must be set only once
st.set_page_config(page_title="color-perception",    layout="wide")

# hide menu and footer
hide_streamlit_style = """
                    <style>
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    </style>
                    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

IMG_W = 700
IMG_H = 90


@st.cache
class SETTING:
    Aperture_X = 20
    Aperture_Y = 20


@st.cache
class WM:
    value_H_ANS: int
    value_S_ANS: int
    value_L_ANS: int
    value_R_ANS: int
    value_G_ANS: int
    value_B_ANS: int
    value_ANS: int
    value_EXP: int
    color_arr_ans = []  # HEX_String
    color_arr_exp = []  # HEX_String


def loadcsv():
    with open('config/config.csv', 'r+', newline='') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            # print('from File:' + row[0],row[1])
            SETTING.Aperture_X = int(row[0])
            SETTING.Aperture_Y = int(row[1])

    WM.color_arr_ans = []  # HEX_String
    WM.color_arr_exp = []  # HEX_String
    with open('config/csv_log.csv', 'r+', newline='') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            # print('from File:' + row[0],row[1])
            WM.color_arr_ans.append(row[0])
            WM.color_arr_exp.append(row[1])
    return WM


loadcsv()


def writecsv(color_ans, color_exp):
    with open('config/csv_log.csv', 'a+', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([color_ans, color_exp])
    return


@st.cache(allow_output_mutation=True)
def create_colorbar_basic(h=40, w=360, x=200):
    basebar = np.zeros((h, w, 3), dtype=np.uint8)
    return basebar


# create a HSV colorbar
def create_colorbar_HSV(h=40, w=360, x=200):
    bar = create_colorbar_basic(h, w, x)
    for j in range(0, h-1, 1):
        for i in range(0, w-1, 1):
            dd = (i-x)*(i-x)+(j-h/2)*(j-h/2)
            if dd < h*h/16 and dd > h*h/64:
                bar[j, i] = (round((1-r)*255),
                             round((1-g)*255), round((1-b)*255))
            else:
                # colorsys.hls_to_rgb
                (r, g, b) = colorsys.hsv_to_rgb(i/w, 1.0, 1.0)
                bar[j, i] = (round(r*255), round(g*255), round(b*255))
    return bar

# RGB to Hex string


def RGB_to_Hex(r:int, g:int, b:int):
    color = '#'
    color += str(hex(r))[-2:].replace('x', '0').upper()
    color += str(hex(g))[-2:].replace('x', '0').upper()
    color += str(hex(b))[-2:].replace('x', '0').upper()
    # print(color)
    return color


# Hex string to RGB int
def Hex_to_RGB(hex:str):
    r = int(hex[1:3], 16)
    g = int(hex[3:5], 16)
    b = int(hex[5:7], 16)
    # print(r,g,b)
    return (r, g, b)


def set_rect(img: Image, aspect_ratio: tuple):
    res = {'left': 100, 'top': 100, 'width': SETTING.Aperture_X,
           'height': SETTING.Aperture_Y}
    return res

# def updateCrop(val):
#     print(val)


def onChangeSliderH():
    print("....")


# def updateSlider(val):
#     print('.x')


@st.cache(suppress_st_warning=True)
def defaultimage():
    return Image.open("./picture/lodka.jpg")


@st.cache(suppress_st_warning=True)
def newselectimage(img_file):
    return Image.open(img_file)


def loadimage():
    img_file = st.sidebar.file_uploader(
        # label='Upload a file', type=['png', 'jpg', 'jpeg'])
        label='Upload a image:')
    if img_file:
        img = newselectimage(img_file)
    else:
        img = defaultimage()
    return img


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
st.sidebar.header("Color Perception")
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

img = loadimage()

# main


def run_main():
    global colorbar
    global img

    col1, col2 = st.columns([100, 50])

    with col1:
        
        cropped_img = st_cropper(img, realtime_update=True,
                                 box_color='#ff0000', aspect_ratio=(1, 1), box_algorithm=set_rect)
            
        if cropped_img:
            (r, g, b) = np.average(cropped_img, axis=(0, 1))
            (h, l, s) = colorsys.rgb_to_hls(r/255, g/255, b/255)
            WM.value_H_ANS = round(h * 360)
            WM.value_S_ANS = round(s * 100)
            WM.value_L_ANS = round(l * 100)
            WM.value_R_ANS = round(r)
            WM.value_G_ANS = round(g)
            WM.value_B_ANS = round(b)
            WM.value_ANS = WM.value_EXP = RGB_to_Hex(
                round(r), round(g), round(b))

            if "value_EXP" not in st.session_state or not st.session_state["value_EXP"] == WM.value_EXP:
                st.session_state["value_ANS"] = WM.value_ANS
                st.session_state["value_EXP"] = WM.value_EXP
                st.session_state["new_problem"] = True
                st.write("new...")
                # print("1:", WM.value_H_ANS, WM.value_S_ANS, WM.value_L_ANS)
            else:
                WM.value_ANS = st.session_state["value_ANS"]
                WM.value_EXP = st.session_state["value_EXP"]
                st.session_state["new_problem"] = False

        # =========== read ===========
        WM.value_ANS = st.session_state["value_ANS"]
        (WM.value_R_ANS, WM.value_G_ANS, WM.value_B_ANS) = (
            r, g, b) = Hex_to_RGB(WM.value_ANS)
        (h, l, s) = colorsys.rgb_to_hls(r/255, g/255, b/255)
        WM.value_H_ANS = round(h * 360)
        WM.value_S_ANS = round(s * 100)
        WM.value_L_ANS = round(l * 100)
        # print("2:", WM.value_H_ANS, WM.value_S_ANS, WM.value_L_ANS)
        # =========== read ===========

    with col2:

        colorSpace = st.radio(
            "Color Model:", ('HSL', 'RGB'), horizontal=True, index=0)

        ph_picker = st.empty()
        ph_colorbar = st.empty()
        ph_value_1 = st.empty()
        ph_value_2 = st.empty()
        ph_value_3 = st.empty()

        if colorSpace == 'HSL':

            WM.value_H_ANS = ph_value_1.slider(
                "Hue (H):", min_value=0, max_value=360, step=1, value=WM.value_H_ANS, format='%d°')
            WM.value_S_ANS = ph_value_2.slider(
                "Saturation (S):", min_value=0, max_value=100, step=1, value=WM.value_S_ANS, format='%d%%')
            WM.value_L_ANS = ph_value_3.slider(
                "Lightness (L):", min_value=0, max_value=100, step=1, value=WM.value_L_ANS, format='%d%%')

            (r, g, b) = colorsys.hls_to_rgb(
                WM.value_H_ANS/360, WM.value_L_ANS/100, WM.value_S_ANS/100)
            (WM.value_R_ANS, WM.value_G_ANS, WM.value_B_ANS) = (
                round(r*255), round(g*255), round(b*255))
            WM.value_ANS = RGB_to_Hex(
                WM.value_R_ANS, WM.value_G_ANS, WM.value_B_ANS)
            
            t = ph_picker.color_picker(key="Percepted or Expected Color:",
                                           label="Percepted Color:", value=WM.value_ANS)
                                          
            (WM.value_R_ANS, WM.value_G_ANS, WM.value_B_ANS) = (
                r, g, b) = Hex_to_RGB(t)
            WM.value_ANS = RGB_to_Hex(
                WM.value_R_ANS, WM.value_G_ANS, WM.value_B_ANS)
                   
            (h, l, s) = colorsys.rgb_to_hls(r/255, g/255, b/255)
            WM.value_H_ANS = round(h * 360)
            WM.value_S_ANS = round(s * 100)
            WM.value_L_ANS = round(l * 100)

            if not t == st.session_state["value_ANS"]:
                st.session_state["value_ANS"] = t   
                if not st.session_state["new_problem"]:   
                    st.session_state["new_problem"] = True          
                st.experimental_rerun()

            colorbar = create_colorbar_HSV(40, 700, WM.value_H_ANS*700/360)
            ph_colorbar.image(colorbar)

        elif colorSpace == 'RGB':                        
            WM.value_R_ANS = ph_value_1.slider(
                "Red (R):", min_value=0, max_value=255, step=1, value=WM.value_R_ANS)
            WM.value_G_ANS = ph_value_2.slider(
                "Green (G):", min_value=0, max_value=255, step=1, value=WM.value_G_ANS)
            WM.value_B_ANS = ph_value_3.slider(
                "Blue (B):", min_value=0, max_value=255, step=1, value=WM.value_B_ANS)

            WM.value_ANS = RGB_to_Hex(
                WM.value_R_ANS, WM.value_G_ANS, WM.value_B_ANS)

            if not st.session_state["new_problem"]:
                t = ph_picker.color_picker(key="Percepted or Expected Color:",
                                           label="Percepted Color:", value=WM.value_ANS)
            else:
                t = ph_picker.color_picker(key="Percepted or Expected Color:",
                                           label="Expected Color:", value=WM.value_ANS)

            if not t == st.session_state["value_ANS"]:
                st.session_state["value_ANS"] = t   
                if not st.session_state["new_problem"]:   
                    st.session_state["new_problem"] = True          
                st.experimental_rerun()


            (WM.value_R_ANS, WM.value_G_ANS, WM.value_B_ANS) = (
                r, g, b) = Hex_to_RGB(t)
            WM.value_ANS = RGB_to_Hex(
                WM.value_R_ANS, WM.value_G_ANS, WM.value_B_ANS)

            (h, l, s) = colorsys.rgb_to_hls(r/255, g/255, b/255)
            WM.value_H_ANS = round(h * 360)
            WM.value_S_ANS = round(s * 100)
            WM.value_L_ANS = round(l * 100)

            colorbar = create_colorbar_HSV(40, 700, WM.value_H_ANS*700/360)
            ph_colorbar.image(colorbar)

        submit = st.button("Submit")
        if submit:
            WM.color_arr_ans.append(WM.value_ANS)  # string
            WM.color_arr_exp.append(WM.value_EXP)  # string
            print('Times:', len(WM.color_arr_ans), 'Expected:',
                  WM.value_EXP, 'Percepted:', WM.value_ANS)  # string

            writecsv(WM.value_ANS, WM.value_EXP)

    # The Left List
    for i in range(len(WM.color_arr_ans)):
        st.sidebar.color_picker(
            label="Percepted :"+str(i+1), value=WM.color_arr_ans[i])
    clr_his = st.sidebar.button("Clear History")
    if (clr_his):
        with open('config/csv_log.csv', 'w+', newline='') as csv_file:
            writer = csv.writer(csv_file)
        WM.color_arr_ans = []
        WM.color_arr_exp = []
        st.experimental_rerun()


if __name__ == "__main__":
    run_main()

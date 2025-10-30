import streamlit as st

st.set_page_config(
    page_title="Students Mental Health"
)

visualize = st.Page('studentmental.py', title= 'Pencapaian Akademik', icon=":material/school:")

home = st.Page('home.py' , title = "Homepage",default=True, icon=":material/home:")

pg = st.navigation(
        {
            "Menu":[home,visualize]
        }
    )

pg.run()

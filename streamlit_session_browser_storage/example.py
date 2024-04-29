import streamlit as st
# from __init__ import SessionStorage
from streamlit_session_browser_storage import SessionStorage

st.set_page_config(layout="wide")

sessionS = SessionStorage() 
sessionS.setItem("Mike", "Dame")

result = sessionS.getItem("King")
st.write(result)

# sessionS.deleteItem("King")
result = sessionS.getItem("King")
st.write(result)

st.write(sessionS.getAll()  )

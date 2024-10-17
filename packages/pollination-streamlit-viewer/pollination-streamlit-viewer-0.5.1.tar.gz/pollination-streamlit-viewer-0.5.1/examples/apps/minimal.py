import streamlit as st
# viewer is taken from __init__.py context
from pollination_streamlit_viewer import viewer

# session variables
if 'count' not in st.session_state:
    st.session_state.count = 0

file = st.file_uploader(
    label=".vtkjs scene uploader",
    type=["vtkjs", "vtk", "vtp"],
    help="Upload a .vtkjs scene file"
)

if file:
    viewer(
        content=file.getvalue(),  
        key='vtkjs-viewer',
        subscribe=False,
        style={
            'height' : '640px'
        }
    )
st.session_state.count += 1
st.warning(f'I ran n.{st.session_state.count} times.')
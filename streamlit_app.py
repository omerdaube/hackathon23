import streamlit as st

def toggle_checkbox(checkbox_id):
    checkboxes[checkbox_id][1] = not checkboxes[checkbox_id][1]

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    lines = uploaded_file.read().decode("utf-8").splitlines()

    checkboxes = {}
    for i, line in enumerate(lines):
        text, marked = line.strip().split(",")
        checkboxes[i] = [text, marked == "YES"]

    st.set_page_config(page_title="helo", page_icon=":clipboard:")
    st.title("helo")

    for i in range(len(checkboxes)):
        checkbox_id = str(i)
        text, marked = checkboxes[i]
        if marked:
            checkbox_state = st.checkbox(text, key=checkbox_id)
        else:
            checkbox_state = st.checkbox(text, value=False, key=checkbox_id)
        if checkbox_state:
            toggle_checkbox(i)

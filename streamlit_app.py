import streamlit as st

# Define a function to read the uploaded file and display checkboxes for each line
def process_file(uploaded_file):
    if uploaded_file is not None:
        # Read the contents of the file as a string
        contents = uploaded_file.getvalue().decode('utf-8')
        # Split the contents into lines
        lines = contents.split('\n')
        # Display a checkbox for each line, marking the ones with "YES" after the comma
        for line in lines:
            if "," in line:
                parts = line.split(",")
                if len(parts) == 2 and parts[1].strip() == "YES":
                    checkbox_value = st.checkbox(parts[0], value=True)
                else:
                    checkbox_value = st.checkbox(parts[0], value=False)
            else:
                checkbox_value = st.checkbox(parts[0], value=False)

# Create the Streamlit app
def main():
    st.title("File Uploader and Checkbox Demo")
    # Add a file uploader to the app
    uploaded_file = st.file_uploader("Choose a file")
    # Call the process_file function when the file is uploaded
    process_file(uploaded_file)

if __name__ == '__main__':
    main()

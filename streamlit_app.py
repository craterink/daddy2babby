import streamlit as st


def main():
    st.title("Big Text Box Input Example")
    
    # Add a big text box for user input
    user_input = st.text_area("Enter your text here:", height=200)

    # Check if user has submitted text
    if st.button('Submit'):
        # Parse user input for variables in curly braces
        variables = [v.strip('{}') for v in user_input.split() if v.startswith('{') and v.endswith('}')]

        # Add a form to group the text inputs
        with st.form(key='query_form'):
            # Render an input for each variable with the label "Give a basic query example"
            for var in variables:
                query = st.text_input(f"Give a basic query example for {var}:", key=var)

            # Add a button to generate examples
            st.form_submit_button('Generate Examples')

if __name__ == '__main__':
    main()

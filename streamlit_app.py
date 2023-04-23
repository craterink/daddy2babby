import streamlit as st


def main():
    st.title("Daddy 2 Babby")
    
    # Add a big text box for user input
    user_input = st.text_area("1. Paste your prompt template here:", height=200)

    # Check if user has submitted text
    if st.button('Submit'):
        # Parse user input for variables in curly braces
        variables = [v.strip('{}') for v in user_input.split() if v.startswith('{') and v.endswith('}')]

        # Print the parsed variables
        st.write("Variables found in text:", variables)

        # Render an input for each variable with the label "Give a basic query example"
        for var in variables:
            query = st.text_input(f"Give a basic query example for {var}:")

if __name__ == '__main__':
    main()
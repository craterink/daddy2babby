import streamlit as st
import openai
import csv
from math import ceil
import io

# Define the batch size (number of examples per batch)
BATCH_SIZE = 20

def generate_and_evaluate_batches(api_key, agent_description, prompt, num_examples, batch_size):
    openai.api_key = api_key

    # Calculate the number of batches required
    num_batches = ceil(num_examples / batch_size)
    all_examples = []

    # Create a progress bar
    progress_bar = st.progress(0)

    for batch_idx in range(num_batches):
        # Calculate the start and end index for the current batch
        start_idx = batch_idx * batch_size
        end_idx = min(start_idx + batch_size, num_examples)

        # Determine the number of examples to request in the current batch
        current_batch_size = end_idx - start_idx
        
        # Generate examples for the current batch
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=50 * current_batch_size,
            n=1,
            stop=None,
            temperature=0.8,
        )

        examples_raw = response.choices[0].text.strip().split("\n\n")
        batch_examples = []
        for ex in examples_raw:
            if ex.count("\n") == 1:  # Ensure there is exactly one newline character
                input_text, output_text = ex.split("\n")
                input_value = input_text.replace("Input: ", "").strip()
                output_value = output_text.replace("Output: ", "").strip()

                input_output_grade_tuple = (input_value, output_value)
                if len(input_output_grade_tuple) == 2:
                    batch_examples.append(input_output_grade_tuple)
        
        all_examples.extend(batch_examples)

        # Update the progress bar
        progress = (batch_idx + 1) / num_batches
        progress_bar.progress(progress)

    return all_examples

def main():
    st.title("Training Specialized Agents for the Edge")
    st.header("Training Data Generator")

    api_key = st.text_input("Enter your OpenAI API key:")
    agent_description = st.text_input("Enter the agent description:", value="You are a language tutor who is tasked with giving feedback on a student's translation of a German sentence. The student's grade level is 6th grade and you should follow the following principles when giving feedback: * be particularly helpful and reference parts of the translated/target sentences in quotes * be helpful, do not e.g. scold the student * please provide two parts of your feedback: 1) an overall grade Needs work, Good, Excellent; and 2) a note on what could be improved")
    example_type = st.text_input("Enter the types of example training data to create (input, output):", value="Input: Ich bin ein Geheimagent. Output: I am a secret agent.")
    num_examples = st.number_input("Enter the number of examples you want:", min_value=1, value=10, step=1)

    if st.button("Generate Examples"):
        prompt = f"You are an AI language model ({agent_description}). Generate {num_examples} examples of {example_type} training data. Strictly follow the Input/Output format, and only return the Input and Output."
        generated_examples = generate_and_evaluate_batches(api_key, agent_description, prompt, num_examples, BATCH_SIZE)

        csv_output = io.StringIO()
        csv_writer = csv.writer(csv_output)
        csv_writer.writerow(["Input", "Output"])
        for row in generated_examples:
            csv_writer.writerow(row)
        csv_content = csv_output.getvalue()
        # Add a download button for the generated CSV file
        st.download_button(
            label="Download CSV",
            data=csv_content,
            file_name="generated_dummy_data.csv",
            mime="text/csv",
        )
        st.success(f"Generated {len(generated_examples)} examples")

if __name__ == "__main__":
    main()

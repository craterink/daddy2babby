import streamlit as st
import openai
import csv

def generate_dummy_data(api_key, agent_description, prompt, num_examples):
    openai.api_key = api_key
    
    examples = []

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50 * num_examples,
        n=1,
        stop=None,
        temperature=0.8,
    )

    examples_raw = response.choices[0].text.strip().split("\n\n")
    for ex in examples_raw:
        input_text, output_text = ex.split("\n")
        input_value = input_text.replace("Input: ", "").strip()
        output_value = output_text.replace("Output: ", "").strip()

        # Generate grade for each input/output pair
        grade_prompt = f"You are an AI language model ({agent_description}). The student translated the sentence '{input_value}' to '{output_value}'. Evaluate the translation and provide feedback."
        grade_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=grade_prompt,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.8,
        )
        grade_value = grade_response.choices[0].text.strip()

        input_output_grade_tuple = (input_value, output_value, grade_value)
        if len(input_output_grade_tuple) == 3:
            examples.append(input_output_grade_tuple)

    return examples[:num_examples]

def save_to_csv(examples, output_file):
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["Input", "Output", "Grade"])
        for row in examples:
            csv_writer.writerow(row)

def main():
    st.title("Dummy Data Generator")
    st.header("OpenAI Language Model")

    api_key = st.text_input("Enter your OpenAI API key:")
    agent_description = st.text_input("Enter the agent description:", value="You are a language tutor who is tasked with giving feedback on a student's translation of a german sentence. The student's grade level is 6th grade and you should follow the following principles when giving feedback: * be particularly helpful and reference parts of the translated/target sentences in quotes * be helpful, do not e.g. scold the student * please provide two parts of your feedback: 1) an overall grade Needs work, Good, Excellent; and 2) a note on what could be improved")
    example_type = st.text_input("Enter the types of example training data to create (input, output):", value="Input: Ich bin ein Geheimagent. Output: I am a secret agent.")
    num_examples = st.number_input("Enter the number of examples you want:", min_value=1, value=10, step=1)
    output_file = st.text_input("Enter the output CSV filename:", value="generated_dummy_data.csv")

    if st.button("Generate Examples"):
        prompt = f"You are an AI language model ({agent_description}). Generate {num_examples} examples of {example_type} training data. Strictly follow the Input/Output format, and only return the Input and Output."
        generated_examples = generate_dummy_data(api_key, agent_description, prompt, num_examples)
        save_to_csv(generated_examples, output_file)
        st.success(f"Generated {len(generated_examples)} examples")

if __name__ == "__main__":
    main()

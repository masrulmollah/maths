import streamlit as st
import pandas as pd
import os

# Function to save problems to a local file
def save_problems(file_path, df):
    df.to_csv(file_path, index=False)

# Function to load problems from the file if it exists and has data
def load_problems(file_path):
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame(columns=['Class', 'Category', 'Problem', 'Answer'])

# Main App
def main():
    # Custom colorful subheader
    st.markdown(
        """
        <h1 style='text-align: center; color: #FFFFFF; 
        background: linear-gradient(90deg, rgba(29,53,87,1) 0%, rgba(69,123,157,1) 35%, rgba(241,95,95,1) 100%); 
        padding: 10px; border-radius: 10px;'>Muhammad Math Challenge</h1>
        """, 
        unsafe_allow_html=True
    )

    # File to save problems
    file_path = "math_problems.csv"

    # Load existing problems from the CSV file
    if "problem_data" not in st.session_state:
        st.session_state.problem_data = load_problems(file_path)

    # Get unique categories
    unique_categories = st.session_state.problem_data['Category'].unique().tolist()

    # Tabs at the top: "View Challenge" and "Add Challenge"
    tab1, tab2 = st.tabs(["View Challenge", "Add Challenge"])

    with tab1:
        if unique_categories:
            category_tabs = st.tabs(unique_categories)
            for category, cat_tab in zip(unique_categories, category_tabs):
                with cat_tab:
                    # Filter classes based on the selected category
                    filtered_classes = st.session_state.problem_data[
                        st.session_state.problem_data['Category'] == category
                    ]['Class'].unique().tolist()

                    # Create columns to align the class dropdown on the right
                    col1, col2 = st.columns([3, 1])

                    with col2:
                        # Dropdown to select a class within the selected category
                        if filtered_classes:
                            selected_class = st.selectbox("", filtered_classes, key=f"class_{category}")
                        else:
                            selected_class = None
                            st.write("No classes available yet. Please add problems in the 'Add Challenge' tab.")

                    if selected_class:
                        with col1:
                            class_data = st.session_state.problem_data[
                                (st.session_state.problem_data['Class'] == selected_class) &
                                (st.session_state.problem_data['Category'] == category)
                            ]

                            if not class_data.empty:
                                for index, row in class_data.iterrows():
                                    # Display the problem figures
                                    problem_html = f"""
                                    <p style="color:#2E86C1; font-size:24px; margin-left: 20px;"><strong>{row['Problem']}</strong></p>
                                    """
                                    st.markdown(problem_html, unsafe_allow_html=True)

                                    # Answer box and submit button
                                    user_answer = st.text_input("Put your answer below", key=f"answer_{index}_{category}")
                                    
                                    col1, col2 = st.columns([1, 2])
                                    
                                    with col1:
                                        submit_button = st.button("Submit", key=f"submit_{index}_{category}")

                                    with col2:
                                        if submit_button and user_answer:
                                            try:
                                                if int(user_answer.strip()) == int(row['Answer']):
                                                    st.success("Correct!")
                                                else:
                                                    st.error("Incorrect, try again.")
                                            except ValueError:
                                                st.error("Please enter a valid integer.")

                            else:
                                st.write(f"No problems available for the selected class.")
        else:
            st.write("No categories available yet. Please add problems in the 'Add Challenge' tab.")

    with tab2:
        # Custom subheader with a suitable color scheme
        st.markdown(
            """
            <h2 style='color:#FFFFFF; background-color:#FF5733; padding:10px; border-radius:5px;'>Add New Math Problem</h2>
            """, 
            unsafe_allow_html=True
        )

        # Input fields for adding a problem
        problem = st.text_input("Enter the math problem (e.g., 3 + 2):")
        answer = st.number_input("Enter the answer:", min_value=0)
        problem_class = st.text_input("Enter the class of the problem:")
        problem_category = st.text_input("Enter the category of the problem:")

        if st.button("Add Problem"):
            if problem and problem_class and problem_category:
                new_problem = pd.DataFrame([[problem_class, problem_category, problem, answer]], 
                                           columns=['Class', 'Category', 'Problem', 'Answer'])
                st.session_state.problem_data = pd.concat([st.session_state.problem_data, new_problem], ignore_index=True)
                st.success(f"Problem '{problem}' added successfully!")
            else:
                st.warning("Please enter the problem, answer, class, and category.")

        st.subheader("Save Problems to CSV")
        if st.button("Save Problems"):
            save_problems(file_path, st.session_state.problem_data)
            st.success(f"Problems saved to {file_path} successfully!")

if __name__ == "__main__":
    main()

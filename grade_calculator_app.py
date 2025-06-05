import pandas as pd
import streamlit as st

# Grade calculation logic
def calculate_grade(total_marks, grade_boundaries):
    if total_marks >= grade_boundaries['A']:
        return 'A'
    elif total_marks >= grade_boundaries['A-']:
        return 'A-'
    elif total_marks >= grade_boundaries['B+']:
        return 'B+'
    elif total_marks >= grade_boundaries['B']:
        return 'B'
    elif total_marks >= grade_boundaries['B-']:
        return 'B-'
    elif total_marks >= grade_boundaries['C+']:
        return 'C+'
    elif total_marks >= grade_boundaries['C']:
        return 'C'
    elif total_marks >= grade_boundaries['C-']:
        return 'C-'
    elif total_marks >= grade_boundaries['D']:
        return 'D'
    else:
        return 'F'

# UI App
st.title("📊 Grade Calculator App")
st.caption("Project by Affan Zulfiqar")

uploaded_file = st.file_uploader("Upload an Excel file (.xlsx) with columns 'Name' and 'Total Marks (100)'", type="xlsx")

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file, header=1)
        df.columns = df.columns.str.strip()

        if 'Name' not in df.columns or 'Total Marks (100)' not in df.columns:
            st.error("The file must contain 'Name' and 'Total Marks (100)' columns.")
        else:
            mean = df['Total Marks (100)'].mean()
            std = df['Total Marks (100)'].std()

            grade_boundaries = {
                'A': mean + 1.5 * std,
                'A-': mean + 1 * std,
                'B+': mean + 0.5 * std,
                'B': mean,
                'B-': mean - 0.5 * std,
                'C+': mean - 1 * std,
                'C': mean - 1.5 * std,
                'C-': mean - 2 * std,
                'D': mean - 2.5 * std,
                'F': float('-inf')
            }

            df['Grade'] = df['Total Marks (100)'].apply(lambda x: calculate_grade(x, grade_boundaries))

            st.subheader("📋 Students and Their Grades")
            st.dataframe(df[['Name', 'Total Marks (100)', 'Grade']].reset_index(drop=True))

            st.subheader("📐 Grade Boundaries")
            for grade, lower in grade_boundaries.items():
                if grade == 'F':
                    st.write(f"{grade}: less than {grade_boundaries['D']:.2f}")
                elif grade == 'A':
                    st.write(f"{grade}: {grade_boundaries['A']:.2f} and above")
                else:
                    upper = grade_boundaries[list(grade_boundaries.keys())[list(grade_boundaries.keys()).index(grade) - 1]]
                    st.write(f"{grade}: {lower:.2f} to {upper:.2f}")

            st.markdown(f"**Mean:** {mean:.2f}  **Standard Deviation:** {std:.2f}")

    except Exception as e:
        st.error(f"Error reading file: {e}")

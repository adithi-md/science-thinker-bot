import ollama

def grade_experiment(report_text):
    """
    Grades a student's science experiment report using Llama 3.2.
    """

    prompt = f"""
    You are a science teacher.

    Grade the following science experiment report out of 100 using this rubric:

    1. Aim clarity (10 marks)
    2. Materials completeness (20 marks)
    3. Procedure clarity (20 marks)
    4. Scientific explanation (30 marks)
    5. Safety precautions (10 marks)
    6. Overall presentation (10 marks)

    For each section:
    - Give marks
    - Give short feedback
    - At the end, give total score out of 100

    Report:
    {report_text}
    """

    try:
        response = ollama.chat(
            model="llama3.2:latest",
            messages=[{"role": "user", "content": prompt}]
        )

        return response["message"]["content"]

    except Exception as e:
        return f"Error grading report: {e}"

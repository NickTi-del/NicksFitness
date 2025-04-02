
import streamlit as st
from fpdf import FPDF
import io

st.title("Personalised Fitness & Nutrition Planner")

st.header("Enter Your Details")
age = st.number_input("Age", min_value=10, max_value=100, value=22)
height = st.number_input("Height (cm)", min_value=140, max_value=220, value=180)
weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=90.3)
body_fat = st.number_input("Current Body Fat %", min_value=5.0, max_value=50.0, value=17.8)
goal_body_fat = st.number_input("Target Body Fat %", min_value=5.0, max_value=20.0, value=12.0)
goal_type = st.selectbox("Goal", ["Cut", "Bulk", "Maintain"])

fat_mass = weight * (body_fat / 100)
lean_mass = weight - fat_mass
target_weight = lean_mass / (1 - (goal_body_fat / 100))
fat_to_lose = weight - target_weight

if goal_type == "Cut":
    calorie_target = 2500
elif goal_type == "Bulk":
    calorie_target = 3200
else:
    calorie_target = 2900

protein = round(2.4 * lean_mass)
fats = round(0.8 * weight)
carbs = round((calorie_target - (protein * 4 + fats * 9)) / 4)

st.header("Your Personalised Plan")
st.markdown(f"**Target Weight:** {target_weight:.1f} kg")
st.markdown(f"**Fat to Lose:** {fat_to_lose:.1f} kg")
st.markdown(f"**Calories per Day:** {calorie_target} kcal")
st.markdown(f"**Protein:** {protein}g | **Fats:** {fats}g | **Carbs:** {carbs}g")

if st.button("Download Plan as PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Fitness & Nutrition Plan", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.ln(10)
    pdf.multi_cell(0, 10, f"Age: {age}\nHeight: {height} cm\nWeight: {weight} kg\n"
                          f"Body Fat: {body_fat}%\nGoal Body Fat: {goal_body_fat}%\nGoal: {goal_type}\n\n"
                          f"Target Weight: {target_weight:.1f} kg\nFat to Lose: {fat_to_lose:.1f} kg\n"
                          f"Calories: {calorie_target} kcal\nProtein: {protein} g\nFats: {fats} g\nCarbs: {carbs} g")

    pdf_output = io.BytesIO()
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    pdf_output.write(pdf_bytes)
    pdf_output.seek(0)

    st.download_button(
        label="Download Your Plan",
        data=pdf_output,
        file_name="Fitness_Nutrition_Plan.pdf",
        mime="application/pdf"
    )

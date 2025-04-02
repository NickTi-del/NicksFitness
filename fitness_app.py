
import streamlit as st
from fpdf import FPDF
import io

# Sample meal templates for simplicity
MEAL_LIBRARY = {
    "high protein": [
        {
            "meal": "Grilled Chicken with Quinoa & Veggies",
            "ingredients": ["200g chicken breast", "1/2 cup quinoa", "broccoli", "olive oil", "garlic"],
            "instructions": "Grill chicken. Cook quinoa. Sauté veggies in olive oil. Combine and season."
        },
        {
            "meal": "Protein Oats",
            "ingredients": ["1/2 cup oats", "1 scoop whey protein", "banana", "almond butter"],
            "instructions": "Cook oats. Stir in protein powder, top with banana & almond butter."
        },
        {
            "meal": "Tuna Salad Bowl",
            "ingredients": ["1 can tuna", "mixed greens", "cherry tomatoes", "avocado", "balsamic dressing"],
            "instructions": "Mix all ingredients in a bowl."
        }
    ]
}

# Streamlit App
st.title("Advanced Fitness & Nutrition Planner")

st.header("Enter Your Details")
age = st.number_input("Age", min_value=10, max_value=100, value=22)
height = st.number_input("Height (cm)", min_value=140, max_value=220, value=180)
weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=90.3)
body_fat = st.number_input("Current Body Fat %", min_value=5.0, max_value=50.0, value=17.8)
goal_body_fat = st.number_input("Target Body Fat %", min_value=5.0, max_value=20.0, value=12.0)
goal_type = st.selectbox("Goal", ["Cut", "Bulk", "Maintain"])
diet_pref = st.selectbox("Diet Preference", ["high protein", "vegetarian", "pescatarian"])

# Calculations
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

# PDF Generation
if st.button("Download Plan as PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Fitness & Nutrition Plan", ln=True)

    pdf.set_font("Arial", '', 12)
    pdf.ln(10)
    pdf.multi_cell(0, 10, f"Age: {age}\nHeight: {height} cm\nWeight: {weight} kg\nBody Fat: {body_fat}%\nGoal Body Fat: {goal_body_fat}%\nGoal: {goal_type}\nDiet: {diet_pref}\n\nTarget Weight: {target_weight:.1f} kg\nFat to Lose: {fat_to_lose:.1f} kg\nCalories: {calorie_target} kcal\nProtein: {protein} g\nFats: {fats} g\nCarbs: {carbs} g")

    # Add Meal Plan Section
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, "Sample Meal Plan", ln=True)
    pdf.set_font("Arial", '', 12)

    meal_plan = MEAL_LIBRARY.get(diet_pref, [])
    all_ingredients = []

    for idx, meal in enumerate(meal_plan, start=1):
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, f"Meal {idx}: {meal['meal']}", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 10, f"Ingredients: {', '.join(meal['ingredients'])}\nInstructions: {meal['instructions']}\n")
        all_ingredients.extend(meal['ingredients'])

    # Shopping List
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, "Shopping List", ln=True)
    pdf.set_font("Arial", '', 12)
    for item in sorted(set(all_ingredients)):
        pdf.cell(200, 10, f"- {item}", ln=True)

    # Weekly Tracker
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, "Weekly Progress Tracker", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, "| Week | Weight (kg) | Notes |\n|------|-------------|-------|\n" + "\n".join([f"| {i} |             |       |" for i in range(1, 13)]))

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

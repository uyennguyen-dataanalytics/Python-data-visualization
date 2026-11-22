import pandas as pd
import matplotlib.pyplot as plt

#--------------------------------------------------------------------------------------------
# Loading and inspecting the data
#--------------------------------------------------------------------------------------------
# Load dataset into a DataFrame named patients  
patients = pd.read_csv("patients.csv")

# Print the number of rows and the number of columns
print("Number of rows and columns", patients.shape)

# Print the first 5 rows
print(patients.head())

# Print the column names as a list
print(list(patients.columns))

#--------------------------------------------------------------------------------------------
# Cleaning the data
#--------------------------------------------------------------------------------------------
# Print how many values are missing from the cholesterol column
print(f"Missing cholesterol values: {patients['cholesterol'].isna().sum()}")

# Print how many rows are exact duplicates of another row
print(f"Duplicated rows: {patients.duplicated().sum()}")

# Function to clean data
def clean_patients(df):
    """Clean the patients dataset by removing duplicate rows and replacing missing cholesterol values with the median"""
    cleaned_df = df.drop_duplicates()
    median_cholesterol = cleaned_df['cholesterol'].median()
    cleaned_df['cholesterol'] = cleaned_df['cholesterol'].fillna(median_cholesterol)
    return cleaned_df

# Call function and store the result backin patients dataset
patients = clean_patients(patients)

# Print the number of rows and the total number of missing values in the cleaned data
print(f"Rows after cleaning: {len(patients)}")
print(f"Missing value after cleaning: {patients.isna().sum().sum()}")

#--------------------------------------------------------------------------------------------
# Selecting and filtering
#--------------------------------------------------------------------------------------------
# Print the patient_id, age and department columns for the first 3 patients
patients.loc[0:2, ['patient_id', 'age', 'department']]

# Create a DataFrame containing only the patients over 65, and print how many there are
filtered_patients_65 = patients.loc[(patients['age'] > 65)]
print(filtered_patients_65.head())
print(f"Patients over 65: {len(filtered_patients_65)}")

# Create a DataFrame containing only the smokers, and print how many there are
filtered_patients_smoking = patients.loc[(patients['smoker'] == "Yes")]
print(filtered_patients_smoking.head())
print(f"Smokers: {len(filtered_patients_smoking)}")

# Print the patient_id, age and department of every patient who is both over 65 and a smoker
filtered_patients = patients.loc[(patients['age'] > 65) & (patients['smoker'] == "Yes")]
print(filtered_patients[['patient_id', 'age', 'department']])

#--------------------------------------------------------------------------------------------
# Summary statisitcs
#--------------------------------------------------------------------------------------------
# Print the average (mean) age, to one decimal place
print(f"Average age: {patients['age'].mean():.1f}")

# Print the median length of stay
print(f"Median length of stay: {patients['length_of_stay'].median()} days")

# Print the highest systolic blood pressure
print(f"Highest systolic blood pressure: {patients['systolic_bp'].max()} mmHg")

# Print how many patients each department treated
print(patients['department'].value_counts())

# Print the percentage of patients who were readmitted, to one decimal place
readmitted = (patients['readmitted'] == "Yes").mean()*100
print(f"Readmitted: {readmitted:.1f}%")

#--------------------------------------------------------------------------------------------
# Creating new column and grouping
#--------------------------------------------------------------------------------------------
def bp_category(systolic):
    """Classify systolic blood pressure into three categories:
        - "Normal" if the value is below 120 mmHg
        - "Elevated" if the value is between 120 and 129 mmHg
        - "High" if the value is 130 mmHg or above"""
    if systolic < 120:
        return "Normal"
    elif systolic >= 120 and systolic <= 129:
        return "Evevated"
    else:
        return "High"

# Call the bp_category function on every value in column systolic_bp
patients['bp_category'] = patients['systolic_bp'].apply(bp_category)

# Add a new column bp_category to patients, print the number of patients in each category
print(patients['bp_category'].value_counts())

# Calculate the average length of stay for each department, sorted descending, and print it to one decimal place
stay_by_department = patients.groupby('department')['length_of_stay'].mean().sort_values(ascending=False).round(1)

print(stay_by_department)

#--------------------------------------------------------------------------------------------
# Creating charts from DataFrames
#--------------------------------------------------------------------------------------------
# Bar chart of stay_by_department
stay_by_department.plot(kind="bar", edgecolor = "black")
plt.title("Average length of stay by department")
plt.xlabel("Department")
plt.ylabel("Average length of stay (day)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("stay_by_department.png")
plt.show()

# Histogram of patient ages
patients['age'].plot(kind="hist", bins = range(0,101,10),  edgecolor = "black")
plt.title("Distribution of patients' ages")
plt.xlabel("Age (year)")
plt.savefig("age_histogram.png")
plt.show()

# Scatter plot of systolic blood pressure against age
patients.plot(kind="scatter", x='age', y='systolic_bp')
plt.title("Systolic blood pressure by age")
plt.xlabel("Age (year)")
plt.ylabel("Systolic blood pressure (mmHg)")
plt.axhline(y=130, ls = "--", color = "red", label = "High blood pressure threshold")
plt.legend()
plt.savefig("age_vs_bp.png")
plt.show()

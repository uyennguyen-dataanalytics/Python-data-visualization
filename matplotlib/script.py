import matplotlib.pyplot as plt

#-----------------------------------------------------------------------------------------------------------------
# 1. Plot temperature line chart
#-----------------------------------------------------------------------------------------------------------------
days = [1, 2, 3, 4, 5, 6, 7]
temperatures = [37.2, 37.8, 38.5, 38.9, 38.1, 37.4, 36.9]

def plot_temperature():
    """Create a line chart of a patient's temperature over a week"""
    plt.plot(days, temperatures)
    plt.title("Patient's Temperature Over a Week")
    plt.xlabel("Day")
    plt.ylabel("Temperature (°C)")
    plt.savefig("temperature_chart.png")
    plt.show()

# Call function plot temperature chart
plot_temperature()

# Print the highest temperature and the day it was recorded
print(f"Highest temperature: {max(temperatures)} °C on day {days[temperatures.index(max(temperatures))]}")

#-----------------------------------------------------------------------------------------------------------------
# 2. Compare two patients' heart rates
#-----------------------------------------------------------------------------------------------------------------
hours = [0, 4, 8, 12, 16, 20, 24]
patient_a_hr = [72, 75, 80, 78, 74, 76, 73]
patient_b_hr = [88, 95, 104, 110, 102, 97, 92]

def plot_heart_rates(hours, patient_a, patient_b):
    """Create two lines in a chart to show two patients' heart rates in 24 hours """
    plt.figure(figsize=(12, 8))
    plt.plot(hours, patient_a, marker = 'o', color = "blue", label = "Patient A")    
    plt.plot(hours, patient_b, marker = 'o', color = "red", label = "Patient B")
    plt.axhline(100, ls = "--", color = 'gray', label= 'Normal resting heart rate')
    plt.title("Heart Rates Over 24 Hours")
    plt.xlabel("Hour")
    plt.ylabel("Heart rate (bpm)")
    plt.xticks(hours)
    plt.legend(loc="upper right")
    plt.savefig("heart_rate_chart.png")
    plt.show()

def hours_above(hours, heart_rates, limit):
    """Return a list of the hours at which the heart rates were above the upper limit of normal restiing heart rate"""
    above_limit = []
    for hour, heart_rate in zip(hours, heart_rates):
        if heart_rate > limit:
            above_limit.append(hour)
    return above_limit

# Call function plot heart rates chart
plot_heart_rates(hours, patient_a_hr, patient_b_hr)

# Find hours above 100 bpm of Patient B
print(f"Patient B was above 100 bpm at hours: {hours_above(hours, patient_b_hr, 100)}")

#-----------------------------------------------------------------------------------------------------------------
# 3. Admissions by department
#-----------------------------------------------------------------------------------------------------------------
departments = ["A&E", "Cardiology", "Maternity", "Oncology", "Orthopaedics", "Paediatrics"]
admissions = [142, 87, 64, 39, 71, 58]

def bar_colours(values, threshold):
    """Return a list of colours for bar chart: "red" for values over threshold and "blue" for the rest"""
    colour_list = []
    for x in values:
        if x >= threshold:
            colour_list.append("red")
        else:
            colour_list.append("blue")
    return colour_list

def plot_admission(departments, admissions):
    """Create a bar chart of admissions per department, color "red" for departments with over 80 admissions and color "blue" for the rest"""
    plt.bar(departments, admissions, color = bar_colours(admissions,80))
    plt.title("Hospital Admissions per Department")
    plt.xticks(rotation = 45)
    plt.xlabel("Departments")
    plt.ylabel("Number of admissions")
    plt.tight_layout()
    plt.savefig("admissions_chart.png")
    plt.show()

# Call function plot admission chart
plot_admission(departments, admissions)

# Print departments with 80 or more admissions
department_list = []
for i in range(len(admissions)):
    if admissions[i] >= 80:
        department_list.append(departments[i])

print(f"Departments with 80 or more admissions: {department_list}")

#-----------------------------------------------------------------------------------------------------------------
# 4. The ages of patients
#-----------------------------------------------------------------------------------------------------------------
ages = [23, 45, 67, 34, 78, 56, 89, 12, 45, 67, 72, 38, 61, 54, 81,
        29, 47, 66, 73, 58, 5, 41, 69, 77, 52, 36, 84, 63, 49, 70]

def plot_age_histogram(ages):
    """Create histogram to show distribution of patients' ages, calculate, draw a vertical line on chart to show mean age and return mean age"""
    plt.hist(ages, bins = range(0,101,10), edgecolor = "black")
    plt.title("Distribution of Patients' Ages")
    plt.xlabel("Age (years)")
    plt.ylabel("Number of patients")
    sum_of_ages = ages[0]
    for a in range(len(ages)-1):
        sum_of_ages = sum_of_ages + ages[a+1]
    mean_age=sum_of_ages/len(ages)
    plt.axvline(mean_age, ls = "--", color = "red", label = "Mean age")
    plt.legend()
    plt.savefig("age_histogram.png")
    plt.show()
    return mean_age

# Call function age histogram    
mean_age = plot_age_histogram(ages)

# Print mean age to one decimal place
print(f"Mean age: {mean_age:.1f}")

#-----------------------------------------------------------------------------------------------------------------
# 5. Height, weight and BMI
#-----------------------------------------------------------------------------------------------------------------
heights = [1.62, 1.75, 1.80, 1.55, 1.68, 1.90, 1.72, 1.60, 1.85, 1.66, 1.78, 1.58]
weights = [58, 82, 77, 70, 61, 95, 68, 52, 88, 74, 72, 49]

def calculate_bmi():
    """Calculate BMI for all patients, with BMI = Weight/(Height**2)"""
    patient_bmi = []
    for x in range(len(heights)):
        bmi = weights[x]/(heights[x]**2)
        patient_bmi.append(bmi)
    return patient_bmi

result_bmi = calculate_bmi()

def plot_bmi_scatter():
    """Create a scatter plot, color data points with "orange" if BMI value is 25 or more, with "green" if BMI value is less then 25.
    Return the result of how many patients have BMI higher than 25"""
    scatter_plot_color = []
    for x in range(len(result_bmi)):
        if result_bmi[x] >= 25:
            scatter_plot_color.append("orange")
        else:
            scatter_plot_color.append("green")
    print(scatter_plot_color)
    count_25 = 0
    for i in range (len(result_bmi)):
        if result_bmi[i] >= 25:
            count_25 = count_25 + 1
    plt.scatter(heights, weights, color = scatter_plot_color)
    plt.title("Height, Weight and BMI")
    plt.xlabel("Height (m)")
    plt.ylabel("Weight (kg)")
    plt.savefig("bmi_scatter.png")
    plt.show()
    return count_25

result = plot_bmi_scatter()

# Print number of patients with a BMI of 25 or more
print (f"Patients with a BMI of 25 or more: {result}")

#-----------------------------------------------------------------------------------------------------------------
# 6. Create a hosputal ward dashboard
#-----------------------------------------------------------------------------------------------------------------
def plot_dashboard():
    """Create a dashboard in 2x2 grid, containing four charts in one figure.
    Four charts are temperature line chart, admission bar chart, age histogram and height and weight scatter plot"""
    fig,axes = plt.subplots(2, 2, figsize = (20,15))
    fig.suptitle("Ward Dashboard", fontsize = 20)

    # First chart: the temperature line chart
    axes[0,0].plot(days, temperatures)
    axes[0,0].set_title("Patient's Temperature Over a Week")
    axes[0,0].set_xlabel("Day")
    axes[0,0].set_ylabel("Temperature (°C)")

    # Second chart: the admissions bar chart
    axes[0,1].bar(departments, admissions, color = bar_colours(admissions, 80))
    axes[0,1].set_title("Hospital Admissions per Department")
    axes[0,1].set_xlabel("Departments")
    axes[0,1].set_ylabel("Number of admissions")

    # Third chart: the age histogram
    axes[1,0].hist(ages, bins = range(0,101,10), edgecolor = "black")
    axes[1,0].axvline(mean_age, ls = "--", color = "red", label = "Mean age")
    axes[1,0].set_title("Distribution of Patients' Ages")
    axes[1,0].set_xlabel("Age (years)")
    axes[1,0].set_ylabel("Number of patients")
    axes[1,0].legend()

    # Forth chart: the height and weight scatter plot
    bmi_plot_colours = []
    for x in range (len(result_bmi)):
        if result_bmi[x] >= 25: 
            bmi_plot_colours.append("red")
        else:
            bmi_plot_colours.append("green")

    axes[1,1].scatter(heights, weights, color = bmi_plot_colours)
    axes[1,1].set_title("Height, weight and BMI")
    axes[1,1].set_xlabel("Height (m)")
    axes[1,1].set_ylabel("Weight (kg)")

    fig.tight_layout()
    plt.savefig("dashboard.png")
    plt.show()

# Call function plot dashboard
plot_dashboard()


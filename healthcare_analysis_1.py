import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Database connection setup
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Keerthi@2503',
    'database': 'Healthcare_DB'
}

# Establish a database connection
try:
    conn = mysql.connector.connect(**db_config)
    print("Database connection successful.")
except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit()

# Load data from the tables into pandas DataFrames
try:
    patients_df = pd.read_sql('SELECT * FROM patients', conn)
    doctors_df = pd.read_sql('SELECT * FROM doctors', conn)
    admissions_df = pd.read_sql('SELECT * FROM admissions', conn)
    treatments_df = pd.read_sql('SELECT * FROM treatments', conn)
    print("Data loaded successfully.")
except Exception as e:
    print(f"Error loading data: {e}")
    conn.close()
    exit()

# Close the database connection
conn.close()

# 1. Patient Demographics: Age Distribution
plt.figure(figsize=(10, 6))
sns.histplot(patients_df['age'].dropna(), bins=20, kde=True)
plt.title('Age Distribution of Patients')
plt.xlabel('Age')
plt.ylabel('Number of Patients')
plt.show()

# 2. Admissions Over Time
admissions_df['admission_date'] = pd.to_datetime(admissions_df['admission_date'])
admissions_per_month = admissions_df.resample('M', on='admission_date').size()

plt.figure(figsize=(12, 6))
admissions_per_month.plot()
plt.title('Monthly Admissions Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Admissions')
plt.show()

# 3. Admissions by Department
plt.figure(figsize=(12, 6))
sns.countplot(data=admissions_df, y='hospital_department', order=admissions_df['hospital_department'].value_counts().index)
plt.title('Number of Admissions by Department')
plt.xlabel('Number of Admissions')
plt.ylabel('Hospital Department')
plt.show()

# 4. Pie Chart: Distribution of Doctor Specializations
specialization_counts = doctors_df['specialization'].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(specialization_counts, labels=specialization_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Distribution of Doctor Specializations')
plt.show()

# 5. Column Chart: Average Length of Stay by Department
admissions_df['discharge_date'] = pd.to_datetime(admissions_df['discharge_date'])
admissions_df['admission_date'] = pd.to_datetime(admissions_df['admission_date'])
admissions_df['length_of_stay'] = (admissions_df['discharge_date'] - admissions_df['admission_date']).dt.days
avg_length_of_stay = admissions_df.groupby('hospital_department')['length_of_stay'].mean().sort_values()

plt.figure(figsize=(12, 6))
avg_length_of_stay.plot(kind='bar', color='skyblue')
plt.title('Average Length of Stay by Department')
plt.xlabel('Hospital Department')
plt.ylabel('Average Length of Stay (days)')
plt.xticks(rotation=45)
plt.show()

merged_df = treatments_df.merge(patients_df, on='patient_id', how='left').merge(doctors_df, on='doctor_id', how='left')

# 6. Example Visualization: Number of Treatments by Department	
plt.figure(figsize=(12, 8))  # Set figure size
sns.countplot(data=merged_df, y='department', order=merged_df['department'].value_counts().index, palette='viridis')
plt.title('Number of Treatments by Department', fontsize=16)
plt.xlabel('Number of Treatments', fontsize=14)
plt.ylabel('Department', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()  # Adjust layout
plt.savefig('treatments_by_department.png', bbox_inches='tight')  # Save figure
plt.show()


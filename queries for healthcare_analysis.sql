# Determine the Most Common Diagnosis per Department:

SELECT hospital_department, reason, COUNT(reason) AS occurrence
FROM admissions
GROUP BY hospital_department, reason
ORDER BY hospital_department, occurrence DESC;


# List Patients Along with Their Treating Doctors and Admission Details:
SELECT p.name AS Patient_Name,
       d.name AS Doctor_Name,
       a.admission_date,
       a.reason
FROM patients p
JOIN admissions a ON p.patient_id = a.patient_id
JOIN doctors d ON a.doctor_id = d.doctor_id;

# Count of Admissions per Department:

SELECT a.hospital_department,
       COUNT(a.admission_id) AS Admission_Count
FROM admissions a
GROUP BY a.hospital_department;

# Doctors with the Highest Number of Admissions:
SELECT d.name AS Doctor_Name,
       COUNT(a.admission_id) AS Number_of_Admissions
FROM doctors d
JOIN admissions a ON d.doctor_id = a.doctor_id
GROUP BY d.name
ORDER BY Number_of_Admissions DESC;

# doctors and their corresponding treatments

SELECT d.name AS Doctor_Name,
       t.treatment_name,
       t.treatment_date
FROM doctors d
JOIN treatments t ON d.doctor_id = t.doctor_id;

# Identify Doctors with the Highest Patient Load Over a Specific Period:
SELECT 
    d.name AS Doctor_Name,
    COUNT(DISTINCT a.patient_id) AS Unique_Patient_Count
FROM 
    doctors d
JOIN 
    admissions a ON d.doctor_id = a.doctor_id
WHERE 
    a.admission_date BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY 
    d.name
ORDER BY 
    Unique_Patient_Count DESC
LIMIT 5;

# Determine Departments with the Longest Average Patient Stay:

SELECT 
    a.hospital_department AS Department,
    AVG(DATEDIFF(a.discharge_date, a.admission_date)) AS Average_Stay_Days
FROM 
    admissions a
WHERE 
    a.discharge_date IS NOT NULL
GROUP BY 
    a.hospital_department
HAVING 
    AVG(DATEDIFF(a.discharge_date, a.admission_date)) > 0
ORDER BY 
    Average_Stay_Days DESC
LIMIT 5;



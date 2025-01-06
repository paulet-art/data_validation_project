import pandas as pd
import random
from faker import Faker

faker = Faker()

def generate_sample_data(num_records=100):
    data = {
        "id": [i + 1 if i != 50 else 1 for i in range(num_records)], 
        "name": [None if i % 10 == 0 else faker.name() for i in range(num_records)],  
        "age": [random.randint(16, 70) for _ in range(num_records)],  
        "salary": [round(random.uniform(-5000, 120000), 2) for _ in range(num_records)],  
        "hire_date": [faker.date_between(start_date="-10y", end_date="today").strftime("%Y-%m-%d") if i % 5 != 0 else "invalid-date" for i in range(num_records)] 
    }
    return pd.DataFrame(data)

num_records = 100
file_path = "data/employee_data.csv"
df = generate_sample_data(num_records)
df.to_csv(file_path, index=False)
print(f"Sample data generated and saved to {file_path}")

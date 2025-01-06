import pandas as pd
from datetime import datetime

def load_data(file_path):
    return pd.read_csv(file_path)

def validate_data(df):
    validation_results = {}

    validation_results["id_not_null"] = df["id"].notnull().all()
    validation_results["id_unique"] = df["id"].is_unique

    validation_results["name_not_null"] = df["name"].notnull().all()

    validation_results["age_valid_range"] = df["age"].between(18, 65, inclusive="both").all()

    validation_results["salary_positive"] = (df["salary"] > 0).all()

    try:
        pd.to_datetime(df["hire_date"], format="%Y-%m-%d", errors="raise")
        validation_results["hire_date_valid"] = True
    except Exception:
        validation_results["hire_date_valid"] = False

    return validation_results

def generate_report(validation_results, output_path):
    with open(output_path,"w") as f:
        f.write("Validation Report\n")
        f.write(f"Generated on {datetime.now()}\n\n")
        for rule, result in validation_results.items():
            f.write(f"{rule} : {'Passed' if result else 'Failed'} \n")

if __name__ == "__main__":
    file_path = "data/employee_data.csv"
    df = load_data(file_path)

    validation_results = validate_data(df)

    report_path = "reports/validation_report.txt"
    generate_report(validation_results, report_path)
    print(f"Validation report geneated: {report_path}")
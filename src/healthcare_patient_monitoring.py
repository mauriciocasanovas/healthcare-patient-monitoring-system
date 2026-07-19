import os
import numpy as np
import pandas as pd


def run_healthcare_patient_monitoring():
    """
    Process clinical patient data to identify temperature trends,
    detect fever alerts, and generate healthcare monitoring reports.
    """

    dataset_path = "../data/patient_monitoring_dataset.xlsx"

    # Create output directory
    output_folder = "../results"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # ------------------------------------------------------------------
    # LOAD DATASET
    # ------------------------------------------------------------------

    if not os.path.exists(dataset_path):
        print(f"Error: '{dataset_path}' not found.")
        return

    df = pd.read_excel(dataset_path, decimal=",")

    initial_rows = len(df)

    # ------------------------------------------------------------------
    # DATA CLEANING
    # ------------------------------------------------------------------

    numeric_columns = [
        "Age",
        "Temperature_Pre",
        "Temperature_Post",
        "Cervical_Dilation",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.dropna(
        subset=[
            "Age",
            "Temperature_Pre",
            "Temperature_Post",
        ]
    )

    df["Age"] = df["Age"].astype(int)

    removed_rows = initial_rows - len(df)

    print("=" * 70)
    print("HEALTHCARE PATIENT MONITORING SYSTEM")
    print("=" * 70)
    print(f"Invalid records removed: {removed_rows}")
    print("-" * 70)

    # ------------------------------------------------------------------
    # FEATURE ENGINEERING
    # ------------------------------------------------------------------

    df["Age_Group"] = pd.cut(
        df["Age"],
        bins=[-float("inf"), 24, 25, float("inf")],
        labels=[
            "Below Average",
            "Average",
            "Above Average",
        ],
    )

    df["Average_Temperature"] = df[
        [
            "Temperature_Pre",
            "Temperature_Post",
        ]
    ].mean(axis=1)

    df["Average_Temperature"] = pd.to_numeric(
        df["Average_Temperature"],
        errors="coerce",
    )

    # Fever alert (>= 38°C)

    df["Fever_Alert"] = (
        df["Average_Temperature"] >= 38
    ).astype(int)

    # ------------------------------------------------------------------
    # LINEAR REGRESSION
    # ------------------------------------------------------------------

    x = df["Cervical_Dilation"].fillna(0)

    y = df["Temperature_Post"].fillna(
        df["Temperature_Post"].mean()
    )

    slope, intercept = np.polyfit(x, y, 1)

    df["Regression_Trend"] = (
        slope * x
    ) + intercept

    df["Correlation_Index"] = x.corr(y)

    # ------------------------------------------------------------------
    # SUMMARY STATISTICS
    # ------------------------------------------------------------------

    average_age = df["Age"].mean()

    average_temperature = df[
        "Average_Temperature"
    ].mean()

    fever_cases = len(
        df[df["Average_Temperature"] >= 38]
    )

    print(f"Average age: {average_age:.1f} years")
    print(
        f"Average temperature: "
        f"{average_temperature:.2f} °C"
    )
    print(
        f"Detected fever cases: "
        f"{fever_cases}"
    )

    print("-" * 70)

    # ------------------------------------------------------------------
    # EXCEL STYLING
    # ------------------------------------------------------------------

    def highlight_fever(value):
        if value == 1:
            return (
                "background-color: red;"
                "color: white;"
            )
        return ""

    styled_df = df.style.map(
        lambda _: "background-color: yellow",
        subset=[
            "Age_Group",
            "Average_Temperature",
        ],
    )

    styled_df = styled_df.map(
        highlight_fever,
        subset=["Fever_Alert"],
    )

    # ------------------------------------------------------------------
    # EXPORT RESULTS
    # ------------------------------------------------------------------

    output_excel = os.path.join(
        output_folder,
        "patient_monitoring_results.xlsx",
    )

    styled_df.to_excel(
        output_excel,
        engine="openpyxl",
        index=False,
    )

    # ------------------------------------------------------------------
    # GENERATE TECHNICAL REPORT
    # ------------------------------------------------------------------

    total_patients = len(df)

    fever_percentage = (
        fever_cases / total_patients
    ) * 100

    report_path = os.path.join(
        output_folder,
        "healthcare_analysis_report.txt",
    )

    with open(report_path, "w") as file:

        file.write("=" * 60 + "\n")
        file.write("HEALTHCARE PATIENT MONITORING REPORT\n")
        file.write("=" * 60 + "\n\n")

        file.write("DATASET SUMMARY\n")
        file.write("-" * 60 + "\n")
        file.write(
            f"Total patients analyzed: {total_patients}\n"
        )
        file.write(
            f"Invalid records removed: {removed_rows}\n"
        )
        file.write(
            f"Average age: {average_age:.1f} years\n"
        )
        file.write(
            f"Average temperature: "
            f"{average_temperature:.2f} °C\n"
        )
        file.write(
            f"Fever cases detected: {fever_cases}\n"
        )
        file.write(
            f"Patients with fever: "
            f"{fever_percentage:.1f}%\n\n"
        )

        file.write("CORRELATION ANALYSIS\n")
        file.write("-" * 60 + "\n")
        file.write(
            "Linear regression was applied to evaluate "
            "the relationship between cervical dilation "
            "and post-procedure temperature.\n\n"
        )

        file.write(
            f"Regression slope: {slope:.4f}\n"
        )
        file.write(
            f"Regression intercept: {intercept:.4f}\n"
        )
        file.write(
            f"Correlation coefficient: "
            f"{df['Correlation_Index'].iloc[0]:.4f}\n\n"
        )

        file.write("CLINICAL INTERPRETATION\n")
        file.write("-" * 60 + "\n")

        if fever_percentage > 10:
            file.write(
                "Warning: The percentage of patients "
                "with fever exceeds the predefined "
                "clinical threshold and should be "
                "reviewed.\n"
            )
        else:
            file.write(
                "The percentage of fever cases "
                "remains within the expected range.\n"
            )

        file.write("\n")
        file.write("=" * 60)

    # ------------------------------------------------------------------
    # FINAL SUMMARY
    # ------------------------------------------------------------------

    print("PROCESSING SUMMARY")
    print("-" * 70)
    print(f"Patients analyzed: {total_patients}")
    print(f"Fever cases: {fever_cases}")
    print(
        f"Fever rate: {fever_percentage:.1f}%"
    )

    if fever_percentage > 10:
        print("Dataset status: REVIEW REQUIRED")
    else:
        print("Dataset status: STABLE")

    print("=" * 70)
    print("Healthcare analysis completed successfully.")
    print(f"Excel report: {output_excel}")
    print(f"Technical report: {report_path}")
    print("=" * 70)


if __name__ == "__main__":
    print("Running healthcare patient monitoring...")
    run_healthcare_patient_monitoring()
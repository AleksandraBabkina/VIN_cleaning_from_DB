# VIN_Cleaning_from_DB

## Description
Vehicle Identification Numbers (VIN) are unique 17-character codes used to identify vehicles. Each VIN serves as a fingerprint for a vehicle, containing important details such as the manufacturer, model, engine type, place of manufacture, and more. VINs are regulated by the National Highway Traffic Safety Administration (NHTSA) in the United States and similar regulatory bodies worldwide. The structure of a VIN is defined by the ISO 3779 and ISO 4030 standards, ensuring consistency across vehicles.

Given their critical role in vehicle tracking, ownership verification, and regulatory compliance, it is essential that VINs are accurate and formatted correctly. Improper formats can arise due to data entry errors, encoding issues, or the presence of non-standard characters, particularly with vehicles from different regions (e.g., Japanese vehicles that may include special characters or separate body and engine numbers).

This program performs VIN data cleansing on records retrieved from an Oracle database. It identifies and eliminates invalid, incomplete, or incorrectly formatted VINs based on industry standards. The program retrieves the necessary data, applies validation checks to ensure correct formatting, handles known invalid VINs, and removes unwanted characters. The cleaned data is then saved for further use or analysis.

## Functional Description
The program performs the following steps:
1. Retrieves records from the database where the VIN values are not null and the `notes` field is empty.
2. Validates the VINs based on a predefined list of known invalid VINs.
3. Transforms the VINs into a standardized format by converting characters to uppercase, replacing Cyrillic letters with Latin equivalents, and removing non-alphanumeric characters.
4. Ensures that the cleaned VINs meet the length requirement of at least 8 characters.
5. Outputs the results in a structured format, with the original and cleaned VINs, saving the cleaned data to a new Excel file for further inspection.

## How It Works
1. The program connects to an Oracle database using SQLAlchemy and retrieves data from the `diasoft_test.v_taxi_4_kostyashov` table where the `notes` field is null and the `VIN` field is not empty.
2. For each VIN, the program compares it against a list of known invalid VINs and standardizes the VIN by applying a set of transformation rules.
3. It applies checks to ensure that the cleaned VINs have a length of at least 8 characters, meeting the expected format for valid VINs.
4. The results, including both the original and cleaned VINs, are saved to a new Excel file for further analysis or validation.

## Input Structure
To run the program, the following parameters need to be provided:
1. Database credentials: Username, Password, Database DSN (Data Source Name)
2. A list of invalid VINs: Predefined set of VINs that are known to be invalid.
3. VIN column: The column containing the VINs to be cleaned, specifically within the `diasoft_test.v_taxi_4_kostyashov` table.

## Technical Requirements
To run the program, the following are required:
1. Python 3.x
2. Installed libraries: sqlalchemy, pandas
3. Oracle Database with the `diasoft_test.v_taxi_4_kostyashov` table, containing the VINs to be cleaned.

## Usage
1. Modify the username, password, and DSN values to connect to your Oracle database.
2. Define the list of invalid VINs you want to exclude.
3. Run the program. It will:
    - Clean VIN values by standardizing their format.
    - Remove known invalid VINs.
    - Output the cleaned VINs to a new Excel file.

## Example Output
For each VIN:
- The program will display the original VIN and the cleaned VIN.
- Any invalid VINs (those in the predefined invalid list or not meeting the length requirement) will be removed.

## Conclusion
This tool ensures that VIN data is cleaned and standardized, improving the accuracy and integrity of vehicle data records for further analysis, reporting, or integration with other systems. By removing invalid and incorrectly formatted VINs, it helps maintain a high level of data quality for effective decision-making.

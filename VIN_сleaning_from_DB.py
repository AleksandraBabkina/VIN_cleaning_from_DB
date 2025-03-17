import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, select, or_, and_
from sqlalchemy.orm import sessionmaker, declarative_base 

# Header with connection - DO NOT TOUCH
username = 'username'
password = 'password'
dsn = 'dsn'

conection_string = f'oracle+oracledb://{username}:{password}@{dsn}' # SQL connection

# Create connection engine
engine = create_engine(conection_string) # Engine
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

try:
    query = "select * from taxi where notes is null and VIN is not null"
    df = pd.read_sql(query, engine)
    df.to_csv(r"C:\Users\aleksandra.babkina\Desktop\Taxi_Registry_sql.csv", index=False)
finally:
    # Close the session
    session.close()

df = pd.read_csv(r'C:\Users\aleksandra.babkina\Desktop\Taxi_Registry_sql.csv')

invalid_vins = ['VIN00000000000000', 'ХТН2411-322282-90', 'ХТН2411-269482-90', 'ХТА2411-122298-87', 'ХТН2411*292060*90', 
                'VIN', '0000000000000000W', '000000000000000000', '-96322132L0667201а', '3.7319551021648896E+16', 
                'XTH311000W016+456', '3,11E+13', 'КРЫША КРАСНАЯ', 'НЕ УСТАНОВЛЕНО', '0РАНЖ КРЫША', 'EL51*027527100000',  
                'FB15*018967000000', 'NZE121*3036264000', 'VHNY11*2939930000', 'AE100*00653610000', 'ST210*40174280000', 
                'SV35*001162000000', 'HC32*025974000000', 'V45*4401339000000', 'DY3W*217017000000','AE110*52866450000', 
                'EF5*3502373000000', 'NCP60*01725540000', 'SCP10*01783710000', 'GC1*0270960000000', 'XTH2410*291329000', 
                'ХТН2411*292060*90', 'NZE121*0223752000', 'AE110*00176320000', 'ХТН2411*322208*90', 'Отсутствует', 
                '173102', '0015844', '1119174','2905', '172552', '-', '172126', '381826', '172642', '173283', '5268098', 
                '381416', '3288251', '0', '932964', '203704', '846295', '2008', '171844', '0303367', 'KY3OB','SAMOSWAL', 
                'ОТСУТСТВУЕТ', 'ОТСУТСВУЕТ']

replace_dict = {'А':'A', 'В':'B', 'Е':'E', 'К':'K', 'М':'M', 
                'Н':'H', 'О':'O', 'Р':'P', 'С':'C', 'Т':'T', 
                'У':'Y', 'Х':'X', 'О':'0', 'I':'1', '-':'',
                '|':''}

# Function for VIN cleaning
def clean_vin(vin):
    if pd.isna(vin):
        return None  # Return None if the value is empty
    vin = str(vin)  # Convert to string
    if vin in invalid_vins:
        return None  # Set as null if VIN is invalid
    else:
        # Convert VIN to uppercase
        vin_upper = vin.upper()  # Convert to uppercase
        # Replace Russian letters and other symbols according to the dictionary
        vin_translated = vin_upper.translate(str.maketrans(replace_dict))
        # Remove non-alphanumeric characters
        vin_cleaned = ''.join(char for char in vin_translated if char.isalnum())
        # Check the length
        if 8 <= len(vin_cleaned):
            return vin_cleaned
        else:
            return None  # Return None if length does not meet the requirements

# Create new columns OLD_VIN and VIN_NEW 
df['old_vin'] = df['vin']  # Save the original VIN 
df['new_vin'] = df.apply(lambda row: None if row['vin'] in invalid_vins else clean_vin(row['vin']), axis=1)
df['vin'].apply(clean_vin)  # Apply the VIN cleaning function

# Debugging outputs
print(f"Total records: {len(df)}")
print(f"Records with non-null VIN_NEW: {df['new_vin'].notna().sum()}")

# Filter only the data where VIN was changed 
# We use ~df['VIN_NEW'].isna() to exclude rows where VIN_NEW is NaN
df_changed = df[~df['new_vin'].isna() & (df['new_vin'] != df['old_vin'])]

# Debugging outputs
print(f"Records with changed VIN: {len(df_changed)}")

# Sort data by old and new VIN 
df_changed = df_changed.sort_values(by=['new_vin', 'old_vin'])

# Save the data to a new CSV file
output_path = r"C:\Users\aleksandra.babkina\Desktop\Taxi_Registry_Cleaned_1.xlsx"
df_changed.to_excel(output_path, index=False)

print(f"Updated data saved to file: {output_path}")

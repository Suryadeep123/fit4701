import pandas as pd
import re

# Define control flow patterns for nested depth
control_flow_patterns = [
    r'\bif\b',
    r'\belse if\b',
    r'\bfor\b',
    r'\bwhile\b',
    r'\bcase\b',
    r'\btry\b',
    r'\bcatch\b',  # Include catch for Java-style exception handling
]

def remove_comments(code):
    # Remove single-line comments
    code = re.sub(r'//.*', '', code)
    # Remove multi-line comments
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    return code

def calculate_combined_nested_depth(code_string):
    # Clean the code by removing comments
    clean_code = remove_comments(code_string)

    nested_depth = 0
    max_depth = 0

    # Split the clean code into lines
    lines = clean_code.splitlines()

    for line in lines:
        # Check for control flow structures
        for pattern in control_flow_patterns:
            if re.search(pattern, line):
                nested_depth += 1
                # Update max_depth if current depth is greater
                max_depth = max(max_depth, nested_depth)
        
        # Check for block endings (like closing braces)
        if re.search(r'\}', line):
            nested_depth -= 1
            
        # Ensure depth doesn't go negative
        if nested_depth < 0:
            nested_depth = 0

    return max_depth

def mccabe_cyclomatic_complexity(assertion_file_case):
    complexity = 1
    clean_code = remove_comments(assertion_file_case)
    for tcase in control_flow_patterns:
        complexity += len(re.findall(tcase, clean_code))
    return complexity

# Path to the Excel file
excel_path = 'C:\\y5s2\\fit4701_p2\\LLM-Assertion-570.xlsx'

# Read the Excel file
df = pd.read_excel(excel_path)

if 'Tm-fm' in df.columns:
    complexities = []
    nested_depths = []  # List to store nested depths
    for index, row in df.iterrows():
        tcase = row['Tm-fm']
        complexity = mccabe_cyclomatic_complexity(tcase)
        nested_depth = calculate_combined_nested_depth(tcase)  # Calculate nested depth
        complexities.append(complexity)
        nested_depths.append(nested_depth)  # Append nested depth
    
    df['Cyclomatic_complexity'] = complexities
    df['Combined_Nested_Depth'] = nested_depths  # Add nested depth to DataFrame

    # Save the updated DataFrame back to Excel
    df.to_excel(excel_path, index=False)

    print("it works")

else:
    print("it has failed")

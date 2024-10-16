import pandas as pd
import re
import statistics

# Define control flow patterns for complexity analysis
control_flow_patterns = [
    r'\bif\b',
    r'\belse if\b',
    r'\bfor\b',
    r'\bwhile\b',
    r'\bcase\b',
    r'\btry\b',
    r'\bcatch\b',  # Include catch for Java-style exception handling
]

# Function to remove comments from code
def remove_comments(code):
    # Remove single-line comments
    code = re.sub(r'//.*', '', code)
    # Remove multi-line comments
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    return code

# Calculate combined nested depth
def calculate_combined_nested_depth(code_string):
    clean_code = remove_comments(code_string)
    nested_depth = 0
    max_depth = 0
    lines = clean_code.splitlines()
    
    for line in lines:
        # Check for control flow structures
        for pattern in control_flow_patterns:
            if re.search(pattern, line):
                nested_depth += 1
                max_depth = max(max_depth, nested_depth)
        if re.search(r'\}', line):
            nested_depth -= 1
        nested_depth = max(nested_depth, 0)
    
    return max_depth

# Calculate McCabe's Cyclomatic Complexity
def mccabe_cyclomatic_complexity(assertion_file_case):
    complexity = 1
    clean_code = remove_comments(assertion_file_case)
    for tcase in control_flow_patterns:
        complexity += len(re.findall(tcase, clean_code))
    return complexity

# Count methods in a class
def count_methods(code_string):
    return len(re.findall(r'\bdef\b|\bpublic\b|\bprivate\b|\bprotected\b', code_string))

# Count fields in a class
def count_fields(code_string):
    return len(re.findall(r'\b(int|long|float|double|String|char)\b \w+', code_string))

# Count loops in the code
def count_loops(code_string):
    return len(re.findall(r'\b(for|while)\b', code_string))

# Count string literals
def count_string_literals(code_string):
    return len(re.findall(r'\".*?\"', code_string))

# Count numeric literals
def count_numeric_literals(code_string):
    return len(re.findall(r'\b\d+\b', code_string))

# Count assignment operations
def count_assignments(code_string):
    return len(re.findall(r'=', code_string))

# Count mathematical operators
def count_math_operators(code_string):
    return len(re.findall(r'[+\-*/%]', code_string))

# Count lines of code (ignoring comments and empty lines)
def count_lines_of_code(code_string):
    clean_code = remove_comments(code_string)
    code_lines = [line for line in clean_code.splitlines() if line.strip() != ""]
    return len(code_lines)

# Count decision branches
def count_decision_branches(code_string):
    return len(re.findall(r'\bif\b|\bswitch\b|\belse if\b', code_string))

# Calculate average method complexity
def calculate_average_method_complexity(code_string):
    methods = re.findall(r'\bdef\b|\bpublic\b|\bprivate\b|\bprotected\b', code_string)
    if len(methods) == 0:
        return 0
    total_complexity = sum(mccabe_cyclomatic_complexity(method) for method in methods)
    return total_complexity / len(methods)

# Count the number of children (sub-classes/methods for simplicity)
def count_children(code_string):
    # Assuming subclasses or methods are prefixed by certain keywords
    return len(re.findall(r'\bclass\b|\bdef\b|\bpublic\b|\bprivate\b|\bprotected\b', code_string)) - 1

# Calculate the Data Access Metric (ratio of private fields to total fields)
def calculate_data_access_metric(code_string):
    total_fields = count_fields(code_string)
    private_fields = len(re.findall(r'\bprivate\b \w+', code_string))
    if total_fields == 0:
        return 0
    return private_fields / total_fields

# Tight Class Cohesion: Calculating the ratio of direct connections among visible methods
def calculate_tight_class_cohesion(code_string):
    methods = re.findall(r'\bdef\b|\bpublic\b|\bprivate\b|\bprotected\b', code_string)
    # Assuming direct connections are based on shared parameters or return types
    cohesion_count = 0
    for method in methods:
        if re.findall(r'\bint\b|\bString\b|\bchar\b', method):  # Check if methods share common parameters
            cohesion_count += 1
    if len(methods) == 0:
        return 0
    return cohesion_count / len(methods)

def calculate_standard_deviation_cyclomatic_complexity(code_string):
    # Find all method definitions in the code string
    methods = re.findall(r'\bdef\b|\bpublic\b|\bprivate\b|\bprotected\b', code_string)
    
    # Calculate the cyclomatic complexity for each method
    complexities = [mccabe_cyclomatic_complexity(method) for method in methods]

    # Check the length of complexities before calculating standard deviation
    if len(complexities) < 2:
        # Not enough data points to calculate standard deviation
        return 0  # or return None or another appropriate value

    # Calculate and return the standard deviation
    return statistics.stdev(complexities)



# Path to the Excel file
excel_path = 'C:\\y5s2\\fit4701_p2\\fit4701\\LLM-Assertion-570.xlsx'

# Read the Excel file
df = pd.read_excel(excel_path)

if 'Tm-fm' in df.columns:
    complexities = []
    nested_depths = []  # List to store nested depths
    method_counts = []
    field_counts = []
    loop_counts = []
    string_literal_counts = []
    numeric_literal_counts = []
    assignment_counts = []
    math_operator_counts = []
    line_counts = []
    decision_branch_counts = []
    avg_method_complexities = []

    # Additional lists for new features
    children_counts = []
    data_access_metrics = []
    tight_class_cohesions = []
    standard_deviation_complexities = []

    for index, row in df.iterrows():
        tcase = row['Tm-fm']
        complexity = mccabe_cyclomatic_complexity(tcase)
        nested_depth = calculate_combined_nested_depth(tcase)  # Calculate nested depth
        method_count = count_methods(tcase)
        field_count = count_fields(tcase)
        loop_count = count_loops(tcase)
        string_literal_count = count_string_literals(tcase)
        numeric_literal_count = count_numeric_literals(tcase)
        assignment_count = count_assignments(tcase)
        math_operator_count = count_math_operators(tcase)
        line_count = count_lines_of_code(tcase)
        decision_branch_count = count_decision_branches(tcase)
        avg_method_complexity = calculate_average_method_complexity(tcase)
        children_count = count_children(tcase)
        data_access_metric = calculate_data_access_metric(tcase)
        tight_class_cohesion = calculate_tight_class_cohesion(tcase)
        std_dev_complexity = calculate_standard_deviation_cyclomatic_complexity(tcase)

        # Append all features to lists
        complexities.append(complexity)
        nested_depths.append(nested_depth)
        method_counts.append(method_count)
        field_counts.append(field_count)
        loop_counts.append(loop_count)
        string_literal_counts.append(string_literal_count)
        numeric_literal_counts.append(numeric_literal_count)
        assignment_counts.append(assignment_count)
        math_operator_counts.append(math_operator_count)
        line_counts.append(line_count)
        decision_branch_counts.append(decision_branch_count)
        avg_method_complexities.append(avg_method_complexity)
        children_counts.append(children_count)
        data_access_metrics.append(data_access_metric)
        tight_class_cohesions.append(tight_class_cohesion)
        standard_deviation_complexities.append(std_dev_complexity)

    
    # Add columns to the DataFrame
    df['Cyclomatic_complexity'] = complexities
    df['Combined_Nested_Depth'] = nested_depths
    df['Method_Count'] = method_counts
    df['Field_Count'] = field_counts
    df['Loop_Count'] = loop_counts
    df['String_Literal_Count'] = string_literal_counts
    df['Numeric_Literal_Count'] = numeric_literal_counts
    df['Assignment_Count'] = assignment_counts
    df['Math_Operator_Count'] = math_operator_counts
    df['Line_Count'] = line_counts
    df['Decision_Branch_Count'] = decision_branch_counts
    df['Avg_Method_Complexity'] = avg_method_complexities
    df['Children_Count'] = children_counts
    df['Data_Access_Metric'] = data_access_metrics
    df['Tight_Class_Cohesion'] = tight_class_cohesions
    df['Standard_Deviation_Complexity'] = standard_deviation_complexities


    # Save the updated DataFrame back to Excel
    df.to_excel(excel_path, index=False)

    print("Updated features have been calculated and saved.")

else:
    print("The 'Tm-fm' column is not found.")

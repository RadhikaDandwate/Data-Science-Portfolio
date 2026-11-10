import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Regex Function

def get_pattern_match(pattern, text):
    matches = re.findall(pattern, text)
    if matches:
        return matches[0] 

#extract college data

def extract_college_data(text):

    college = get_pattern_match(r'College:\s*(.*)', text)

    location = get_pattern_match(r'Location:\s*(.*)', text)

    year = get_pattern_match(r'Year:\s*(\d{4})', text)

    placement = get_pattern_match(
        r'Placement Percentage:\s*(\d+\.?\d*)\s*%',
        text
    )

    average_package = get_pattern_match(
        r'Average Package:\s*?\s*(\d+\.?\d*)\s*LPA',
        text
    )

    highest_package = get_pattern_match(
        r'Highest Package:\s*?\s*(\d+\.?\d*)\s*LPA',
        text
    )

    companies = get_pattern_match(
        r'Companies Visited:\s*(\d+)',
        text
    )

    rating = get_pattern_match(
        r'Rating:\s*(\d+\.?\d*)',
        text
    )

    return [
        college,
        location,
        year,
        placement,
        average_package,
        highest_package,
        companies,
        rating
    ]


#college data

college1 = """
College: COEP Pune
Location: Pune, Maharashtra
Year: 2025
Placement Percentage: 90%
Average Package: 12 LPA
Highest Package: 52 LPA
Companies Visited: 205
Rating: 4.5
"""


college2 = """
College: VJTI Mumbai
Location: Mumbai, Maharashtra
Year: 2025
Placement Percentage: 85%
Average Package: 16 LPA
Highest Package: 54 LPA
Companies Visited: 250
Rating: 4.4
"""

college3 = """
College: VIT Pune
Location: Pune, Maharashtra
Year: 2025
Placement Percentage: 86%
Average Package: 9.6 LPA
Highest Package: 51 LPA
Companies Visited: 160
Rating: 4.3
"""

college4 = """
College: WCE Sangli
Location: Sangli, Maharashtra
Year: 2025
Placement Percentage: 80%
Average Package: 10 LPA
Highest Package: 60 LPA
Companies Visited: 120
Rating: 4.2
"""

college5 = """
College: Cummins Pune
Location: Pune, Maharashtra
Year: 2025
Placement Percentage: 90%
Average Package: 11 LPA
Highest Package: 50 LPA
Companies Visited: 140
Rating: 4.4
"""


#extract data

data = [
    extract_college_data(college1),
    extract_college_data(college2),
    extract_college_data(college3),
    extract_college_data(college4),
    extract_college_data(college5)
]


# create dataset

columns = [
    "College",
    "Location",
    "Year",
    "Placement_Percentage",
    "Average_Package",
    "Highest_Package",
    "Companies",
    "Rating"
]

df = pd.DataFrame(data, columns=columns)


# Convert numbers

df["Year"] = pd.to_numeric(df["Year"])

df["Placement_Percentage"] = pd.to_numeric(
    df["Placement_Percentage"]
)

df["Average_Package"] = pd.to_numeric(
    df["Average_Package"]
)

df["Highest_Package"] = pd.to_numeric(
    df["Highest_Package"]
)

df["Companies"] = pd.to_numeric(
    df["Companies"]
)

df["Rating"] = pd.to_numeric(
    df["Rating"]
)


#save dataset

print(df)

df.to_csv("college_dataset.csv", index=False)


#Graphical representation

# Average Package

sns.barplot(
    x="College",
    y="Average_Package",
    data=df
)

plt.title("Average Package Comparison")
plt.xticks(rotation=20)
plt.show()


# Placement Percentage

sns.barplot(
    x="College",
    y="Placement_Percentage",
    data=df
)

plt.title("Placement Percentage Comparison")
plt.xticks(rotation=20)
plt.show()


# Highest Package

sns.barplot(
    x="College",
    y="Highest_Package",
    data=df
)

plt.title("Highest Package Comparison")
plt.xticks(rotation=20)
plt.show()


# Companies

sns.barplot(
    x="College",
    y="Companies",
    data=df
)

plt.title("Companies Visited Comparison")
plt.xticks(rotation=20)
plt.show()


# Rating

sns.barplot(
    x="College",
    y="Rating",
    data=df
)

plt.title("College Rating Comparison")
plt.xticks(rotation=20)
plt.show()


# Placement vs Average Package

sns.scatterplot(
    x="Placement_Percentage",
    y="Average_Package",
    data=df
)

plt.title("Placement vs Average Package")
plt.show()



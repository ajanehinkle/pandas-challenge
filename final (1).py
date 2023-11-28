#!/usr/bin/env python
# coding: utf-8

# # PyCity Schools Analysis
# 
# - Charter schools tend to outperform public schools, as they typically have a smaller student ratio.
# - The amount of money spent per student does not determine how well they do on average during testing.
# ---

# In[1]:


# Dependencies and Setup
import pandas as pd
from pathlib import Path

# File to Load
school_file = Path("Resources/schools_complete.csv")
stu_file = Path("Resources/students_complete.csv")

# Read School and Student Data File and store into Pandas DataFrames
school_data = pd.read_csv(school_file)
stu_data = pd.read_csv(stu_file)

# Combine the data into a single dataset.  
school_complete = pd.merge(stu_data, school_data, how="left", on=["school_name", "school_name"])
school_complete.head()


# ## District Summary

# In[2]:


# Calculate the total number of unique schools
school_count = len (school_complete ["school_name"].unique())
school_count


# In[3]:


# Calculate the total number of students
student_count = len (school_complete["Student ID"].unique())
student_count


# In[4]:


# Calculate the total budget
total_budget = sum (school_data["budget"]) 
total_budget


# In[5]:


# Calculate the average (mean) math score
average_math_score = stu_data ["math_score"].mean()
average_math_score


# In[6]:


# Calculate the average (mean) reading score
average_reading_score = stu_data["reading_score"].mean()
average_reading_score


# In[7]:


# Use the following to calculate the percentage of students who passed math (math scores greather than or equal to 70)
passing_math_count = school_complete[(school_complete["math_score"] >= 70)].count()["student_name"]
passing_math_percentage = passing_math_count / float(student_count) * 100
passing_math_percentage


# In[8]:


# Calculate the percentage of students who passed reading (hint: look at how the math percentage was calculated)  
passing_reading_count = school_complete[(school_complete["reading_score"] >= 70)].count()["student_name"]
passing_reading_percentage = passing_reading_count / float(student_count) * 100
passing_reading_percentage


# In[9]:


# Use the following to calculate the percentage of students that passed math and reading
passing_both_count = school_complete[
    (school_complete["math_score"] >= 70) & (school_complete["reading_score"] >= 70)
].count()["student_name"]
overall_passing_rate = passing_both_count /  float(student_count) * 100
overall_passing_rate


# In[10]:


# Create a high-level snapshot of the district's key metrics in a DataFrame
summary = pd.DataFrame({"Total Schools":[school_count],
                                 "Total Students":[student_count],
                                 "Total Budget":[total_budget],
                                 "Average Math Score":[average_math_score],
                                 "Average Reading Score":[average_reading_score],
                                 "Number Passing Math":[passing_math_count],
                                 "Number Passing Reading":[passing_reading_count],
                                 "% Overall Passing Rate":[overall_passing_rate]})

# Formatting
summary["Total Students"] = summary.apply(lambda x: "{:,.0f}".format(x["Total Students"]), axis=1)
summary["Total Budget"] = summary.apply(lambda x: "${:,.2f}".format(x["Total Budget"]), axis=1)

# Display the DataFrame
summary


# ## School Summary

# In[65]:


# Use the code provided to select all of the school types
school_types = school_data.set_index('type').groupby(['school_name'])


# In[66]:


# Calculate the total student count per school
per_school_counts = school_complete["school_name"].count()


# In[67]:


# Calculate the total school budget and per capita spending per school
per_school_budget = school_complete.groupby(["school_name"])["budget"].mean()
per_school_capita = per_school_budget/per_school_counts


# In[68]:


# Calculate the average test scores per school
per_school_math = school_complete.groupby(["school_name"])["math_score"].mean()
per_school_reading = school_complete.groupby(["school_name"])["reading_score"].mean()


# In[69]:


# Calculate the number of students per school with math scores of 70 or higher
students_passing_math = school_complete.loc[school_complete["math_score"]>=70]
school_students_passing_math = students_passing_math["school_name"].value_counts()


# In[70]:


# Calculate the number of students per school with reading scores of 70 or higher
students_passing_reading = school_complete.loc[school_complete["reading_score"]>=70]
school_students_passing_reading = students_passing_reading["school_name"].value_counts()


# In[71]:


# Use the provided code to calculate the number of students per school that passed both math and reading with scores of 70 or higher
students_passing_math_and_reading = school_complete[
    (school_complete["reading_score"] >= 70) & (school_complete["math_score"] >= 70)
]
school_students_passing_math_and_reading = students_passing_math_and_reading.groupby(["school_name"]).size()


# In[72]:


# Use the provided code to calculate the passing rates
per_school_passing_math = school_students_passing_math / per_school_counts * 100
per_school_passing_reading = school_students_passing_reading / per_school_counts * 100
overall_passing_rate = school_students_passing_math_and_reading / per_school_counts * 100


# In[80]:


school_summary_df = pd.DataFrame({"School Type": school_types,
      "Total Students": per_school_counts,
      "Total School Budget": per_school_budget,
      "Per Student Budget": per_school_capita,
      "Average Math Score": per_school_math,
      "Average Reading Score": per_school_reading,
      "% Passing Math": school_students_passing_math,
      "% Passing Reading": school_students_passing_reading,
      "% Overall Passing Rate": school_students_passing_math_and_reading})

school_summary_df["Total School Budget"] = school_summary_df["Total School Budget"].map("${:,.2f}".format)
school_summary_df["Per Student Budget"] = school_summary_df["Per Student Budget"].map("${:,.2f}".format)

school_summary_df


# ## Highest-Performing Schools (by % Overall Passing)

# In[81]:


# Sort the schools by `% Overall Passing` in descending order and display the top 5 rows.
school_summary_df = school_summary_df.sort_values(["% Overall Passing Rate"], ascending=False)


school_summary_df.head(5)


# ## Bottom Performing Schools (By % Overall Passing)

# In[83]:


# Sort the schools by `% Overall Passing` in ascending order and display the top 5 rows.
school_summary_df = school_summary_df.sort_values(["% Overall Passing Rate"], ascending=True)
school_summary_df.head(5)


# ## Math Scores by Grade

# In[88]:


# Use the code provided to separate the data by grade
ninth_graders = school_complete[(school_complete["grade"] == "9th")]
tenth_graders = school_complete[(school_complete["grade"] == "10th")]
eleventh_graders = school_complete[(school_complete["grade"] == "11th")]
twelfth_graders = school_complete[(school_complete["grade"] == "12th")]

# Group by `school_name` and take the mean of the `math_score` column for each.
grade9= school_complete.loc[school_complete["grade"] == "9th"].groupby(["school_name"])["math_score"].mean()
grade10 = school_complete.loc[school_complete["grade"] == "10th"].groupby(["school_name"])["math_score"].mean()
grade11 = school_complete.loc[school_complete["grade"] == "11th"].groupby(["school_name"])["math_score"].mean()
grade12 = school_complete.loc[school_complete["grade"] == "12th"].groupby(["school_name"])["math_score"].mean()

# Combine each of the scores above into single DataFrame called `math_scores_by_grade`
math_scores_by_grade = pd.DataFrame({"9th": grade9,
      "10th": grade10,
      "11th": grade11,
       "12th": grade12
                                    })

# Minor data wrangling
math_scores_by_grade.index.name = None

# Display the DataFrame
math_scores_by_grade


# ## Reading Score by Grade 

# In[90]:


# Use the code provided to separate the data by grade
ninth_graders = school_complete[(school_complete["grade"] == "9th")]
tenth_graders = school_complete[(school_complete["grade"] == "10th")]
eleventh_graders = school_complete[(school_complete["grade"] == "11th")]
twelfth_graders = school_complete[(school_complete["grade"] == "12th")]

# Group by `school_name` and take the mean of the the `reading_score` column for each.
ninth_grade_reading_scores = school_complete.loc[school_complete["grade"] == "9th"].groupby(["school_name"])["reading_score"].mean()
tenth_grade_reading_scores =  school_complete.loc[school_complete["grade"] == "10th"].groupby(["school_name"])["reading_score"].mean()
eleventh_grade_reading_scores =  school_complete.loc[school_complete["grade"] == "11th"].groupby(["school_name"])["reading_score"].mean()
twelfth_grade_reading_scores = school_complete.loc[school_complete["grade"] == "12th"].groupby(["school_name"])["reading_score"].mean() 

# Combine each of the scores above into single DataFrame called `reading_scores_by_grade`
reading_scores_by_grade = pd.DataFrame({"9th": ninth_grade_reading_scores,
      "10th": tenth_grade_reading_scores,
      "11th": eleventh_grade_reading_scores,
       "12th": twelfth_grade_reading_scores
                                    })

# Minor data wrangling
reading_scores_by_grade = reading_scores_by_grade[["9th", "10th", "11th", "12th"]]
reading_scores_by_grade.index.name = None

# Display the DataFrame
reading_scores_by_grade


# ## Scores by School Spending

# In[162]:


# Establish the bins 
spending_bins = [0, 585, 615, 645, 675]
group_names = ["<$585", "$585-615", "$615-645", "$645-675"]


# In[178]:


# Create a copy of the school summary since it has the "Per Student Budget" 
school_spending_df = per_summary.copy()
school_spending_df= pd.DataFrame({"School Type": school_types,
      "Total Students": per_school_counts,
      "Total School Budget": per_school_budget,
      "Per Student Budget": per_school_capita,
      "Average Math Score": per_school_math,
      "Average Reading Score": per_school_reading,
      "% Passing Math": school_students_passing_math,
      "% Passing Reading": school_students_passing_reading,
      "% Overall Passing Rate": school_students_passing_math_and_reading})


# In[179]:


scores_by_spending = school_summary_df[["school_name",
                                    "Average Math Score",
                                    "Average Reading Score",
                                    "% Passing Math",
                                    "% Passing Reading",
                                    "% Overall Passing Rate"]]
scores_by_spending["Spending Summary"] = pd.cut(school_summary_df["Per Student Budget"], spending_bins, labels=group_names)
scores_by_spending = scores_by_spending.groupby(["Spending Summary"])
scores_by_spending.head()


# In[189]:


#  Calculate averages for the desired columns. 
spending_math_scores = per_summary.groupby(["Spending Ranges (Per Student)"])["Average Math Score"].mean()
spending_reading_scores = per_summary.groupby(["Spending Ranges (Per Student)"])["Average Reading Score"].mean()
spending_passing_math = per_summary.groupby(["Spending Ranges (Per Student)"])["% Passing Math"].mean()
spending_passing_reading = per_summary.groupby(["Spending Ranges (Per Student)"])["% Passing Reading"].mean()
overall_passing_spending = per_summary.groupby(["Spending Ranges (Per Student)"])["% Overall Passing"].mean()


# In[28]:


# Assemble into DataFrame
spending_summary = 

# Display results
spending_summary


# ## Scores by School Size

# In[114]:


# Establish the bins.
size_bins = [0, 1000, 2000, 5000]
labels = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]


# In[116]:


# Categorize the spending based on the bins
# Use `pd.cut` on the "Total Students" column of the `per_school_summary` DataFrame.

school_summary_df = school_summary_df.reset_index()
# Add Spending Ranges by Bins
school_summary_df["School Size"] = pd.cut(school_summary_df["Total Students"], size_bins, labels=labels)
# Groupby Spending ranges
grouped_size_df = school_summary_df.groupby(["School Size"])   
# Calculate the values for the data table
size_summary_df = grouped_size_df.mean()

size_summary_df


# In[31]:


# Calculate averages for the desired columns. 
size_math_scores = per_school_summary.groupby(["School Size"])["Average Math Score"].mean()
size_reading_scores = per_school_summary.groupby(["School Size"])["Average Reading Score"].mean()
size_passing_math = per_school_summary.groupby(["School Size"])["% Passing Math"].mean()
size_passing_reading = per_school_summary.groupby(["School Size"])["% Passing Reading"].mean()
size_overall_passing = per_school_summary.groupby(["School Size"])["% Overall Passing"].mean()


# In[32]:


# Create a DataFrame called `size_summary` that breaks down school performance based on school size (small, medium, or large).
# Use the scores above to create a new DataFrame called `size_summary`
size_summary = 

# Display results
size_summary


# ## Scores by School Type

# In[33]:


# Group the per_school_summary DataFrame by "School Type" and average the results.
average_math_score_by_type = per_school_summary.groupby(["School Type"])["Average Math Score"].mean()
average_reading_score_by_type = per_school_summary.groupby(["School Type"])["Average Reading Score"].mean()
average_percent_passing_math_by_type = per_school_summary.groupby(["School Type"])["% Passing Math"].mean()
average_percent_passing_reading_by_type = per_school_summary.groupby(["School Type"])["% Passing Reading"].mean()
average_percent_overall_passing_by_type = per_school_summary.groupby(["School Type"])["% Overall Passing"].mean()


# In[34]:


# Assemble the new data by type into a DataFrame called `type_summary`
type_summary = 

# Display results
type_summary


# In[ ]:





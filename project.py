#DSA Practice Tracker
import streamlit as st
import json
import os
from datetime import datetime

#Load Data
FILE = "data.json"
if os.path.exists(FILE):
    with open(FILE, "r") as s:
        try:
            data = json.load(s)
        except:
            data = []
else:
    data = []
        
#UI  
st.title("Your DSA Practice Tracker")
st.header("Add your practice stats")

with st.form("practice_form"):
    problem_name = st.text_input("Problem Name: ")
    Difficulty = st.selectbox("Difficulty", ["Easy","Medium","Hard"])
    Topic = st.text_input("Topic Name: ")
    Time_taken = st.number_input("Time Taken (in mins)", min_value=0, step=1)
    status = st.selectbox("Status:", ["SOLVED", "FAILED"])
    revision_count = st.number_input("Revision Count: ", min_value=0,step=1)
    date = st.date_input("Date of Practice: ")
    submit = st.form_submit_button("Add Practice")
    

#Add practice
if submit:
    if problem_name.strip() == "":
        st.warning("Problem cannot be empty!")
    else:
        found = False
        for problem in data:
            if problem["Problem"].lower() == problem_name.lower():
                problem["revision_count"] += 1
                found = True
                st.info(f"'{problem_name}' already exists. Revision count incremented!")
                break
        if not found:
            Details = {
            "Problem": problem_name,
            "Difficulty": Difficulty,
            "Topic name": Topic,
            "Time": Time_taken,
            "Status": status,
            "revision_count": revision_count,
            "Date": str(date),
                }
            data.append(Details) 
            st.success(f"{problem_name} added successfully.")
        
        

        with open(FILE, "w") as s:
            json.dump(data,s,indent=4)
            

#View
st.header("All practice data: ")
if data:  
    st.dataframe(data)
else:
    st.info("No Practice yet")
    
#Filter 
st.header("Filter by Difficulty: ")
difficulty_filter = st.selectbox("Choose Difficulty to filter: ", ["All", "Easy", "Medium", "Hard"])

for s in data:
    if difficulty_filter == "All" or s['Difficulty'] == difficulty_filter: 
        st.write(f"Problem: {s['Problem']} | Difficulty Level: {s['Difficulty']}")

# Weak Topics - Count failed problems by topic
fail_count = {} #count per topic
for item in data: #each problem 
    topic = item["Topic name"] #extract each topic
    if topic not in fail_count: #initialize if new topic
        fail_count[topic] = 0
        
    if item["Status"] == "FAILED":
        fail_count[topic] += 1
        
for t, count in fail_count.items():
    if count > 0:
        st.write(f" Weak topic: {t} ({count} fails)")

# avg solved time
if data:
    avg_time = sum(d["Time"] for d in data) / len(data)
    st.write("Average time practiced is:", avg_time)
else:
    st.write("Add some practice data to see average time.")


# 1. Initialize counters
easy_count = 0
medium_count = 0
hard_count = 0


for c in data: 
    if c["Difficulty"] == "Easy":
        easy_count += 1 
    elif c["Difficulty"] == "Medium":
        medium_count += 1 
    elif c["Difficulty"] == "Hard":
        hard_count += 1 

col1, col2, col3 = st.columns(3)


with col1:
    st.metric(label="Easy Problems", value=easy_count)

with col2:
    st.metric(label="Medium Problems", value=medium_count)

with col3:
    st.metric(label="Hard Problems", value=hard_count)
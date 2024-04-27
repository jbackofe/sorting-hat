from pymongo import MongoClient
from urllib.parse import quote_plus
from or_solver import or_solver
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sorting Hat", layout="wide")

st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        .stDeployButton {display:none;}
    </style>
""", unsafe_allow_html=True)

majors = ['Computer Engineering', 'Environmental Engineering', 'Electrical Engineering', 'Mechanical Engineering', 'Design Engineering', 'Other']

@st.cache_resource
def init_connection():
    host = "mongo"
    port = 27017
    user = "root"
    password = "example"

    uri = "mongodb://%s:%s@%s:%i" % (
        quote_plus(user),
        quote_plus(password),
        host,
        port
    )

    return MongoClient(uri)

# Function to get all unique project names
def get_unique_project_names(collection):
    unique_projects = {}
    for project in collection.find({}, {"name": 1, "_id": 1}):
        unique_projects[project['_id']] = project['name']
    
    # Now get just the names of these unique projects
    return list(unique_projects.values())

def get_all_documents(collection: str, database: str, client):
    db = client[database]
    student_collection = db[collection]
    return list(student_collection.find({}))

def insert_mongo_data(document, collection: str, database: str, client):
    db = client[database]
    collec = db[collection]

    collec.insert_one(document)

# Function to add a student entry form
def add_student_form(majors):
    with st.form(key='student_form'):
        name = st.text_input('Name')
        major = st.selectbox('Major', majors)  # Add more majors as needed
        project_preferences = st.multiselect('Project Preferences', get_unique_project_names(client["sorting-hat"]["projects"]))  # List all projects
        student_preferences = st.multiselect('Student Preferences', [])  # List all students

        # Form submission button
        submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            # Validate input before creating the student object and inserting into MongoDB
            if not name:
                st.error('Name is required.')
                return
            if not major:
                st.error('Major is required.')
                return
            if len(set(project_preferences)) < 6:
                st.error('At least 6 unique project preferences are required.')
                return
            
            # Create student object
            student = {
                'name': name,
                'major': major,
                'project_preferences': project_preferences,
                'student_preferences': student_preferences
            }
            
            insert_mongo_data(
                student,
                collection="students",
                database="sorting-hat",
                client=client)
            
            st.success('Student added successfully!')

def add_project_form(majors):
    with st.form(key='project_form'):
        project_name = st.text_input('Project Name')

        # Assuming you have a predefined list of majors
        majors = majors  # Add or remove majors as needed
        major_counts = {major: st.number_input(f'Number of slots for {major}', min_value=0, max_value=10, value=0) for major in majors}

        submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            if not project_name:
                st.error('Project name is required.')
                return
            
            # Check if the project name is unique
            existing_project = client["sorting-hat"]["projects"].find_one({"name": project_name})
            if existing_project:
                st.error('Project name already exists.')
                return
            
            # Check if at least one major has more than 0 slots
            if not any(count > 0 for count in major_counts.values()):
                st.error('At least one major must have more than 0 slots.')
                return
            
            # Check if no more than 10 slots for a major
            if any(count > 10 for count in major_counts.values()):
                st.error('No major can have more than 10 slots.')
                return
            
            project = {
                'name': project_name,
                'majors': major_counts
            }

            insert_mongo_data(
                project,
                collection="projects",
                database="sorting-hat",
                client=client)

            st.success('Project added successfully!') 

#Initialize the mongo client
client = init_connection()

projects_tab, students_tab, solution_tab = st.tabs(["Projects", "Students", "Solution"])

with projects_tab:
    st.title("Project Submission Form")

    new_project = add_project_form(majors)

    if new_project:
        st.write("New Project Added:")
        st.json(new_project)  # Display the submitted data as JSON
    
    all_projects_df = pd.DataFrame(
        get_all_documents(
            collection="projects",
            database="sorting-hat",
            client=client
        )
    )
    
    st.dataframe(all_projects_df)

with students_tab:
    st.title("Student Submission Form")

    new_student = add_student_form(majors)
    
    if new_student:
        st.write("New Student Added:")
        st.json(new_student)  # Display the submitted data as JSON
        
    all_students_df = pd.DataFrame(
        get_all_documents(
            collection="students",
            database="sorting-hat",
            client=client
        )
    )

    st.dataframe(all_students_df)

with solution_tab:
    st.title("Student-Project Assignment")

    all_projects = get_all_documents(
        collection="projects",
        database="sorting-hat",
        client=client
    )

    all_students = get_all_documents(
        collection="students",
        database="sorting-hat",
        client=client
    )

    solution_df = pd.DataFrame(
        or_solver(all_students, all_projects)
    )

    st.dataframe(solution_df)

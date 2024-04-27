from ortools.linear_solver import pywraplp
import pandas as pd
import random
import json

def or_solver(students, projects, decay_factor=0.5, seat_fill_weight=1, student_preference_weight=1):
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Solver not found")
        return

    # Decision variables for project assignment
    x = {}
    for student in students:
        for project in projects:
            if student['major'] in project['majors']:
                x[student['name'], project['name']] = solver.BoolVar(f'x[{student["name"]},{project["name"]}]')

    # Hard constraints
    # Each student must be assigned 1 project
    for student in students:
        solver.Add(solver.Sum([x[student['name'], project['name']] for project in projects if (student['name'], project['name']) in x]) == 1)

    # Do not exceed maximum number of students in a major for each project
    for project in projects:
        for m in project['majors']:
            solver.Add(solver.Sum([x[student['name'], project['name']] for student in students if student['major'] == m and (student['name'], project['name']) in x]) <= project['majors'][m])

    # Soft constraints
    # Exponential decay for project preferences
    project_preferences_score = solver.Sum(
        [(decay_factor ** student['project_preferences'].index(proj_name)) * x[student['name'], proj_name]
         for student in students
         for proj_name in student['project_preferences']
         if (student['name'], proj_name) in x])

    # Score for student preferences
    student_preferences_score = solver.Sum(
        [x[student['name'], project['name']] for student in students for project in projects for student_pref in student.get('student_preferences', []) if student_pref in [s['name'] for s in students] and project['name'] in [s['project_preferences'] for s in students if s['name'] == student_pref][0] and (student['name'], project['name']) in x and (student_pref, project['name']) in x]) * student_preference_weight

    # Score for filling seats in a project
    seat_filling_score = solver.Sum([x[student['name'], project['name']] for student in students for project in projects if (student['name'], project['name']) in x]) * seat_fill_weight

    # Objective function
    solver.Maximize(project_preferences_score + seat_filling_score + student_preferences_score)

    # Solve the problem
    status = solver.Solve()

    # Output the solution
    solution = []
    if status == pywraplp.Solver.OPTIMAL:
        for student in students:
            for project in projects:
                if (student['name'], project['name']) in x and x[student['name'], project['name']].solution_value() > 0.5:
                    solution.append({'student': student['name'], 'project': project['name']})
        return solution
    else:
        print('The problem does not have an optimal solution.')
        return None
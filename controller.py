import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

midterm = ctrl.Antecedent(np.arange(0, 101, 1), 'midterm')
final = ctrl.Antecedent(np.arange(0, 101, 1), 'final')
homework = ctrl.Antecedent(np.arange(0, 101, 1), 'homework')
attendance = ctrl.Antecedent(np.arange(0, 101, 1), 'attendance')
participation = ctrl.Antecedent(np.arange(0, 11, 1), 'participation')

grade = ctrl.Consequent(np.arange(0, 101, 1), 'grade')
tutoring = ctrl.Consequent(np.arange(0, 11, 1), 'tutoring')

for var in (midterm, final, homework):
    var['low'] = fuzz.trapmf(var.universe, [0, 0, 40, 60])
    var['medium'] = fuzz.trimf(var.universe, [40, 60, 80])
    var['high'] = fuzz.trapmf(var.universe, [60, 80, 100, 100])

attendance['low'] = fuzz.trapmf(attendance.universe, [0, 0, 30, 50])
attendance['fair'] = fuzz.trimf(attendance.universe, [30, 50, 80])
attendance['excellent'] = fuzz.trapmf(attendance.universe, [60, 80, 100, 100])

participation['low'] = fuzz.trapmf(participation.universe, [0, 0, 3, 5])
participation['medium'] = fuzz.trimf(participation.universe, [3, 5, 8])
participation['high'] = fuzz.trapmf(participation.universe, [6, 8, 10, 10])

grade['F'] = fuzz.trapmf(grade.universe, [0, 0, 40, 50])
grade['C'] = fuzz.trimf(grade.universe, [40, 55, 70])
grade['B'] = fuzz.trimf(grade.universe, [60, 75, 90])
grade['A'] = fuzz.trapmf(grade.universe, [80, 90, 100, 100])

tutoring['none'] = fuzz.trapmf(tutoring.universe, [0, 0, 1, 2])
tutoring['low'] = fuzz.trimf(tutoring.universe, [1, 3, 5])
tutoring['medium'] = fuzz.trimf(tutoring.universe, [4, 6, 8])
tutoring['high'] = fuzz.trapmf(tutoring.universe, [7, 9, 10, 10])

rules = []

grades_map = {
    ('low','low'):    ('F','high'),
    ('low','medium'): ('F','medium'),
    ('low','high'):   ('C','medium'),
    ('medium','low'): ('F','medium'),
    ('medium','medium'): ('C','low'),
    ('medium','high'):   ('B','low'),
    ('high','low'):   ('C','low'),
    ('high','medium'): ('B','low'),
    ('high','high'):  ('A','none'),
}
for m_level, f_level in grades_map:
    g_label, t_label = grades_map[(m_level, f_level)]
    rules.append(
        ctrl.Rule(
            midterm[m_level] & final[f_level],
            (grade[g_label], tutoring[t_label])
        )
    )

hw_att_map = {
    ('low','low'):      ('F','high'),
    ('low','fair'):     ('F','high'),
    ('low','excellent'):('C','medium'),
    ('medium','low'):   ('F','high'),
    ('medium','fair'):  ('C','medium'),
    ('medium','excellent'):('B','low'),
    ('high','low'):     ('C','medium'),
    ('high','fair'):    ('B','low'),
    ('high','excellent'):('A','none'),
}
for hw_level, att_level in hw_att_map:
    g_label, t_label = hw_att_map[(hw_level, att_level)]
    rules.append(
        ctrl.Rule(
            homework[hw_level] & attendance[att_level],
            (grade[g_label], tutoring[t_label])
        )
    )

rules.append(ctrl.Rule(participation['low'],    tutoring['high']))
rules.append(ctrl.Rule(participation['medium'], tutoring['medium']))
rules.append(ctrl.Rule(participation['high'],   tutoring['low']))

f_att_map = {
    ('low','low'):      ('F','high'),
    ('medium','fair'):  ('C','medium'),
    ('high','excellent'):('A','none'),
}
for f_level, att_level in f_att_map:
    g_label, t_label = f_att_map[(f_level, att_level)]
    rules.append(
        ctrl.Rule(
            final[f_level] & attendance[att_level],
            (grade[g_label], tutoring[t_label])
        )
    )

m_hw_map = {
    ('low','low'):      ('F','high'),
    ('medium','medium'):('C','low'),
    ('high','high'):    ('B','low'),
}
for m_level, hw_level in m_hw_map:
    g_label, t_label = m_hw_map[(m_level, hw_level)]
    rules.append(
        ctrl.Rule(
            midterm[m_level] & homework[hw_level],
            (grade[g_label], tutoring[t_label])
        )
    )

system = ctrl.ControlSystem(rules)
sim = ctrl.ControlSystemSimulation(system)
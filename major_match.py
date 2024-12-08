# match major to fields
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

training_data = [
    ("Computer Science Major", "STEM"),
    ("Chemistry Major", "STEM"),
    ("Mathematics Major", "STEM"),
    ("Earth and Planetary Sciences Major", "STEM"),
    ("Mechanical Engineering Major", "STEM"),
    ("Applied Mathematics Major", "STEM"),
    ("Physics Major", "STEM"),
    ("Art History Major", "Humanities"),
    ("English Major", "Humanities"),
    ("Asian Humanities Major", "Humanities"),
    ("Classics Major", "Humanities"),
    ("Philosophy Major", "Social Sciences"),
    ("Economics Major", "Social Sciences"),
    ("Sociology Major", "Social Sciences"),
    ("Black Studies Major", "Social Sciences"),
    ("Russian Language Major", "Humanities"),
    ("String Instruments Major", "Fine Arts"),
    ("Opera Major", "Fine Arts"),
    ("Music Theory Major", "Fine Arts"),
    ("Theater Major", "Fine Arts"),
    ("Dance Major", "Fine Arts"),
    ("Art Practice", "Fine Arts"),
    ('Middle East and North African Studies Major', 'Social Sciences'),
    ("Creative Writing Major", "Humanities"),

    ("Computer Science Minor", "STEM"),
    ("Chemistry Minor", "STEM"),
    ("Mathematics Minor", "STEM"),
    ("Earth and Planetary Sciences Minor", "STEM"),
    ("Mechanical Engineering Minor", "STEM"),
    ("Applied Mathematics Minor", "STEM"),
    ("Physics Minor", "STEM"),
    ("Art History Minor", "Humanities"),
    ("English Minor", "Humanities"),
    ("Asian Humanities Minor", "Humanities"),
    ("Classics Minor", "Humanities"),
    ("Philosophy Minor", "Social Sciences"),
    ("Economics Minor", "Social Sciences"),
    ("Sociology Minor", "Social Sciences"),
    ("Black Studies Minor", "Social Sciences"),
    ("Russian Language Minor", "Humanities"),
    ("String Instruments Minor", "Fine Arts"),
    ("Opera Minor", "Fine Arts"),
    ("Music Theory Minor", "Fine Arts"),
    ("Theater Minor", "Fine Arts"),
    ("Dance Minor", "Fine Arts"),
    ("Art Practice", "Fine Arts"),
    ('Middle East and North African Studies Minor', 'Social Sciences'),
    ("Creative Writing Minor", "Humanities"),
    ('Portuguese', 'Humanities'),
    ('Spanish Major', 'Humanities'),
    ('Spanish Minor', 'Humanities'),
]

texts = [t[0] for t in training_data]
labels = [t[1] for t in training_data]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)
y = labels


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, y_train)

def match(majors):

    res = {}

    for i in majors:
        X_new = vectorizer.transform([i])
        predicted_category = str(clf.predict(X_new)[0])

        res[i] = predicted_category

    return res

# print(match(['Advanced Asian Languages Minor', 'African Studies Adjunct Major', 'African Studies Minor', 'American Studies Major', 'Anthropology Major', 'Anthropology Minor', 'Applied Mathematics Degree', 'Arabic Minor', 'Architectural Engineering and Design Minor', 'Art History Major', 'Art History Minor', 'Art Theory and Practice Major', 'Art Theory and Practice Minor', 'Artificial Intelligence', 'Asian American Studies Major', 'Asian American Studies Minor', 'Asian Humanities Minor', 'Asian Languages and Cultures Major', 'Biological Sciences Major', 'Biological Sciences Second Major for ISP Students', 'Biomedical Engineering Degree', 'Biotechnology and Biochemical Engineering Minor', 'Black Studies Major', 'Black Studies Minor', 'Brady Scholars Program', 'Business German Minor', 'Business Institutions Minor', 'Catholic Studies Minor', 'Chemical Engineering Degree', 'Chemistry BA/MS', 'Chemistry Major', 'Chemistry Minor', 'Chemistry Second Major for ISP Students', 'Chicago Field Studies', 'Civic Engagement Certificate', 'Civil Engineering Degree', 'Classics Major', 'Classics Minor Concentrations', 'Cognitive Science Major', 'Cognitive Science Minor', 'Communication Studies Major', 'Comparative Literary Studies BA/MA', 'Comparative Literary Studies Major', 'Composition Major', 'Composition Minor', 'Computer Engineering Degree', 'Computer Science BA/MS', 'Computer Science Degree', 'Computer Science Major', 'Computer Science Minor (McCormick School of Engineering)', 'Computer Science Minor (Weinberg College)', 'Computer Science Second Major for ISP Students', 'Conducting and Ensembles', 'Creative Writing Cross-Genre Minor', 'Creative Writing Major', 'Creative Writing Sequence-Based Minor', 'Critical Theory Minor', 'Curious Life Certificate', 'Dance Major', 'Dance Minor', 'Data Science Major', 'Data Science Minor', 'Earth and Planetary Sciences Major', 'Earth and Planetary Sciences Minor', 'Earth and Planetary Sciences Second Major for ISP Students', 'Economics BA/MA', 'Economics Major', 'Economics Minor', 'Electrical Engineering Degree', 'Elementary Teaching Major', 'English Major', 'English Minor', 'Entrepreneurship Minor', 'Environmental Engineering Degree', 'Environmental Engineering Minor', 'Environmental Policy and Culture Adjunct Major', 'Environmental Policy and Culture Minor', 'Environmental Sciences Major', 'Environmental Sciences Second Major for ISP Students', 'Ethics and Civic Life', 'Experiential Learning', 'Film and Media Studies Minor', 'Financial Economics Certificate', 'French BA/MA', 'French Major', 'French Minor', 'Game Design + Media Arts + Animation Minor', 'Gender and Sexuality Studies Major', 'Gender and Sexuality Studies Minor', 'General Engineering', 'German Major', 'German Minor', 'German Studies Minor', 'Global Health Studies Adjunct Major', 'Global Health Studies Minor', 'Hebrew Studies Minor', 'History Major', 'History Minor', 'Human Communication Sciences Major', 'Human Communication Sciences Minor', 'Human Computer Interaction Certificate', 'Human Development in Context Major', 'Humanities Minor', 'Industrial Engineering Degree', 'Integrated Marketing Communications Certificate', 'Integrated Science Major', 'Interdepartmental Communication Options', 'International Studies Adjunct Major', 'International Studies Minor', 'Italian', 'Italian Literature and Culture Major', 'Italian Minor', 'Jazz Studies Major', 'Jewish Studies Major', 'Jewish Studies Minor', 'Journalism Degree', 'Latin American and Caribbean Studies Minor', 'Latina and Latino Studies Major', 'Latina and Latino Studies Minor', 'Leadership', 'Learning and Organizational Change Major', 'Learning Sciences Major', 'Legal Studies Major', 'Legal Studies Minor', 'Linguistics BA/MA', 'Linguistics Major', 'Linguistics Minor', 'Machine Learning and Data Science Minor', 'Managerial Analytics Certificate', 'Manufacturing and Design Engineering Degree', 'Materials Science and Engineering Degree', 'Materials Science Minor', 'Mathematics Major', 'Mathematics Minor', 'Mathematics Second Major for ISP Students', 'Mathematics Second Major or Minor for MMSS Students', 'Mechanical Engineering Degree', 'Middle East and North African Studies Major', 'Middle East and North African Studies Minor', 'MMSS Adjunct Major', 'Music Cognition', 'Music Cognition Major', 'Music Cognition Minor', 'Music Education Major', 'Music Education Minor', 'Music Technology Minor', 'Music Theatre Certificate', 'Music Theory Major', 'Music Theory Minor', 'Musicology Major', 'Musicology Minor', 'Native American and Indigenous Studies Minor', 'Naval Science', 'Neuroscience Major', 'Neuroscience Second Major for ISP Students', 'Performance Studies Major', 'Performance Studies Minor', 'Persian', 'Philosophy Major', 'Philosophy Minor', 'Physics Major', 'Physics Minor', 'Physics Second Major for ISP Students', 'Piano Major', 'Political Science Major', 'Political Science Minor', 'Portuguese', 'Portuguese Language and Lusophone Cultures Minor', 'Premedical Scholars Program', 'Psychology Major', 'Psychology Minor', 'Radio/Television/Film Major', 'Religious Studies Major', 'Religious Studies Minor', 'Russian', 'Russian and East European Studies Minor', 'Science in Human Culture Adjunct Major', 'Science in Human Culture Minor', 'Secondary Teaching', 'Segal Design Certificate', 'Slavic Languages and Literatures Major', 'Social Policy Major', 'Sociological Research Minor', 'Sociological Studies Minor', 'Sociology Major', 'Sound Design Minor', 'Spanish Major', 'Spanish Minor', 'Statistics Major', 'Statistics Minor', 'String Instruments Major', 'Sustainability and Energy', 'Theatre Major', 'Theatre Minor', 'Transportation and Logistics Minor', 'Voice and Opera Major', 'Winds and Percussion Instruments Major', 'World Literature Minor', 'Writing Program']))
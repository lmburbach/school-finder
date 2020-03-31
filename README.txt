CAN CHICAGO TEACHERS AFFORD TO LIVE WHERE THEY TEACH?
Analyzing teacher salaries and nearby property values for Chicago Public Schools

LauraMargaret Burbach, Jonathan Rockower, Mike Feldman

README CONTENTS
    0. How to Run School Finder Application
    1. Files
    2. Member Contributions
    3. Project Goals and Accomplishments
        (also in burbach-jrockower-mikefeldman.pdf)
    4. Data Selection Notes

0. HOW TO RUN SCHOOL FINDER APPLICATION
    1. Install Python3.7 from source:
        https://linuxize.com/post/how-to-install-python-3-7-on-ubuntu-18-04/
    2. Run install shell script
        $ ./install.sh
    3. Enter virtual environment
        $ source env/bin/activate
    4. Open data/school_codes.csv
        $ subl data/school_codes.csv
    5. Run main.py
        $ python3.7 main.py [-a]
          Optional [-a] parameter can be used to pull from archived versions of
          files without pulling via API. Without [-a], the application takes us
          about 30 seconds to run.

1. FILES
    a. README.txt
    b. requirements.txt
    c. install.sh
    d. socrata_request.py
    e. assessors_request.py
    f. cps_request.py
    g. school_class.py
    h. main.py

2. MEMBER CONTRIBUTIONS
    LauraMargaret Burbach
        Primary: school_class.py, main.py 
        Secondary: README.txt

    Jonathan Rockower
        Primary: assessors_request.py, socrata_request.py, install.sh
        Secondary: main.py, README.txt

    Mike Feldman
        Primary: socrata_request.py, cps_request.py, requirements.txt
        Secondary: install.sh, README.txt
        [Mike also worked on a maps.py module that would have visualized salary/property data by Chicago neighborhood, but that was ultimately scrapped due to time constraints]

3. PROJECT GOALS AND ACCOMPLISHMENTS
    Our project set out to answer the question: Can Chicago Public Schools teachers afford to buy homes near the schools where they teach?

    The impetus for this work was the October 2019 Chicago Teachers Union strike, particularly the Union’s ask for teacher and staff raises in response to the rising cost of living. Much of the existing research on property values and schools is directed at parents looking at school attendance zones. We wanted to reframe property analyses from a teacher perspective, considering locations close to the school, but irrespective of attendance boundaries.

    As the teacher workforce continues to become younger and less experienced nationwide, we wanted to look specifically at home-buying opportunities within 5 miles of a school. Home ownership, rather than renting, would signal stability and community investment. Real estate and budgeting websites cite a rule of thumb that buyers can afford a house priced at about 2 – 2.5 times their household income.
    
    Our project addresses this question by providing an interactive tool that allows users to select a school and set a distance to see how teacher salaries at that school and sale prices around that school compare to those of all Chicago Public Schools teachers and all Cook County homes.

4. DATA SELECTION NOTES
    1. Assessor Data
        a. Keep sales >= $10000
        b. Remove observations with NaN values in both 'apts' (number of apartments) and 'n_units' (number of units within condominium complex) because it is unclear what type of properties these are
        c. Set observations with '0' apts equal to '1' and those with negative apts to the absolute value of apts
        d. Keep observations where 'most_recent_sale' == 1 to keep the most recent sale on a property
        e. Remove 30,000 additional duplicates on 'pin' by keeping the most recent 'sale_date' observation for each 'pin'
        f. Keep single family home and condominiums only to analyze data on sales of individual properties, not apartment buildings
    2. Teacher Salary Data
        a. Keep full-time employees
        b. Keep people with job title:
            i. Includes the word 'Teacher'
            ii. Doesn't include the words: 'Assistant', 'Asst', 'Specialist', 'Analyst', 'Recruitment', 'Part-Time'
        c. Filter out teachers who are not linked (through their Finance ID) to a specific school/school ID (approximately 600 observations dropped)



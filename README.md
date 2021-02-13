# SwimScheduler
## Goal: Minimize scheduling conflicts
## Procedure
1. Practice classes are created with a maximum number of participants, a time slot, and a designation (morning/afternoon)
2. Swimmer classes are created by parsing a provided CSV file
  a. Each swimmer-practice pairing is evaluated and assigned one of four designations
    1. Dogshit: practice and classes directly overlap (e.g. Swimmer A has class from 1-4pm and practice from 2-3:30pm)
    2. Horrible: class follows practice immediately (e.g. Swimmer A has practice from 8-9am and class from 9-9:50am)
    3. Manageable: practice follows class immediately (e.g. Swimmer A has class from 1-4pm and practice from 4-5:30pm)
    4. Ideal: there is at least a one hour gap inbetween a practice and a class and a 15 minute gap between class and practice (examples below)
    5. Swimmer A has practice from 5-6:30pm and class at 7-9:30pm. This is NOT ideal because there is not enough time after practice (ending practice at 6 would be enough)
    6. Swimmer B has class from 1-1:50pm and practice  from 2-3:30pm. This is NOT ideal because there  is not enough time after class (ending class at 1:45 would be enough)
3. Recursively place Swimmers into Practices
4. Output a CSV file of all "un-parsable" individuals
5. Ouptut a CSV file of sorted swimmers

## Instructions
1. Get everybody to fill out a form with their practices.
2. Format -> Last Name | class1 | class2 | class3 | class4 | class5 (if needed)
3. Give CSV to Caleb (not Coach Caleb)
# Inspection Tracker

## Purpose and intent
The idea behind this application was to develope a better way to track inspections, manage the information gathered from projects, inspections, building departments, and clients, and use that information to identify patterns and areas of improvement. Closing out projects in a timely manner is key to mainting cash flow and understanding the key reasons inspections are failed can help educate future projects and inspections thus increasing the closing percentage on the first attempt.

### API's Used
[QuickChart](https://quickchart.io/documentation/)

### Database notes
There are 7 primary tables representing building deparments, clients, installations teams, inspections, projects, building department contacts, and inspection sitters along with their key attributes.

**Building departments** are the jurisdiction responsible for conducting the inspection, these are typically either city wide or county wide.

**Clients** are the entities who have had the work done that needs to be inspected. 

**Installation teams** are the teams that did the work that is being inspected.

**Inspections** are individual instances of one particular type of inspection related to one specific project.

**Projects** represent the details of a given project, there is one client, one building department, the job number, and a link to the details in our CRM

**Building department contacts** are known contacts from the building department. This can include inspectors, reviewers, building officials, or anyone relevant to the inspection phase of the project.

**Inspection Sitters** are the people sitting the inspection/ meeting with the inspector on site. Typically this is the installation team themselves, but occasionally we hire a 3rd party to sit and represent us. If the team is sitting the inspection it is not required to enter a sitter on an inspection instance.

#### Challenges
Designing the database properly was key for this application is it relies heavily on data integrity and proper relationships that will be used for different reporting and analysis.

Consider routes for projects should they be /project/.../.../... or should they be clients/client.id/projects/.../.../...?

Why am I not showing prefilled job# on edit_inspection form?
-- show all inspections that are to close out a project
SELECT c.first_name, c.last_name, it.team_name, i.type, i.date
FROM inspections AS i
JOIN projects AS p
ON i.project_id = p.id
JOIN clients AS c
ON c.id = p.client_id
JOIN installation_teams AS it
ON i.team_id = it.id
WHERE i.to_close = True;

-- show all inspections where installer is nidel
SELECT c.first_name, c.last_name, it.team_name, bd.name, i.type, i.date, i.result
FROM inspections AS i
JOIN installation_teams AS it
ON i.team_id = it.id
JOIN projects AS p
ON i.project_id = p.id
JOIN building_depts AS bd
ON bd.id = p.bd_id
JOIN clients AS c
ON c.id = p.client_id
WHERE team_name = 'nidel';

-- show all inspections in miami-dade
SELECT c.first_name, c.last_name, it.team_name, bd.name, i.type, i.date, i.result
FROM inspections AS i
JOIN installation_teams AS it
ON i.team_id = it.id
JOIN projects AS p
ON i.project_id = p.id
JOIN building_depts AS bd
ON bd.id = p.bd_id
JOIN clients AS c
ON c.id = p.client_id
WHERE bd.name = 'city of miami-dade';

-- show all inspection scheduled for 3/11/24
SELECT c.first_name, c.last_name, it.team_name, bd.name, i.type, i.date, i.result
FROM inspections AS i
JOIN installation_teams AS it
ON i.team_id = it.id
JOIN projects AS p
ON i.project_id = p.id
JOIN building_depts AS bd
ON bd.id = p.bd_id
JOIN clients AS c
ON c.id = p.client_id
WHERE i.date = '2024-03-11';
Run the command in in project directory: docker-compose up

1.Instead of using a database, I am using a session stored dictionary to save the data in between API calls. As we are only storing the data in JSON format, we can store them directly as python dictioaries.
Start by hitting the Init API call in the postman collections. This will create an empty dictionary.
2. The ignest API call will store the data sent, in JSON format.
3. "GET Backlog" will retrieve the current status of the data in JSON format.
4. "searchByBug" will sent a request with the bug to be searched in the request body.
"updateByEpic" since its not mentioned how the data to be updated has to be formatted. An assumption has been made, with the request format in JSON format with fields that has to be updated in.
7. "DeleteTaskOrBug" will delete the associated bug or task.
8. "ExportBacklog" will export the data in a JSON format.

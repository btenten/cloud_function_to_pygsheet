# cloud_function_to_pygsheet_line_notify
Demonstrate using Google Cloud Function to get data and paste to Google Sheet using pygsheet, then notify the process result via LINE


## prerequisites
- LINE token
- Google service account and keys.
- Prepared Google Sheet which already granted access to Google service account.

### Steps
1. Go to Google Cloud Platform > Cloud Functions
2. Select 'Create Function'
3. In section 'Trigger' select 'Cloud Pub/Sub', create and save your topic.
4. In section 'Variables, Networking and advanced settings' select 'Environment variables'
5. Input key-value pair of your credentials in section 'Runtime environment variables' > Next
6. For main.py, place the code.
7. For requirements.txt place list of required Python libraries.
8. Select 'Deploy'
9. Go to Google Cloud Platform > Cloud Scheduler
10. Select 'Create job'
11. For 'Frequency' box, input your schedule time in cron format (e.g. 0 20 * * * = everyday at 8PM)
12. For 'target', select Pub/Sub and put in your topic name. For payload, can input anything e.g. 'Run now'
13. Select 'Create'
14. Test the whole process by clicking 'RUN NOW'

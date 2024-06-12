# How to run the OLX Bot:

## 1. Prepare the necessary XML files:

### account_data.xml
```xml
<?xml version="1.0" encoding="UTF-8"?>
<account_data>
    <login>YOUR_LOGIN</login>
    <password>YOUR_PASSWORD</password>
</account_data>
```


### job_application_data.xml
```xml
<?xml version="1.0" encoding="UTF-8"?>
<job_application>
    <search_url>URL</search_url>
    <name>NAME</name>
    <surname>SURNAME</surname>
    <phone>PHONE</phone>
    <email>EMAIL</email>
    <cv_file_path>PATH_TO_FILE</cv_file_path>
    <message>MESSAGE_TEXT</message>
    <expected_salary>SALARY</expected_salary>
</job_application>
```
NOTE fields: name, surname, phone, email and cv_file_path are not in use, 
because OLX allows for saving the candidate profile and this data doesn'e 
need to be entered every time 


## 2. Run the main.py script
# Credentials Folder

## The purpose of this folder is to store all credentials needed to log into your server and databases. This is important for many reasons. But the two most important reasons is
    1. Grading , servers and databases will be logged into to check code and functionality of application. Not changes will be unless directed and coordinated with the team.
    2. Help. If a class TA or class CTO needs to help a team with an issue, this folder will help facilitate this giving the TA or CTO all needed info AND instructions for logging into your team's server. 


# Below is a list of items required. Missing items will causes points to be deducted from multiple milestone submissions.

1. Server URL or IP
   - http://ec2-34-228-231-71.compute-1.amazonaws.com/
2. SSH username
   - ubuntu
3. SSH password or key.
   - Check pem file
    <br> If a ssh key is used please upload the key to the credentials folder.
7. Database URL or IP and port used.
    - 127.0.0.1 (IP)
    - 3306 (Port)
    <br><strong> NOTE THIS DOES NOT MEAN YOUR DATABASE NEEDS A PUBLIC FACING PORT.</strong> But knowing the IP and port number will help with SSH tunneling into the database. The default port is more than sufficient for this class.
8. Database username
    - ubuntu
10. Database password
    - Aman2423!
12. Database name (basically the name that contains all your tables)
    - teams_4
14. Instructions on how to use the above information.

  **Setting up an SSH Tunnel**:
   An SSH tunnel forwards a port on your local machine to a port on the remote server securely over SSH. You can set up an SSH tunnel using the following command in your local terminal:
   - ssh -L 3306:127.0.0.1:3306 -N -i /path/to/your-key.pem ubuntu@ec2-34-228-231-71.compute-1.amazonaws.com
   Replace `/path/to/your-key.pem` with the actual path to your `.pem` key file. This command will not give you a shell on the remote server; it will only set up the tunnel.

 **Connecting to the MySQL Database**:
   With the SSH tunnel established, you can now connect to the MySQL database using a local MySQL client or a database management tool like MySQL Workbench or phpMyAdmin. Use the following connection details:

   - **Host**: `127.0.0.1` (because the SSH tunnel makes it look as if the MySQL server is running on your local machine)
   - **Port**: `3306` (the local port you're forwarding to the remote MySQL server)
   - **Username**: `ubuntu` (the MySQL username)
   - **Password**: `Aman2423!` (the MySQL password)
   - **Database**: `teams_4` (the specific database you want to connect to)

 **Using MySQL Workbench**:
   If you are using MySQL Workbench, you can set up a new connection with the following details:

   - **Connection Method**: Standard TCP/IP over SSH
   - **SSH Hostname**: `ec2-34-228-231-71.compute-1.amazonaws.com`
   - **SSH Username**: `ubuntu`
   - **SSH Key File**: Browse to your `.pem` key file
   - **MySQL Hostname**: `127.0.0.1`
   - **MySQL Server Port**: `3306`
   - **Username**: `ubuntu`
   - **Password**: Store the password `Aman2423!` in the password vault

 **Accessing the Database**:
   Once connected, you can access and manage your database `teams_4` as needed, run SQL queries, and perform other database operations as permitted by the user's privileges.

# Most important things to Remember
## These values need to kept update to date throughout the semester. <br>
## <strong>Failure to do so will result it points be deducted from milestone submissions.</strong><br>
## You may store the most of the above in this README.md file. DO NOT Store the SSH key or any keys in this README.md file.

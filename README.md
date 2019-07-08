# Udacity-fsnd-log-analysis
Udacity Full Stack NanoDegree Log Analysis Project

## Project Description
>This is a project assigned by Udacity in part of the Udacity Full Stack Nanodegree program. In This project, we're provided a sql file to generate a `PostgreSQL` database and a `Vagrantfile` settings to run a VM server to run the database.
>Your task is to create a reporting tool that prints out reports (in plain text) based on the data in the database. This reporting tool is a Python program using the psycopg2 module to connect to the database.

We need to answer the following questions by writing queries for the database and outputs the result onto a text file `logs-reports.txt`:  
1. What are the most popular three articles of all time?  
2. Who are the most popular article authors of all time?  
3. On which days did more than 1% of requests lead to errors?

## Setting up the VM using VirtualBox and Vagrant
1. Download and install VM using [VirtualBox](https://www.virtualbox.org/wiki/Downloads)  
2. Download and install [Vagrant](https://www.vagrantup.com/downloads.html) for the VM settings 
3. Download Vagrantfile in the working folder and Run command `vagrant up` to load box and settings the VM
4. Run `vagrant ssh` to log into the VM
5. Install psycog2 using command pip install psycog2
  
## Setting up the database and Creating Views:
1. Download the [news data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)  and save it in the working VM folder 
2. Load the data in local database using the command:

  ```
    psql -d news -f newsdata.sql
  ```
• Use `psql -d news` to connect to database.
  
## Running the script python to generate reports:
  Run logs_reports.py using:
  ```
    $ python logs_reports.py
  ```
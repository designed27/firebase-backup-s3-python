Backup Firebase data to AWS S3
==============================

Using python, you can automatically (with cron or heroku scheduler) backup all
your Firebase data and store it safely on AWS S3.

The result is a new .json file in your S3 bucket whenever you run this script.

Install
-------

    virtualenv -p python2.7 --distribute venv
    source venv/bin/activate
    pip install -r requirements.txt


Run
---

Set your environment variables. Then run:

    python backup-firebase.py

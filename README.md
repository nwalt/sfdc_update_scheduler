# sfdc_update_scheduler
Cron script for making scheduled updates to a salesforce environment.

Intended to be run hourly. Accepts one filesystem path as an argument, and processes all .json files found there.
Requires a username/password/security token credential file for your sfdc env, in the same directory as the script itself. Reccomend restricting access to this file that only the cron user can read it. Also recommend using a different directory for the update files and logs.
credential file should look like: {"user":"your_sfdc_username", "pass":"your_password",toke:"your_security_token"}

Install with:
```
$ git clone https://github.com/nwalt/sfdc_update_scheduler
$ python3 ./sfdc_update_scheduler/setup.py install
```
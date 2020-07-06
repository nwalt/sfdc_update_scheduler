# sfdc_update_scheduler
Cron script for making scheduled updates to a salesforce environment.

Intended to be run hourly. Accepts one filesystem path as an argument, and processes all .json files found there.
Requires a username/password/security token credential file for your sfdc env. Reccomend restricting access to this file that only the cron user can read it.

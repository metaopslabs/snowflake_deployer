# Task

Snowflake Docs - [CREATE TASK](https://docs.snowflake.com/en/sql-reference/sql/create-task)

Snowflake Docs - [ALTER TASK](https://docs.snowflake.com/en/sql-reference/sql/alter-task)

## Usage 
* A Task is made up of 2 parts
    * YAML Configuration
    * SQL code with the task execution code
* All tasks must live inside a [DATABASE]/[SCHEMA]/TASKS folder and contain both a .yml file and .sql file with the same name.
* Object name = name of the yml config file within [DATABASE]/[SCHEMA]/TASKS folder

## Snowflake Attributes

| <div style="width:175px">Parameter</div>          | Description                          |
| ------------------------------------------------  | ------------------------------------ |
| `WAREHOUSE`         | (String) - Optional |
| `USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE`         | (String) - <ul><li>Valid Values = [XSMALL, SMALL, MEDIUM, LARGE, XLARGE, XXLARGE, XXXLARGE, X4LARGE, X5LARGE, X6LARGE]</li><li>The initial warehouse size is currently not available to pull in via the reverse engineering (not visible in Snowflake SHOW/DESC).  It is assumed that if the WAREHOUSE is null, that this initial value is XSMALL.  This is only relavent for the initial creation of the task, else the "serverless" handles all compute.</li></ul> |
| `SCHEDULE`         | (String) - Optional |
| `ALLOW_OVERLAPPING_EXECUTION`         | (Bool) - Optional |
| `PREDECESSORS`         | (List[String]) - Optional |
| `ERROR_INTEGRATION`         | (String) - Optional |
| `CONDITION`         | (String) - Optional |
| `USER_TASK_TIMEOUT_MS`         | (Int) - Optional |
| `SUSPEND_TASK_AFTER_NUM_FAILURES`         | (Int) - Optional |
| `COMMENT`         | (String) - Optional |
| `OWNER`         | (String) - Optional <ul><li>If HANDLE_OWNERSHIP=ERROR, be careful not to set OWNER to a role that the deployer does not have access to as it will no longer have access to manage</li></ul>|
| `TAGS`         | ({KEY:VALUE}) - Optional |
| `GRANTS`         | ({KEY:VALUE}) - Optional |
| `ENABLED`         | (Bool) - Optional <ul><li>If enabled, deployer runs a "RESUME" command to start task.  If disable, deployer runs a "SUSPEND" commend to pause task</li></ul>|
        
Optional Parameter Defaults - if omitted, Snowflake defaults for parameters are used, just like creating an object manually.

## Deployment attributes

| <div style="width:175px">Parameter</div>          | Description                          |
| ------------------------------------------------  | ------------------------------------ |
| `DEPLOY_ENV`         | (List) - Optional <ul><li>Default = []</li><li>List of the deployment environments to deploy to</li><li>Deployment environment set in the environment config yaml using the DEPLOY_ENV parameter.  See Setup/Config for docs.</li><li>When empty or not included, deployed to all environments</li></ul> |
| `DEPLOY_LOCK`         | (Bool) - Optional <ul><li>Default = False</li><li>Locks the config file to being over written by reverse engineer process.</li><li>Use if source code should always be source of truth and any changes pulled from database should be ignored</li></ul> |

## Folder Structure

Configuration:
  `snowflake/data/[database name]/[schema name]/TASKS/[task name].yml`

Policy
  `snowflake/data/[database name]/[schema name]/TASKS/[task name].sql`
  

!!! note annotate "Example Structure"
    snowflake/data/CONTROL/AUTOMATION/TASKS/RUN_MONTHLY_PROCESS.yml
    
    snowflake/data/CONTROL/AUTOMATION/TASKS/RUN_MONTHLY_PROCESS.sql

    snowflake/data/CONTROL/AUTOMATION/TASKS/TAG_COLUMNS.yml

    snowflake/data/CONTROL/AUTOMATION/TASKS/TAG_COLUMNS.sql
    
    This specifies the metadata for 2 tasks named "RUN_MONTHLY_PROCESS" and "TAG_COLUMNS" within the CONTROL.AUTOMATION schema, each with their own yml config file & sql based on the task name

## Samples

Config File - Serverless Task
```
WAREHOUSE: 
USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE: XSMALL
SCHEDULE: USING CRON  0 * * * * America/Los_Angeles
ALLOW_OVERLAPPING_EXECUTION: true
PREDECESSORS: 
- {{ref('CODE__AUTOMATION__SOME_OTHER_TASK')}}
- {{ref('CODE__AUTOMATION__ANOTHER_TASK')}}
ERROR_INTEGRATION: 
OWNER: INSTANCEADMIN
COMMENT: This is a demo automation task
ENABLED: true
CONDITION: 
USER_TASK_TIMEOUT_MS: 600
SUSPEND_TASK_AFTER_NUM_FAILURES: 5
TAGS: 
- {{ref('CONTROL__GOVERNANCE__ENV')}}: {{env}}
GRANTS: 
- {{role('SOME_ROLE')}}: USAGE
```

Code file with .sql extension
```
BEGIN
  ALTER SESSION SET TIMESTAMP_OUTPUT_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF';
  SELECT CURRENT_TIMESTAMP;
END
```

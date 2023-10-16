# Object

Tables & Views
Snowflake Docs - [ALTER TABLE](https://docs.snowflake.com/en/sql-reference/sql/alter-table)

Snowflake Docs - [ALTER VIEW](https://docs.snowflake.com/en/sql-reference/sql/alter-view)

## Usage 
* Tables and views are grouped simply into "objects" as these can sometimes be interchangeable depending on the environment, or materialization.
* Currently only supported the meta data of an object, not the creation the object.
* The primary use case currently is for managing metadata such as tags and grants on objects created with other applications or via Snowflake procedures/scripts.
* All objects must live inside a [DATABASE]/[SCHEMA]/OBJECTS folder
* Object name = name of the yml config file within [DATABASE]/[SCHEMA]/OBJECTS folder

## Snowflake Attributes

| <div style="width:175px">Parameter</div>          | Description                          |
| ------------------------------------------------  | ------------------------------------ |
| `RETENTION_TIME_IN_DAYS`         | (Int) - Optional |
| `OBJECT_TYPE`         | (String) - Optional |
| `COMMENT`         | (String) - Optional |
| `OWNER`         | (String) - Optional <ul><li>If HANDLE_OWNERSHIP=ERROR, be careful not to set OWNER to a role that the deployer does not have access to as it will no longer have access to manage</li></ul>|
| `CHANGE_TRACKING`         | (Bool) - Optional |
| `ROW_ACCESS_POLICY`         | (dict) - Optional (see below for structure) |
| `COLUMNS`         | (COLUMN) - Optional |
| `TAGS`         | ({KEY:VALUE}) - Optional |
| `GRANTS`         | ({KEY:VALUE}) - Optional |


## ROW_ACCESS_POLICY

| <div style="width:175px">Parameter</div>          | Description                          |
| ------------------------------------------------  | ------------------------------------ |
| `NAME`         | (String) - Optional <ul><li>Name of ROW ACCESS POLICY - use jinja REF to ensure dependencies during deployment</li></ul>|
| `INPUT_COLUMNS`         | (LIST) - Optional <ul><li>List of input columns to row access policy as row access policy can access multiple columns as input</li></ul>|

Optional Parameter Defaults - if omitted, Snowflake defaults for parameters are used, just like creating an object manually.

## COLUMN

| <div style="width:175px">Parameter</div>          | Description                          |
| ------------------------------------------------  | ------------------------------------ |
| `NAME`         | (String) - Optional |
| `TAGS`         | ({KEY:VALUE}) - Optional |

Used within the list of Columns to tag specific columns

## Deployment attributes

| <div style="width:175px">Parameter</div>          | Description                          |
| ------------------------------------------------  | ------------------------------------ |
| `DEPLOY_ENV`         | (List) - Optional <ul><li>Default = []</li><li>List of the deployment environments to deploy to</li><li>Deployment environment set in the environment config yaml using the DEPLOY_ENV parameter.  See Setup/Config for docs.</li><li>When empty or not included, deployed to all environments</li></ul> |
| `DEPLOY_LOCK`         | (Bool) - Optional <ul><li>Default = False</li><li>Locks the config file to being over written by reverse engineer process.</li><li>Use if source code should always be source of truth and any changes pulled from database should be ignored</li></ul> |

## Folder Structure

  `snowflake/data/[database name]/[schema name]/OBJECTS/[object name].yml`

!!! note annotate "Example Structure"
    snowflake/data/MY_DATABASE1/HR/OBJECTS/PEOPLE.yml
    
    snowflake/data/MY_DATABASE1/HR/OBJECTS/DEPARTMENT.yml
    
    This specifies the metadata for 2 objects named "PEOPLE" and "DEPARTMENT" within the MY_DATABASE1.HR schema, each with their own yml config file based on the object name

## Samples

Basic
```
COMMENT: This is the comment telling what this is all about
OWNER: INSTANCEADMIN
DATA_RETENTION_TIME_IN_DAYS: 1
CHANGE_TRACKING: true
COLUMNS:
- name: ID
  tags:
  - {{ref('CONTROL__GOVERNANCE__SENSITIVITY')}}: INTERNAL
  - {{ref('CONTROL__GOVERNANCE__SEMANTIC')}}: IDENTIFIER
- name: FIRST_NAME
  tags:
  - {{ref('CONTROL__GOVERNANCE__SENSITIVITY')}}: CONFIDENTIAL
  - {{ref('CONTROL__GOVERNANCE__SEMANTIC')}}: NAME
TAGS:
- {{ref('CONTROL__GOVERNANCE__DOMAIN')}}: HR
GRANTS:
- {{role('SOME_ROLE')}}: SELECT, INSERT
```

With a deploy lock & restricted deployment environments.  
```
COMMENT: This is the comment telling what this is all about
OWNER: INSTANCEADMIN
DATA_RETENTION_TIME_IN_DAYS: 1
CHANGE_TRACKING: true
COLUMNS:
- NAME: ID
  TAGS:
  - {{ref('CONTROL__GOVERNANCE__SENSITIVITY')}}: INTERNAL
  - {{ref('CONTROL__GOVERNANCE__SEMANTIC')}}: IDENTIFIER
- NAME: FIRST_NAME
  TAGS:
  - {{ref('CONTROL__GOVERNANCE__SENSITIVITY')}}: CONFIDENTIAL
  - {{ref('CONTROL__GOVERNANCE__SEMANTIC')}}: NAME
TAGS:
- {{ref('CONTROL__GOVERNANCE__DOMAIN')}}: HR
GRANTS:
- {{role('SOME_ROLE')}}: SELECT, INSERT
DEPLOY_LOCK: true
DEPLOY_ENV:
- PROD
- TEST
```
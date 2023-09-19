# Row Access Policy

Snowflake Docs - [CREATE ROW ACCESS POLICY](https://docs.snowflake.com/en/sql-reference/sql/alter-table)

Snowflake Docs - [ALTER ROW ACCESS POLICY](https://docs.snowflake.com/en/sql-reference/sql/alter-view)

## Usage 
* A row access policy is made up of 2 parts
    * YAML Configuration
    * SQL code with the policy itself
* All row access policies must live inside a [DATABASE]/[SCHEMA]/ROW_ACCESS_POLICIES folder and contain both a .yml file and .sql file with the same name.
* Object name = name of the yml config file within [DATABASE]/[SCHEMA]/ROW_ACCESS_POLICIES folder

## Snowflake Attributes

| <div style="width:175px">Parameter</div>          | Description                          |
| ------------------------------------------------  | ------------------------------------ |
| `SIGNATURE`         | (List[{name: datatype}]) - Optional |
| `RETURN_TYPE`         | (String) - Optional |
| `EXEMPT_OTHER_POLICIES`         | (Bool) - Optional |
| `COMMENT`         | (String) - Optional |
| `OWNER`         | (String) - Optional <ul><li>If HANDLE_OWNERSHIP=ERROR, be careful not to set OWNER to a role that the deployer does not have access to as it will no longer have access to manage</li></ul>|
| `TAGS`         | ({KEY:VALUE}) - Optional |
| `GRANTS`         | ({KEY:VALUE}) - Optional |

Optional Parameter Defaults - if omitted, Snowflake defaults for parameters are used, just like creating an object manually.

## Deployment attributes

| <div style="width:175px">Parameter</div>          | Description                          |
| ------------------------------------------------  | ------------------------------------ |
| `DEPLOY_ENV`         | (List) - Optional <ul><li>Default = []</li><li>List of the deployment environments to deploy to</li><li>Deployment environment set in the environment config yaml using the DEPLOY_ENV parameter.  See Setup/Config for docs.</li><li>When empty or not included, deployed to all environments</li></ul> |
| `DEPLOY_LOCK`         | (Bool) - Optional <ul><li>Default = False</li><li>Locks the config file to being over written by reverse engineer process.</li><li>Use if source code should always be source of truth and any changes pulled from database should be ignored</li></ul> |

## Folder Structure

Configuration:
  `snowflake/data/[database name]/[schema name]/ROW_ACCESS_POLICIES/[policy name].yml`

Policy
  `snowflake/data/[database name]/[schema name]/ROW_ACCESS_POLICIES/[policy name].sql`
  

!!! note annotate "Example Structure"
    snowflake/data/CONTROL/GOVERNANCE/ROW_ACCESS_POLICIES/SALES_POLICY.yml
    
    snowflake/data/CONTROL/GOVERNANCE/ROW_ACCESS_POLICIES/SALES_POLICY.sql

    snowflake/data/CONTROL/GOVERNANCE/ROW_ACCESS_POLICIES/PEOPLE_POLICY.yml

    snowflake/data/CONTROL/GOVERNANCE/ROW_ACCESS_POLICIES/PEOPLE_POLICY.sql
    
    This specifies the metadata for 2 row access policies named "SALES_POLICY" and "PEOPLE_POLICY" within the CONTROL.GOVERNANCE schema, each with their own yml config file & sql based on the policy name

## Samples

Basic
```
SIGNATURE:
- VAR1: VARCHAR
- VAR2: INT
RETURN_TYPE: VARCHAR
EXEMPT_OTHER_POLICIES: false
OWNER: INSTANCEADMIN
COMMENT: Row access policy associated for sales records based on department
TAGS: 
- {{ref('CONTROL__GOVERNANCE__ENV')}}: {{env}}
GRANTS: 
- {{role('SOME_ROLE')}}: USAGE
```

With a deploy lock & restricted deployment environments.  
```
SIGNATURE:
- VAR1: VARCHAR
- VAR2: INT
RETURN_TYPE: VARCHAR
EXEMPT_OTHER_POLICIES: false
OWNER: INSTANCEADMIN
COMMENT: Row access policy associated for sales records based on department
TAGS: 
- {{ref('CONTROL__GOVERNANCE__ENV')}}: {{env}}
GRANTS: 
- {{role('SOME_ROLE')}}: USAGE
DEPLOY_LOCK: true
DEPLOY_ENV:
- PROD
- TEST
```

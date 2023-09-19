# Masking Policy

Snowflake Docs - [CREATE MASKING POLICY](https://docs.snowflake.com/en/sql-reference/sql/alter-table)

Snowflake Docs - [ALTER MASKING POLICY](https://docs.snowflake.com/en/sql-reference/sql/alter-view)

## Usage 
* A masking policy is made up of 2 parts
    * YAML Configuration
    * SQL code with the policy itself
* All masking policies must live inside a [DATABASE]/[SCHEMA]/MASKING_POLICIES folder and contain both a .yml file and .sql file with the same name.
* Object name = name of the yml config file within [DATABASE]/[SCHEMA]/MASKING_POLICIES folder

## Snowflake Attributes

| <div style="width:175px">Parameter</div>          | Description                          |
| ------------------------------------------------  | ------------------------------------ |
| `SIGNATURE`         | (List[{name: datatype}]) - Optional |
| `RETURN_TYPE`         | (String) - Optional |
| `EXEMPT_OTHER_POLICIES`         | (Bool) - Optional <ul><li>default = FALSE</li></ul> |
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
  `snowflake/data/[database name]/[schema name]/MASKING_POLICIES/[policy name].yml`

Policy
  `snowflake/data/[database name]/[schema name]/MASKING_POLICIES/[policy name].sql`
  

!!! note annotate "Example Structure"
    snowflake/data/CONTROL/GOVERNANCE/MASKING_POLICIES/SENSITIVITY_STRING.yml
    
    snowflake/data/CONTROL/GOVERNANCE/MASKING_POLICIES/SENSITIVITY_STRING.sql

    snowflake/data/CONTROL/GOVERNANCE/MASKING_POLICIES/SENSITIVITY_ARRAY.yml

    snowflake/data/CONTROL/GOVERNANCE/MASKING_POLICIES/SENSITIVITY_ARRAY.sql
    
    This specifies the metadata for 2 masking policies named "SENSITIVITY_STRING" and "SENSITIVITY_ARRAY" within the CONTROL.GOVERNANCE schema, each with their own yml config file & sql based on the policy name

## Samples

Basic
```
SIGNATURE:
- VAR1: VARCHAR
- VAR2: INT
RETURN_TYPE: VARCHAR
EXEMPT_OTHER_POLICIES: false
OWNER: INSTANCEADMIN
COMMENT: Masking policy associated with the sensitivity tag
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
COMMENT: Masking policy associated with the sensitivity tag
TAGS: 
- {{ref('CONTROL__GOVERNANCE__ENV')}}: {{env}}
GRANTS: 
- {{role('SOME_ROLE')}}: USAGE
DEPLOY_LOCK: true
DEPLOY_ENV:
- PROD
- TEST
```

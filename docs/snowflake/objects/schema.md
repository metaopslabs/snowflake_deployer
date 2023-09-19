# Schema

Snowflake Docs - [CREATE SCHEMA](https://docs.snowflake.com/en/sql-reference/sql/create-schema)

Snowflake Docs - [ALTER SCHEMA](https://docs.snowflake.com/en/sql-reference/sql/alter-schema)

## Usage 
* Each folder within a Database folder represents a schema
* Schema name = folder name of schema
* Config file in "schema.yml" within schema name folder

## Snowflake Attributes

| <div style="width:175px">Parameter</div>          | Description                          |
| ------------------------------------------------  | ------------------------------------ |
| `DATA_RETENTION_TIME_IN_DAYS`         | (Int) - Optional |
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

  `snowflake/data/[database name]/[schema name]/schema.yml`

!!! note annotate "Example Structure"
    snowflake/data/MY_DATABASE1/HR/schema.yml
    
    snowflake/data/MY_DATABASE1/ACCOUNTING/schema.yml
    
    This creates 2 schemas named "HR" and "ACCOUNT" within database "MY_DATABASE1", each with their own schema.yml file within their respected folder

## Samples

Basic
```
COMMENT: This is the comment on a schema
OWNER: INSTANCEADMIN
DATA_RETENTION_TIME_IN_DAYS: 1
TAGS:
- {{ref('CONTROL__GOVERNANCE__ENV')}}: PROD
- {{ref('CONTROL__GOVERNANCE__ZONE')}}: ANALYTICS
GRANTS:
- {{role('SOME_ROLE')}}: USAGE
```

With a deploy lock & restricted deployment environments.  
```
COMMENT: {{var_from_env_config}}
OWNER: INSTANCEADMIN
TAGS:
- {{ref('CONTROL__GOVERNANCE__ENV')}}: PROD
- {{ref('CONTROL__GOVERNANCE__ZONE')}}: ANALYTICS
GRANTS:
- {{role('SOME_ROLE')}}: USAGE
DEPLOY_LOCK: true
DEPLOY_ENV:
- PROD
- TEST
```
# Procedure

Snowflake Docs - [CREATE PROCEDURE](https://docs.snowflake.com/en/sql-reference/sql/alter-procedure)

Snowflake Docs - [ALTER PROCEDURE](https://docs.snowflake.com/en/sql-reference/sql/alter-procedure)

## Usage 
* A Procedure is made up of 2 parts
    * YAML Configuration
    * Code with the policy itself (see next sections for supported languages and associated file extensiosn)
* All masking policies must live inside a [DATABASE]/[SCHEMA]/PROCEDURES folder and contain both a .yml file and code file with the same name.
* Object name = name of the yml config file within [DATABASE]/[SCHEMA]/PROCEDURES folder
* In Snowflake, multiple procedures can share the same name with different signatures.  Therefore, the signature with associated data types (no input names, just data types) must be include in the file name to make the file unique.  See example sections below.

## Supported Languages
| <div style="width:175px">Language</div>          | File Extension                          |
| ------------------------------------------------  | ------------------------------------ |
| `SQL`         | .sql |
| `JAVASCRIPT`         | .js |
| `PYTHON`         | .py |

## Snowflake Attributes

| <div style="width:175px">Parameter</div>          | Description                          |
| ------------------------------------------------  | ------------------------------------ |
| `INPUT_ARGS`         | (List[{name: datatype}]) - Optional |
| `IS_SECURE`         | (Bool) - Optional |
| `RETURNS`         | (String) - Optional |
| `LANGUAGE`         | (String) - Optional <ul><li>Valid Values = [SQL,JAVASCRIPT,PYTHON]</li></ul> |
| `NULL_HANDLING`         | (String) - Optional  <ul><li>Valid Values = [CALLED ON NULL INPUT, RETURNS NULL ON NULL INPUT, STRICT]</li></ul> |
| `EXECUTE_AS`         | (String) - Optional |
| `COMMENT`         | (String) - Optional |
| `OWNER`         | (String) - Optional <ul><li>If HANDLE_OWNERSHIP=ERROR, be careful not to set OWNER to a role that the deployer does not have access to as it will no longer have access to manage</li></ul>|
| `TAGS`         | ({KEY:VALUE}) - Optional |
| `GRANTS`         | ({KEY:VALUE}) - Optional |

Python Only 

| `IMPORTS`         | (List[String]) - Optional |
| `HANDLER`         | (String) - Optional |
| `RUNTIME_VERSION`         | (String) - Optional |
| `PACKAGES`         | (List[String]) - Optional |

Optional Parameter Defaults - if omitted, Snowflake defaults for parameters are used, just like creating an object manually.

## Deployment attributes

| <div style="width:175px">Parameter</div>          | Description                          |
| ------------------------------------------------  | ------------------------------------ |
| `DEPLOY_ENV`         | (List) - Optional <ul><li>Default = []</li><li>List of the deployment environments to deploy to</li><li>Deployment environment set in the environment config yaml using the DEPLOY_ENV parameter.  See Setup/Config for docs.</li><li>When empty or not included, deployed to all environments</li></ul> |
| `DEPLOY_LOCK`         | (Bool) - Optional <ul><li>Default = False</li><li>Locks the config file to being over written by reverse engineer process.</li><li>Use if source code should always be source of truth and any changes pulled from database should be ignored</li></ul> |

## Folder Structure

Configuration:
  `snowflake/data/[database name]/[schema name]/PROCEDURES/[procedure name].yml`

Code
  `snowflake/data/[database name]/[schema name]/PROCEDURES/[procedure name].[extension]`
  

!!! note annotate "Example Structure"
    snowflake/data/CONTROL/CODE/PROCEDURES/GET_FISCAL_YEARS().yml
    
    snowflake/data/CONTROL/CODE/PROCEDURES/GET_FISCAL_YEARS.sql

    snowflake/data/CONTROL/CODE/PROCEDURES/PY_PI(varchar,int).yml

    snowflake/data/CONTROL/CODE/PROCEDURES/PY_PI(varchar,int).py
    
    This specifies the metadata for a sql procedure named "GET_FISCAL_YEARS" with an empty signature and a python procedure "PY_PI" with a signature of (varchar,int).  Both within the CONTROL.CODE schema, each with their own yml config file & code based on the procedure name.

## Samples

Config
```
INPUT_ARGS:
- TABLENAME: VARCHAR
- ROLE: VARCHAR
RETURNS: TABLE (ID NUMBER, NAME VARCHAR, ROLE VARCHAR)
LANGUAGE: PYTHON
EXECUTE_AS: OWNER
OWNER: INSTANCEADMIN
COMMENT: 
IS_SECURE: false
IMPORTS: 
HANDLER: filter_by_role
RUNTIME_VERSION: 3.8
PACKAGES: 
- snowflake-snowpark-python
TAGS: 
- {{ref('CONTROL__GOVERNANCE__ENV')}}: {{env}}
GRANTS: 
- {{role('SOME_ROLE')}}: USAGE
```

Code file (.py in this example)
```          
from snowflake.snowpark.functions import col

def filter_by_role(session, table_name, role):
   df = session.table(table_name)
   return df.filter(col("role") == role)  
```

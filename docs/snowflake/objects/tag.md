# Tag

Tables & Views
Snowflake Docs - [CREATE TAG](https://docs.snowflake.com/en/sql-reference/sql/create-tag)

Snowflake Docs - [ALTER TAG](https://docs.snowflake.com/en/sql-reference/sql/alter-tag)

## Usage 
* Used to create and manage tags within a schema
* All objects must live inside a [DATABASE]/[SCHEMA]/TAGS folder
* Tag name = name of the yml config file within [DATABASE]/[SCHEMA]/TAGS folder

## Snowflake Attributes

| <div style="width:175px">Parameter</div>          | Description                          |
| ------------------------------------------------  | ------------------------------------ |
| `COMMENT`         | (String) - Optional |
| `OWNER`         | (String) - Optional <ul><li>If HANDLE_OWNERSHIP=ERROR, be careful not to set OWNER to a role that the deployer does not have access to as it will no longer have access to manage</li></ul>|
| `ALLOWED_VALUES`         | (List[string]) - Optional |
| `MASKING_POLICIES`         | (List[string]) - Optional |
| `GRANTS`         | ({KEY:VALUE}) - Optional |



Optional Parameter Defaults - if omitted, Snowflake defaults for parameters are used, just like creating an object manually.

## Deployment attributes

| <div style="width:175px">Parameter</div>          | Description                          |
| ------------------------------------------------  | ------------------------------------ |
| `DEPLOY_ENV`         | (List) - Optional <ul><li>Default = []</li><li>List of the deployment environments to deploy to</li><li>Deployment environment set in the environment config yaml using the DEPLOY_ENV parameter.  See Setup/Config for docs.</li><li>When empty or not included, deployed to all environments</li></ul> |
| `DEPLOY_LOCK`         | (Bool) - Optional <ul><li>Default = False</li><li>Locks the config file to being over written by reverse engineer process.</li><li>Use if source code should always be source of truth and any changes pulled from database should be ignored</li></ul> |

## Folder Structure

  `snowflake/data/[database name]/[schema name]/TAGS/[tag name].yml`

!!! note annotate "Example Structure"
    snowflake/data/CONTROL/GOVERNANACE/TAGS/SENSITIVITY.yml
    
    snowflake/data/CONTROL/GOVERNANACE/TAGS/SEMANTIC.yml
    
    This specifies the metadata for 2 tags named "SENSITIVITY" and "SEMANTIC" within the CONTROL.GOVERNANCE schema, each with their own yml config file based on the tag name

## Samples

Basic
```
COMMENT: This is the comment telling what this is all about
OWNER: INSTANCEADMIN
ALLOWED_VALUES:
- NEW
- PUBLIC
- INTERNAL
- CONFIDENTIAL
- RESTRICTED
MASKING_POLICIES:
- {{ref('CONTROL__GOVERNANCE__SEMANTIC')}}
```

With a deploy lock & restricted deployment environments.  
```
COMMENT: This is the comment telling what this is all about
OWNER: INSTANCEADMIN
ALLOWED_VALUES:
- NEW
- PUBLIC
- INTERNAL
- CONFIDENTIAL
- RESTRICTED
MASKING_POLICIES:
- {{ref('CONTROL__GOVERNANCE__SEMANTIC')}}
DEPLOY_LOCK: true
DEPLOY_ENV:
- PROD
- TEST
```

## Reference in other config

Other objects may need to reference this object and can do so using jinja references.

Reference Structure: 
{{ref('[database name]__[schema name]__[tag name]')}}

Example - reference the tag named SENSITIVITY in the CONTROL.GOVERNANCE schema:
```
TAGS:
- {{ref('CONTROL__GOVERNANCE__SENSITIVITY')}}: HR
```
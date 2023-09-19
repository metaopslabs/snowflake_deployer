# Warehouse

Snowflake Docs - [CREATE WAREHOUSE](https://docs.snowflake.com/en/sql-reference/sql/create-warehouse)

Snowflake Docs - [ALTER WAREHOUSE](https://docs.snowflake.com/en/sql-reference/sql/alter-warehouse)

## Usage 
* Warehouse name = file name of warehouse yml config

## Environment Config
* Use the ENV_WAREHOUSE_PREFIX in the environment config file to specify a prefix for ALL warehouses within an environment.
* If the warehouse filename is INGEST_WH.yml and the ENV_WAREHOUSE_PREFIX is "PROD_", the warehouse name will compile to "PROD_INGEST_WH"
* See Setup/Config for additional details & examples

## Snowflake Attributes

| <div style="width:175px">Parameter</div>          | Description                          |
| ------------------------------------------------  | ------------------------------------ |
| `WAREHOUSE_TYPE`         | (String) - Optional <ul><li>Valid Values = [STANDARD, SNOWPARK-OPTIMIZED]</li></ul>|
| `WAREHOUSE_SIZE`         | (String) - Optional <ul><li>Valid Values = [XSMALL, SMALL, MEDIUM, LARGE, XLARGE, XXLARGE, XXXLARGE, X4LARGE, X5LARGE, X6LARGE]</li></ul>|
| `MIN_CLUSTER_COUNT`         | (Int) - Optional |
| `MAX_CLUSTER_COUNT`         | (Int) - Optional |
| `SCALING_POLICY`         | (String) - Optional <ul><li>Valid Values = [STANDARD, ECONOMY]</li></ul>|
| `AUTO_SUSPEND`         | (Int) - Optional |
| `QUERY_ACCELERATION_MAX_SCALE_FACTOR`         | (Int) - Optional |
| `AUTO_RESUME`         | (Bool) - Optional |
| `ENABLE_QUERY_ACCELERATION`         | (Bool) - Optional |
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

  `snowflake/instance/warehouses/[warehouse name].yml`

!!! note annotate "Example Structure"
    snowflake/instance/warehouses/INGEST_WH.yml
    
    snowflake/instance/warehouses/AD_HOC_WH.yml
    
    This creates 2 warehouses named "INGEST_WH" and "AD_HOC_WH" each with their own yml file.

## Samples

Basic
```
WAREHOUSE_TYPE: STANDARD
WAREHOUSE_SIZE: XSMALL
MIN_CLUSTER_COUNT: 1
MAX_CLUSTER_COUNT: 1
SCALING_POLICY: ECONOMY
AUTO_SUSPEND: 10
AUTO_RESUME: true
OWNER: INSTANCEADMIN
COMMENT: Test compute resources
ENABLE_QUERY_ACCELERATION: false
QUERY_ACCELERATION_MAX_SCALE_FACTOR: 8
TAGS:
- {{ref('CONTROL__GOVERNANCE__ENV')}}: PROD
GRANTS:
- {{role('SOME_ROLE')}}: USAGE
```

With a deploy lock & restricted deployment environments.  
```
WAREHOUSE_TYPE: STANDARD
WAREHOUSE_SIZE: XSMALL
MIN_CLUSTER_COUNT: 1
MAX_CLUSTER_COUNT: 1
SCALING_POLICY: ECONOMY
AUTO_SUSPEND: 10
AUTO_RESUME: true
OWNER: INSTANCEADMIN
COMMENT: Test compute resources
ENABLE_QUERY_ACCELERATION: false
QUERY_ACCELERATION_MAX_SCALE_FACTOR: 8
TAGS:
- {{ref('CONTROL__GOVERNANCE__ENV')}}: PROD
GRANTS:
- {{role('SOME_ROLE')}}: USAGE
DEPLOY_LOCK: true
DEPLOY_ENV:
- PROD
- TEST
```

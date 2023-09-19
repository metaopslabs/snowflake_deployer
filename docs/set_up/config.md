# Configuration

## Environment Configuration Overview
Once installed, additional environment configuration can be set up using environment specific yaml files.

In the base folder of the database config (base working directory), create a yml file for each environment.

For example:

deploy_config_dev.yml
deploy_config_prod.yml

## Referencing a Config File

There are 2 ways to tell MetaOps Deployer which config file to use during execution.

Option 1 - Command Line Parameter

Use the -c parameter when calling
```
snowflake-deployer deploy -c "deploy_config_dev.yml"
```

Option 2 - Environment Var

Use the environment variable DEPLOY_CONFIG_PATH.

```
export DEPLOY_CONFIG_PATH="deploy_config_dev.yml"
```

Usage - If both the command line parameter AND environment variable are set, execution will use the command line parameter.

## Supported Config Parameters

| <div style="width:175px">Parameter</div>          | Description                          |
| ------------------------------------------------  | ------------------------------------ |
| `ENV_DATABASE_PREFIX`         | (String) Database Prefix within environment <ul><li>Default = ""</li><li>Valid Values = ["A","B"]</li></ul> |
| `ENV_WAREHOUSE_PREFIX`        | (String) Warehoue Prefix within environment <ul><li>Default = ""</li><li>Valid Values = ["A","B"]</li></ul> |
| `ENV_ROLE_PREFIX`             | (String) Role Prefix within environment <ul><li>Default = ""</li><li>Valid Values = ["A","B"]</li></ul> |
| `ENV_PROCEDURE_PREFIX`        | (String) Procedure Prefix within environment <ul><li>Default = ""</li><li>Valid Values = ["A","B"]</li></ul> |
| `ENV_FUNCTION_PREFIX`         | (String) Function Prefix within environment <ul><li>Default = ""</li><li>Valid Values = ["A","B"]</li></ul> |
| `OBJECT_METADATA_ONLY`        | (Boolean) Flag to support the creation of Tables & Views or only the metadata. <ul><li>Currently deployer does not support creation of the tables and views, only the metadata, tags & grants on an object</li><li>Default = True</li></ul> |
| `MAX_THREADS`                 | (Int) Number of threads the deployer will process in parrellel during deployment.  Balance Snowflake warehouse load with python execution environment. <ul><li>Default = 3</li></ul>|
| `DEPLOY_ENV`                  | (String) Name of the current environment.<ul><li>Used in conjunction with the DEPLOY_ENV list on an object.</li><li>If an object should only be deployed to certain environments, set the current environment name here, and then list the environments to deploy to within the DEPLOY_ENV config on each object.</li><li>Default = None</li></ul> |
| `VARS`                        | List({key:value}) A list of key value pairs of variables within an environment.<ul>Vars can be referenced as Jinja vars in any object config and will take precedence over any values returned from the reverse engineering process.</li><li>Default = None</li></ul> |
| `HANDLE_OWNERSHIP`            | (String) How to handle the ownership of existing objects.<ul><li>For deployments in existing environments, the deployer can manage existing options.  But the DEPLOY_ROLE may not have ownership of the objects to manage. This config tells the deployer how to handle that scenario.</li><li>Default = ERROR</li><li>Valid Values = [ERROR,GRANT]</li><li>GRANT = Grant ownership role of object to DEPLOY_ROLE so the DEPLOY_ROLE inherits ownership capabilities.  Be careful of any objects that are object by ACCOUNTADMIN as this tells the deployer to make DEPLOY_ROLE the parent role to ACCOUNTADMIN</li><li>ERROR = Deployer will error out if it does not have ownership privilege on objects it's managing.  These errors will need to be fixed manually by granting ownership to a role that the DEPLOY role is a parent role to.</li></ul> |
| `DEPLOY_DATABASE_NAME`        | (String) Name of the MetaOps Deploy Database.<ul><li>Only needing configuration if modified database in the Snowflake set up script.  Else exclude.</li><li>For multiple environments within a single instance, environments can reference the same deploy db</li><li>Default = "_DEPLOY"</li></ul> |
| `DEPLOY_ROLE`                 | (String) Name of the MetaOps Deploy Role.<ul><li>Only needing configuration if modified fole in the Snowflake set up script.  Else exclude.</li><li>For multiple environments within a single instance, environments can use the same role</li><li>Default = "INSTANCEADMIN"</li></ul>|

## Example config

deploy_config_dev.yml
```
ENV_DATABASE_PREFIX: DEV_
ENV_WAREHOUSE_PREFIX: 
ENV_ROLE_PREFIX: 
ENV_PROCEDURE_PREFIX: 
ENV_FUNCTION_PREFIX: 
OBJECT_METADATA_ONLY: True
MAX_THREADS: 5
HANDLE_OWNERSHIP: ERROR
DEPLOY_ENV: dev
VARS:
- my_comment: some dev comment
- another_var: some other var in dev
```
# Snowflake Deployer

DataOps python framework for managing Snowflake environment. 

All code stored in source control & deployed directly to Snowflake.  

## Reason for this project

There's 2 primary automated deployment methods for data warehouses.  Terraform & Migration based tools (schemachange, flyway, etc).

#### Why Terraform is not ideal

Terraform is fantastic for slowly changing infastructure projects like aws cloud infrastructure deployments that have a single location for managing changes.  Data warehouse changes have a much higher number of changes and often need to come from different applications.  Some objects are managed by the replication tool, others by the transformation tool and others by the meta data management tool.  Terraform simply wasn't meant to manage a complex environment like this.  Given the "state" is stored in a seperate state file, state drift becomes a real problem with data warehousing and troubleshooting state drift is an extremely time consuming task.

#### Why Migration tools are not ideal

Because of the issues with Terraform, most companies turn to migration based tools.  The problem here is scale as every statement needs to be written out in SQL, and every update needs an ALTER statement.  This quickly becomes impossible to determine the state of any object at any one time.  Some work arounds can be done with using CREATE or REPLACE statements, but this only goes so far as constanly replacing objects leads to issues with governance policies & tags, time travel, and dependencies. 

#### Best of both worlds

The snowflake-deployer uses the best of worlds.  A yml state based config files for each object with the flexibility that migration based tools give.  


## CREATES and ALTERS

The snowflake-deployer converts the yml config into CREATE or ALTER statements based on current objects within the database.

## File Hash & Object Hash

File hashes and object hashes are both store and calculated at run time.  So if either a file changed or an object changed from another application (ie. FiveTran loading a table and adding a column or a transformation removing tags), the deployer will detect that the object needs to be updated.  This also allows the deployment to ignore objects that match the config file to prevent every object to be deployed on every run.

## Deploy & Import

The Snowflake Deployer includes both a "deployer" for pushing yaml config to the database. As well as an "import" process for reverse engineering an existing database to config files.

## Deployment Tags

Tags can specify objects only be deployed for certain environments.

Within each object config, add the following code (list of environments to deploy to):
```
DEPLOY_ENV:
- dev
```

Within each environment config file, add the following code (configured environment name):
```
DEPLOY_ENV: dev
```

## Jinja Variables

Jinja variables can be used throughout the config files for parametization and cross file depency references.

#### Parametization

Any value in the config files can use a jinja variable for parametization by environment. 

Example:

Object yaml - The "COMMENT" config references the "my_comment" variable.
```
COMMENT: {{my_comment}}
```

Config - the "deploy_config_dev.yml" environment config file stores the value of the my_comment value.
```
VARS:
- my_comment: some dev comment
```

NOTE: The import process will not bring in variables (no way to reverse engineer a variable reference).  However, the import process will ignore any values that already have a variable reference.  

#### References

ref - Object reference based on the naming convention of {db}__{schema}__{object_name}

role - Specific role reference based on the naming convention of {role}

Example
```
TAGS:
- {{ref('CONTROL__GOVERNANCE__ENV')}}: {{env}}
GRANTS:
- {{role('PROCESSING')}}: APPLY
```

NOTE: The import process will bring in jinja ref and role references.

## Parallelization
Snowflake Deployer uses the jinja ref's to determine dependencies and creates a deployment parrallelization path.  The MAX_THREADS parameter in the environment config file controls how many active threads can be running at once.

## Commands

Deployment - deploy config files to Snowflake based on configuration in config file
```
snowflake-deploy deploy -c deploy_config_dev.yml
```

Import - Reverse engineer existing Snowflake account into yml config files
```
snowflake-deploy deploy -c deploy_config_dev.yml
```

Keys - create Public/Private RSA Tokens for authentication
```
snowflake-deploy keys -p Th1sI$@Pa$$w0d
```

## Sample Project

See sample project for an example structure.

https://github.com/metaopslabs/snowflake_deploy_example/tree/main

# Initial Install

## Python Module Install 

Install python module locally:
```
python -m pip install snowflake-deployer
```

## Create RSA Tokens

MetaOps Deploy comes with a RSA Token generater which uses an environment variable to encrypt.

1. Create a random generated password
2. Create RSA private & public keys

```
snowflake-deployer keys -p {password key}
```

3. Save keys from output to a vault or secure location!

## Snowflake 

1. Update the RSA_PUBLIC_KEY in the below script with the PUBLIC KEY from the previous step.  Make sure to NOT include the "-----BEGIN PUBLIC KEY-----" or "-----END PUBLIC KEY-----" in the Snowflake RSA_PUBLIC_KEY value.

```
USE ROLE ACCOUNTADMIN;
 
--owned by ACCOUNTADMIN to greatly limit who can alter; should be an orphan role to not automatically give admins access to the objects it creates
CREATE ROLE IF NOT EXISTS INSTANCEADMIN; 

CREATE WAREHOUSE IF NOT EXISTS DEPLOY_WH WITH WAREHOUSE_SIZE = 'XSMALL' WAREHOUSE_TYPE = 'STANDARD' AUTO_SUSPEND = 10 AUTO_RESUME = TRUE MIN_CLUSTER_COUNT = 1 MAX_CLUSTER_COUNT = 1 SCALING_POLICY = 'ECONOMY' COMMENT = 'Compute for deployment objects with MetaOps Deploy';
GRANT USAGE ON WAREHOUSE DEPLOY_WH TO ROLE INSTANCEADMIN; 
GRANT OWNERSHIP ON WAREHOUSE DEPLOY_WH TO ROLE INSTANCEADMIN COPY CURRENT GRANTS;

CREATE USER IF NOT EXISTS SERVICE_DEPLOY default_role = INSTANCEADMIN default_warehouse=DEPLOY_WH must_change_password = false;
GRANT ROLE INSTANCEADMIN TO USER SERVICE_DEPLOY;
ALTER USER SERVICE_DEPLOY SET RSA_PUBLIC_KEY='<update me>';

GRANT MANAGE GRANTS ON ACCOUNT TO ROLE INSTANCEADMIN;
GRANT CREATE DATABASE ON ACCOUNT TO ROLE INSTANCEADMIN;
GRANT CREATE USER ON ACCOUNT TO ROLE INSTANCEADMIN;
GRANT CREATE ROLE ON ACCOUNT TO ROLE INSTANCEADMIN;
GRANT CREATE WAREHOUSE ON ACCOUNT TO ROLE INSTANCEADMIN;
GRANT APPLY MASKING POLICY ON ACCOUNT TO ROLE INSTANCEADMIN;
GRANT EXECUTE MANAGED TASK ON ACCOUNT TO ROLE INSTANCEADMIN;
GRANT EXECUTE TASK ON ACCOUNT TO ROLE INSTANCEADMIN;
```

## Environment Variables

Store the follow environment variables.  

- SNOWFLAKE_ACCOUNT
    * Snowflake account - Only include the [account identifier].[region].[cloud provider]
    * example: wf79437.us-central1.gcp
- SNOWFLAKE_USERNAME
    * Service account of the deployment user in Snowflake.  Below is the default from the Snowflake set up script.  This can be updated in the script to fit the naming convention of the environment.
    * default: SERVICE_DEPLOY
- SNOWFLAKE_WAREHOUSE
    * Snowflake warehoue used to execute deployments (for statements requiring an active warehouse).  Below is the default from the Snowflake set up script. This can be updated in the script to fit the naming convention of the environment.
    * default: DEPLOY_WH
- SNOWFLAKE_PRIVATE_KEY_PASSWORD
    * The private key password described in the beginning of this section used to create the private key.  This is the same password randomly generated in created the RSA tokens.
- SNOWFLAKE_PRIVATE_KEY
    * The private key.  This should include the "-----BEGIN ENCRYPTED PRIVATE KEY-----" and "-----END ENCRYPTED PRIVATE KEY-----" within the private key.

## Multiple Environments

To set up multiple environments, simply repeat these steps and store the values within your vault.  Then set up multiple environments within GitHub with seperate environment variables per github environment (or via secrets with an environment prefix).
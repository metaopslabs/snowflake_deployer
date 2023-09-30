# Github Action - Deploy

## Github Action - Without Environment Config
Sample GitHub Action that uses action secrets with the branch name as the prefix to the secret name.

-----------------------------------------------------------------
#### Example Secrets

### main
* MAIN_CONFIG_FILENAME
* MAIN_SNOWFLAKE_USERNAME
* MAIN_SNOWFLAKE_ACCOUNT
* MAIN_SNOWFLAKE_WAREHOUSE
* MAIN_SNOWFLAKE_ROLE
* MAIN_SNOWFLAKE_PRIVATE_KEY
* MAIN_SNOWFLAKE_PRIVATE_KEY_PASSWORD
### dev
* DEV_CONFIG_FILENAME
* DEV_SNOWFLAKE_USERNAME
* DEV_SNOWFLAKE_ACCOUNT
* DEV_SNOWFLAKE_WAREHOUSE
* DEV_SNOWFLAKE_ROLE
* DEV_SNOWFLAKE_PRIVATE_KEY
* DEV_SNOWFLAKE_PRIVATE_KEY_PASSWORD

```
name: deploy-snowflake-example

on:
  push:
    branches:
      - main
      - dev
    paths:
      - 'snowflake/**'
  workflow_dispatch:

jobs:
  # Get the branch name from the branch this is being executed against
  # This is used to set the environment parameter in the main job to know which 
  # Alternatively this can be used as a prefix for repo's that don't utile environments but rather use prefixes on action secrets
  set_env:
    runs-on: ubuntu-latest
    steps:
      - name: Get Branch Name
        id: branch_name
        run: |
          echo "Running on branch ${{github.ref}}"
          echo "::set-output name=branch_env::${GITHUB_REF#refs/heads/}"
    outputs:
      env_name: ${{steps.branch_name.outputs.branch_env}}

  deploy-snowflake:
    needs: [set_env] # orchestration dependencies set_env job to execute first
    runs-on: ubuntu-latest
    #environment: ${{needs.set_env.outputs.env_name}}  # For enterprise accounts utilizing secrets environments
    env:
      ENVIRONMENT_PREFIX: ${{needs.set_env.outputs.env_name}}
      
    steps:
      - name: Checkout Repo
        uses: actions/checkout@v2

      - name: Setup Python 3.10.x
        uses: actions/setup-python@v2.2.1
        with:
          python-version: 3.10.x

      - name: run snowflake-deployer
        env:
          CONFIG_FILENAME: ${{secrets[format('{0}_CONFIG_FILENAME', env.ENVIRONMENT_PREFIX)]}}
          SNOWFLAKE_USERNAME: ${{secrets[format('{0}_SNOWFLAKE_USERNAME', env.ENVIRONMENT_PREFIX)]}}
          SNOWFLAKE_ACCOUNT: ${{secrets[format('{0}_SNOWFLAKE_ACCOUNT', env.ENVIRONMENT_PREFIX)]}}
          SNOWFLAKE_WAREHOUSE: ${{secrets[format('{0}_SNOWFLAKE_WAREHOUSE', env.ENVIRONMENT_PREFIX)]}}
          SNOWFLAKE_ROLE: ${{secrets[format('{0}_SNOWFLAKE_ROLE', env.ENVIRONMENT_PREFIX)]}}
          SNOWFLAKE_PRIVATE_KEY: ${{secrets[format('{0}_SNOWFLAKE_PRIVATE_KEY', env.ENVIRONMENT_PREFIX)]}}
          SNOWFLAKE_PRIVATE_KEY_PASSWORD: ${{secrets[format('{0}_SNOWFLAKE_PRIVATE_KEY_PASSWORD', env.ENVIRONMENT_PREFIX)]}}

        run: |
          echo "GITHUB_WORKSPACE: $GITHUB_WORKSPACE"
          python --version
          echo "Installing snowflake-deployer"
          pip install snowflake-deployer
          
          echo "Using Config File:"
          echo $ENVIRONMENT_PREFIX
          echo $CONFIG_FILENAME
          
          echo "Running snowflake-deployer"
          snowflake-deployer deploy -c $CONFIG_FILENAME
        
```

----------------------------------------------------
## Github Action - With Environment Config

Sample GitHub Action that uses environments with the name of the environment as the branch name.  Each environment contains the following secrets.

----------------------------------------------------
#### Secrets
* CONFIG_FILENAME
* SNOWFLAKE_USERNAME
* SNOWFLAKE_ACCOUNT
* SNOWFLAKE_WAREHOUSE
* SNOWFLAKE_ROLE
* SNOWFLAKE_PRIVATE_KEY
* SNOWFLAKE_PRIVATE_KEY_PASSWORD

```
name: deploy-snowflake-example

on:
  push:
    branches:
      - main
      - dev
    paths:
      - 'snowflake/**'
  workflow_dispatch:

jobs:
  # Get the branch name from the branch this is being executed against
  # This is used to set the environment parameter in the main job to know which 
  # Alternatively this can be used as a prefix for repo's that don't utile environments but rather use prefixes on action secrets
  set_env:
    runs-on: ubuntu-latest
    steps:
      - name: Get Branch Name
        id: branch_name
        run: |
          echo "Running on branch ${{github.ref}}"
          echo "::set-output name=branch_env::${GITHUB_REF#refs/heads/}"
    outputs:
      env_name: ${{steps.branch_name.outputs.branch_env}}

  deploy-snowflake:
    needs: [set_env] # orchestration dependencies set_env job to execute first
    runs-on: ubuntu-latest
    environment: ${{needs.set_env.outputs.env_name}}  

    steps:
      - name: Checkout Repo
        uses: actions/checkout@v2

      - name: Setup Python 3.10.x
        uses: actions/setup-python@v2.2.1
        with:
          python-version: 3.10.x

      - name: run snowflake-deployer
        env:
          CONFIG_FILENAME: ${{secrets.CONFIG_FILENAME}}
          SNOWFLAKE_USERNAME: ${{secrets.SNOWFLAKE_USERNAME}}
          SNOWFLAKE_ACCOUNT: ${{secrets.SNOWFLAKE_ACCOUNT}}
          SNOWFLAKE_WAREHOUSE: ${{secrets.SNOWFLAKE_WAREHOUSE}}
          SNOWFLAKE_ROLE: ${{secrets.SNOWFLAKE_ROLE}}
          SNOWFLAKE_PRIVATE_KEY: ${{secrets.SNOWFLAKE_PRIVATE_KEY}}
          SNOWFLAKE_PRIVATE_KEY_PASSWORD: ${{secrets.SNOWFLAKE_PRIVATE_KEY_PASSWORD}}

        run: |
          echo "GITHUB_WORKSPACE: $GITHUB_WORKSPACE"
          python --version
          echo "Installing snowflake-deployer"
          pip install snowflake-deployer
          
          echo "Running snowflake-deployer"
          snowflake-deployer deploy -c $CONFIG_FILENAME
        
```
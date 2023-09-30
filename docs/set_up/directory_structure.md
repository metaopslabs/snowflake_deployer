# Directory Structure

Create a new repo & open locally in VS Code.

```
{project-name}
    .github/
        - workflows/
            - deploy-snowflake.yml
    snowflake/
        - account/
            - roles/
            - warehouses/
        - data/
            - {DATABASE_NAME}/
                - {SCHEMA_NAME}/
                    - OBJECTS/
                    - TASKS/
                    - PROCEDURES/
                    - MASKING_POLICIES/
                    - ROW_ACCESS_POLICIES/
                    - TAGS/
                    schema.yml
                database.yml
    .gitignore
    deploy_config_dev.yml
    deploy_config_prod.yml
    README.md
```

Actual deployment docs will vary by environments.

See Snowflake Objects sections for config of individual config files for each object type.

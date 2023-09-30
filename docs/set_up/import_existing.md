# Import Existing Account

Reverse Engineer an existing Snowflake account by importing existing objects to yml config.

Below is an example execution based on the dev configuration file named deploy_config_dev.yml

```
snowflake-deployer import -c deploy_config_dev.yml

```

This will build the file structure and config files based on supported objects.
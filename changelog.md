# 0.1.8
- import: list of databases to reverse engineer
    deploy config parameter = IMPORT_DATABASES

# 0.1.9
- Bug fixes

# 0.1.10
- New subcommand - classify!  This auto classifies column data uses the build in Snowflake classification function and returns results as tags in the deployer YAML format
- Added support for child role mapping in a role
- Bug fixes

# 0.1.11
- Support for Row Access Policies on objects
- Objects tagged with LAST_UDPATE so metadata is redeployed if DDL update since last deploy

# 0.1.12-0.1.14
- Bugfixes

# 0.1.16
- Multi threading of tags & grants for performance improvements
- Added config value IMPORT_OBJECT_TYPES to limit object types

# 0.1.24
- Fixed the circular reference check and added circular path outputs
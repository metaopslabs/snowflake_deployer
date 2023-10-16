from src.util.util import remove_prefix
def wrangle_object(self, database_name:str, schema_name:str, env_database_prefix:str, env_role_prefix:str, deploy_db_name:str, ignore_roles_list:str, deploy_tag_list:list[str], current_role:str, available_roles:list[str], handle_ownership)->dict:
    # database_name should include any db prefixes
    if env_database_prefix is None:
        env_database_prefix = ''
    if env_role_prefix is None:
        env_role_prefix = ''

    objects = self._sf.objects_get(database_name, schema_name)  

    data = []
    for o in objects:
        object_name_with_db_schema = database_name + '.' + schema_name + '.' + o['OBJECT_NAME']
        o['OWNER'] = self._handle_ownership(handle_ownership, o['OWNER'], 'table', object_name_with_db_schema, current_role, available_roles)

        if o['OWNER'] not in ignore_roles_list: # if role managed by deployer (not out of the box) then add the jinja reference
            o['OWNER'] = self.create_jinja_role_instance(o['OWNER'])
        
        # Get row access policies associated with an object
        row_access_policy = self._sf.object_row_access_policy_reference(object_name_with_db_schema)
        o['ROW_ACCESS_POLICY'] = {}
        if row_access_policy != {}:
            row_access_policy_db = remove_prefix(row_access_policy['POLICY_DB'],env_database_prefix)
            o['ROW_ACCESS_POLICY']['NAME'] = self.create_jinja_ref(row_access_policy_db, row_access_policy['POLICY_SCHEMA'], row_access_policy['POLICY_NAME'])
            o['ROW_ACCESS_POLICY']['INPUT_COLUMNS'] = row_access_policy['INPUT_COLUMNS_LIST']

        tags = []
        tags_raw = self._sf.tag_references_get(database_name, object_name_with_db_schema, o['OBJECT_TYPE'])
        for t in tags_raw:
            if not (t['TAG_DATABASE'] == deploy_db_name and t['TAG_SCHEMA'] == 'TAG' and t['TAG_NAME'] in deploy_tag_list):
                tv = {}
                db_name = remove_prefix(t['TAG_DATABASE'],env_database_prefix)
                #tv['name'] = self.create_jinja_ref(db_name, t['TAG_SCHEMA'], t['TAG_NAME'])
                #tv['value'] = t['TAG_VALUE']
                tag_name = self.create_jinja_ref(db_name, t['TAG_SCHEMA'], t['TAG_NAME'])
                tv[tag_name] = t['TAG_VALUE']
                tags.append(tv)
        o['TAGS'] = tags

        grants_raw = self._sf.grants_get(object_name_with_db_schema, 'table')
        grants = []
        for g in grants_raw:
            if g['PRIVILEGE'] != 'OWNERSHIP' and g['GRANTEE_NAME'] != current_role and g['GRANT_TYPE'] == 'ROLE':
                grant = {}
                role_name = remove_prefix(g['GRANTEE_NAME'],env_role_prefix)
                grant_to = self.create_jinja_role_instance(role_name) if role_name not in ignore_roles_list else role_name
                grant[grant_to] = g['PRIVILEGE']
                if g['GRANT_OPTION'] is True:
                    grant['GRANT_OPTION'] = True
                grants.append(grant)
        grants_combined = self._combine_grants(grants)
        o['GRANTS'] = grants_combined

        #o.pop('OBJECT_TYPE')
        data.append(o)
    
    return data   

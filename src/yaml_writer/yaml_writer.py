from pathlib import Path
#import yaml
import os
import ruamel.yaml

class yaml_writer:
    #def __init__(self):
        
    from .functions.write_database_file import write_database_file
    from .functions.write_function_file import write_function_file
    from .functions.write_masking_policy_file import write_masking_policy_file
    from .functions.write_object_file import write_object_file
    from .functions.write_procedure_file import write_procedure_file
    from .functions.write_role_file import write_role_file
    from .functions.write_row_access_policy_file import write_row_access_policy_file
    from .functions.write_schema_file import write_schema_file
    from .functions.write_tag_file import write_tag_file
    from .functions.write_task_file import write_task_file
    from .functions.write_warehouse_file import write_warehouse_file

    def create_parent_load_data(self,yml_path: str)->dict:
        db_file_exists = os.path.isfile(yml_path)
        db_output_file = Path(yml_path)

        # Create directory if not exists
        if not db_file_exists:
            db_output_file.parent.mkdir(exist_ok=True, parents=True)
            data = {}
        # Else read current config to baseline from current file
        else:
            #yaml = ruamel.yaml.YAML(typ='safe')
            ryaml = ruamel.yaml.YAML()
            #ryaml = ruamel_yaml.YAML()
            with open(yml_path, "r") as yamlfile:
                data_raw = yamlfile.read().replace('{{', '<~<~').replace('}}', '~>~>') #.replace("'", "!!|!!")
                #print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                #print(data_raw)
                #print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                data = dict(ryaml.load(data_raw))
                #data = dict(ryaml.load(yamlfile))
                
                #data = dict(yaml.safe_load(yamlfile))
                #print(data)
                #data = yaml.load(yamlfile, Loader=yaml.FullLoader)
        return data

    def replace_jinja_ref_string(self, yaml_string:str):
        output = yaml_string.replace("'!!{{!!","{{")
        output = output.replace("!!}}!!'", "}}")
        output = output.replace("<~<~","{{")
        output = output.replace("~>~>","}}")
        output = output.replace("!!|!!","'")
        return output
    
    def replace_jinja_multiline_string(self, yaml_string:str):
        output = yaml_string.replace("'||$$",'|\n')
        output = output.replace("$$||'","")
        output = output.replace('"||$$','|\n')
        output = output.replace('$$||"',"")
        output = output.replace('\"','"')
        return output
    
    def replace_jinja_list(self, yaml_string:str):
        output = yaml_string.replace("'[","[")
        output = output.replace("]'","]")
        output = output.replace("''","'")
        return output

    def create_jinja_var(self, var_name:str):
        #return "!!{{!!" + var_name + "!!}}!!"
        return "<~<~" + var_name + "~>~>"
    
    def choose_value_string(self, file_data, field_name, db_data, db_field_name, default_value)-> str:
        use_file_data = False

        if db_field_name not in db_data:
            db_value_exists = False
        #elif db_data[db_field_name] is None or db_value == []: # commenting this out as a blank value from the db can mean it was removed in the db
        #    db_value_exists = False
        else:
            db_value_exists = True
            
        if field_name in file_data and file_data[field_name] is not None:
            field_value = str(file_data[field_name])

            #if "{ordereddict([('" in field_value:
            if "<~<~" in field_value:
                #return_value_raw = field_value.replace("{ordereddict([('", "").replace("', None)]): None}", "")
                #return_value = self.create_jinja_var(return_value_raw)
                return_value = field_value.replace('<~<~','{{').replace('~>~>','}}')
                use_file_data = True
            if not use_file_data and not db_value_exists: # if there's no jinja value, but there's also no db value, then also use the file value
                return_value = field_value
                use_file_data = True

        if not use_file_data and db_value_exists:
            if db_data[db_field_name] is None or db_data[db_field_name] == '':
                return_value = default_value
            else:
                return_value = db_data[db_field_name]
        elif not use_file_data:
            return_value = default_value
        return return_value

    def choose_value_list(self, file_data, field_name, db_data, db_field_name, default_value)->list:
        use_file_data = False
        
        #d['ALLOWED_VALUES'] if (tag['ALLOWED_VALUES'] is not None and tag['ALLOWED_VALUES'] != []) else var.EMPTY_STRING

        if db_field_name not in db_data:
            db_value_exists = False
        #elif db_data[db_field_name] is None or db_value == []: # commenting this out as a blank value from the db can mean it was removed in the db
        #    db_value_exists = False
        else:
            db_value_exists = True
            
        if field_name in file_data and file_data[field_name] is not None:
            field_value_list = list(file_data[field_name])
                
            for field_value in field_value_list:
                if "{ordereddict([('" in field_value:
                    return_value_raw = field_value.replace("{ordereddict([('", "").replace("', None)]): None}", "")
                    return_value = self.create_jinja_var(return_value_raw)
                    use_file_data = True
            if not use_file_data and not db_value_exists: # if there's no jinja value, but there's also no db value, then also use the file value
                return_value = field_value
                use_file_data = True

        if not use_file_data and db_value_exists:
            if db_data[db_field_name] is None or db_data[db_field_name] == []:
                return_value = default_value
            else:
                return_value = db_data[db_field_name]
        else:
            return_value = default_value

        return return_value
    
    def create_jinja_ref_string(self, yaml_string:str):
        output = yaml_string.replace("{{", "'!!{{!!")
        output = output.replace("<~<~","'!!{{!!")
        output = output.replace("}}", "!!}}!!'")
        output = output.replace("~>~>", "!!}}!!'")
        output = output.replace("'","!!|!!")
        return output
    
#[{"<~<~ref('CONTROL__GOVERNANCE__ENV')~>~>": '<~<~env~>~>'}]
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#[{'!!{{!!ref(!!|!!CONTROL__GOVERNANCE__ENV!!|!!)!!}}!!': 'DEV'}]
    def choose_list_objects(self, db_list, file_list)->list:
        new_list = []
        # convert list of dicts to a single dict (to search dict later)
        db_dict = {}
        for db_obj in db_list:
            for k in db_obj.keys():
                db_dict[k] = db_obj[k]
            
        file_dict = {}
        for file_obj in file_list:
            for k in file_obj.keys():
                file_dict[k] = file_obj[k]

        db_keys = db_dict.keys()
        for db_key in db_keys:
            new_item = {}
            if db_key in file_dict.keys():
                if '<~<~' in file_dict[db_key]: # file value exists and contains jinja --> use file version
                    new_item[db_key] = file_dict[db_key]
                else: # file valuel exists but does NOT contain jinja --> use db value to override
                    new_item[db_key] = db_dict[db_key]
            else: # value only exists in db (file is blank) --> take db value
                new_item[db_key] = db_dict[db_key]
            new_list.append(new_item)
        return new_list
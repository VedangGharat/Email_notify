import yaml
from lxml import etree as ET
import sys

# No arguments provided, use hard-coded defaults
if len(sys.argv) == 1:
    yaml_cfg = r'C:\Users\haoyuan.zhang\source\repos\SSIS_TEST\sftp_ssis.yaml' # 'ssis_test_params.yaml' 

    orig_ssis_cfg = r'C:\Users\haoyuan.zhang\source\repos\SSIS_TEST\SFTP-Download-Test\Package.dtsx' # 'Package.dtsx'

    new_ssis_cfg = 'new_Package.dtsx'

# Arguments provided, set variables
elif len(sys.argv) == 4:
    script_filename, yaml_cfg, orig_ssis_cfg, new_ssis_cfg = sys.argv
    
    if not yaml_cfg.endswith('.yaml'):
        raise Exception('Provide a yaml file')
    if orig_ssis_cfg == new_ssis_cfg:
        raise Exception('Provide a different path for the original and new SSIS files.')

# Inappropriate number of arguments provided, quit
else:
    raise Exception("Wrong number of parameters.\nUse none for hard-coded values OR enter the following 3 paramters: \n1. Parameter YAML File\n2. Original SSIS Filepath\n3. New SSIS Filepath.")




def read_yaml(yaml_cfg):
    # Load YAML as python dict
    with open(yaml_cfg, 'r') as yaml_f:
        try:
            yaml_dict = yaml.safe_load(yaml_f)
            print(yaml_dict)
        except yaml.YAMLError as exc:
            print(exc)
    
    return yaml_dict

# Debug logging - disabled by default
#debug_file = open('setup_debug.log', 'w+')
def reg_namespaces():
    # Register SSIS xml namespaces to avoid "xmlns1" type flags
    ET.register_namespace('clr', "http://schemas.microsoft.com/soap/encoding/clr/1.0")
    ET.register_namespace('SOAP-ENC',"http://schemas.xmlsoap.org/soap/encoding/")
    ET.register_namespace('SOAP-ENV',"http://schemas.xmlsoap.org/soap/envelope/")
    ET.register_namespace('xsd',"http://www.w3.org/2001/XMLSchema")
    ET.register_namespace('xsi',"http://www.w3.org/2001/XMLSchema-instance")
    ET.register_namespace('DTS',"www.microsoft.com/SqlServer/Dts")

    # Passed to root.find() to allow writing 'DTS:' instead of whole namespace
    ns = {'DTS': 'www.microsoft.com/SqlServer/Dts', 'xml': 'http://www.w3.org/XML/1998/namespace'}

    # Used in root.find().attrib dict obj to avoid writing whole namespace between {}
    # Allows for: dict[dts_ns+'ServerName']
    # And avoids: dict['{www.microsoft.com/SqlServer/Dts}ServerName']
    dts_ns = f"{{{ns['DTS']}}}"
    xml_ns = f"{{{ns['xml']}}}"
    
    return ns, dts_ns, xml_ns 

# Debug file header
# YAML param object, YAML param value, Old SSIS value, Modified SSIS value
#debug_file.write('yaml_param\tyaml_value\told_ssis_value\tnew_ssis_value\n')

def set_package_params(root, yaml_dict, ns, dts_ns, xml_ns):
    # Update Package Parameters if present
    if root.find('DTS:PackageParameters', ns) is not None:

        # Search for SSIS Package Parameters and update them with values from the YAML
        for param in root.find('DTS:PackageParameters', ns).findall('DTS:PackageParameter', ns):
            p = param.attrib
            for y in yaml_dict['Parameters'].keys():

                yaml_var = yaml_dict['Parameters'][y]

                if p[dts_ns+'ObjectName'] == yaml_var['SSIS_Name']:
                    
                    old_value = param.find('DTS:Property', ns)
                    
                    if old_value.text is None:
                        old_value.attrib.pop(xml_ns+'space')
                        
                    param.find('DTS:Property', ns).text =  yaml_var['Value']
                    #debug_file.write(f"{y}\t{old_value.text}\t{yaml_var['Value']}\t{param.find('DTS:Property', ns).text}\n")
    return root

#debug_file.close()

def set_connection_managers(root, yaml_dict, ns, dts_ns, xml_ns):
    # Update SSIS Connection Managers if present
    if root.find('DTS:ConnectionManagers', ns) is not None:
        
        for cm in root.find('DTS:ConnectionManagers', ns).findall('DTS:ConnectionManager', ns):
            
            for y in yaml_dict['Connection_Managers'].keys():
                yaml_cm = yaml_dict['Connection_Managers'][y]

                if cm.attrib[dts_ns+'ObjectName'] == yaml_cm['SSIS_Name']:
                
                    old_cs = cm.find('DTS:ObjectData', ns).find('DTS:ConnectionManager', ns).attrib[dts_ns+'ConnectionString']
                    old_cs_list = old_cs.split(';')

                    new_cs_list = []
                    
                    # Iterate through each element of the Connection String
                    # Save the yaml's value to a list if a flag is present. Otherwise append original value
                    for seg in old_cs_list:
                        flag_present = False
                        
                        for yaml_con in yaml_cm['Connection_String'].keys():
                            
                            yaml_seg = yaml_cm['Connection_String'][yaml_con]
                            
                            flag_present = seg.startswith(yaml_seg['XML_Flag'])

                            if flag_present:
                                print(f"{yaml_seg['XML_Flag']}={yaml_seg['New_Value']}")
                                new_cs_list.append(f"{yaml_seg['XML_Flag']}={yaml_seg['New_Value']}")
                                break
                        
                        # Element not updated by the yaml, write original value
                        if not flag_present:
                            new_cs_list.append(seg)
                                
                    # Join the updated elements into the connection string attribute
                    connection_string = ';'.join(new_cs_list)
                    cm.find('DTS:ObjectData', ns).find('DTS:ConnectionManager', ns).attrib[dts_ns+'ConnectionString'] = connection_string
                    print(connection_string)
    
    return root


def main(yaml_cfg, orig_ssis_cfg, new_ssis_cfg):
    
    yaml_dict = read_yaml(yaml_cfg)
    ns, dts_ns, xml_ns = reg_namespaces()
    
    tree = ET.parse(orig_ssis_cfg, parser = ET.XMLParser(strip_cdata=False))

    # Get root XML object
    root = tree.getroot()

    root = set_package_params(root, yaml_dict, ns, dts_ns, xml_ns)

    root = set_connection_managers(root, yaml_dict, ns, dts_ns, xml_ns)

    tree.write(new_ssis_cfg, xml_declaration=True, encoding='utf-8')

# python .\ssis_setup.py ssis_test_params.yaml Package.dtsx new_Package.dtsx
# python .\ssis_setup.py ssis_prod_params.yaml Package.dtsx new_Package.dtsx

main(yaml_cfg, orig_ssis_cfg, new_ssis_cfg)

from utils.Properties import Properties
import os
class Config_unit:
    def __init__(self,ele_name,ele_id,co2_per_unit,co2_unit,ele_unit):
        self.ele_name = ele_name
        self.ele_id = ele_id
        self.co2_per_unit = co2_per_unit
        self.co2_unit = co2_unit
        self.ele_unit = ele_unit



root_path = os.path.abspath(os.path.dirname(__file__))

class Co2_Cal:

    def __init__(self):
        self.unit_config_dict = {}
        self.init_all_unit()

    def init_all_unit(self):
        properties_path =root_path+  "/config/unit_conf.properties"
        properties = Properties(properties_path).getProperties()

        '''
        unit_energy=电力_electric_kg CO₂e_kWh##petroleum__kg CO₂e_m³
        unit_makings=铝_aluminum_kg CO₂e_kg##steel__kg CO₂e_kg
        '''
        unit_energy = properties.get("unit_energy")
        unit_makings = properties.get("unit_makings")
        self.save_conf2dict(unit_energy)
        self.save_conf2dict(unit_makings)

    def save_conf2dict(self,config_str:str):
        metrics_value = config_str.split("##")
        for metric in metrics_value:
            field_config = metric.split("_")
            config_unit_obj = Config_unit(field_config[0], field_config[1], field_config[2], field_config[3], field_config[4])
            self.unit_config_dict[field_config[1]] = config_unit_obj

    def out_parse(self,ele_id,input_val,output_val):
        config_unit_obj:Config_unit = self.unit_config_dict[ele_id]
        result = {}
        # input 对应 ele_unit
        result["input_val"] = input_val
        # output_val 对应 co2_unit
        result["output_val"] = output_val
        result["ele_name"] = config_unit_obj.ele_name
        result["ele_unit"] = config_unit_obj.ele_unit
        result["co2_unit"] = config_unit_obj.co2_unit
        result["co2_per_unit"] = config_unit_obj.co2_per_unit
        return result

    def do_cal(self,ele_id,input_val):
        try:
            input_val = float(input_val)
            ele_match_unit_conf:Config_unit = self.unit_config_dict[ele_id]
            if ele_match_unit_conf is not None:
                output_val = input_val * float(ele_match_unit_conf.co2_per_unit)
                return self.out_parse(ele_id,input_val,output_val)
            else:
                raise Exception("输入数据有误")
        except Exception as e:
            raise e







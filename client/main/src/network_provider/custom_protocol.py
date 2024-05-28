class CustomProtocol:
    def __init__(self) -> None:
        pass

    # root body
    def string_to_dict(self, dataL:str):
        data=data.split()
        dict_data={"root":"","body":"body"}
        dict_data["root"]=data[0]
        dict_data["body"]=data[1]
        
        return dict_data
    
    
    # root:PATH bname:STATION body:Target
    # root bname body
    def dict_to_string(self, dict_data:dict)->str:
        try:
            string_data=""
            for value in dict_data.values():
                string_data += value
                string_data += " "
        except Exception as e:
            string_data = f"error {e}"

        finally:
            return string_data


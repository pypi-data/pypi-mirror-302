from rajaongkir_python_sdk import RajaOngkirAPI, CostBodyRequest

if __name__ == "__main__":
    api = RajaOngkirAPI(api_key="d6a61bc56823ac1b4477844385e8d838")
    res = api.province(province_id=1)
    print(res)

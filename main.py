from co2_cal import Co2_Cal
from aiohttp import web
import aiohttp_cors
import json
import asyncio
import  os

from utils.Properties import Properties

root_path = os.path.abspath(os.path.dirname(__file__))

class Request_Controller:

    def __init__(self,co2_cal:Co2_Cal):
        self.co2_cal = co2_cal
        self.SUCCESS_CODE = 200
        self.ERROR_CODE = 500
        self.CODE_KEY = "code"
        self.RESULT_KEY = "result"

    def cal_(self,ele_id,input_val):
        result = self.co2_cal.do_cal(ele_id, input_val)
        return result
    async def cal_input(self,request):
        res = await request.json()
        input_list = res.get("input_list", '')
        if input_list == "":
            result = {}
            result[self.CODE_KEY] = self.ERROR_CODE
            result[self.RESULT_KEY] = "请输入需要计算的值"
            result = str(result)
            result = result.replace("'", '"')
            return web.Response(text=f"{result}")
        try:
            result_list = []
            if len(input_list) == 0:
                result = {}
                result[self.CODE_KEY] = self.ERROR_CODE
                result[self.RESULT_KEY] = "请输入需要计算的值"
                result = str(result)
                result = result.replace("'", '"')
                return web.Response(text=f"{result}")

            for item in input_list:
                ele_id = item["ele_id"]
                input_val = item["input_val"]
                cal_result = self.cal_(ele_id,input_val)
                result_list.append(cal_result)

            data = {}
            data["list_output"] = result_list
            total_co2 = sum([float(ele["output_val"]) for ele in result_list])
            total_info = {}
            total_info["output_val"] = total_co2
            total_info["output_unit"] = result_list[0]["co2_unit"]
            data["total_info"] = total_info

            result = {}
            result[self.CODE_KEY] = self.SUCCESS_CODE
            result[self.RESULT_KEY] = data
            result = str(result)
            result = result.replace("'", '"')
            return web.Response(text=f"{result}")

        except Exception as e:
            print(repr(e))
            result = {}
            result[self.CODE_KEY] = self.ERROR_CODE
            result[self.RESULT_KEY] = e.__str__()
            result = str(result)
            result = result.replace("'", '"')
            return web.Response(text=f"{result}")




async def start_app(app, port):
    print("start init web in port %d" % (port))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()








if __name__ == '__main__':


    properties_path = root_path+"/config/conf.properties"
    model = None
    tokenizer = None
    # 声明一个Properties类的实例，调用其getProperties方法，返回一个字典
    properties = Properties(properties_path).getProperties()

    port = int(properties.get('server.port'))
    co2_cal = Co2_Cal()
    request_handler = Request_Controller(co2_cal)

    app = web.Application()
    app.add_routes([
        web.post('/cal_input', request_handler.cal_input)
    ])
    # Configure default CORS settings.
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    # Configure CORS on all routes.
    for route in list(app.router.routes()):
        cors.add(route)


    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start_app(app, port))
        loop.run_forever()
    except Exception as e:
        print(e)
    finally:
        print("app exit ...")
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()





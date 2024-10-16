import json

import lark_oapi as lark
from lark_oapi.api.calendar.v4 import *


# SDK 使用说明: https://github.com/larksuite/oapi-sdk-python#readme
# 以下示例代码是根据 API 调试台参数自动生成，如果存在代码问题，请在 API 调试台填上相关必要参数后再使用
# 复制该 Demo 后, 需要将 "YOUR_APP_ID", "YOUR_APP_SECRET" 替换为自己应用的 APP_ID, APP_SECRET.
def main():
    # 创建client
    client = lark.Client.builder() \
        .app_id("cli_a5d1921ef9d3500b") \
        .app_secret("GAmmmAMgI4UXYZyGMDqfAevPRVHrR6T1") \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象
    request: CreateCalendarRequest = CreateCalendarRequest.builder() \
        .request_body(Calendar.builder()
            .summary("测试日历")
            .description("使用开放接口创建日历")
            .permissions("private")
            .color(-1)
            .summary_alias("日历备注名")
            .build()) \
        .build()

    # 发起请求
    response: CreateCalendarResponse = client.calendar.v4.calendar.create(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.calendar.v4.calendar.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))


if __name__ == "__main__":
    main()

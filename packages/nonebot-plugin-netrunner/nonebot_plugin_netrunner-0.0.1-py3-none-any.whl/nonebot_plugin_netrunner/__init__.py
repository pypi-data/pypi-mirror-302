from nonebot.rule import to_me
from nonebot.plugin import on_command, PluginMetadata


__plugin_meta__ = PluginMetadata(
    name="Netrunner 矩阵潜袭卡查",
    description="识别群聊信息中的卡名并展示卡片信息",
    usage="在聊天记录中使用 【】 或 [[]] 引用卡名即可。",
    type="application",
    homepage="https://github.com/hoshiko-shiro/nonebot-plugin-netrunner",
    extra={},
)


weather = on_command("天气", rule=to_me())

@weather.handle()
async def weather_handler():
    await weather.finish("天气是...")

from business_rules.variables import BaseVariables, numeric_rule_variable
from business_rules.actions import BaseActions, rule_action

from app.flows import update_ad_config


class DataVariables(BaseVariables):
    def __init__(self, data):
        self.data = data

    @numeric_rule_variable()
    def daily_consume(self):
        return self.data.get("daily_consume", 0)

    @numeric_rule_variable()
    def balance(self):
        return self.data.get("balance", 0)

    @numeric_rule_variable()
    def roi(self):
        return self.data.get("balance", 0)


class Actions(BaseActions):
    def __init__(self, task):
        self.task_name = task.name

    @rule_action()
    def notify(self):
        print(f"🚀 任务 [{self.task_name}] 满足条件，发送通知")

    @rule_action()
    def update_ad_config(self):
        print(f"🚀 任务 [{self.task_name}] 满足条件，变更ad config")
        update_ad_config.remote_run(self.task_name)

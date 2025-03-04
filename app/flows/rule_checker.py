from prefect import flow, task
from app.models import RuleTask
from app.database import SessionLocal
from app.rules import DataVariables, Actions
from business_rules.engine import run_all

fake_data = {
    "test1": {"daily_consume": 100, "balance": 1000, "roi": 0.1},
    "test2": {"daily_consume": 200, "balance": 1200, "roi": 2.1},
    "test3": {"daily_consume": 300, "balance": 800, "roi": 1.1},
}


@task
def fetch_tasks():
    db = SessionLocal()
    return db.query(RuleTask).all()


@task
def get_realtime_data(task_name):
    return fake_data.get(task_name)


@task
def evaluate_rule(task: RuleTask, data):
    run_all(
        rule_list=task.rules,
        defined_variables=DataVariables(data),
        defined_actions=Actions(task.name),
        stop_on_first_trigger=False
    )


@flow(name="Rule Checker Flow")
def rule_checker_flow():
    tasks = fetch_tasks()
    for task in tasks:
        data = get_realtime_data(task.name)
        evaluate_rule(task, data)

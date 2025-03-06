from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.flows import rule_checker
from fastapi.responses import HTMLResponse
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI()


@app.post("/tasks")
def create_task(task: schemas.RuleTaskCreate, db: Session = Depends(database.get_db)):
    db_task = models.RuleTask(name=task.name, rules=task.rules)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.get("/prefect-ui")
def prefect_ui():
    return HTMLResponse("""
        <iframe src="http://localhost:4200" width="100%" height="800px"></iframe>
    """)


if __name__ == "__main__":
    import uvicorn

    scheduler = BackgroundScheduler()
    scheduler.add_job(rule_checker.remote_rule_checker_flow, 'interval', seconds=10)
    scheduler.start()

    uvicorn.run(app='main:app', host="0.0.0.0", port=8080, reload=True)

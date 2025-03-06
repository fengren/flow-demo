from prefect import task, flow, get_run_logger
from prefect.deployments import run_deployment


@task
def step1(ad_id):
    logger = get_run_logger()
    logger.info(f"Step1: {ad_id}")
    return f"step1_{ad_id}_data"


@task
def step2(ad_id):
    logger = get_run_logger()
    logger.debug(f"Step2: {ad_id}")
    return f"step2_{ad_id}_rule"


@task
def step3(data1, data2):
    logger = get_run_logger()
    logger.info(f"应用策略, {data1}, {data2}")


@flow(name="Update AD Config", retries=3)
def update_ad_config(ad_id):
    logger = get_run_logger()
    data1 = step1(ad_id)
    data2 = step2(ad_id)
    step3(data1, data2)
    logger.info(f"{ad_id} Update Success")


@flow(name="remote_update_ad_config")
def remote_run(ad_id):
    run_deployment(name="Update AD Config/Update AD Config Deployment", parameters={"ad_id": ad_id})


if __name__ == "__main__":
    update_ad_config.serve(name="Update AD Config Deployment")

from app.agents.wholesale_agents import run_wholesale_agents
from app.agents.car_finance_agents import run_finance_agents

async def start_agents():

    run_wholesale_agents()
    run_finance_agents()

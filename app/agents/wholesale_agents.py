def run_wholesale_agents():

    agents = []

    for i in range(25):

        agent = {
            "id": i,
            "type": "wholesale",
            "status": "scanning"
        }

        agents.append(agent)

    return agents

import requests

def solve_maintenance_schedule(api_url, auth_token):
    # 1. Fetch data from the API
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(api_url, headers=headers)
    data = response.json()
    
    tasks = data['tasks'] # List of {duration, importance_score}
    max_hours = data['available_mechanic_hours']
    
    # 2. Dynamic Programming for 0/1 Knapsack
    # dp[i] will store the max importance for 'i' hours
    dp = [0] * (max_hours + 1)
    # To reconstruct the solution, keep track of chosen items
    keep = [[False] * (max_hours + 1) for _ in range(len(tasks) + 1)]

    for i, task in enumerate(tasks, 1):
        duration = task['duration']
        score = task['importance_score']
        for w in range(max_hours, duration - 1, -1):
            if dp[w - duration] + score > dp[w]:
                dp[w] = dp[w - duration] + score
                keep[i][w] = True

    # 3. Reconstruct the subset of vehicles
    selected_tasks = []
    curr_w = max_hours
    for i in range(len(tasks), 0, -1):
        if keep[i][curr_w]:
            selected_tasks.append(tasks[i-1])
            curr_w -= tasks[i-1]['duration']

    return {
        "max_importance": dp[max_hours],
        "selected_vehicles": selected_tasks
    }

# Example Usage (Replace with actual endpoint/token)
# result = solve_maintenance_schedule("http://api.logistics.com/tasks", "YOUR_TOKEN")
# print(f"Total Score: {result['max_importance']}")
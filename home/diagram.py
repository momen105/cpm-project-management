from home.models import *
from collections import defaultdict
def generate_network_diagram(project_id):

    tasks = Task.objects.filter(project=project_id).prefetch_related('predecessors')

    node_lines = []
    edge_lines = []
    node_data = {}

    all_nodes = set()
    incoming = defaultdict(set)
    outgoing = defaultdict(set)

    for task in tasks:
        node = task.name
        node_label = f"{node}(({task.name}))"
        node_lines.append(node_label)

        deps = ", ".join(p.name for p in task.predecessors.all())
        node_data[node] = {
            "title": task.name,
            "description": deps or "None",
            "duration": f"{task.duration} days"
        }

        all_nodes.add(node)

        for pred in task.predecessors.all():
            pred_name = pred.name
            edge_lines.append(f"{pred_name} --> {node}")
            incoming[node].add(pred_name)
            outgoing[pred_name].add(node)
            all_nodes.add(pred_name)

    # Identify start nodes
    start_nodes = [n for n in all_nodes if not incoming[n]]
    end_nodes = [n for n in all_nodes if not outgoing[n]]

    # Add virtual Start node
    if start_nodes:
        node_lines.append("Start((Start))")
        for start_node in start_nodes:
            edge_lines.append(f"Start --> {start_node}")

    if end_nodes:
        node_lines.append("End((End))")
        for end in end_nodes:
            edge_lines.append(f"{end}  --> End")

    diagram = "graph LR\n  " + "\n  ".join(node_lines + edge_lines)
    return diagram, node_data




def generate_Schedule_Diagram(project_id):

    tasks = Task.objects.filter(project_id=project_id).prefetch_related('predecessors')

    task_map = {}
    predecessors = defaultdict(list)
    successors = defaultdict(list)
    connections = []
    node_data = {}
    for task in tasks:
        task_id = task.name.strip()
        task_map[task_id] = {
            "id": task_id,
            "name": task.name.strip(),
            "duration": task.duration,
            "description": task.description,
            "es": 0, "ef": 0, "ls": 0, "lf": 0,
            "slack": 0, "critical": False,
        }
        node_data[task_id] = {
            "title": task.name,
            "description": task.description,
            "duration": task.duration,
        }

    # Build real task connections
    for task in tasks:
        task_id = task.name.strip()
        for pred in task.predecessors.all():
            pred_id = pred.name.strip()
            connections.append([pred_id, task_id])
            predecessors[task_id].append(pred_id)
            successors[pred_id].append(task_id)

    # Add dummy Start and End tasks
    START, END = "Start", "End"
    task_map[START] = {
        "id": START, "name": START, "duration": 0,
        "es": 0, "ef": 0, "ls": 0, "lf": 0,
        "slack": 0, "critical": False
    }
    task_map[END] = {
        "id": END, "name": END, "duration": 0,
        "es": 0, "ef": 0, "ls": 0, "lf": 0,
        "slack": 0, "critical": False
    }

    # Connect Start to tasks with no predecessors
    for task_id in task_map:
        if task_id not in [START, END] and not predecessors[task_id]:
            connections.append([START, task_id])
            predecessors[task_id].append(START)
            successors[START].append(task_id)

    # Connect tasks with no successors to End
    for task_id in task_map:
        if task_id not in [START, END] and not successors[task_id]:
            connections.append([task_id, END])
            successors[task_id].append(END)
            predecessors[END].append(task_id)

    # Forward Pass
    def forward_pass():
        visited = set()
        def dfs(node):
            if node in visited:
                return
            visited.add(node)
            es = 0
            for pred in predecessors[node]:
                dfs(pred)
                es = max(es, task_map[pred]["ef"])
            task_map[node]["es"] = es
            task_map[node]["ef"] = es + task_map[node]["duration"]
        for task_id in task_map:
            dfs(task_id)

    # Backward Pass
    def backward_pass():
        visited = set()
        max_ef = max(task["ef"] for task in task_map.values())
        def dfs(node):
            if node in visited:
                return
            visited.add(node)
            lf = max_ef if not successors[node] else max(task_map[succ]["ls"] for succ in successors[node])
            task_map[node]["lf"] = lf
            task_map[node]["ls"] = lf - task_map[node]["duration"]
            for pred in predecessors[node]:
                dfs(pred)
        for task_id in task_map:
            if not successors[task_id]:  # End tasks
                dfs(task_id)

    # Slack Calculation
    def calculate_slack():
        for task in task_map.values():
            task["slack"] = task["ls"] - task["es"]
            task["critical"] = (task["slack"] == 0)

    forward_pass()
    backward_pass()
    calculate_slack()

    activities = list(task_map.values())
    
    critical_path_duration = task_map["End"]["ef"]

  
    # Optional: Get sorted critical tasks
    critical_tasks = sorted(
        [task["id"] for task in activities if task["critical"] and task["id"] != "End"],
        key=lambda tid: task_map[tid]["es"]
    )
    return activities, connections,critical_path_duration, critical_tasks,node_data



def gantt_chart_data(project_id):
    tasks = Task.objects.filter(project_id=project_id).prefetch_related('predecessors')

    task_map = {}
    predecessors = defaultdict(list)
    successors = defaultdict(list)

    for task in tasks:
        task_id = task.name.strip()
        task_map[task_id] = {
            "id": task_id,
            "name": task.description.strip(),
            "duration": task.duration,
            "es": 0, "ef": 0
        }

    for task in tasks:
        task_id = task.name.strip()
        for pred in task.predecessors.all():
            pred_id = pred.name.strip()
            predecessors[task_id].append(pred_id)
            successors[pred_id].append(task_id)

    def forward_pass():
        visited = set()
        def dfs(node):
            if node in visited:
                return
            visited.add(node)
            es = 0
            for pred in predecessors[node]:
                dfs(pred)
                es = max(es, task_map[pred]["ef"])
            task_map[node]["es"] = es
            task_map[node]["ef"] = es + task_map[node]["duration"]
        for task_id in task_map:
            dfs(task_id)

    forward_pass()

    # Now convert to Chart.js format
    labels = []
    data = []
    
    for task in task_map.values():
        labels.append(task["name"])
        data.append({
            "x": [task["es"], task["ef"]],
            "y": task["name"]
        })

    return labels, data

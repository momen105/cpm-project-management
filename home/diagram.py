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
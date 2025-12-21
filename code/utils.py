import json
import os
import re
from graphviz import Digraph
import numpy as np


def load_config(cfg_path=os.path.join(os.path.dirname(__file__), "config.json")):
    with open(os.path.join(os.path.dirname(__file__), "config.json"), "r") as f:
        return json.load(f)
    
def split_content(content: str,delimiterStr: str):
    delimiter = delimiterStr
    parts = content.split(delimiter, 1)
    
    if len(parts) == 2:
        before = parts[0]
        after = delimiter + parts[1]
    else:
        before = content
        after = ""
    
    return before, after

def extract_steps(text):
    plan = []
    pattern = re.compile(r'\d+\.\s(.*?)(?=\n\d+\.|\n*$)', re.DOTALL)
    matches = pattern.findall(text)
    
    for match in matches:
        step_lines = match.strip().split("\n", 1)
        step = step_lines[0] if len(step_lines) > 1 else match.strip()  # Extract only the first line; if no newline exists, keep all content (remove newline)
        step = step.replace("*", "")  # Remove all * symbols
        plan.append(step)
    
    return plan

def extract_steps_to_val(text):
    content = ""
    pattern = re.compile(r'(\d+\.\s)(.*?)(?=\n\d+\.|\n*$)', re.DOTALL)
    matches = pattern.findall(text)
    
    for match in matches:
        step_lines = match[1].strip().split("\n", 1)
        step = step_lines[0] if len(step_lines) > 1 else match[1].strip()  # Extract only the first line; if no newline exists, keep all content (remove newline)
        step = step.replace("*", "")  # Remove all * symbols
        content += match[0]+step + '\n'
    
    return content

class TreeNode:
    def __init__(self, action=None, parent=None):
        self.action = action  # current node's action
        self.children = {}  # store child nodes, key is action name
        self.parent = parent  # parent node

    def add_child(self, action):
        if action not in self.children:
            self.children[action] = TreeNode(action, parent=self)
        return self.children[action]

    def get_child(self, action):
        return self.children.get(action, None)

class ActionTree:
    def __init__(self):
        self.root = TreeNode()  # create root node

    def construct_from_plans(self, plans):
        for plan in plans:
            current_node = self.root
            for action in plan:
                current_node = current_node.add_child(action)  # Add actions by level

    def display(self, node=None, level=0):
        if node is None:
            node = self.root
        
        for action, child in node.children.items():
            print("  " * level + f"-> {action}")
            self.display(child, level + 1)

    def visualize(self, save_path):
        os.makedirs(os.path.dirname(save_path), exist_ok=True)  # Ensure the save directory exists
        dot = Digraph(format="png")
        dot.attr(fontname="Microsoft YaHei")  # Suitable for Windows
        dot.node("root", "Root", fontname="Microsoft YaHei")  # Root node

        self._add_nodes(dot, self.root, "root")
        dot.render(save_path, cleanup=True)
        # print(f"Action Tree visualization saved as {save_path}.png")

    def _add_nodes(self, dot, node, node_name):
        for action, child in node.children.items():
            child_name = f"{node_name}_{hash(action)}"
            dot.node(child_name, action, fontname="Microsoft YaHei")
            dot.edge(node_name, child_name)
            self._add_nodes(dot, child, child_name)

def process_array(arr):
    arr = np.array(arr)
    content=""
    ndim = arr.ndim # get the number of dimensions
    
    # process based on the number of dimensions
    if ndim == 1:
        for i in range(len(arr)):
            content+= f"{i+1}.{arr[i]}"+""+'\n'
    elif ndim == 2:
        for i, sub_arr in enumerate(arr):
            for j, item in enumerate(sub_arr):
                content+= f"{j+1}.{item}"+""+'\n'
    else:
        print(f"Unsupported array dimension: {ndim}")

    return content
# =============================================================================
# Project 11: Sum of Subsets – State Space Tree
# Unit IV – Backtracking | DAA Macro Project
# Set = {5, 10, 12}, Target Sum = 15
# =============================================================================

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


# =============================================================================
# PART 1: BACKTRACKING ALGORITHM
# =============================================================================

def sum_of_subsets(arr, target):
    """
    Solve the Sum of Subsets problem using recursive backtracking.
    Returns a list of all solutions (each solution is a list of elements).
    """
    solutions = []

    def backtrack(index, current_subset, current_sum):
        # Base case: if current sum equals target, record the solution
        if current_sum == target:
            solutions.append(list(current_subset))
            return

        # Pruning: if sum exceeds target or all elements exhausted, backtrack
        if index >= len(arr) or current_sum > target:
            return

        # --- Include arr[index] ---
        current_subset.append(arr[index])
        backtrack(index + 1, current_subset, current_sum + arr[index])
        current_subset.pop()  # backtrack

        # --- Exclude arr[index] ---
        backtrack(index + 1, current_subset, current_sum)

    backtrack(0, [], 0)
    return solutions


# =============================================================================
# PART 2: BUILD TREE STRUCTURE (mirrors the recursive execution exactly)
# =============================================================================

def build_tree(arr, target):
    """
    Build the state-space tree by simulating the backtracking recursion.
    Each node stores: id, label, subset, sum, status, parent_id, edge_label.
    Status: 'solution' | 'pruned' | 'explored'
    """
    nodes = []
    node_id_counter = [0]

    def add_node(subset, current_sum, parent_id, edge_label):
        nid = node_id_counter[0]
        node_id_counter[0] += 1

        if current_sum == target:
            status = 'solution'
        elif current_sum > target:
            status = 'pruned'
        else:
            status = 'explored'

        subset_str = "{" + ",".join(str(x) for x in subset) + "}" if subset else "{}"
        label = f"Subset: {subset_str}\nSum: {current_sum}"
        if status == 'solution':
            label += "\nSOLUTION"
        elif status == 'pruned':
            label += "\nPRUNED"

        nodes.append({
            'id': nid,
            'label': label,
            'subset': list(subset),
            'sum': current_sum,
            'status': status,
            'parent_id': parent_id,
            'edge_label': edge_label,
            'depth': 0,          # filled later
            'pos_x': 0.0,        # filled later
            'pos_y': 0.0,        # filled later
            'children': []
        })
        if parent_id is not None:
            nodes[parent_id]['children'].append(nid)
        return nid

    def recurse(index, subset, current_sum, parent_id):
        nid = add_node(subset, current_sum, parent_id, None)

        # Don't expand if solution or pruned
        if current_sum == target or current_sum > target:
            return nid
        if index >= len(arr):
            return nid

        # Include
        inc_id = recurse(index + 1, subset + [arr[index]], current_sum + arr[index], nid)
        nodes[inc_id]['edge_label'] = f"Include {arr[index]}"

        # Exclude
        exc_id = recurse(index + 1, subset, current_sum, nid)
        nodes[exc_id]['edge_label'] = f"Exclude {arr[index]}"

        return nid

    recurse(0, [], 0, None)
    return nodes


# =============================================================================
# PART 3: ASSIGN POSITIONS (top-down, left-right BFS layout)
# =============================================================================

def assign_positions(nodes):
    """
    Assign (x, y) positions to each node using a bottom-up leaf-counting
    approach so sibling subtrees never overlap.
    """
    # --- Step 1: compute depth ---
    def set_depth(nid, d):
        nodes[nid]['depth'] = d
        for cid in nodes[nid]['children']:
            set_depth(cid, d + 1)

    set_depth(0, 0)

    # --- Step 2: compute subtree leaf count (used for x-centering) ---
    def leaf_count(nid):
        if not nodes[nid]['children']:
            return 1
        return sum(leaf_count(c) for c in nodes[nid]['children'])

    # --- Step 3: assign x positions with a running counter ---
    x_counter = [0]

    def assign_x(nid):
        children = nodes[nid]['children']
        if not children:
            nodes[nid]['pos_x'] = x_counter[0]
            x_counter[0] += 1
        else:
            for cid in children:
                assign_x(cid)
            child_xs = [nodes[c]['pos_x'] for c in children]
            nodes[nid]['pos_x'] = (child_xs[0] + child_xs[-1]) / 2

    assign_x(0)

    # --- Step 4: y from depth ---
    max_depth = max(n['depth'] for n in nodes)
    for n in nodes:
        n['pos_y'] = max_depth - n['depth']   # root at top


# =============================================================================
# PART 4: DRAW THE STATE-SPACE TREE
# =============================================================================

COLORS = {
    'solution': '#2ecc71',   # Green
    'pruned':   '#e74c3c',   # Red
    'explored': '#3498db',   # Blue
    'edge':     '#555555',
    'bg':       '#f8f9fa',
}

EDGE_LABEL_COLOR = {
    'Include': '#27ae60',
    'Exclude': '#c0392b',
}


def draw_tree(nodes, output_path):
    total_leaves = sum(1 for n in nodes if not n['children'])
    fig_w = max(16, total_leaves * 2.2)
    fig_h = 14

    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    fig.patch.set_facecolor(COLORS['bg'])
    ax.set_facecolor(COLORS['bg'])

    max_depth = max(n['depth'] for n in nodes)
    x_scale = 2.8
    y_scale = 2.6

    NODE_W = 1.85
    NODE_H = 0.78

    # ---- Draw edges first (so nodes appear on top) ----
    for node in nodes:
        if node['parent_id'] is None:
            continue
        parent = nodes[node['parent_id']]
        px = parent['pos_x'] * x_scale
        py = parent['pos_y'] * y_scale
        cx = node['pos_x'] * x_scale
        cy = node['pos_y'] * y_scale

        # Arrow from bottom of parent to top of child
        ax.annotate(
            "",
            xy=(cx, cy + NODE_H / 2 + 0.05),
            xytext=(px, py - NODE_H / 2 - 0.05),
            arrowprops=dict(
                arrowstyle="-|>",
                color=COLORS['edge'],
                lw=1.4,
                mutation_scale=14,
                connectionstyle="arc3,rad=0.0"
            ),
        )

        # Edge label
        if node['edge_label']:
            mid_x = (px + cx) / 2
            mid_y = (py + cy) / 2
            word = node['edge_label'].split()[0]   # 'Include' or 'Exclude'
            ec = EDGE_LABEL_COLOR.get(word, '#333333')
            ax.text(
                mid_x, mid_y, node['edge_label'],
                fontsize=7.5, ha='center', va='center',
                color=ec, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.18', fc='white', ec=ec, lw=0.8, alpha=0.92)
            )

    # ---- Draw nodes ----
    for node in nodes:
        nx = node['pos_x'] * x_scale
        ny = node['pos_y'] * y_scale
        color = COLORS[node['status']]

        # Rounded rectangle
        fancy = FancyBboxPatch(
            (nx - NODE_W / 2, ny - NODE_H / 2),
            NODE_W, NODE_H,
            boxstyle="round,pad=0.08",
            linewidth=2.0,
            edgecolor='white' if node['status'] == 'solution' else '#2c3e50',
            facecolor=color,
            zorder=3
        )
        ax.add_patch(fancy)

        # Node text
        lines = node['label'].split('\n')
        text_color = 'white' if node['status'] in ('solution', 'pruned') else 'white'

        # Draw each line
        line_spacing = 0.22
        total_text_h = (len(lines) - 1) * line_spacing
        for i, line in enumerate(lines):
            ty = ny + total_text_h / 2 - i * line_spacing
            fs = 8.0
            fw = 'bold' if (i == len(lines) - 1 and node['status'] in ('solution', 'pruned')) else 'normal'
            if i == 0:
                fw = 'bold'
            ax.text(nx, ty, line, fontsize=fs, ha='center', va='center',
                    color='white', fontweight=fw, zorder=4)

    # ---- Title & Subtitle ----
    fig.text(0.5, 0.975, "Sum of Subsets – State Space Tree",
             ha='center', va='top', fontsize=17, fontweight='bold', color='#2c3e50')
    fig.text(0.5, 0.952, "Backtracking  |  Set = {5, 10, 12}  |  Target = 15",
             ha='center', va='top', fontsize=11, color='#555555')

    # ---- Legend ----
    legend_patches = [
        mpatches.Patch(color=COLORS['explored'], label='Explored / Valid State'),
        mpatches.Patch(color=COLORS['solution'], label='Solution State'),
        mpatches.Patch(color=COLORS['pruned'],   label='Pruned (Sum > 15)'),
    ]
    ax.legend(
        handles=legend_patches,
        loc='lower left',
        fontsize=9,
        framealpha=0.9,
        edgecolor='#cccccc',
        title='Legend',
        title_fontsize=9
    )

    # ---- Bottom annotation ----
    fig.text(0.5, 0.018,
             "Solution Found:  {5, 10}       Target Sum: 15",
             ha='center', va='bottom', fontsize=11, fontweight='bold',
             color='#27ae60',
             bbox=dict(boxstyle='round,pad=0.4', fc='#eafaf1', ec='#27ae60', lw=1.2))

    # ---- Axis cleanup ----
    all_x = [n['pos_x'] * x_scale for n in nodes]
    all_y = [n['pos_y'] * y_scale for n in nodes]
    ax.set_xlim(min(all_x) - 1.8, max(all_x) + 1.8)
    ax.set_ylim(min(all_y) - 1.2, max(all_y) + 1.5)
    ax.axis('off')

    plt.tight_layout(rect=[0, 0.04, 1, 0.94])
    plt.savefig(output_path, dpi=180, bbox_inches='tight',
                facecolor=COLORS['bg'])
    plt.close()
    print("Visualization Generated: Yes")


# =============================================================================
# PART 5: MAIN
# =============================================================================

def main():
    arr    = [5, 10, 12]
    target = 15

    print("=" * 40)
    print("Sum of Subsets using Backtracking")
    print(f"Set = {{{', '.join(map(str, arr))}}}")
    print(f"Target Sum = {target}")
    print("=" * 40)
    print()

    solutions = sum_of_subsets(arr, target)

    print(f"Solutions Found: {len(solutions)}")
    print()
    for i, sol in enumerate(solutions, 1):
        print(f"Solution {i}:")
        print("{" + ", ".join(map(str, sol)) + "}")
        print()

    # Build and draw the state-space tree
    nodes = build_tree(arr, target)
    assign_positions(nodes)

    output_path = "Unit4_Backtracking/Visualization.png"
    draw_tree(nodes, output_path)

    print("Project Status: Complete")


if __name__ == "__main__":
    main()

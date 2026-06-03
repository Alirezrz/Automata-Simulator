import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.animation as animation
import networkx as nx
from dfa import DFA, DEAD

# ── colours 
C_DEFAULT     = "#ffffff"
C_CURRENT     = "#add8e6"   # light-blue  → active state
C_ACCEPTED    = "#90ee90"   # green       → accepted final state
C_REJECTED    = "#ffaaaa"   # red-pink    → rejected halt state
C_DEAD_NODE   = "#dddddd"   # light-grey  → DEAD state
C_ACTIVE_EDG  = "#cc0000"   # red         → active transition arrow
C_DEAD_EDG    = "#aaaaaa"   # grey        → DEAD self-loop
C_DEFAULT_EDG = "#333333"
BORDER_ACTIVE = "#cc0000"
BORDER_DEAD   = "#aaaaaa"
BORDER_DEF    = "#333333"


class DFAVisualizer:
    def __init__(self, output_dir: str = "dfa_visualizations"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)


    def generate_graph(self, dfa: DFA, current_state: str = None,
                       active_transition: tuple = None) -> tuple:
        """Returns (fig, ax) — used by main.py for the base structure save."""
        return self._build_figure(dfa, current_state, active_transition,
                                  title="DFA Structure", subtitle="")

    def visualize_step(self, dfa: DFA, step_name: str, current_state: str,
                       active_transition: tuple = None):
        """Saves a single PNG frame (kept for backward-compat; not used in animation path)."""
        fig, _ = self._build_figure(dfa, current_state, active_transition)
        path = os.path.join(self.output_dir, step_name + ".png")
        fig.savefig(path, dpi=120, bbox_inches="tight")
        plt.close(fig)

    def animate(self, dfa: DFA, input_string: str, frames: list[dict],
                filename: str = None, fps: int = 1) -> str:
        """
        Build and save an animated GIF for one input string.

        Each element of `frames` is a dict:
            {
                "current_state": str,
                "active_transition": (from_state, symbol) | None,
                "label": str,          # shown as subtitle
                "result": None | "accepted" | "rejected"
            }

        Returns the path to the saved GIF.
        """
        if filename is None:
            safe = input_string if input_string else "empty"
            filename = os.path.join(self.output_dir, f"animation_{safe}.gif")

        fig_frames = []
        for frame in frames:
            result  = frame.get("result")
            title   = f'Input: "{input_string}"' if input_string else 'Input: (empty string)'
            subtitle = frame.get("label", "")
            fig, _  = self._build_figure(
                dfa,
                current_state     = frame["current_state"],
                active_transition = frame.get("active_transition"),
                title             = title,
                subtitle          = subtitle,
                result            = result,
            )
            fig.canvas.draw()
            # Convert figure to an RGB array
            import numpy as np
            buf = fig.canvas.buffer_rgba()
            img = np.asarray(buf)[..., :3]   # drop alpha
            fig_frames.append(img)
            plt.close(fig)

        from PIL import Image
        pil_frames = [Image.fromarray(f) for f in fig_frames]
        duration_ms = int(1000 / fps)
        pil_frames[0].save(
            filename,
            save_all=True,
            append_images=pil_frames[1:],
            duration=duration_ms,
            loop=0,
        )
        return filename


    def _build_figure(self, dfa: DFA, current_state: str,
                      active_transition: tuple,
                      title: str = "", subtitle: str = "",
                      result: str = None) -> tuple:

        G, edge_labels = self._build_nx_graph(dfa)
        pos            = self._layout(G, dfa)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_axis_off()
        fig.patch.set_facecolor("#f9f9f9")

        if title:
            fig.suptitle(title, fontsize=13, fontweight="bold", y=0.97)
        if subtitle:
            ax.set_title(subtitle, fontsize=10, color="#444444", pad=6)

        node_colors, node_edge_colors, node_lw = \
            self._node_styles(dfa, G.nodes(), current_state, result)

        active_edge = self._resolve_active_edge(dfa, active_transition)
        edge_colors, edge_lw, edge_styles = \
            self._edge_styles(dfa, G.edges(), active_edge)

        solid_edges  = [e for e, s in zip(G.edges(), edge_styles) if s == "solid"]
        dashed_edges = [e for e, s in zip(G.edges(), edge_styles) if s == "dashed"]

        def colour_subset(full_edges, subset):
            idx = {e: i for i, e in enumerate(full_edges)}
            return ([edge_colors[idx[e]] for e in subset],
                    [edge_lw   [idx[e]] for e in subset])

        s_col, s_lw = colour_subset(list(G.edges()), solid_edges)
        d_col, d_lw = colour_subset(list(G.edges()), dashed_edges)

        shared = dict(pos=pos, ax=ax, connectionstyle="arc3,rad=0.15",
                      arrows=True, arrowsize=20)

        if solid_edges:
            nx.draw_networkx_edges(G, edgelist=solid_edges,
                                   edge_color=s_col, width=s_lw,
                                   style="solid", **shared)
        if dashed_edges:
            nx.draw_networkx_edges(G, edgelist=dashed_edges,
                                   edge_color=d_col, width=d_lw,
                                   style="dashed", **shared)

        nx.draw_networkx_nodes(G, pos, ax=ax,
                               node_color=node_colors,
                               edgecolors=node_edge_colors,
                               linewidths=node_lw,
                               node_size=1800)

        node_list = list(G.nodes())
        for state in dfa.final_states:
            if state in pos:
                x, y = pos[state]
                ring = plt.Circle((x, y), radius=0.115, fill=False,
                                  edgecolor=node_edge_colors[node_list.index(state)],
                                  linewidth=1.5, transform=ax.transData)
                ax.add_patch(ring)

        nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_weight="bold")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax,
                                     font_size=8, label_pos=0.4,
                                     bbox=dict(boxstyle="round,pad=0.2",
                                               fc="white", ec="none", alpha=0.7))

        self._draw_start_arrow(ax, pos, dfa.start_state)
        self._draw_legend(ax, result)

        plt.tight_layout()
        return fig, ax


    def _build_nx_graph(self, dfa: DFA):
        G = nx.MultiDiGraph()
        G.add_nodes_from(dfa.states)
        edge_groups: dict[tuple, list] = {}
        for state in dfa.states:
            for symbol in dfa.alphabet:
                nxt = dfa.get_next_state(state, symbol)
                if nxt:
                    edge_groups.setdefault((state, nxt), []).append(symbol)
        edge_labels = {}
        for (frm, to), symbols in edge_groups.items():
            label = ", ".join(sorted(symbols))
            G.add_edge(frm, to, label=label)
            edge_labels[(frm, to)] = label
        return G, edge_labels

    def _layout(self, G, dfa: DFA) -> dict:
        nodes = list(G.nodes())
        n     = len(nodes)
        if n == 0:
            return {}
        ordered = [dfa.start_state] + \
                  [s for s in nodes if s != dfa.start_state and s != DEAD]
        if DEAD in nodes:
            ordered.append(DEAD)
        if n <= 8:
            pos = {state: (i * 2.0, 0.0) for i, state in enumerate(ordered)}
            if DEAD in pos:
                dead_x = pos[DEAD][0]
                pos[DEAD] = (dead_x, -1.5)
        else:
            pos = nx.spring_layout(G, seed=42)
        return pos


    def _node_styles(self, dfa, nodes, current_state, result=None):
        colors, edge_colors, lws = [], [], []
        for state in nodes:
            is_current = state == current_state
            if is_current and result == "accepted":
                colors.append(C_ACCEPTED)
                edge_colors.append("#228B22")
                lws.append(3.0)
            elif is_current and result == "rejected":
                colors.append(C_REJECTED)
                edge_colors.append(BORDER_ACTIVE)
                lws.append(3.0)
            elif is_current:
                colors.append(C_CURRENT)
                edge_colors.append(BORDER_ACTIVE)
                lws.append(3.0)
            elif state == DEAD:
                colors.append(C_DEAD_NODE)
                edge_colors.append(BORDER_DEAD)
                lws.append(1.5)
            else:
                colors.append(C_DEFAULT)
                edge_colors.append(BORDER_DEF)
                lws.append(1.5)
        return colors, edge_colors, lws

    def _resolve_active_edge(self, dfa, active_transition):
        if not active_transition:
            return None
        frm, sym = active_transition
        to = dfa.get_next_state(frm, sym)
        return (frm, to) if to else None

    def _edge_styles(self, dfa, edges, active_edge):
        colors, lws, styles = [], [], []
        for frm, to in edges:
            is_active = active_edge and (frm, to) == active_edge
            is_dead   = frm == DEAD and to == DEAD
            if is_active:
                colors.append(C_ACTIVE_EDG); lws.append(2.5); styles.append("solid")
            elif is_dead:
                colors.append(C_DEAD_EDG);   lws.append(1.0); styles.append("dashed")
            else:
                colors.append(C_DEFAULT_EDG); lws.append(1.5); styles.append("solid")
        return colors, lws, styles

    def _draw_start_arrow(self, ax, pos, start_state):
        if start_state not in pos:
            return
        x, y = pos[start_state]
        ax.annotate("", xy=(x - 0.35, y), xytext=(x - 0.75, y),
                    arrowprops=dict(arrowstyle="->", color="black", lw=1.8),
                    annotation_clip=False)

    def _draw_legend(self, ax, result):
        items = [
            mpatches.Patch(facecolor=C_CURRENT,   edgecolor=BORDER_ACTIVE, label="Current state"),
            mpatches.Patch(facecolor=C_ACCEPTED,  edgecolor="#228B22",     label="Accepted"),
            mpatches.Patch(facecolor=C_REJECTED,  edgecolor=BORDER_ACTIVE, label="Rejected"),
            mpatches.Patch(facecolor=C_DEAD_NODE, edgecolor=BORDER_DEAD,   label="DEAD state"),
        ]
        ax.legend(handles=items, loc="upper right", fontsize=8, framealpha=0.85)
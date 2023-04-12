import os
import ast
import tkinter as tk
import customtkinter as ctk
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from Algorithms import ucs, util, astar


ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

plot = None
canvas_frame = None

def main():
    #create main window
    main_window = ctk.CTk()
    main_window.geometry("800x600")
    main_window.title("Path Finding")

    nodes = ctk.StringVar(value=[])
    adj_matrix = ctk.StringVar(value=[[]])
    
    #create the options frame
    options_frame = ctk.CTkFrame(main_window)
    options_frame.pack(padx=20, pady=20, side="left", fill="both")

    #add text to the options frame with font size 12
    ctk.CTkLabel(options_frame, text="Choose Algorithm", font=("Arial", 16)).pack(padx=10, pady=10)

    #create variable to store selected option
    selected_algorithm = ctk.StringVar()

    # create option radio buttons
    ucsButton = ctk.CTkRadioButton(options_frame, text="Uniform Cost Search", variable=selected_algorithm, value="UCS")
    aStarButton = ctk.CTkRadioButton(options_frame, text="A Star Search", variable=selected_algorithm, value="A*")

    #pack the option buttons
    ucsButton.pack(anchor="w", padx=20, pady=10)
    aStarButton.pack(anchor="w", padx=20, pady=10)

    filename_label = ctk.CTkLabel(options_frame, text="Selected file: None", font=("Arial", 14))
    filename_label.pack(anchor="w", padx=20, pady=20)

    # add open file button
    openFileButton = ctk.CTkButton(options_frame, text="Open File", command=lambda: openFileButton_clicked(filename_label, adj_matrix, nodes))
    openFileButton.pack(anchor="w", padx=20, pady=10)

    # add starting node label
    startingNodeLabel = ctk.CTkLabel(options_frame, text="Choose Starting Node", font=("Arial", 12))
    startingNodeLabel.pack(anchor="w", padx=20, pady=5)

    # add starting node dropdown menu
    
    starting_node = ctk.StringVar()
    startingNodeDropdown = ctk.CTkOptionMenu(options_frame, variable=starting_node, values=nodes.get())
    startingNodeDropdown.pack(anchor="w", padx=20, pady=5)

    # add starting node label
    startingNodeLabel = ctk.CTkLabel(options_frame, text="Choose Finishing Node", font=("Arial", 12))
    startingNodeLabel.pack(anchor="w", padx=20, pady=5)

    # add finishing node dropdown menu
    finishing_node = ctk.StringVar()
    finishingNodeDropdown = ctk.CTkOptionMenu(options_frame, variable=finishing_node, values=nodes.get())
    finishingNodeDropdown.pack(anchor="w", padx=20, pady=5)

    # add Find Path button
    findPathButton = ctk.CTkButton(options_frame, text="Find Path",
        command=lambda: findPathButton_clicked(selected_algorithm.get(), starting_node.get(), finishing_node.get(), adj_matrix.get(), nodes.get()))
    findPathButton.pack(anchor="w", padx=20, pady=20)

    canvas_frame = ctk.CTkFrame(main_window, height=600)
    canvas_frame.pack(padx=20, pady=20, fill="both", expand=True)

    canvas = ctk.CTkCanvas(canvas_frame)
    canvas.pack(fill="both", expand=True)

    route_label = ctk.CTkLabel(canvas_frame, text="Route: ", font=("Arial", 14))
    route_label.pack(anchor="w", padx=10, pady=10)

    cost_label = ctk.CTkLabel(canvas_frame, text="Cost: ", font=("Arial", 14))
    cost_label.pack(anchor="w", padx=10, pady=10)

    def openFileButton_clicked(filename_label, adj_matrix, nodes):
        if selected_algorithm.get() == "":
            show_popup("Please select an algorithm first")
        else:
            file_path = open_file()
            if file_path != "":
                filename_label.configure(text="Selected file: " + os.path.basename(file_path))
                graph = util.read_graph(file_path)
                nodes.set(graph[0])
                adj_matrix.set(graph[1])
                nodes_list = [item.strip('\'\'') for item in nodes.get().strip('()').split(', ')]
                startingNodeDropdown.configure(values=nodes_list)
                finishingNodeDropdown.configure(values=nodes_list)
    
    def findPathButton_clicked(algorithm, starting_node, finishing_node, adj_matrix, nodes):
        if algorithm == "":
            show_popup("Please select an algorithm first")
        elif starting_node == "":
            show_popup("Please select a starting node")
        elif finishing_node == "":
            show_popup("Please select a finishing node")
        else:
            if algorithm == "UCS":
                nodes_list = [item.strip('\'\'') for item in nodes.strip('()').split(', ')]
                adj_list = string_to_adj_matrix(adj_matrix)
                result = ucs.ucs(adj_list, nodes_list.index(starting_node), nodes_list.index(finishing_node), nodes_list)
                add_graph(adj_list, result[1], nodes_list, result[0])
    
    # use networkx to draw graph in a frame
    def add_graph(adj_list, path, nodes, cost):
        
        global plot
        if plot:
            plot.get_tk_widget().destroy()
            #clear the matplotlib figure
            plt.clf()
        G = nx.Graph()
        for i in range(len(adj_list)):
            for neighbor, weight in adj_list[i]:
                G.add_edge(nodes[i], nodes[neighbor], weight=weight)

        node_colors = ['red' if i in path else 'blue' for node in G.nodes()]
        edge_colors = ['red' if (u, v) in zip(path, path[1:]) or (v, u) in zip(path, path[1:]) else 'black' for u, v in G.edges()]
        pos = nx.spring_layout(G)
        nx.draw_networkx(G, pos, node_color=node_colors, edge_color=edge_colors, with_labels=True)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

        # show the plot on the canvas
        fig = plt.gcf()
        plot = FigureCanvasTkAgg(fig, master=canvas)
        plot.draw()
        plot.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # add cost label
        cost_label.configure(text="Cost: "+str(cost))

        # add route label
        route_label.configure(text="Route: "+str(path))
        

    main_window.mainloop()

def create_canvas_frame(main_window):
    global canvas_frame
    canvas_frame = ctk.CTkFrame(main_window, height=600)
    canvas_frame.pack(padx=20, pady=20, fill="both", expand=True)
    

def open_file():
    file_path = ctk.filedialog.askopenfilename(
        title="Select a Text File", 
        filetypes=[("Text Files", "*.txt")]
    )
    return file_path

def show_popup(message):
    tk.messagebox.showinfo("Popup Message", message)

def string_to_adj_matrix(adj_matrix_string):
    adj_matrix = ast.literal_eval(adj_matrix_string)
    adj_list = [list(t) for t in adj_matrix]
    return adj_list
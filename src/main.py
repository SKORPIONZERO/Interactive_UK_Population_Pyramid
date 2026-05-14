import merge_data
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.animation import FuncAnimation, PillowWriter

def Filter(df, year):
    """Filters the dataframe by year"""
    filtered = df[df["Year"] == year]
    return filtered

def SetLimits(ax, max_val):
    """Sets limits for the width of the diagram based on the entire census data"""
    buffer = 2
    dynamic_limit = max_val * buffer
    ax.set_xlim(-dynamic_limit, dynamic_limit)

def SetDiagramCharacteristics(ax, max_val):
    """Removes the borders of the diagram, sets limits and removes ticks from y-axis"""
    SetLimits(ax, max_val)
    for i in ["top", "right", "bottom", "left"]:
        ax.spines[i].set_visible(False)
    ax.get_xaxis().set_visible(False)
    ax.tick_params(axis='y', which='major', pad=-50, left=False)
    ax.figure.subplots_adjust(bottom=0.10)

def UpdateDiagram(df, year, males, females, ax, fig):
    """Updates the values for the diagram"""
    filtered = Filter(df, year)
    for txt in list(ax.texts):
        txt.remove()
    for rect, val in zip(males.patches, filtered["Males"]):
        rect.set_width(val)
    for rect, val in zip(females.patches, filtered["Females"]):
        rect.set_width(-val)
    ax.bar_label(males, padding=3, labels=[f"{round(val, -3):,}" for val in filtered["Males"]])
    ax.bar_label(females, padding=3, labels=[f"{round(val, -3):,}" for val in filtered["Females"]])
    ax.set_title(f"Population of the UK in {year}", size=18, weight="bold")
    fig.canvas.draw_idle()

def ProcessSlider(years, df, males, females, ax, fig):
    """Creates the slider and monitors its value"""
    ax_slider = plt.axes([0.60, 0.05, 0.25, 0.03])
    slider = Slider(ax=ax_slider, label="Year ", valmin=years[0], valmax=years[-1], valinit=years[0], valfmt="%d")
    slider.valtext.set_position((1.03, 0.5))
    UpdateDiagram(df, years[0], males, females, ax, fig)
    slider.on_changed(lambda val: UpdateDiagram(df, int(val), males, females, ax, fig))
    return slider

def animate(df, ax, max_val, year):
    ax.clear()
    SetDiagramCharacteristics(ax, max_val)
    filtered = Filter(df, year)
    males = ax.barh(y=filtered["Age Group"], width=filtered["Males"], color="#64E8E0")
    females = ax.barh(y=filtered["Age Group"], width=-filtered["Females"], color="#57E8A9")
    ax.bar_label(males, padding=3, labels=[f"{round(val, -3):,}" for val in filtered["Males"]])
    ax.bar_label(females, padding=3, labels=[f"{round(val, -3):,}" for val in filtered["Females"]])
    ax.set_title(f"Population of the UK in {year}", size=18, weight="bold")
    ax.legend([males, females], ["Males", "Females"])

def main():
    """Main function: Retrieves the dataframe, creates the figure, sets the maximum value for the axis and creates a slider"""
    Save = input("Would you like to save the animation(y/n): ")
    df = merge_data.CreateDataFrame(path_to_census=r"./census")
    years = sorted(df['Year'].unique())
    max_val = round(max([df["Males"].max(), df["Females"].max()]), -3)
    fig, ax = plt.subplots(figsize=(12, 7))
    if Save == "y":
        file_name = input("Input the file name: ")
        animation = FuncAnimation(fig, lambda val: animate(df, ax, max_val, int(val)), frames=range(df["Year"].min(), df["Year"].max()+1))
        animation.save(f"./results/{file_name}.gif", dpi=300, writer=PillowWriter(fps=5))
    else:
        SetDiagramCharacteristics(ax, max_val)
        initial_data = Filter(df, years[0])
        males = ax.barh(y=initial_data["Age Group"], width=initial_data["Males"], color="#64E8E0")
        females = ax.barh(y=initial_data["Age Group"], width=-initial_data["Females"], color="#57E8A9")
        ax.legend([males, females], ["Males", "Females"])
        slider = ProcessSlider(years, df, males, females, ax, fig)
        slider.reset()
    mng = plt.get_current_fig_manager()
    mng.window.wm_geometry(f"+180+10")
    plt.show()

if __name__ == "__main__":
    main()

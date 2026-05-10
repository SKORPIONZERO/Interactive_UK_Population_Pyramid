import merge_data
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def Filter(df, year):
    """Filters the dataframe by year"""
    filtered = df[df["Year"] == year]
    return filtered


def SetLimits(ax, max_val):
    """Sets limits for the width of the diagram based on the entire census data"""
    buffer = 2
    dynamic_limit = max_val * buffer
    ax.set_xlim(-dynamic_limit, dynamic_limit)


def SetDiagramCharacteristics(ax, year, max_val):
    """Removes the borders of the diagram, sets limits, removes ticks from y-axis and sets title"""
    SetLimits(ax, max_val)
    for i in ["top", "right", "bottom", "left"]:
        ax.spines[i].set_visible(False)
    ax.get_xaxis().set_visible(False)
    ax.tick_params(left=False)
    ax.figure.subplots_adjust(bottom=0.10)
    ax.set_title(f"Population of the UK in {year}", size=18, weight="bold")


def UpdateDiagram(df, ax, fig, year, max_val):
    """Prepares the axes for the diagram and sets parameters for the diagram"""
    ax.clear()
    filtered = Filter(df, year)
    males = ax.barh(y=filtered["Age Group"], width=filtered["Males"], color="#64E8E0")
    females = ax.barh(y=filtered["Age Group"], width=-filtered["Females"], color="#57E8A9")
    ax.bar_label(males, padding=3, labels=[f"{round(label, -3):,}" for label in filtered["Males"]])
    ax.bar_label(females, padding=3, labels=[f"{round(label, -3):,}" for label in filtered["Females"]])
    ax.legend([males, females], ["Males", "Females"])
    SetDiagramCharacteristics(ax, year, max_val)
    fig.canvas.draw_idle()


def ProcessSlider(years, df, ax, fig, max_val):
    ax_slider = plt.axes([0.60, 0.05, 0.25, 0.03])
    slider = Slider(ax=ax_slider, label="Year ", valmin=years[0], valmax=years[-1], valinit=years[0], valfmt="%d")
    slider.valtext.set_position((1.03, 0.5))
    slider.on_changed(lambda val: UpdateDiagram(df, ax, fig, int(val), max_val))


def main():
    """Main function: Retrieves the dataframe, creates the figure, sets the maximum value for the axis and creates a slider"""
    df = merge_data.CreateDataFrame(path_to_census=r".\Census")
    years = sorted(df['Year'].unique())
    max_val = round(max([df["Males"].max(), df["Females"].max()]), -3)
    fig, ax = plt.subplots(figsize=(12, 6))
    ProcessSlider(years, df, ax, fig, max_val)
    UpdateDiagram(df, ax, fig, years[0], max_val)
    plt.show()


if __name__ == "__main__":
    main()

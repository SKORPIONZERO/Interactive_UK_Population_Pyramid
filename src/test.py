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



def SetDiagramCharacteristics(ax, max_val):
    """Removes the borders of the diagram, sets limits, removes ticks from y-axis and sets title"""
    SetLimits(ax, max_val)
    for i in ["top", "right", "bottom", "left"]:
        ax.spines[i].set_visible(False)
    ax.get_xaxis().set_visible(False)
    ax.tick_params(left=False)
    ax.figure.subplots_adjust(bottom=0.10)




def UpdateDiagram(df, year, male_bars, female_bars, male_labels, female_labels, ax, fig):
    filtered = Filter(df, year)
    # Update Bar Widths
    for rect, val in zip(male_bars.patches, filtered["Males"]):
        rect.set_width(val)
    for rect, val in zip(female_bars.patches, filtered["Females"]):
        rect.set_width(-val)

    # Update Bar Labels (Text and Position)
    for txt, val in zip(male_labels, filtered["Males"]):
        txt.set_text(f"{round(val, -3):,}")
        txt.set_x(val)
    for txt, val in zip(female_labels, filtered["Females"]):
        txt.set_text(f"{round(val, -3):,}")
        txt.set_x(-val)

    ax.set_title(f"Population of the UK in {year}", size=18, weight="bold")
    fig.canvas.draw_idle()


def main():
    df = merge_data.CreateDataFrame(path_to_census=r".\Census")
    years = sorted(df['Year'].unique())
    max_val = round(max([df["Males"].max(), df["Females"].max()]), -3)

    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Initial Draw
    initial_data = Filter(df, years[0])
    males = ax.barh(y=initial_data["Age Group"], width=initial_data["Males"], color="#64E8E0")
    females = ax.barh(y=initial_data["Age Group"], width=-initial_data["Females"], color="#57E8A9")
    
    # bar_label returns a list of Text objects we can modify
    m_labels = ax.bar_label(males, padding=3)
    f_labels = ax.bar_label(females, padding=3)
    
    ax.legend([males, females], ["Males", "Females"])
    SetDiagramCharacteristics(ax, max_val)
    
    # Slider setup
    ax_slider = plt.axes([0.60, 0.05, 0.25, 0.03])
    slider = Slider(ax=ax_slider, label="Year ", valmin=years[0], valmax=years[-1], valinit=years[0], valfmt="%d")
    slider.valtext.set_position((1.03, 0.5))

    
    # Link slider to the new update function
    slider.on_changed(lambda val: UpdateDiagram(df, int(val), males, females, m_labels, f_labels, ax, fig))
    
    # Initial title
    ax.set_title(f"Population of the UK in {years[0]}", size=18, weight="bold")
    
    plt.show()

if __name__ == "__main__":
    main()

import pandas as pd
import matplotlib.pyplot as plt


def table(data,save_img=None):
    df = pd.DataFrame(data)
    fig, ax = plt.subplots(figsize=(2, len(df)*0.5 + 1))
    ax.axis('off') 

    table_plot = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc='center',
        loc='center'
    )

    # Styling warna hitam dan teks putih
    table_plot.auto_set_font_size(False)
    table_plot.set_fontsize(12)

    # Set row height (jarak antar baris)
    for (i,j), cell in table_plot.get_celld().items():
        cell.set_height(0.07)
        if i == 0:
            cell.set_facecolor("#8C8C8C") 
            cell.set_text_props(color="black", weight="bold")
        else:
            cell.set_facecolor("#FFFFFF")
            
    table_plot.auto_set_column_width(col=list(range(len(df.columns))))
   
    if save_img:
        plt.savefig(save_img, bbox_inches='tight', dpi=300)
        
    plt.show() 
    return table_plot
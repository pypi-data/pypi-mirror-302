import pandas as pd
import altair as alt
import random
import colorsys   # converting between color spaces RGB to HSV


def rgb_to_hsv(r, g, b):
    """
    Convert an RGB color to HSV.
    Input: r, g, b - values between 0 and 255.
    Output: Corresponding hue, saturation, and value in the range [0, 1].
    """
    return colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)

def generate_gradient_hue_color(index, total, color_base_rgb):
    """
    Generate a gradient color by varying the hue in HSV color space, starting from a base RGB color.
    - index: Position of the current color in the gradient.
    - total: Total number of colors to generate.
    - color_base_rgb: A tuple (R, G, B) for the base color in the RGB space.
   
    Returns: Hex color string.
    """
    # Convert the RGB color base to HSV
    base_r, base_g, base_b = color_base_rgb
    base_hue, base_saturation, base_value = rgb_to_hsv(base_r, base_g, base_b)
   
    # Ensure index is between 0 and total - 1
    fraction = index / total if total > 0 else 0
   
    # Adjust the hue to create a gradient (varying hue)
    hue = (base_hue * 360 + fraction * 360) % 360  # Keep hue in the range [0, 360]
   
    # Convert HSV to RGB
    r, g, b = colorsys.hsv_to_rgb(hue / 360.0, base_saturation, base_value)
   
    # Convert the RGB values to hex format
    return '#{:02x}{:02x}{:02x}'.format(int(r * 255), int(g * 255), int(b * 255))


def generate_gradient_rgb_color(index, total, color_base):
    """
    Generate a color based on the index in the gradient scale.
    color_base is a tuple representing the base RGB color (0-1 scale).
    """
    fraction = index / (total - 1) if total > 1 else 0
    r, g, b = [(1 - fraction) * base + fraction * 1.0 for base in color_base]  # Linear interpolation
    return '#{:02x}{:02x}{:02x}'.format(int(r * 255), int(g * 255), int(b * 255))

def generate_unique_color():
    """Generate a random but unique hex color."""
    r, g, b = [random.randint(0, 255) for _ in range(3)]
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def assign_hue_colors_to_columns(
    rois_list:list,     
    columns_list:list, 
    color_base_rgb: dict = {'red':  (255, 0, 0),
                         'green': (0, 255, 0),
                         'blue': (0, 0, 255),                         
                         } ):
    """
    Assign a color gradient for each ROI and RGB parameter (red, green, blue).
    If the column doesn't have ROI or RGB, assign a random unique color.
   
    Parameters:
    - rois_list: List of regions of interest (ROIs).
    - columns_list: List of column names.
    - color_base_rgb: Dictionary with the base colors (R, G, B) for gradient generation.
   
    Returns: Dictionary mapping column names to hex color strings.
    """
    # Initialize the result dictionary
    column_colors = {}
   
    # Keep track of unique random colors for non-RGB/ROI columns
    used_colors = set()
   
    # Iterate through the column list
    for column in columns_list:
        # Check if the column corresponds to any ROI
        assigned = False
        for i, roi in enumerate(rois_list):
            if roi in column:
                # Check if it's related to red, green, or blue
                for color_name in ['red', 'green', 'blue']:
                    if color_name in column:
                        # Assign a gradient hue color based on the ROI index                        
                        gradient_color = generate_gradient_hue_color(i, len(rois_list)+3, color_base_rgb[color_name] )
                        column_colors[column] = gradient_color
                        assigned = True
                        break
            if assigned:
                break
       
        # If the column doesn't match any ROI or RGB, assign a unique random color
        if not assigned:
            unique_color = generate_unique_color()
            while unique_color in used_colors:
                unique_color = generate_unique_color()
            column_colors[column] = unique_color
            used_colors.add(unique_color)
   
    return column_colors


import altair as alt
import pandas as pd

def plot_time_series_by_doy(df: pd.DataFrame, 
                            columns_to_plot: list = None, 
                            plot_options: dict = None, 
                            title: str = 'Time Series Plot', 
                            width: int = 600, 
                            height: int = 400, 
                            interactive: bool = True,
                            substrings: list = None,
                            exclude_columns: list = None,
                            group_by: str = None,
                            facet: bool = False,
                            rois_list: list = None,
                            show_legend: bool = True,
                            legend_position: str = 'right',
                            use_gradient: bool = True):
    """
    Plots a time series using Altair from a pandas DataFrame, focusing on the range of day_of_year
    where data exists, with optional plot customizations and general properties.

    Parameters:
    df (pd.DataFrame): DataFrame containing the data.
    columns_to_plot (list): List of column names to plot on the y-axis. 
                            If None, columns are selected based on `substrings`.
    plot_options (dict): Optional dictionary with customization for each column. The keys are the column names, 
                         and the values are dictionaries with Altair properties like:
                         - 'mark_type' (str): Mark type for the chart (e.g., 'line', 'point', 'bar').
                         - 'color' (str): Color of the line or points.
                         - 'axis' (str): Either 'left' or 'right' to specify which y-axis to use.
                         - 'size' (float): Size of the points (if using points).
                         - 'opacity' (float): Opacity level for the mark.
                         - 'strokeWidth' (float): Width of the line if using line marks.
    title (str): Title of the chart. Defaults to 'Time Series Plot'.
    width (int): Width of the chart. Defaults to 600.
    height (int): Height of the chart. Defaults to 400.
    interactive (bool): Whether the chart should be interactive (zoomable, scrollable). Defaults to True.
    substrings (list): List of substrings to select columns by matching names containing any of them. Defaults to None.
    exclude_columns (list): List of columns to exclude from the selected columns. Defaults to None.
    group_by (str): Optional column name to group the data by (e.g., 'year'). Defaults to None.
    facet (bool): Whether to create a faceted plot by 'group_by'. Defaults to False.
    rois_list (list): List of ROI substrings to identify and plot. Defaults to None (plot all ROIs).
    show_legend (bool): Whether to show the legend. Defaults to True.
    legend_position (str): Position of the legend on the chart. Defaults to 'right'.

    Returns:
    alt.Chart: The Altair chart object.
    """
    
    # Ensure that 'day_of_year' is in the DataFrame
    if 'day_of_year' not in df.columns:
        raise ValueError("'day_of_year' column is required in the DataFrame")

    # Handle column selection based on substrings and exclusions
    if substrings:
        selected_columns = []
        
        # Iterate over the substrings and filter columns containing any of them
        for substring in substrings:
            selected_columns.extend([col for col in df.columns if substring in col]) 
        
        # Remove duplicates in case a column matches multiple substrings
        selected_columns = list(set(selected_columns))
        
        # If no columns were found, or substrings list is empty, use all columns in columns_to_plot
        if not selected_columns:
            selected_columns = columns_to_plot if columns_to_plot else df.columns.tolist()
            
        # Handle exclusion of columns
        if exclude_columns:
            selected_columns = [col for col in selected_columns if col not in exclude_columns]
        
    else:
        # If substrings is None or empty, use all columns_to_plot
        selected_columns = columns_to_plot if columns_to_plot else df.columns.tolist()

        # Handle exclusion of columns
        if exclude_columns:
            selected_columns = [col for col in selected_columns if col not in exclude_columns]

    # Ensure 'day_of_year' is not part of the selected columns
    if 'day_of_year' in selected_columns:
        selected_columns.remove('day_of_year')

    # If no columns were specified after processing, raise an error
    if not selected_columns:
        raise ValueError("No columns specified for plotting.")

    # Filter out rows where all selected columns are NaN
    df_filtered = df.dropna(subset=selected_columns, how='all')

    # Focus only on the range of day_of_year where data exists
    min_day = df_filtered['day_of_year'].min()
    max_day = df_filtered['day_of_year'].max()

    df_filtered = df_filtered[(df_filtered['day_of_year'] >= min_day) & (df_filtered['day_of_year'] <= max_day)]

    # Melt the dataframe to long format for Altair plotting
    id_vars = ['year', 'day_of_year']
    
    # If grouping by 'year' or another column, include it as an identifier
    if group_by and group_by in df.columns:
        id_vars.append(group_by)

    # Melt the DataFrame
    df_melted = df_filtered.melt(
        id_vars=id_vars,
        value_vars=selected_columns, 
        var_name='variable', value_name='value')

    # Extract ROI numbers from the variable names, format as ROI_01, ROI_02, etc.
    df_melted['roi'] = df_melted['variable'].str.extract(r'(ROI_\d+)')

    # Extract color substrings from variable names (e.g., red, green, blue)
    df_melted['color_group'] = df_melted['variable'].apply(lambda x: 'red' if 'red' in x.lower() else ('green' if 'green' in x.lower() else 'blue'))

    # Create gradient color scales
    color_scales = {
        'red':  ['#890200',  '#c60200', '#ff0605', '#ff4242'],   
        'green': ['#33691e', '#4ebe21', '#78f047', '#b1ff91'],   
        'blue': ['#020873', '#0648b8', '#13adf4', "#5bf5f5"],   
    }
    
    
    # Set color palettes for each color group (red, green, blue)
    red_palette = ['#890200',  '#c60200', '#ff0605', '#ff4242']  # darker to lighter shades of red
    green_palette = ['#33691e', '#4ebe21', '#78f047', '#b1ff91']  # lighter to darker shades of green
    blue_palette = ['#020873', '#0648b8', '#13adf4', "#5bf5f5"]  # lighter to darker shades of blue

    # Map colors based on roi and color group
    def get_color(roi, color_group):
        roi_index = rois_list.index(roi) if roi in rois_list else 0
        if color_group == 'red':
            return red_palette[roi_index % len(red_palette)]
        elif color_group == 'green':
            return green_palette[roi_index % len(green_palette)]
        elif color_group == 'blue':
            return blue_palette[roi_index % len(blue_palette)]
        return '#000000'  # fallback to black if no color group found

    # Apply the color assignment
    df_melted['color'] = df_melted.apply(lambda row: get_color(row['roi'], row['color_group']), axis=1)

    # Define ROI shapes for point markers
    roi_symbols = ['circle', 'square', 'triangle', 'diamond', 'cross', 'star']  # Example shapes for ROIs
    df_melted['shape'] = df_melted['roi'].apply(lambda roi: roi_symbols[rois_list.index(roi) % len(roi_symbols)] if roi in rois_list else 'circle')

    # Initialize the base chart
    base = alt.Chart(df_melted).encode(
        x='day_of_year:Q'
    )

    # Container for layers
    layers = []

    # Add each column with custom options (if provided)
    for column in selected_columns:
        # Default options
        mark_type = 'line'  # Default to line
        color = 'variable:N'  # Default to Altair's color scheme
        y_axis = alt.Y('value:Q')  # Default to single y-axis
        size = 30 # default size for points marks
        opacity = 1.0
        strokeWidth = 2.0  # Default line width for line marks
        shape = 'circle'  # Default shape for points

        # Apply custom options if available
        if plot_options and column in plot_options:
            # Set mark_type (e.g., line, point, bar)
            if 'mark_type' in plot_options[column]:
                mark_type = plot_options[column]['mark_type']
            
            # Set color
            if 'color' in plot_options[column]:
                color = alt.value(plot_options[column]['color'])
            else:
                color = None  # Default to None if not specified
            
            # Set y-axis (left or right)
            if 'axis' in plot_options[column]:
                if plot_options[column]['axis'] == 'right':
                    y_axis = alt.Y('value:Q', axis=alt.Axis(title=column, orient='right'))
                else:
                    y_axis = alt.Y('value:Q', axis=alt.Axis(title=column, orient='left'))
            
            # Set size (for point marks)
            if 'size' in plot_options[column]:
                size = plot_options[column]['size']

            # Set opacity
            if 'opacity' in plot_options[column]:
                opacity = plot_options[column]['opacity']
            
            # Set stroke width (for line marks)
            if 'strokeWidth' in plot_options[column]:
                strokeWidth = plot_options[column]['strokeWidth']

        # Determine color scale based on the variable's color
        variable_color = df_melted[df_melted['variable'] == column]['color'].iloc[0]

        if use_gradient:
            color_scale = color_scales.get(variable_color, alt.value('gray'))
        else:
            # Use plain colors if gradients are not used
            color_map = {
                'red': 'red',
                'green': 'green',
                'blue': 'blue'
            }
            color_scale = alt.value(color_map.get(variable_color, 'gray'))
        
        # Add layer based on mark type
        if mark_type == 'line':
            layer = base.mark_line(strokeWidth=strokeWidth, opacity=opacity).encode(
                y=y_axis,
                color=alt.Color('color:N', legend=alt.Legend(title='Color', orient=legend_position) if show_legend else None, title='Color'),
                shape=alt.Shape('shape:N', legend=alt.Legend(title='ROI', orient=legend_position) if show_legend else None, title='ROI'),
            ).transform_filter(
                alt.datum.variable == column
            )
        elif mark_type == 'point':
            layer = base.mark_point(size=size, opacity=opacity).encode(
                y=y_axis,
                color=alt.Color('color:N', legend=alt.Legend(title='Color', orient=legend_position) if show_legend else None, title='Color'),
                shape=alt.Shape('shape:N', legend=alt.Legend(title='ROI', orient=legend_position) if show_legend else None, title='ROI'),
            ).transform_filter(
                alt.datum.variable == column
            )
        elif mark_type is None:
            layer = base.mark_line(strokeWidth=strokeWidth, opacity=opacity).encode(
                y=y_axis,
                color=alt.Color('color:N', legend=alt.Legend(title='Color', orient=legend_position) if show_legend else None, title='Color'),
                shape=alt.Shape('shape:N', legend=alt.Legend(title='ROI', orient=legend_position) if show_legend else None, title='ROI'),
            ).transform_filter(
                alt.datum.variable == column
            )
            layer2 = base.mark_point(size=size, opacity=opacity).encode(
                y=y_axis,
                color=alt.Color('color:N', legend=alt.Legend(title='Color', orient=legend_position) if show_legend else None, title='Color'),
                shape=alt.Shape('shape:N', legend=alt.Legend(title='ROI', orient=legend_position) if show_legend else None, title='ROI'),
            ).transform_filter(
                alt.datum.variable == column
            )
            layers.append(layer2)
        else:  # Fallback for unsupported marks
            layer = base.mark_line(strokeWidth=strokeWidth).encode(
                y=y_axis,
                color=alt.Color('roi:N', scale=color_scale, legend=None if not show_legend else alt.Legend(orient=legend_position)),
                shape=alt.Shape('roi:N', legend=None if not show_legend else alt.Legend(orient=legend_position))
            ).transform_filter(
                alt.datum.variable == column
            )

        layers.append(layer)

    # Combine all layers into one chart
    chart = alt.layer(*layers).properties(
        width=width,
        height=height,
        title=title
    )

    # Add interactivity if specified
    if interactive:
        chart = chart.interactive()

    # Group by the 'group_by' column if specified
    if group_by and group_by in df.columns:
        if facet:
            # Create a faceted chart
            chart = chart.facet(
                facet=alt.Facet(f'{group_by}:N', columns=3),
                columns=3
            )
        else:
            # Overlay the lines and color by 'group_by'
            chart = chart.encode(
                color=f'{group_by}:N'
            )

    # Adjust legend position if required
    if show_legend:
        chart = chart.configure_legend(
            orient=legend_position
        )

    return chart



def layer_altair_charts(charts, x_scale_type='shared'):
    """ Layers multiple Altair charts and optionally allows for independent or shared x-axis. 
    Parameters: 
    	- charts (list): A list of Altair chart objects to layer. 
     	- x_scale_type (str): Determines if the x-axes are 'shared' (default) or 'independent'.  
      		Use 'independent' for separate x-axis scales on each chart. 
    Returns: 
      - alt.Chart: A layered Altair chart with the desired x-axis scale behavior. """
    
    if not charts or len(charts) == 0: 
        raise ValueError("You must provide at least one chart to layer.") 
    # Layer the charts together 
    layered_chart = alt.layer(*charts) 
    # Resolve x-axis scales based on the provided scale type 
    if x_scale_type == 'independent': 
        layered_chart = layered_chart.resolve_scale(x='independent') 
    elif x_scale_type == 'shared': 
        layered_chart = layered_chart.resolve_scale(x='shared') 
    else: 
        raise ValueError("Invalid x_scale_type. Use 'shared' or 'independent'.") 
	
    return layered_chart

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def main():
    '''
    This is the main function that serves as the entry point of the program.
    '''
    df = pd.read_csv('country_vaccinations.csv')
    df['date'] = pd.to_datetime(df['date'])
    plot_daily_vaccinations(df)
    calculate_correlation(df)
    countries_1 = ['China', 'United Kingdom', 'United States']
    column_name_1 = 'total_vaccinations'
    title_average_1 = '''Average total vaccinations vs. Date for China, ''' +\
                      '''United Kingdom, and United States'''
    plot_average(df, countries_1, column_name_1, 'Average total_vaccinations',
                 title_average_1)
    countries_2 = ['India', 'Spain', 'United States']
    column_name_2 = 'people_fully_vaccinated_per_hundred'
    title_average_2 = '''Average percentage of population vaccinated ''' +\
                      '''vs. Date for India, Spain, and United States'''
    plot_average(df, countries_2, column_name_2,
                 'Average percentage of population fully vaccinated',
                 title_average_2)


def plot_daily_vaccinations(df: pd.DataFrame):
    """
    Takes in a DataFrame containing daily vaccination data and plots the daily
    vaccination rates for the top 5 countries over time using Plotly.
    Returns None if ran correctly.
    """
    fig = go.Figure()
    grouped_df = df.groupby('country')
    top_5_countries = ["United States", "China", "Japan", "Germany",
                       "United Kingdom"]
    for country, group in grouped_df:
        group['date'] = pd.to_datetime(group['date'])
        df_downsampled = group.resample('W', on='date').mean()
        visible = country in top_5_countries
        fig.add_trace(go.Scatter(x=df_downsampled.index,
                                 y=df_downsampled['daily_vaccinations'],
                                 mode='lines+markers', name=country,
                                 visible=visible))
    fig.update_layout(
        xaxis_range=[df['date'].min(), df['date'].max()],
        xaxis_title='Date',
        yaxis_title='Daily Vaccinations',
        title='Daily Vaccination Rates',
        xaxis_tickangle=45,
        showlegend=True
    )
    buttons = [
        dict(label='Select All',
             method='update',
             args=[{'visible': [True] * len(fig.data)}, {'showlegend': True}]),
        dict(label='Reset',
             method='update',
             args=[{'visible': [country in top_5_countries for
                                country in df['country']]},
                   {'showlegend': True}])
    ]
    fig.update_layout(updatemenus=[dict(type="buttons", buttons=buttons,
                      x=0.99, y=1.15)])
    fig.show()


def calculate_correlation(df: pd.DataFrame):
    '''
    Calculates the correlation between daily vaccinations
    and total vaccinations for different countries
    and creates an interactive scatter plot using Plotly.
    '''
    title = '''Correlation between Daily Vaccinations and Total Vaccinations'''
    df.sort_values('date', inplace=True)
    fig = px.scatter(df, x='daily_vaccinations', y='total_vaccinations',
                     color='country',
                     hover_data=['date', 'country',
                                 'total_vaccinations_per_hundred'],
                     title=title)
    selected_countries = []

    def update_plot(trace: go.Scatter, state: dict[str]):
        '''
        Callback function to update the scatter plot based on the selected
        countries.
        '''
        selected_countries[:] = [country['label'] for country in state['new']]

        filtered_df = df[df['country'].isin(selected_countries)]

        scatter_data = dict(x=filtered_df['daily_vaccinations'],
                            y=filtered_df['total_vaccinations'],
                            text=filtered_df['country'],
                            color=filtered_df['country'])

        fig.data[0].update(scatter_data)

    fig.update_layout(
        updatemenus=[
            dict(
                buttons=[
                    dict(
                        label="Select All",
                        method="update",
                        args=[{"visible": True}, {"args": [{"visible": True}],
                                                  "label": "Select All"}],
                    ),
                    dict(
                        label="Clear Selection",
                        method="update",
                        args=[{"visible": True}, {"args": [{"visible": False}],
                                                  "label": "Clear Selection"}],
                    )
                ],
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.99,
                xanchor="right",
                y=1.15,
                yanchor="top"
            )
        ]
    )
    fig.data[0].on_selection(update_plot)
    fig.show()


def plot_average(df: pd.DataFrame, countries: list[str], column_name: str,
                 ylabel: str, title: str):
    '''
    Takes in a DataFrame, a list of countries, a column name, ylabel, and title
    and plots the average values of the specified column for the given
    countries over time using Plotly.
    '''
    filtered_df = df[df['country'].isin(countries)]
    df.loc[filtered_df.index, 'date'] = pd.to_datetime(filtered_df['date'])
    filtered_df = filtered_df.set_index('date')
    monthly_data = filtered_df[filtered_df[column_name].notnull() &
                               (filtered_df[column_name] != 0)].groupby(
                                'country')[column_name].resample('M').mean(
                                         ).reset_index()
    fig = px.line(monthly_data, x='date', y=column_name, color='country')
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title=ylabel,
        xaxis_tickangle=45,
        showlegend=True
    )
    fig.show()


if __name__ == '__main__':
    main()

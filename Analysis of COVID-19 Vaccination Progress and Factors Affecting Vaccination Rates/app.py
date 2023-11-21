'''
CSE 163 AC Final Project
Mike Deng, Dexin Sun, Yaqi Lu
6/4/2023

This Flask application uses Plotly to create interactive visualizations
based on COVID-19 vaccination data. The /average_vaccinations route renders
a template and plots the average total vaccinations and average percentage
of population fully vaccinated. The /plot route displays the daily vaccination
rates for different countries. The /correlation route calculates the
correlation between daily vaccinations and total vaccinations, creating an
interactive scatter plot.
'''

from flask import Flask, render_template
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

app = Flask(__name__, template_folder='templates')
df = pd.read_csv('country_vaccinations.csv')
top_5_countries = ["United States", "China", "Japan", "Germany",
                   "United Kingdom"]


@app.route('/')
def index():
    '''
    Renders the index.html template.
    '''
    return render_template('index.html')


@app.route('/average_vaccinations')
def average_vaccinations():
    '''
    Renders the average_vaccinations.html template and plots the average total
    vaccinations and average percentage of population fully vaccinated using
    Plotly.
    '''
    def plot_average(countries: list[str], column_name: str, ylabel: str,
                     title: str):
        '''
        Takes in a list of countries, a column name, ylabel, and title
        and plots the average values of the specified column for the given
        countries over time using Plotly.
        '''
        filtered_df = df[df['country'].isin(countries)]
        filtered_df['date'] = pd.to_datetime(filtered_df['date'])
        filtered_df = filtered_df.set_index('date')

        monthly_data = filtered_df[filtered_df[column_name].notnull() &
                                   (filtered_df[column_name] != 0)].\
            groupby('country')[column_name].resample('M').mean().\
            reset_index()
        fig = px.line(monthly_data, x='date', y=column_name, color='country')
        fig.update_layout(
            title=title,
            xaxis_title='Date',
            yaxis_title=ylabel,
            xaxis_tickangle=45,
            showlegend=True
        )

        plot_div = fig.to_html(full_html=False)
        return plot_div
    title_1 = 'Average total vaccinations vs. Date for China,' +\
        'United Kingdom, and United States'
    plot_div_1 = plot_average(['China', 'United Kingdom', 'United States'],
                              'total_vaccinations',
                              'Average total_vaccinations', title_1)
    plot_div_2 = plot_average(['India', 'Spain', 'United States'],
                              'people_fully_vaccinated_per_hundred',
                              'Average percentage of population' +
                              'fully vaccinated',
                              'Average percentage of population fully' +
                              'vaccinated vs. Date for India, Spain, and' +
                              'United States')
    return render_template('average_vaccinations.html', plot_div_1=plot_div_1,
                           plot_div_2=plot_div_2)


@app.route('/plot')
def plot():
    '''
    Renders the plot.html template and plots the daily vaccination
    rates for different countries.
    '''
    fig = go.Figure()
    grouped_df = df.groupby('country')
    for country, group in grouped_df:
        group['date'] = pd.to_datetime(group['date'])
        df_downsampled = group.resample('W', on='date').mean()
        visible = country in top_5_countries
        fig.add_trace(go.Scatter(x=df_downsampled.index,
                                 y=df_downsampled['daily_vaccinations'],
                                 mode='lines+markers', name=country,
                                 visible=visible))
    fig.update_layout(
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
             args=[{'visible': [country in top_5_countries for country in df[
                    'country']]},
                   {'showlegend': True}])
    ]
    fig.update_layout(updatemenus=[dict(type="buttons", buttons=buttons,
                      x=0.99, y=1.15)])
    plot_html = fig.to_html(full_html=False)
    return render_template('plot.html', plot_html=plot_html)


@app.route('/correlation')
def correlation():
    '''
    Renders the correlation.html template and
    Calculates the correlation between daily vaccinations
    and total vaccinations for different countries
    and creates an interactive scatter plot using Plotly.
    '''
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values('date', inplace=True)
    fig = px.scatter(df, x='daily_vaccinations', y='total_vaccinations',
                     color='country',
                     hover_data=['date', 'country',
                                 'total_vaccinations_per_hundred'],
                     title='Correlation between Daily Vaccinations' +
                           ' and Total Vaccinations')
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
    plot_html = fig.to_html(full_html=False)
    return render_template('correlation.html', plot_html=plot_html)


if __name__ == '__main__':
    app.run(debug=True)

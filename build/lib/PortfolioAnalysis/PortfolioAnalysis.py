import pandas as pd
import numpy as np

class PortfolioAnalysis:

    def __init__(self, returns, cumulative=False, auto_drop=True, window='M'):
        self.returns = self._auto_drop(returns, cumulative=cumulative) if auto_drop else returns
        self.cumulative_returns = returns if cumulative else self._ret_to_cum(self.returns, log=True)
        self.returns = self._cum_to_ret(returns, log=True) if cumulative else returns

        self.sharpe = self._calculate_sharpe(self.returns)
        self.sortino = self._calculate_sortino(self.returns)

        self.drawdown = self._calculate_dd(self.cumulative_returns)
        self.average_drawdown = self.drawdown.mean()
        self.mdd = self._calculate_mdd(self.drawdown)
        self.cagr = self._calculate_cagr(self.cumulative_returns, window=window)

    def report(self):
        from bokeh.plotting import figure, output_file, show
        from bokeh.models import ColumnDataSource
        from bokeh.layouts import column, row, widgetbox
        from bokeh.models.widgets import DataTable, TableColumn

        output_file('outfile.html')


        def to_source(df):
            df.index = pd.to_datetime(df.index, format="%Y-%m-%d")
            return ColumnDataSource(df)


        color_list = ['red', 'blue', 'green', 'black', 'grey']

        static_data = pd.concat([self.cagr, self.sharpe, self.sortino, self.mdd, self.average_drawdown],
                                axis=1)
        static_data.columns = ['CAGR', 'Sharpe ratio', 'Sortino ratio', 'MDD', 'Average drawdown']
        for col in static_data.columns:
            if col in ['CAGR', 'MDD', 'Average drawdown']:
                static_data.loc[:, col] = static_data.loc[:, col].apply(lambda x: str(np.around((x*100), decimals=2))+"%")
            else:
                static_data.loc[:, col] = static_data.loc[:, col].apply(lambda x: np.around(x, decimals=4))
        static_data = static_data.T.reset_index()
        static_data.rename(columns={'index':' '}, inplace=True)
        source = ColumnDataSource(static_data)
        columns = [TableColumn(field=col, title=col) for col in static_data.columns]
        data_table = DataTable(source=source, columns=columns, width=560, height=300)


        '''
        Plot cumulative returns
        '''
        source = to_source(self.cumulative_returns)
        p1 = figure(x_axis_type='datetime', title='Cumulative return', plot_width=600, plot_height=300)
        for i, col in enumerate(self.cumulative_returns.columns):
            p1.line(source=source, x='Date', y=col, color=color_list[i], legend=col + " Cumulative Return")
        p1.legend.location = "top_left"

        '''
        Plot log cumulative returns
        '''
        source = to_source(self.cumulative_returns.apply(np.log))
        p2 = figure(x_axis_type='datetime', title='Log-scale Cumulative return', plot_width=600, plot_height=300)
        for i, col in enumerate(self.cumulative_returns.columns):
            p2.line(source=source, x='Date', y=col, color=color_list[i], legend=col + " Cumulative Return")
        p2.legend.location = "top_left"

        '''
        Plot drawdown
        '''
        source = to_source(self.drawdown)
        p3= figure(x_axis_type='datetime', title='Drawdown', plot_width=600, plot_height=300)
        for i, col in enumerate(self.drawdown.columns):
            #p3.line(source=source, x='Date', y=col, color=color_list[i], legend=col + " Drawdown")
            baseline = np.zeros_like(self.drawdown[col].values)
            y = np.append(baseline, self.drawdown[col].values[::-1])
            x = self.drawdown.index.values
            x = np.append(x, x[::-1])
            p3.patch(x, y, color=color_list[i], fill_alpha=0.1)
        p3.legend.location = "bottom_right"

        show(column(row(p1, p2), row(p3, widgetbox(data_table))))


    def _array_to_df(self, arr):
        try:
            return pd.DataFrame(arr,
                              index=self.returns.index.values,
                              columns=self.returns.columns.values).rename_axis("Date")
        except:
            return pd.DataFrame(arr,
                                index=self.cumulative_returns.index.values,
                                columns=self.cumulative_returns.columns.values).rename_axis("Date")

    def _calculate_dd(self, df):
        max_list = None
        out_list = []
        for ix in df.index:
            if df.index.get_loc(ix) == 0:
                max_list = df.loc[ix].values

            max_list = np.max([max_list, df.loc[ix].values], axis=0)
            out_list.append(df.loc[ix].values / max_list - 1)

        out = self._array_to_df(out_list)
        return out

    @staticmethod
    def _calculate_cagr(df, window='M', num_of_days_for_D = 252):
        if window == 'Y':
            return (df.iloc[-1] / df.iloc[0] - 1).pow((1 / len(df.index))) - 1
        elif window == 'M':
            return (df.iloc[-1] / df.iloc[0] - 1).pow((1 / (len(df.index) / 12))) - 1
        elif window == 'D':
            return (df.iloc[-1] / df.iloc[0] - 1).pow((1 / (len(df.index) / num_of_days_for_D))) - 1
        else:
            raise NotImplementedError()

    @staticmethod
    def _calculate_mdd(df):
        return df.min()

    @staticmethod
    def _calculate_sharpe(df):
        return df.mean()/df.std()

    @staticmethod
    def _calculate_sortino(df):
        func = lambda x: 0 if x >= 0 else x
        tmp = df.applymap(func)
        return df.mean()/tmp.std()

    @staticmethod
    def _cum_to_ret(df, log=True):
        df = df / df.shift(1)
        df.dropna(inplace=True)
        df = df.apply(np.log) if log else df - 1
        return df

    @staticmethod
    def _ret_to_cum(df, log=True):
        df = df.apply(np.exp) if log else df + 1
        df = df.cumprod()
        return df

    @staticmethod
    def _auto_drop(df, cumulative = False):
        base = 1 if cumulative else 0
        flag = True
        drop_list = []
        for i in range(len(df.index)):
            if flag and df.iloc[i + 1, 0] == df.iloc[i, 0] == base:
                drop_list.append(df.index[i])
            else:
                flag = False
        df.drop(drop_list, inplace=True)
        return df


if __name__ == '__main__':
    returns = pd.read_csv(r'C:\Users\QRAFT1\Desktop\data\ks_etf\returns.csv', index_col=['Date'])

    pa = PortfolioAnalysis(returns, cumulative=True)
    pa.report()
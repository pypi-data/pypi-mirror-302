import numpy as np
import pandas as pd
import scipy.integrate as integrate

class series:
    def nFSeries(data, T:float, n_terms:int = 10):
        """
        Compute the Fourier coefficients (a_n, b_n, a_0) for a discrete, periodic dataset using numerical summations for each datapoint.
        
        Parameters: 
            data: pandas DataFrame or 2D array, shape - with columns for 'x' and 'y' axis, the dataset to be numerically analyzed
            T: float - period of the function (if periodic), or interval length (if non-periodic)
            n_terms: int - number of Fourier terms (default is 10)

        Returns: 
            series: numpy array - Fourier series approximation along x
            a_n: numpy array - Fourier cosine coefficients
            b_n: numpy array - Fourier sine coefficients
            a_0: float - Fourier a_0 coefficient

        Examples: 
            data = [[ 0.          0.        ]
                    [ 0.1010101   0.10083842]
                    [ 0.2020202   0.20064886]
                    [ 0.3030303   0.2984138 ]
                    [ 0.4040404   0.39313661]]
            #the first column here is x, the second is y
     
            series, a_n, b_n, a_0 = FSeries.series.nFSeries(data, 240, 20)
            --------------------------------------------------------------
            
            data = [[ 0.          0.        ]
                    [ 0.1010101   0.10083842]
                    [ 0.2020202   0.20064886]
                    [ 0.3030303   0.2984138 ]
                    [ 0.4040404   0.39313661]]
            df = pd.DataFrame(data, columns=['x', 'y'])

            series, a_n, b_n, a_0 = FSeries.series.nFSeries(df, 120, 40)
        """

        if isinstance(data, pd.DataFrame):
            x = data[data.columns[0]].to_numpy()
            y = data[data.columns[1]].to_numpy()
        elif isinstance(data, np.ndarray):
            x = data[:, 0]
            y = data[:, 1]
        else:
            raise ValueError("TypeError: type(data) must be pandas DataFrame (including columns 'x' and 'y') or a numpy array of shape (N, 2).")
        
        L = T / 2
        N = len(x)
        x_values = x.to_numpy()
        differences = np.diff(x_values)
        dt = np.mean(differences)
        nperiods = x.max()/T

        a_n = []
        b_n = []
        a_0 = y.mean()

        for n in range(1, n_terms + 1):
            a_n_val = (2 / (T*nperiods)) * dt * np.sum(y * np.cos(n * np.pi * x / L))
            a_n.append(a_n_val)

            b_n_val = (2 / (T*nperiods)) * dt * np.sum(y * np.sin(n * np.pi * x / L))
            b_n.append(b_n_val)

        series = a_0

        for n in range(0, n_terms):
            series += (a_n[n] * np.cos((n+1) * np.pi * x / L)) + (b_n[n] * np.sin((n+1) * np.pi * x / L))

        return np.array(series), np.array(a_n), np.array(b_n), a_0

    def FSeries(x, f, T:float, n_terms:int = 10):
        """
        Compute the Fourier coefficients (a_n, b_n, a_0) for a periodic function f(x) using numerical integration.

        Parameters:
            x: array type int/float - the 'x' axis column
            f: function - the function to be decomposed
            T: float - period of the function (if periodic), or interval length (if non-periodic)
            n_terms: int - number of Fourier terms (default is 10)

        Returns: 
            series: numpy array - Fourier series approximation along x
            a_n: numpy array - Fourier cosine coefficients
            b_n: numpy array - Fourier sine coefficients
            a_0: float - Fourier a_0 coefficient

        Examples: 
            ... #generate x values
            def f_custom(x):
                return 0.5 * np.sin(3 * x) + 0.25 * np.cos(4 * x)

            T = np.pi
            series, a_n, b_n, a_0 = FSeries(x, f_custom, T=T, n_terms=10)

            #You can also plot the series function:
            plt.plot(x, series, label='Fourier Series Approximation')

        """
        L = T / 2  

        a_n = []
        b_n = []

        a_0 = (1 / L) * integrate.quad(lambda x: f(x), -L, L)[0]

        for n in range(1, n_terms + 1):
            a_n_val = (1 / L) * integrate.quad(lambda x: f(x) * np.cos(n * np.pi * x / L), -L, L)[0]
            a_n.append(a_n_val)

            b_n_val = (1 / L) * integrate.quad(lambda x: f(x) * np.sin(n * np.pi * x / L), -L, L)[0]
            b_n.append(b_n_val)

        series = a_0
        for n in range(0, n_terms):
            series += (a_n[n] * np.cos((n+1) * np.pi * x / L)) + (b_n[n] * np.sin((n+1) * np.pi * x / L))

        return np.array(series), np.array(a_n), np.array(b_n), a_0
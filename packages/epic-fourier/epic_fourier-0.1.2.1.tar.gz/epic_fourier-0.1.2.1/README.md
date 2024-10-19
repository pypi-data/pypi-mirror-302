Hello!

It has become evident to me that Python Scipy lacks a Fourier SERIES function! Unbelievable! I have made this for my peers in the Imperial College London Physics Department, I hope you find it useful :). 

This package contains two components under the 'series' directory so far. Firstly, Fourier series computation for a periodic function, 'FSeries'. Secondly, Fourier Series computation for a periodic dataset, 'nFSeries'.

Please direct bug reports, feature requests, or anything else regarding this custom library to my personal email: LiuLouis1@gmail.com

For those of you reading on GitHub, running 'pip install FSeries' in Python should import this library!

Happy coding!

'series':
    'series.FSeries':
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
            series, a_n, b_n, a_0 = epic_fourier.series.FSeries(x, f_custom, T=T, n_terms=10)

            #You can also plot the series function:
            plt.plot(x, series, label='Fourier Series Approximation')
        

    'series.nFSeries': 
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
     
            series, a_n, b_n, a_0 = epic_fourier.series.nFSeries(data, 240, 20)
            
        
            data = [[ 0.          0.        ]
                    [ 0.1010101   0.10083842]
                    [ 0.2020202   0.20064886]
                    [ 0.3030303   0.2984138 ]
                    [ 0.4040404   0.39313661]]
            df = pd.DataFrame(data, columns=['x', 'y'])

            series, a_n, b_n, a_0 = epic_fourier.series.nFSeries(df, 120, 40)


            #You might even find this useful with the scipy.signal.sawtooth 
            function!

            f_values = signal.sawtooth(2 * np.pi * x / (2 * np.pi))  # Sawtooth wave
            data = np.column_stack((x, f_values))

            T = 2 * np.pi  # Period of the sawtooth wave
            series, a_n, b_n, a_0 = epic_fourier.series.nFSeries(data, T, n_terms=10)

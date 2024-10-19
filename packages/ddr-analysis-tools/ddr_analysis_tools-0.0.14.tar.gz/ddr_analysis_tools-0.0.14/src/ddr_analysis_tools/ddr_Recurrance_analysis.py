


from operator import sub

import numpy as np
from sklearn import metrics
from sklearn.neighbors import NearestNeighbors
from toolz import curry


def global_false_nearest_neighbors(x, lag, min_dims=1, max_dims=10, **cutoffs):
    """
    Across a range of embedding dimensions $d$, embeds $x(t)$ with lag $\tau$, finds all nearest neighbors,
    and computes the percentage of neighbors that that remain neighbors when an additional dimension is unfolded.
    See [1] for more information.

    Parameters
    ----------
    x : array-like
        Original signal $x(t).
    lag : int
        Time lag $\tau$ in units of the sampling time $h$ of $x(t)$.
    min_dims : int, optional
        The smallest embedding dimension $d$ to test.
    max_dims : int, optional
        The largest embedding dimension $d$ to test.
    relative_distance_cutoff : float, optional
        The cutoff for determining neighborliness,
        in distance increase relative to the original distance between neighboring points.
        The default, 15, is suggested in [1] (p. 41).
    relative_radius_cutoff : float, optional
        The cutoff for determining neighborliness,
        in distance increase relative to the radius of the attractor.
        The default, 2, is suggested in [1] (p. 42).

    Returns
    -------
    dims : ndarray
        The tested dimensions $d$.
    gfnn : ndarray
        The percentage of nearest neighbors that are false neighbors at each dimension.

    See Also
    --------
    reconstruct

    References
    ----------
    [1] Arbanel, H. D. (1996). *Analysis of Observed Chaotic Data* (pp. 40-43). New York: Springer.

    """
    x = _vector(x)

    dimensions = np.arange(min_dims, max_dims + 1)
    false_neighbor_pcts = np.array([_gfnn(x, lag, n_dims, **cutoffs) for n_dims in dimensions])
    return dimensions, false_neighbor_pcts


def _gfnn(x, lag, n_dims, **cutoffs):
    # Global false nearest neighbors at a particular dimension.
    # Returns percent of all nearest neighbors that are still neighbors when the next dimension is unfolded.
    # Neighbors that can't be embedded due to lack of data are not counted in the denominator.
    offset = lag*n_dims
    is_true_neighbor = _is_true_neighbor(x, _radius(x), offset)
    return np.mean([
        not is_true_neighbor(indices, distance, **cutoffs)
        for indices, distance in _nearest_neighbors(reconstruct(x, lag, n_dims))
        if (indices + offset < x.size).all()
    ])


def _radius(x):
    # Per Arbanel (p. 42):
    # "the nominal 'radius' of the attractor defined as the RMS value of the data about its mean."
    return np.sqrt(((x - x.mean())**2).mean())


@curry
def _is_true_neighbor(
        x, attractor_radius, offset, indices, distance,
        relative_distance_cutoff=15,
        relative_radius_cutoff=2
):
    distance_increase = np.abs(sub(*x[indices + offset]))
    return (distance_increase / distance < relative_distance_cutoff and
            distance_increase / attractor_radius < relative_radius_cutoff)


def _nearest_neighbors(y):
    """
    Wrapper for sklearn.neighbors.NearestNeighbors.
    Yields the indices of the neighboring points, and the distance between them.

    """
    distances, indices = NearestNeighbors(n_neighbors=2, algorithm='kd_tree').fit(y).kneighbors(y)
    for distance, index in zip(distances, indices):
        yield index, distance[1]


def reconstruct(x, lag, n_dims):
    """Phase-space reconstruction.

    Given a signal $x(t)$, dimensionality $d$, and lag $\tau$, return the reconstructed signal
    \[
        \mathbf{y}(t) = [x(t), x(t + \tau), \ldots, x(t + (d - 1)\tau)].
    \]

    Parameters
    ----------
    x : array-like
        Original signal $x(t)$.
    lag : int
        Time lag $\tau$ in units of the sampling time $h$ of $x(t)$.
    n_dims : int
        Embedding dimension $d$.

    Returns
    -------
    ndarray
        $\mathbf{y}(t)$ as an array with $d$ columns.

    """
    x = _vector(x)

    if lag * (n_dims - 1) >= x.shape[0] // 2:
        raise ValueError('longest lag cannot be longer than half the length of x(t)')

    lags = lag * np.arange(n_dims)
    return np.vstack([x[lag:lag - lags[-1] or None] for lag in lags]).transpose()


def ami(x, y=None, n_bins=10):
    """Calculate the average mutual information between $x(t)$ and $y(t)$.

    Parameters
    ----------
    x : array-like
    y : array-like, optional
        $x(t)$ and $y(t)$.
        If only `x` is passed, it must have two columns;
        the first column defines $x(t)$ and the second $y(t)$.
    n_bins : int
        The number of bins to use when computing the joint histogram.

    Returns
    -------
    scalar
        Average mutual information between $x(t)$ and $y(t)$, in nats (natural log equivalent of bits).

    See Also
    --------
    lagged_ami

    References
    ----------
    Arbanel, H. D. (1996). *Analysis of Observed Chaotic Data* (p. 28). New York: Springer.

    """
    x, y = _vector_pair(x, y)
    if x.shape[0] != y.shape[0]:
        raise ValueError('timeseries must have the same length')

    return metrics.mutual_info_score(None, None, contingency=np.histogram2d(x, y, bins=n_bins)[0])


def lagged_ami(x, min_lag=0, max_lag=None, lag_step=1, n_bins=10):
    """Calculate the average mutual information between $x(t)$ and $x(t + \tau)$, at multiple values of $\tau$.

    Parameters
    ----------
    x : array-like
        $x(t)$.
    min_lag : int, optional
        The shortest lag to evaluate, in units of the sampling period $h$ of $x(t)$.
    max_lag : int, optional
        The longest lag to evaluate, in units of $h$.
    lag_step : int, optional
        The step between lags to evaluate, in units of $h$.
    n_bins : int
        The number of bins to use when computing the joint histogram in order to calculate mutual information.
        See |ami|.

    Returns
    -------
    lags : ndarray
        The evaluated lags $\tau_i$, in units of $h$.
    amis : ndarray
        The average mutual information between $x(t)$ and $x(t + \tau_i)$.

    See Also
    --------
    ami

    """
    if max_lag is None:
        max_lag = x.shape[0]//2
    lags = np.arange(min_lag, max_lag, lag_step)

    amis = [ami(reconstruct(x, lag, 2), n_bins=n_bins) for lag in lags]
    return lags, np.array(amis)


def _vector_pair(a, b):
    a = np.squeeze(a)
    if b is None:
        if a.ndim != 2 or a.shape[1] != 2:
            raise ValueError('with one input, array must have be 2D with two columns')
        a, b = a[:, 0], a[:, 1]
    return a, np.squeeze(b)


def _vector(x):
    x = np.squeeze(x)
    if x.ndim != 1:
        raise ValueError('x(t) must be a 1-dimensional signal')
    return x














def distance_matrix(data, dimension, delay, norm='euclidean'):
    N = int(len(data) - (dimension-1) * delay)
    distance_matrix = np.zeros((N, N), dtype="float32")
    if norm == 'manhattan':
        for i in range(N):
            for j in range(i, N, 1):
                temp = 0.0
                for k in range(dimension):
                    temp += np.abs(data[i+k*delay] - data[j+k*delay])
                distance_matrix[i,j] = distance_matrix[j,i] = temp
    elif norm == 'euclidean':
        for i in range(N):
            for j in range(i, N, 1):
                temp = 0.0
                for k in range(dimension):
                    temp += np.power(data[i+k*delay] - data[j+k*delay], 2)
                distance_matrix[i,j] = distance_matrix[j,i] = np.sqrt(temp)
    elif norm == 'supremum':
        temp = np.zeros(dimension)
        for i in range(N):
            for j in range(i, N, 1):
                for k in range(dimension):
                    temp[k] = np.abs(data[i+k*delay] - data[j+k*delay])
                distance_matrix[i,j] = distance_matrix[j,i] = np.max(temp)
    return distance_matrix

def recurrence_matrix(data, dimension, delay, threshold, norm='euclidean'):
    recurrence_matrix = distance_matrix(data, dimension, delay, norm)
    N = len(recurrence_matrix[:,0])
    for i in range(N):
        for j in range(i, N, 1):
            if recurrence_matrix[i,j] <= threshold:
                recurrence_matrix[i,j] = recurrence_matrix[j,i] = 1
            else:
                recurrence_matrix[i,j] = recurrence_matrix[j,i] = 0
    return recurrence_matrix.astype(int)





def recurrence_quantification_analysis(recurrence_matrix, minimum_diagonal_line_length, minimum_vertical_line_length, minimum_white_vertical_line_length):
    # Calculating the number of states - N
    number_of_vectors = recurrence_matrix.shape[0]
    
    # Calculating the diagonal frequency distribution - P(l)
    diagonal_frequency_distribution = np.zeros(number_of_vectors+1)
    for i in range(number_of_vectors-1, -1, -1):
        diagonal_line_length = 0
        for j in range(0, number_of_vectors-i):
            if recurrence_matrix[i+j,j] == 1:
                diagonal_line_length += 1
                if j == (number_of_vectors-i-1):
                    diagonal_frequency_distribution[diagonal_line_length] += 1.0
            else:
                if diagonal_line_length != 0:
                    diagonal_frequency_distribution[diagonal_line_length] += 1.0
                    diagonal_line_length = 0
    for k in range(1,number_of_vectors):
        diagonal_line_length = 0
        for i in range(number_of_vectors-k):
            j = i + k
            if recurrence_matrix[i,j] == 1:
                diagonal_line_length += 1
                if j == (number_of_vectors-1):
                    diagonal_frequency_distribution[diagonal_line_length] += 1.0
            else:
                if diagonal_line_length != 0:
                    diagonal_frequency_distribution[diagonal_line_length] += 1.0
                    diagonal_line_length = 0

    # Calculating the vertical frequency distribution - P(v)
    vertical_frequency_distribution = np.zeros(number_of_vectors+1)
    for i in range(number_of_vectors):
        vertical_line_length = 0
        for j in range(number_of_vectors):
            if recurrence_matrix[i,j] == 1:
                vertical_line_length += 1
                if j == (number_of_vectors-1):
                    vertical_frequency_distribution[vertical_line_length] += 1.0
            else:
                if vertical_line_length != 0:
                    vertical_frequency_distribution[vertical_line_length] += 1.0
                    vertical_line_length = 0

    # Calculating the white vertical frequency distribution - P(w)
    white_vertical_frequency_distribution = np.zeros(number_of_vectors+1)
    for i in range(number_of_vectors):
        white_vertical_line_length = 0
        for j in range(number_of_vectors):
            if recurrence_matrix[i,j] == 0:
                white_vertical_line_length += 1
                if j == (number_of_vectors-1):
                    white_vertical_frequency_distribution[white_vertical_line_length] += 1.0
            else:
                if white_vertical_line_length != 0:
                    white_vertical_frequency_distribution[white_vertical_line_length] += 1.0
                    white_vertical_line_length = 0

    # Calculating the recurrence rate - RR
    recurrence_rate = np.float(np.sum(recurrence_matrix))/np.power(number_of_vectors, 2)

    # Calculating the determinism - DET
    numerator = np.sum([l * diagonal_frequency_distribution[l] for l in range(minimum_diagonal_line_length, number_of_vectors)])
    denominator = np.sum([l * diagonal_frequency_distribution[l] for l in range(1, number_of_vectors)])
    determinism = numerator / denominator

    # Calculating the average diagonal line length - L
    numerator = np.sum([l * diagonal_frequency_distribution[l] for l in range(minimum_diagonal_line_length, number_of_vectors)])
    denominator = np.sum([diagonal_frequency_distribution[l] for l in range(minimum_diagonal_line_length, number_of_vectors)])
    average_diagonal_line_length = numerator / denominator

    # Calculating the longest diagonal line length - Lmax
    for l in range(number_of_vectors-1, 0, -1):
        if diagonal_frequency_distribution[l] != 0:
            longest_diagonal_line_length = l
            break

    # Calculating the  divergence - DIV
    divergence = 1. / longest_diagonal_line_length

    # Calculating the entropy diagonal lines - Lentr
    sum_diagonal_frequency_distribution = np.float(np.sum(diagonal_frequency_distribution[minimum_diagonal_line_length:-1]))
    entropy_diagonal_lines = 0
    for l in range(minimum_diagonal_line_length, number_of_vectors):
        if diagonal_frequency_distribution[l] != 0:
            entropy_diagonal_lines +=  (diagonal_frequency_distribution[l]/sum_diagonal_frequency_distribution) * np.log(diagonal_frequency_distribution[l]/sum_diagonal_frequency_distribution)
    entropy_diagonal_lines *= -1

    # Calculating the ratio determinism_recurrence - DET/RR
    ratio_determinism_recurrence_rate = determinism / recurrence_rate

    # Calculating the laminarity - LAM
    numerator = np.sum([v * vertical_frequency_distribution[v] for v in range(minimum_vertical_line_length, number_of_vectors+1)])
    denominator = np.sum([v * vertical_frequency_distribution[v] for v in range(1, number_of_vectors+1)])
    laminarity = numerator / denominator

    # Calculating the average vertical line length - V
    numerator = np.sum([v * vertical_frequency_distribution[v] for v in range(minimum_vertical_line_length, number_of_vectors+1)])
    denominator = np.sum([vertical_frequency_distribution[v] for v in range(minimum_vertical_line_length, number_of_vectors+1)])
    average_vertical_line_length = numerator / denominator

    # Calculating the longest vertical line length - Vmax
    for v in range(number_of_vectors, 0, -1):
        if vertical_frequency_distribution[v] != 0:
            longest_vertical_line_length = v
            break

    # Calculating the entropy vertical lines - Ventr
    sum_vertical_frequency_distribution = np.float(np.sum(vertical_frequency_distribution[minimum_vertical_line_length:]))
    entropy_vertical_lines = 0
    for v in range(minimum_vertical_line_length, number_of_vectors+1):
        if vertical_frequency_distribution[v] != 0:
            entropy_vertical_lines +=  (vertical_frequency_distribution[v]/sum_vertical_frequency_distribution) * np.log(vertical_frequency_distribution[v]/sum_vertical_frequency_distribution)
    entropy_vertical_lines *= -1

    # Calculatint the ratio laminarity_determinism - LAM/DET
    ratio_laminarity_determinism = laminarity / determinism

    # Calculating the average white vertical line length - W
    numerator = np.sum([w * white_vertical_frequency_distribution[w] for w in range(minimum_white_vertical_line_length, number_of_vectors+1)])
    denominator = np.sum([white_vertical_frequency_distribution[w] for w in range(minimum_white_vertical_line_length, number_of_vectors+1)])
    average_white_vertical_line_length = numerator / denominator

    # Calculating the longest white vertical line length - Wmax
    for w in range(number_of_vectors, 0, -1):
        if white_vertical_frequency_distribution[w] != 0:
            longest_white_vertical_line_length = w
            break

    # Calculating the entropy white vertical lines - Wentr
    sum_white_vertical_frequency_distribution = np.float(np.sum(white_vertical_frequency_distribution[minimum_white_vertical_line_length:]))
    entropy_white_vertical_lines = 0
    for w in range(minimum_white_vertical_line_length, number_of_vectors+1):
        if white_vertical_frequency_distribution[w] != 0:
            entropy_white_vertical_lines +=  (white_vertical_frequency_distribution[w]/sum_white_vertical_frequency_distribution) * np.log(white_vertical_frequency_distribution[w]/sum_white_vertical_frequency_distribution)
    entropy_white_vertical_lines *= -1

    return diagonal_frequency_distribution, vertical_frequency_distribution, white_vertical_frequency_distribution, recurrence_rate, determinism, average_diagonal_line_length, longest_diagonal_line_length, divergence, entropy_diagonal_lines, laminarity, average_vertical_line_length, longest_vertical_line_length, entropy_vertical_lines, average_white_vertical_line_length, longest_white_vertical_line_length, entropy_white_vertical_lines, ratio_determinism_recurrence_rate, ratio_laminarity_determinism
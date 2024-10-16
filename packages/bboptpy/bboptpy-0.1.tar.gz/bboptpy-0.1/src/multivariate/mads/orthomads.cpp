/*
 Copyright (c) 2020 Mike Gimelfarb

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the > "Software"), to
 deal in the Software without restriction, including without limitation the
 rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
 sell copies of the Software, and to permit persons to whom the Software is
 furnished to do so, > subject to the following conditions:

 The above copyright notice and this permission notice shall be included in
 all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.

 ================================================================
 REFERENCES:

 [1] Abramson, Mark A., et al. "OrthoMADS: A deterministic MADS instance with
 orthogonal directions." SIAM Journal on Optimization 20.2 (2009): 948-966.

 [2] Audet, Charles, et al. "Reducing the number of function evaluations in mesh
 adaptive direct search algorithms." SIAM Journal on Optimization 24.2 (2014):
 621-642.
 */

#include <algorithm>
#include <cmath>
#include <numeric>
#include <iostream>
#include <stdexcept>

#include "../../blas.h"

#include "orthomads.h"

OrthoMADSMesh::OrthoMADSMesh(bool reduced) {
	_reduced = reduced;
}

void OrthoMADSMesh::init(MADS *parent) {
	const int n = parent->_n;
	_primes = std::vector<long long int>(n);
	_nhalton = std::vector<long long int>(n, 0L);
	_dhalton = std::vector<long long int>(n, 1L);
	_q = std::vector<long long int>(n);
	_uhalton = std::vector<double>(n);
	_uhat = std::vector<double>(n);
	_D.clear();
	if (_reduced) {
		_D.resize(n + 1, std::vector<long long int>(n, 0L));
	} else {
		_D.resize(2 * n, std::vector<long long int>(n, 0L));
	}
	_t0 = fillPrimes(n);
	_tkmax = _t0;
	_tk = _t0;

	// generate initial Halton sequence to p_n
	for (int it = 1; it <= _tk; it++) {
		nextHalton(n);
	}

	// initialize mesh size parameters
	_lk = 0;
	_deltap = 1.;
	_deltapmin = _deltap;
	_deltam = 1.;
}

void OrthoMADSMesh::update(MADS *parent) {

	// update t_k
	const int tkold = _tk;
	if (_deltap <= _deltapmin) {
		_deltapmin = _deltap;
		_tk = _lk + _t0;
	} else {
		_tk = 1 + _tkmax;
	}
	_tkmax = std::max(_tkmax, _tk);

	// generate Halton sequence
	const int n = parent->_n;
	for (int it = 1; it <= _tk - tkold; it++) {
		nextHalton(n);
	}

	// compute alpha by solving the optimization problem
	// 				max_alpha || q_t(alpha) ||
	//				s.t. || q_t(alpha) || <= 2 ^ (|l| / 2)
	computeAlpha(n, _lk);
	long long int qnorm2 = 0L;
	for (int i = 0; i < n; i++) {
		qnorm2 += _q[i] * _q[i];
	}

	// compute the orthogonal integer matrix H by Householder transform
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			if (i == j) {
				_D[i][j] = qnorm2 - 2L * _q[i] * _q[j];
			} else {
				_D[i][j] = -2L * _q[i] * _q[j];
			}
		}
	}

	// construct the poll directions
	if (_reduced) {

		// follow the procedure in the paper for generating n + 1 vectors
		for (int i = 0; i < n; i++) {
			_uhat[i] = parent->_x[i] - parent->_pbest[i];
			_D[n][i] = 0L;
		}
		for (int i = 0; i < n; i++) {
			double dw = 0.;
			for (int j = 0; j < n; j++) {
				dw += _D[i][j] * _uhat[j];
			}
			for (int j = 0; j < n; j++) {
				if (dw < 0.) {
					_D[i][j] = -_D[i][j];
				}
				_D[n][j] -= _D[i][j];
			}
		}
	} else {

		// compute D = [H -H]
		for (int i = 0; i < n; i++) {
			for (int j = 0; j < n; j++) {
				_D[i + n][j] = -_D[i][j];
			}
		}
	}
}

void OrthoMADSMesh::updateParameters(MADS *parent) {
	if (parent->_searchsuccess || !parent->_minframe) {
		_lk--;
	} else {
		_lk++;
	}
	if (_lk <= 0) {
		_deltam = 1.;
	} else {
		_deltam = std::pow(4., -_lk);
	}
	_deltap = std::pow(2., -_lk);
}

bool OrthoMADSMesh::converged(MADS *parent) {

	// minimal frame with small poll size parameter
	if (_deltap < parent->_tol) {
		return true;
	}

	// check for overflow
	if (_lk > 63) {
		std::cerr
				<< "Warning [LTMADS]: small l value detected. Algorithm may become unstable."
				<< std::endl;
	}

	return false;
}

void OrthoMADSMesh::computeTrial(MADS *parent, int idx, double *x0,
		double *out) {
	for (int i = 0; i < parent->_n; i++) {
		out[i] = x0[i] + _deltam * _D[idx][i];
	}
}

void OrthoMADSMesh::computeAlpha(int n, int l) {

	// compute 2 u - 1, its norms, and then normalize
	double unorminf = 0.;
	double unormmin = std::numeric_limits<double>::infinity();
	for (int i = 0; i < n; i++) {
		_uhat[i] = 2. * _uhalton[i] - 1.;
		unorminf = std::max(unorminf, std::fabs(_uhat[i]));
		unormmin = std::min(unormmin, std::fabs(_uhat[i]));
	}
	const double unorm2 = dnrm2(n, &_uhat[0]);
	if (unorm2 <= 0.) {
		throw std::invalid_argument("Error [OrthoMADS]: bad Halton sequence.");
	}
	dscalm(n, 1. / unorm2, &_uhat[0], 1);

	// compute the minimum bound on alpha in Lemma 3.2
	const long long int rhs2 = 1L << std::abs(l);
	const double beta = std::sqrt(1. * rhs2 / n) - 0.5;

	// initial guess
	const double alpha0 = unorm2 / (2. * unorminf);
	long long int qnorm2best = computeQ(n, alpha0, &_uhat[0], &_q[0]);

	// solve the alpha subproblem naively
	int j = std::max(0, static_cast<int>(beta * unormmin / unorm2 - 0.5));
	bool jfeasible = true;
	while (jfeasible) {
		jfeasible = false;
		for (int i = 0; i < n; i++) {
			const double alpha = (2. * j + 1.) / (2. * std::fabs(_uhat[i]));
			const long long int qnorm2 = computeQ(n, alpha, &_uhat[0], &_q[0]);
			if (qnorm2 <= rhs2) {
				jfeasible = true;
				if (qnorm2 >= qnorm2best) {
					qnorm2best = qnorm2;
				}
			}
		}
		j++;
	}
	if (qnorm2best <= 0L) {
		std::cerr
				<< "Warning [OrthoMADS]: subproblem could not be solved optimally."
				<< std::endl;
	}
}

long long int OrthoMADSMesh::computeQ(const int n, const double alpha,
		const double *uhat, long long int *q) {
	long long int qnorm2 = 0L;
	for (int i = 0; i < n; i++) {
		q[i] = static_cast<long long int>(std::round(alpha * uhat[i]));
		qnorm2 += q[i] * q[i];
	}
	return qnorm2;
}

void OrthoMADSMesh::nextHalton(const int n) {
	for (int i = 0; i < n; i++) {
		const long long int x = _dhalton[i] - _nhalton[i];
		if (x == 1L) {
			_nhalton[i] = 1L;
			_dhalton[i] *= _primes[i];
		} else {
			long long int y = _dhalton[i] / _primes[i];
			while (y >= x) {
				y /= _primes[i];
			}
			_nhalton[i] = (_primes[i] + 1L) * y - x;
		}
		_uhalton[i] = (1. * _nhalton[i]) / _dhalton[i];
	}
}

int OrthoMADSMesh::fillPrimes(const int n) {
	int m = 2;
	int nprime = 0;
	_primes.clear();
	while (true) {
		if (isPrime(m)) {
			nprime++;
			_primes.push_back(m);
			if (nprime == n) {
				return m;
			}
		}
		m++;
	}
}

bool OrthoMADSMesh::isPrime(const int n) {
	if (n % 2 == 0) {
		return n == 2;
	}
	if (n % 3 == 0) {
		return n == 3;
	}
	int s = 4;
	int m = static_cast<int>(std::sqrt(1. * n)) + 1;
	for (int i = 5; i < m; s = 6 - s, i += s) {
		if (n % i == 0) {
			return false;
		}
	}
	return true;
}

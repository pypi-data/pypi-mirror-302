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

 [1] Di Pillo, Gianni, et al. "A controlled random search algorithm with local
 Newton-type search for global optimization." High Performance Algorithms and
 Software in Nonlinear Optimization. Springer, Boston, MA, 1998. 143-159.
 */

#include <algorithm>
#include <iostream>

#include "../../blas.h"
#include "../../random.hpp"

#include "palo.h"

using Random = effolkronium::random_static;

PALO::PALO(int mfev, int np, double tol, double omega) {
	_mfev = mfev;
	_np = np;
	_tol = tol;
	_omega = omega;
}

void PALO::init(const multivariate_problem &f, const double *guess) {

	// define problem
	if (f._hasc || f._hasbbc) {
		std::cerr << "Warning [PALO]: problem constraints will be ignored."
				<< std::endl;
	}
	_f = f;
	_n = f._n;
	_lower = std::vector<double>(f._lower, f._lower + _n);
	_upper = std::vector<double>(f._upper, f._upper + _n);

	// adjust memory size
	if (_np < _n + 1) {
		std::cerr
				<< "Warning [PALO]: number of sample points is too small - adjusted."
				<< std::endl;
		_np = _n + 1;
	}

	// define pool of points
	_fev = 0;
	_points.clear();
	for (int i = 0; i < _np; i++) {
		std::vector<double> x(_n);
		for (int d = 0; d < _n; d++) {
			x[d] = Random::get(_lower[d], _upper[d]);
		}
		const double fx = _f._f(&x[0]);
		const point pt { x, fx };
		_points.push_back(std::move(pt));
		_fev++;
	}

	// centroid
	_indices = std::vector<int>(_n + 1);
	_centroid = std::vector<double>(_n);
	_weights = std::vector<double>(_n);
	_trial = std::vector<double>(_n);
	_trial2 = std::vector<double>(_n);

	// find the best and worst points
	std::sort(_points.begin(), _points.end(), point::compare_fitness);
	_f0min = _points[0]._f;
	_f0max = _points[_np - 1]._f;
}

void PALO::iterate() {
	trial();
	update();
}

multivariate_solution PALO::optimize(const multivariate_problem &f,
		const double *guess) {
	init(f, guess);
	bool converged = false;
	while (_fev < _mfev) {
		iterate();
		if (stop()) {
			converged = true;
			break;
		}
	}
	return {_points[0]._x, _fev, converged};
}

/* =============================================================
 *
 * 				UPDATING POINT SET SUBROUTINES
 *
 * =============================================================
 */

void PALO::trial() {

	// compute phi
	const double fkmin = _points[0]._f;
	const double fkmax = _points[_np - 1]._f;
	const double phi = _omega * std::pow(fkmax - fkmin, 2) / (_f0max - _f0min);

	// choose n + 1 random points
	for (int i = 0; i < _n + 1; i++) {
		_indices[i] = Random::get(0, _np - 1);
	}

	// compute the centroid weights
	double etasum = 0.0;
	for (int i = 0; i < _n; i++) {
		const double fxi = _points[_indices[i + 1]]._f;
		_weights[i] = 1.0 / (fxi - fkmin + phi);
		etasum += _weights[i];
	}
	for (int d = 0; d < _n; d++) {
		_weights[d] /= etasum;
	}

	// compute the weighted centroid
	std::fill(_centroid.begin(), _centroid.end(), 0.0);
	for (int i = 0; i < _n; i++) {
		for (int d = 0; d < _n; d++) {
			const double xid = _points[_indices[i + 1]]._x[d];
			_centroid[d] += _weights[i] * xid;
		}
	}

	// compute the weighted function value
	double fw = 0.0;
	for (int i = 0; i < _n; i++) {
		const double fxi = _points[_indices[i + 1]]._f;
		fw += _weights[i] * fxi;
	}

	// compute the trial point
	const double fx0 = _points[_indices[0]]._f;
	const double alpha = 1.0 - (std::fabs(fx0 - fw) / (fkmax - fkmin + phi));
	if (fw <= fx0) {
		for (int d = 0; d < _n; d++) {
			const double x0d = _points[_indices[0]]._x[d];
			_trial[d] = _centroid[d] - alpha * (x0d - _centroid[d]);
		}
	} else {
		for (int d = 0; d < _n; d++) {
			const double x0d = _points[_indices[0]]._x[d];
			_trial[d] = x0d - alpha * (_centroid[d] - x0d);
		}
	}

	// accept or reject trial point
	if (!inBounds(&_trial[0])) {
		trial();
	}
	_ftrial = _f._f(&_trial[0]);
	_fev++;

	// local mutation
	if (_ftrial >= fkmax) {

		// compute another trial point using the mutation operator
		for (int d = 0; d < _n; d++) {
			const double w = Random::get(0.0, 1.0);
			_trial2[d] = (1.0 + w) * _points[0]._x[d] - w * _trial[d];
		}
		_ftrial2 = _f._f(&_trial2[0]);
		_fev++;

		// accept or reject new trial point
		if (_ftrial2 >= fkmax) {
			trial();
		}

		// point is accepted, this will become the replacement
		_ftrial = _ftrial2;
		std::copy(_trial2.begin(), _trial2.end(), _trial.begin());
	}
}

void PALO::update() {

	// replace the worst point with the local solution
	_points[_np - 1]._f = _ftrial;
	std::copy(_trial.begin(), _trial.end(), _points[_np - 1]._x.begin());

	// find the best and worst points
	std::sort(_points.begin(), _points.end(), point::compare_fitness);
	std::cout << _points[0]._f << std::endl;
}

bool PALO::stop() {
	double fl = _points[0]._f;
	double fh = _points[_np - 1]._f;
	return std::fabs(fl - fh) < _tol;
}

bool PALO::inBounds(double *p) {
	for (int d = 0; d < _n; d++) {
		if (p[d] < _lower[d] || p[d] > _upper[d]) {
			return false;
		}
	}
	return true;
}


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

 [1] Audet, Charles & Dennis, J.. (2006). Mesh Adaptive Direct Search Algorithms
 for Constrained Optimization. SIAM Journal on Optimization. 17. 188-217.
 10.1137/060671267.

 [2] Le Digabel, Sébastien. "Algorithm 909: NOMAD: Nonlinear optimization with
 the MADS algorithm." ACM Transactions on Mathematical Software (TOMS) 37.4 (2011):
 1-15.
 */

#define _USE_MATH_DEFINES
#include <algorithm>
#include <cmath>
#include <iostream>

#include "../../blas.h"
#include "mads.h"

/* =============================================================
 *
 * 						BASE MADS ALGORITHM
 *
 * =============================================================
 */
MADS::MADS(MADSMesh *mesh, MADSSearch *search, int mfev, double tol) {
	_mesh = mesh;
	_search = search;
	_mfev = mfev;
	_tol = tol;
}

void MADS::init(const multivariate_problem &f, const double *guess) {

	// define problem
	if (f._hasc) {
		std::cerr << "Warning [MADS]: (in)equality constraints will be ignored."
				<< std::endl;
	}
	_f = f;
	_n = _f._n;
	_guess = std::vector<double>(guess, guess + _n);
	_lower = std::vector<double>(f._lower, f._lower + _n);
	_upper = std::vector<double>(f._upper, f._upper + _n);

	// define memory
	_fev = _bbev = 0;
	_x = std::vector<double>(_guess);
	_fx = evaluateBarrier(&_x[0]);
	_pbest = std::vector<double>(_x);
	_trial = std::vector<double>(_n);
	_succdir = std::vector<double>(_n);

	// initialize strategies
	_mesh->init(this);
	if (_search) {
		_search->init(this);
	}

	_indices = std::vector<int>(_mesh->size());
	for (int i = 0; i < _mesh->size(); i++) {
		_indices[i] = i;
	}
}

void MADS::iterate() {

	// search
	_searchsuccess = false;
	if (_search) {
		_search->search(this);
	}

	// poll if search unsuccessful
	if (!_searchsuccess) {
		poll();
	}

	// parameter update
	_mesh->updateParameters(this);
}

multivariate_solution MADS::optimize(const multivariate_problem &f,
		const double *guess) {
	init(f, guess);
	bool converged = false;
	while (true) {
		iterate();

		// check convergence of mesh
		if (_mesh->converged(this)) {
			converged = true;
			break;
		}

		// reached budget
		if (_fev >= _mfev || _bbev >= _mfev) {
			converged = false;
			break;
		}
	}
	return {_x, _fev, 0, _bbev, converged};
}

void MADS::poll() {

	// update the mesh
	_mesh->update(this);

	// sort mesh points by angle with last successful direction
	std::sort(_indices.begin(), _indices.end(),
			[&](const int i, const int j) -> bool {
				const double iang = angle(_n, &_succdir[0], &(_mesh->_D[i])[0]);
				const double jang = angle(_n, &_succdir[0], &(_mesh->_D[j])[0]);
				return std::fabs(iang) < std::fabs(jang);
			});

	// evaluate f_omega on the frame P_k
	// the frame computed by generateBasis() is guaranteed to satisfy
	// the assumptions of Definition 2.2
	for (int idx = 0; idx < _mesh->size(); idx++) {

		// evaluate each x + delta * d
		const int iact = _indices[idx];
		_mesh->computeTrial(this, iact, &_x[0], &_trial[0]);
		const double ftrial = evaluateBarrier(&_trial[0]);

		// an improved mesh point is found
		// take an opportunistic approach as in the original paper
		if (ftrial < _fx) {
			std::copy(_x.begin(), _x.end(), _pbest.begin());
			std::copy(_trial.begin(), _trial.begin() + _n, _x.begin());
			_fx = ftrial;
			for (int i = 0; i < _n; i++) {
				_succdir[i] = static_cast<double>(_mesh->_D[iact][i]);
			}
			_minframe = false;
			return;
		}
	}

	// an improved mesh point is not found
	_minframe = true;
}

double MADS::angle(const int n, const double *x, const long long int *y) {
	const double xnorm = dnrm2(n, x);
	const long long int ynormsq = std::inner_product(y, y + n, y, 0L);
	if (xnorm < 1e-15 || ynormsq == 0) {
		return M_PI / 2.;
	}
	const double ynorm = std::sqrt(1. * ynormsq);
	double dot = 0.;
	for (int i = 0; i < n; i++) {
		dot += (x[i] / xnorm) * (y[i] / ynorm);
	}
	return std::acos(dot);
}

double MADS::evaluateBarrier(const double *x) {

	// check the bound constraints
	for (int i = 0; i < _n; i++) {
		if (x[i] < _lower[i] || x[i] > _upper[i]) {
			return INF;
		}
	}

	// check the feasibility
	if (_f._hasbbc) {
		_bbev++;
		if (!_f._bbc(x)) {
			return INF;
		}
	}

	// function evaluation
	_fev++;
	return _f._f(x);
}

/* =============================================================
 *
 * 				SEARCH STRATEGIES FOR MADS
 *
 * =============================================================
 */
void OpportunisticSearch::init(MADS *parent) {
	_trial = std::vector<double>(parent->_n);
	_descent = std::vector<double>(parent->_n);
	_xold = std::vector<double>(parent->_guess);
	_fxold = parent->_fx;
}

void OpportunisticSearch::search(MADS *parent) {

	// bookkeeping for tracking improvement
	const bool improvement = parent->_fx < _fxold;
	for (int i = 0; i < parent->_n; i++) {
		_descent[i] = parent->_x[i] - _xold[i];
		_trial[i] = _xold[i] + 4. * _descent[i];
	}
	std::copy(parent->_x.begin(), parent->_x.end(), _xold.begin());
	_fxold = parent->_fx;

	// simulate dynamic ordering according to the paper
	// when the previous iteration succeeds in finding an improved mesh point
	if (improvement) {
		const double ftrial = parent->evaluateBarrier(&_trial[0]);
		if (ftrial < parent->_fx) {
			std::copy(parent->_x.begin(), parent->_x.end(),
					parent->_pbest.begin());
			std::copy(_trial.begin(), _trial.end(), parent->_x.begin());
			std::copy(_descent.begin(), _descent.end(),
					parent->_succdir.begin());
			parent->_fx = ftrial;
			parent->_searchsuccess = true;
		}
	}
}

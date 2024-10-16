/*
 * main.cpp
 *
 *  Created on: Oct 9, 2024
 *      Author: mgime
 */

#include <iostream>
#include <cmath>

#include "../src/linear_blas.h"
#include "../src/multivariate/multivariate.h"
#include "multivariate/de/ssde.h"

#include "../src/random.hpp"

using Random = effolkronium::random_static;
using namespace std;

double fx(const double *x) {
	double tot = 0.0;
	for (int i = 1; i < 10; i++) {
		tot += 100 * pow(x[i] - pow(x[i - 1], 2.), 2.) + pow(1 - x[i - 1], 2.);
	}
	return tot;
//	double tot = 0.0;
//	double prod = 1.0;
//	for (int i = 0; i < 10; i++){
//		tot += x[i] * x[i];
//		prod *= cos(x[i] / sqrt(i + 1));
//	}
//	return 1 + tot / 4000 - prod;
}
;

int main() {
	SSDESearch alg { 50000, 40, 1e-10, 1000 };

	std::vector<double> lower(10, -30.0);
	std::vector<double> upper(10, 30.0);
	multivariate_problem problem { fx, 10, &lower[0], &upper[0] };

	std::vector<double> guess(10);
	for (int i = 0; i < 10; i++) {
		guess[i] = Random::get(-30., 30.);
	}

	multivariate_solution sol = alg.optimize(problem, &guess[0]);
	std::cout << sol.toString() << std::endl;
	std::cout << fx(&sol._sol[0]) << std::endl;
	std::cout << "yes" << std::endl;

}


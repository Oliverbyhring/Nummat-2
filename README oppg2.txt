###################################
##### Tidsplan
###################################

26. oktober - start

29. oktober - lest og forst�tt B splines quadrature + alle oppgaver

1. november - 2a-2d kj�rende

6. nov - Kj�rende kode 2e-2h. Even bortreist. 

Tid for stokmod.

12. november - Fungerende kode for alle oppgaver

15. november - Even back

17. november - Optimalisert kode for alle oppgaver

21. november - ferdig skrevet i Latex

24. november - deadline

###################################
##### Kodeplan
###################################

2d)

	Prepare_Data :
w og xi initialiseres
F evalueres
dF evalueres
Kalkulerer eksakte integraler som lagres i Spline_Quadrature
returnerer initialbetingelser med 2nXn ivaretatt

	Assembly:
opdaterer F og dF ut fra nye l�sninger mhp xi og w

	Spline_Quadrature:
Lagrer eksakte integraler
kj�rer loop som bruker assembly i hver loop

###################################
##### Resources
###################################

https://docs.google.com/document/d/1_qiC80mygluc7YxwivCQ2touO0cV4QCjtIwwOKhWDrE/edit?usp=sharing

Splipy har f�lgende innebygd:
integrate(t0, t1)[source]
	Integrate all basis functions over a given domain

evalute_derivative(u, v[, d=(1, 1)])�
	Evaluate the derivative of the surface at the given parametric values.

Progmester Sivert, kan det brukes?



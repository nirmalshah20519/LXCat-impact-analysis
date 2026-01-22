MDPI

Article

# Crossing Frequency Method Applicable to Intermediate Pressure Plasma Diagnostics Using the Cutoff Probe

Si-jun Kim <sup>1</sup>, Jang-jae Lee <sup>2</sup>, Young-seok Lee <sup>2</sup>, Chul-hee Cho <sup>2</sup> and Shin-jae You <sup>2,3,\*</sup>

- <sup>1</sup> Nanotech Optoelectronics Research Center, Yongin 16882, Korea; kim\_sijun@naver.com
- Applied Physics Lab for PLasma Engineering (APPLE), Department of Physics, Chungnam National University, Daejeon 34134, Korea; leejj3800@naver.com (J.-j.L.); ys.dunphy@gmail.com (Y.-s.L.); paulati@naver.com (C.-h.C.)
- Institute of Quantum Systems (IQS), Chungnam National University, Daejeon 34134, Korea
- \* Correspondence: sjyou@cnu.ac.kr

**Abstract:** Although the recently developed cutoff probe is a promising tool to precisely infer plasma electron density by measuring the cutoff frequency (  ) in the S<sub>21</sub> spectrum, it is currently only applicable to low-pressure plasma diagnostics below several torr. To improve the cutoff probe, this paper proposes a novel method to measure the crossing frequency (  ), which is applicable to high-pressure plasma diagnostics where the conventional    method does not operate. Here,    is the frequency where the S<sub>21</sub> spectra in vacuum and plasma conditions cross each other. This paper demonstrates the    method through three-dimensional electromagnetic wave simulation as well as experiments in a capacitively coupled plasma source. Results demonstrate that the method operates well at high pressure (several tens of torr) as well as low pressure. In addition, through circuit model analysis, a method to estimate electron density from    is discussed. It is believed that the proposed method expands the operating range of the cutoff probe and thus contributes to its further development.

**Keywords:** plasma diagnostics; electron density measurement; cutoff probe; high-pressure plasma; crossing frequency method

Citation: Kim, S.-j.; Lee, J.-j.; Lee, Y.-s.; Cho, C.-h.; You, S.-j. Crossing Frequency Method Applicable to Intermediate Pressure Plasma Diagnostics Using the Cutoff Probe. *Sensors* **2022**, 22, 1291. https://doi.org/10.3390/s22031291

Academic Editor: Bruno Goncalves

Received: 6 January 2022 Accepted: 3 February 2022 Published: 8 February 2022

**Publisher's Note:** MDPI stays neutral with regard to jurisdictional claims in published maps and institutional affiliations.

Copyright: © 2022 by the authors. Licensee MDPI, Basel, Switzerland. This article is an open access article distributed under the terms and conditions of the Creative Commons Attribution (CC BY) license (https://creativecommons.org/licenses/by/4.0/).

## 1. Introduction

Composed of physically energetic charged particles and chemically reactive neutral particles, plasma has been widely used in various fields including material fabrication and nuclear fusion as well as medical, environmental, and aerospace industries [1,2]. Plasma processing techniques such as plasma etching [3–7], ashing [8–11], and deposition [12–16] are the most important steps to fabricate the high-end memory and system semiconductors used in internet of things and artificial intelligence technologies. For plasma deposition in particular, plasma sputtering, plasma-enhanced chemical vapor deposition (PECVD), and plasma-enhanced atomic layer deposition (PEALD) approaches have been widely used for their high deposition rates, low-temperature processing, good film conformality, and high film uniformity [12,13,17,18].

In conventional deposition processing, trial-and-error methods were first adopted to find the optimum process window [19]. However, these days, such an approach seems ill-suited since the current challenges in cutting-edge material fabrication involve processing steps that abruptly increase and also involve complicated chemistries [1,3,4,12,13]. To overcome this limitation, two alternatives have been proposed, namely computer simulation and plasma internal parameter diagnostic methods [20].

For the former, accompanied by the explosive improvements in computing power, multiphysics methods allow us to simulate the plasma deposition process, predict the processing results from plasma sputtering [21], PECVD [22], and PEALD [23], and finally estimate the optimum process window based on the results. However, there remains

*Sensors* **2022**, *22*, 1291 2 of 11

a lack of basic atomic data especially for new complex precursors such as bulk reaction cross sections, surface coefficients, and sputtering and secondary electron emission yields [\[24\]](#page-8-17). Consequently, simulation is at present applicable to specific processes using simple chemistries.

The latter, referring to methods that find the optimum process window based on internal plasma parameters, has attracted great interest in industrial as well as academic fields since plasma has an influence on most chemical reactions contributing to the deposition process [\[25](#page-8-18)[–28\]](#page-9-0). Specifically, electrons produce chemical species, which play a dominant role in deposition chemistry, while energetic ions and metastables activate the material surface, which enhances surface chemical reactions [\[12,](#page-8-6)[19\]](#page-8-11). Here, the plasma internal parameters include electron density, electron temperature, ion flux, and ion energy distribution. Among them, electron density is known as one of the most important parameters because it is directly related to the deposition rate and processing productivity [\[29](#page-9-1)[,30\]](#page-9-2).

Various plasma diagnostics to measure electron density have been developed, such as the Langmuir probe measuring electron and ion current [\[31](#page-9-3)[,32\]](#page-9-4), the line ratio method analyzing optical emission spectra by excited atoms and molecules [\[33\]](#page-9-5), the laser Thomson scattering method measuring scattered laser light by electrons [\[34\]](#page-9-6), and microwave probes analyzing absorbed, reflected, and transmitted microwave signals [\[35](#page-9-7)[–38\]](#page-9-8). The Langmuir probe can infer various electron characteristics such as electron density, temperature, and energy distribution, but is not applicable to deposition processing since films deposited on the probe tip block the conduction current, and the design of an RF filter to block high-frequency noise is difficult [\[39\]](#page-9-9). As for the optical methods, while the measurement of a plasma emission spectrum through a viewport in a process chamber is relatively simple, these approaches are only applicable to a narrow processing window since the emission spectrum by each species overlaps, which complicates spectra analysis [\[33\]](#page-9-5). The laser Thomson scattering method requires a large and stable space to generate the laser and detect scattered light since the detection signal is small. Furthermore, both optical and laser methods are vulnerable to deposition on the viewport, which induces a decrease in emission and scattered light signals.

On the other hand, the microwave probes are free from the issue of film deposition on the probe antenna [\[40\]](#page-9-10) as displacement current can flow through a dielectric film. Furthermore, the microwave signal only slightly distorts the processing plasma because the probes operate at relatively low power, i.e., <1 mW [\[41\]](#page-9-11), in comparison to common RF powers ranging from several hundreds to thousands of watts. Hence, microwave probes are seen as useful tools in deposition processing, and various types of probes have been developed. Details of these probes, such as the curling probe (CLP), the multipole resonance probe (MRP), the cutoff probe (CP), etc., are well explained in [\[42,](#page-9-12)[43\]](#page-9-13).

Recently, microwave probes have been applied to measure the electron density of deposition plasma. Styrnoll et al. applied the MRP to the ion-assisted deposition used in optical coatings at a relatively low pressure (<0.2 Torr) [\[44\]](#page-9-14). Ogawa et al. applied the CLP to a hydrogenated amorphous carbon film deposition process (<0.01 Torr) [\[45\]](#page-9-15), and Lee et al. applied the CP to a fluorocarbon film deposition process (<0.02 Torr) [\[7\]](#page-8-3). The probes in these works showed good performance in measuring electron density during the deposition process at low pressure.

However, based on the analysis in [\[46\]](#page-9-16), the CLP and MRP might be seen as unsuitable for high-pressure applications. The CP, likewise, has a limitation for high-pressure plasma measurement [\[47–](#page-9-17)[49\]](#page-9-18). Probe performance reduction in such an environment results from frequent electron–neutral collisions that decrease plasma–electromagnetic wave interaction and diminish the resonant character of the probe system. Accordingly, there is a great demand for the means to measure high-pressure deposition plasma to analyze and optimize the deposition process.

Considering that the CP is a promising microwave probe showing high reproducibility and high accuracy [\[43,](#page-9-13)[50,](#page-9-19)[51\]](#page-9-20), improvements of the CP for high-pressure plasma meaSensors 2022, 22, 1291 3 of 11

surement are highly desirable. In the current paper, an alternative method to measure electron density using the CP in a high-pressure condition is proposed, called the crossing frequency method.

The remainder of this paper is as follows. In the second section, simulation analysis for the crossing frequency method is given. In the third section, experimental validation of the proposed method is given, and a simple relation between electron density and crossing frequency is presented. Finally, in the fourth section, a summary of this paper is provided.

#### <span id="page-2-1"></span>2. Simulation Demonstration

A commercial software to solve Maxwell's equations in three-dimensional space, Computer Simulation Technology (CST) MicroWave Studio Suite, was adopted in this study. CST simulation is based on a finite-difference time-domain method and is quite accurate compared with experiments [50]. This simulation considers plasma as a dispersive dielectric material, called the Drude model, in which ions and electrons are immobile and freely mobile, respectively, with a plasma dielectric constant (  ) given by

<span id="page-2-0"></span>

(1)

where j is a complex number,    is the vacuum dielectric constant,    is the microwave frequency,    (=8980  ) is the plasma oscillation frequency,    is the electron density in units of cm<sup>-3</sup>, and    is the electron–neutral collision frequency. Here, the dispersive dielectric material means that its dielectric constant has frequency dependence. Equation (1) is used to solve Maxwell's equation inside the plasma domain. Here, for simplicity, it is assumed that the electron–neutral elastic collision is only considered for the calculation of    between an electron and argon atom at an electron temperature of 2 eV and a gas temperature of 300 K. The 2 eV is a mean value commonly used in plasma processing. A Maxwellian electron energy distribution is also assumed. Then,    is equal to    in MHz, where p is the pressure in mTorr.

CST simulation provides several boundary conditions including electrical ground, magnetic ground, open, and periodic conditions. To study microwave probes, the electrical ground and open boundary conditions are the most commonly used. To include vacuum chamber effects, the former is usually applied, while to only consider the principal effect without any boundary effects, the latter is typically used. In the current work, the purpose of the simulation-based study was to investigate the basic operation of the crossing frequency method, and so the open boundary condition was applied to all simulation domain boundaries.

Figure 1 shows the simulation configuration, where the CP is immersed in a uniform rectangular plasma (  ) having an    of   . The CP consists of radiating and detecting tips that are each connected to separate coaxial cables, which play the role of a transmission line with characteristic impedance of   . The plasma dimension is larger than the skin depth of the microwaves ranging from 0 to 5 GHz, so the plasma shape is not an important factor. The probe tip length, distance, and radius are 5.0 mm, 4.0 mm, and 0.26 mm, respectively, and the length of the coaxial cables is 30.0 mm. The sheath covering the cutoff probe is considered as a vacuum with a dielectric constant of    and a width of 0.234 mm, which is the same as the floating sheath width,   , where    is the Debye length [52].

The    spectrum calculation in this simulation is as follows. A Gaussian pulse signal including microwaves from 0 to 5 GHz enters the end of the coaxial cable and proceeds toward the radiation tip with radiation power   . The pulse signals are reflected at the plasma–sheath interface, absorbed inside the plasma, and transmitted through the plasma by way of evanescent waves to the detection tip with detection power   . Then, each power in the time domain is transformed via the fast Fourier transform method in the frequency domain as    and   . The    spectrum can then be calculated by   .

*Sensors* **2022**, *22*, 1291 4 of 11

<span id="page-3-0"></span>**Figure 1.** Configuration in a three-dimensional electromagnetic wave simulation.

Figure [2](#page-4-0) shows S<sup>21</sup> spectra at vacuum and various pressure conditions. Here, the vacuum condition means that there is no plasma and the CP is immersed in a vacuum material whose dielectric constant is *e*0. There is a clear resonance peak (maximum S<sup>21</sup> value) in the vacuum spectrum near 2 GHz that results from the quarter-wavelength resonance by the coaxial cable, which is the same as in [\[53\]](#page-9-22). The simple estimation that the length of the coaxial cable is 30 mm and the quarter-wavelength of 2 GHz is about 30 mm support this quarter-wavelength resonance. Otherwise, in the case of plasma (<10 Torr), there is a clear cutoff peak in the S<sup>21</sup> spectrum as marked in Figure [2,](#page-4-0) and this frequency is defined as the cutoff frequency, *f*cutoff. As the pressure increases, the cutoff peak broadens before finally disappearing above 5 Torr [\[47\]](#page-9-17), which is known as the pressure limitation of the CP. That is, the conventional method measuring *f*cutoff can operate below several torr.

We note here that there is a specific frequency where the vacuum spectrum and the spectra at various pressures cross each other, i.e., they have the same S<sup>21</sup> value at constant electron density. This frequency can also be seen in a similar simulation in [\[48\]](#page-9-23). In the current paper, this point was defined as the crossing frequency, *f*cross. The *f*cross frequency is clearly seen even at high pressure where *f*cutoff disappears. Hence, the proposed method of measuring *f*cross can operate up to several tens of torr, providing a wider dynamic range than the *f*cutoff method in terms of pressure. In fact, the *f*cross is a direct function of electron density and sheath width and is independent of pressure. A detailed analysis of *f*cross is discussed in the next section.

Sensors **2022**, 22, 1291 5 of 11

<span id="page-4-0"></span>**Figure 2.** Simulated    spectra at various pressures with an electron density of    cm<sup>-3</sup>, tip length of 5.0 mm, sheath width of 0.234 mm, and tip distance of 4 mm.

#### 3. Experimental Demonstration and Circuit Model Analysis

#### <span id="page-4-1"></span>3.1. Experimental Demonstration

Figure 3 shows a schematic diagram of the experimental setup. To demonstrate the crossing frequency method, a capacitively coupled plasma (CCP) was adopted. A 13.56 MHz power generator (RF5S, Advanced Energy Inc., Denver, CO, USA) was applied to a powered electrode with a diameter of 150 mm via an impedance matching box (PathFinder, Plasmart Inc., Daejeon, Korea) which maintains a load impedance of    from the rf generator. The gap distance between the powered and grounded electrodes was 68 mm. The CP had a length of 5.0 mm, a tip distance of 5.0 mm, and a radius of 0.26 mm. The probe was inserted in the middle of the gap distance and connected with a vector network analyzer (S3601B, Saluki Technology Inc., Taipei, Taiwan) to measure the S<sub>21</sub> spectrum. A rotary pump (GHP-800K, KODIVAC Ltd., Gyeong buk, Korea) and a turbomolecular pump (D-35614 Asslar, Pfeiffer Vacuum, Inc., Asslar, Germany) sustained a high-purity vacuum. The base pressure measured by a vacuum gauge (FullRange Gauge, Pfeiffer Vacuum, Inc, Asslar, Germany) was    Torr. Ar gas was injected into the chamber via a mass flow controller (MFC) (TN280, SMTEK CO., Ltd., Seongnam-si, Korea), and an MFC controller (GMC1200, ATOVAC Ltd., Yongin-si, Korea) maintained a constant gas flow rate of 50.0 sccm. The chamber pressure with Ar gas injection was measured by a precise vacuum gauge (Baratron 1 Torr, MKS Instruments Inc., Andover, MA, USA), and the pressure was controlled by changing the open and close ratio of a manual gate valve, as shown in Figure 3.

Sensors **2022**, 22, 1291 6 of 11

<span id="page-5-0"></span>Figure 3. Schematic diagram of the experimental setup in a capacitively coupled plasma source.

It is well known that in CCP discharge, the electron density depends on the pressure due to changes in the electron heating mechanism [54,55]. To demonstrate the proposed method, it is important to maintain the same electron density while the chamber pressure changes the same as in the simulation. To accomplish this, the rf power was slightly adjusted to preserve the same    in the S<sub>21</sub> spectrum. After    vanished at high pressure (  0.7 Torr), the rf power adjustment was no longer conducted. In [54,55], one can find that the electron density is nearly constant with a pressure above 1 Torr. Therefore, the adjustment approach in the current work was believed to be reasonable.

Figure 4a shows the experimental    spectra at vacuum and various pressure conditions. In contrast to the simulation results, the vacuum spectrum shows several resonance peaks that result from the chamber cavity effect [56], as the vacuum chamber is an electrical ground that forms a cavity structure. As shown in Figure 3, since the chamber dimension is long, the cavity resonance frequency forms in a relatively low frequency regime (several gigahertz). As for the plasma cases, there is a clear cutoff peak at low pressure that broadens with increasing pressure, showing the same trend as in the simulation results of Figure 2.

<span id="page-5-1"></span>**Figure 4.** (a) Experimental    spectra at various pressures and vacuum with a cutoff frequency (  ) of 1.5 GHz. (b) Measured    at constant    over pressure.

Sensors **2022**, 22, 1291 7 of 11

We note the clear    in the experimental    spectra. Figure 4b plots    over the chamber pressure and measurable range of   . As shown in that figure, the    method is applicable below 700 mTorr, while    shows a higher range. Since the vacuum gauge used in this experiment can measure pressure up to 1 Torr, higher pressure experiments were not conducted. Nevertheless, by combining the experimental and simulation results, the proposed method can reasonably be said to be applicable at several torr.

It should also be noted that the cavity peaks can distort the vacuum spectrum, which means that the vacuum spectrum does not cross    even though the spectra from plasma do. While a full discussion of this point is beyond the scope of this paper, two solutions are briefly given as follows. The first is to remove the cavity resonance peaks through the time-gating method as in [57], which does not use continuous sinusoidal signals but pulse signals and removes the detection signals that include the cavity information in the time domain. The second approach is to choose an alternative reference signal, such as one of the pressure conditions shown in Figure 4a.

## 3.2. Circuit Model Analysis

Until now, the operation of the    method has been demonstrated by simulation and experiment. In this subsection, a circuit model analysis is provided to elucidate the meaning of the proposed method and to derive a relation between electron density and   . The circuit model is the same as in [48], and the same geometric parameters as in Section 2 are used in this model. Figure 5a shows    spectra at vacuum and various pressures, with the results representing that the circuit model well reproduces    as well as the vanishing of   . Since the circuit model does not include electromagnetic effects such as cavity resonance, electron heating, etc., this analysis allows us to simply and clearly understand the    method. Via the circuit model analysis, the    method seems to have no limitation in terms of pressure. However, in practice, various causes such as cavity resonance, rf noise, instrument limitations, etc., distort the spectrum and give rise to the limitation of    as shown in Section 3.1. Nevertheless, the model result implies that the    method basically has a wider application window than that of the    method.

<span id="page-6-0"></span>**Figure 5.** (a)    spectra at 100 mTorr, 1 Torr, 5 Torr, 10 Torr, and vacuum (without plasma) with an electron density of    cm<sup>-3</sup> and a fixed sheath width of 0.234 mm. (b) Normalized crossing frequency (  ) over the sheath width portion with antenna distance (s/d), where s and d are the sheath width and the antenna distance, respectively.

Since the sheath width changes the plasma width, the    was affected by the sheath width. To investigate this effect, Figure 5b shows a normalized crossing frequency,   , over the sheath width portion s/d at various electron densities, where   , s and d are the plasma oscillation frequency, sheath width, and antenna distance, respectively.

Sensors 2022, 22, 1291 8 of 11

The normalized frequency ranges from 0.7 to 1.0 over a sheath width portion from 1% to 99%, and interestingly,    is independent of the electron density. Therefore, if s is provided, the electron density (  ) can be obtained from    (  ) by measuring    based on Figure 5.

The sheath width around the CP can be estimated by measuring the series resonance frequency and the cutoff frequency in the    spectrum; this is well explained in [58]. However, as previously mentioned,    disappears at high pressure, and thus estimating s becomes a challenge. To overcome this, one alternative way is to take the average as

 (2)

where x and g(x) are defined as s/d and   , respectively, with this equation having a standard deviation of 0.07. As a result, the averaged crossing frequency over sheath width,   , is given by

<span id="page-7-0"></span>

If other diagnostics to measure the sheath width are available, the best way is to measure the sheath width and derive the electron density from the result of Figure 5. However, if the sheath width is unknown, by using Equation (3), the electron density can be estimated with a theoretical discrepancy of about 10%.

## 4. Conclusions

This paper proposed a novel method to measure the crossing frequency   , which is applicable for high-pressure plasma diagnostics where the conventional    method does not operate. The suggested method was demonstrated through both a CST simulation and an experiment with CCP discharge. Moreover, through the use of the circuit model, the relation between    and    was investigated. If the sheath width can be provided, the electron density can be estimated by measuring    with the result from Figure 5. On the other hand, if the sheath width is unknown, by using Equation (3), the electron density can be estimated with a theoretical discrepancy of about 10%. In conclusion, the results show that the proposed method operates well in high pressure (several tens of torr) as well as low pressure.

**Author Contributions:** Conceptualization, S.-j.Y.; validation, S.-j.K., J.-j.L., Y.-s.L. and C.-h.C.; formal analysis, S.-j.K.; writing—original draft preparation, S.-j.K.; review and editing, S.-j.Y.; supervision, S.-j.Y. All authors have read and agreed to the published version of the manuscript.

Funding: This research was supported by National Research Council of Science & Technology (NST) grants by the Korean government (MSIP) (no. CAP-17-02-NFRI, CRF-20-01-NFRI); by the Technology Innovation Program (20014366) funded By the Ministry of Trade, Industry & Energy (MOTIE, Korea); by the Next-generation Intelligence semiconductor R&D Program through the Korea Evaluation Institute of Industrial Technology (KEIT) funded by the Korean government (MOTIE); by the Korea Institute of Energy Technology Evaluation and Planning (KETEP) and the MOTIE of the Korea (20202010100020); by the MOTIE (20009818, 20010420) and KSRC (Korea Semiconductor Research Consortium) support program for the development of future semiconductor devices; by a Korea Institute for Advancement of Technology (KIAT) grant funded by the Korean Government (MOTIE) (P0008458, The Competency Development Program for Industry Specialist); and by the Basic Science Research Program through the National Research Foundation of Korea (NRF) funded by the Ministry of Education (NRF-2020R1A6A1A03047771).

Institutional Review Board Statement: Not applicable.

Informed Consent Statement: Not applicable.

**Data Availability Statement:** The data presented in this study are available on request from the corresponding author.

Conflicts of Interest: The authors declare no conflict of interest.

*Sensors* **2022**, *22*, 1291 9 of 11

### **References**

<span id="page-8-0"></span>1. Adamovich, I.; Baalrud, S.D.; Bogaerts, A.; Bruggeman, P.J.; Cappelli, M.; Colombo, V.; Czarnetzki, U.; Ebert, U.; Eden, J.G. The 2017 Plasma Roadmap: Low temperature plasma science and technology. *J. Phys. D Appl. Phys.* **2017**, *50*, 323001. [\[CrossRef\]](http://doi.org/10.1088/1361-6463/aa76f5)

- <span id="page-8-1"></span>2. Bogaerts, A.; Tu, X.; Whitehead, J.C.; Centi, G.; Lefferts, L.; Guaitella, O.; Azzolina-Jury, F.; Kim, H.; Murphy, A.B.; Schneider, W.F. The 2020 plasma catalysis roadmap. *J. Phys. D Appl. Phys.* **2020**, *53*, 443001. [\[CrossRef\]](http://dx.doi.org/10.1088/1361-6463/ab9048)
- <span id="page-8-2"></span>3. Ishikawa, K.; Karahashi, K.; Ishijima, T.; Cho, S.I.I.; Elliott, S.; Hausmann, D.; Mocuta, D.; Wilson, A.; Kinoshita, K. Progress in nanoscale dry processes for fabrication of high-aspect-ratio features: How can we control critical dimension uniformity at the bottom? *Jpn. J. Appl. Phys.* **2018**, *57*, 06JA01. [\[CrossRef\]](http://dx.doi.org/10.7567/JJAP.57.06JA01)
- <span id="page-8-12"></span>4. Donnelly, V.M.; Kornblit, A. Plasma etching: Yesterday, today, and tomorrow. *J. Vac. Sci. Technol.* **2013**, *31*, 050825. [\[CrossRef\]](http://dx.doi.org/10.1116/1.4819316)
- 5. Cho, C.; You, K.; Kim, S.; Lee, Y.; Lee, J.; You, S. Characterization of SiO<sup>2</sup> Etching Profiles in Pulse-Modulated Capacitively Coupled Plasmas. *Materials* **2021**, *14*, 5036. [\[CrossRef\]](http://dx.doi.org/10.3390/ma14175036) [\[PubMed\]](http://www.ncbi.nlm.nih.gov/pubmed/34501123)
- 6. Seong, I.H.; Lee, J.J.; Cho, C.H.; Lee, Y.S.; Kim, S.J.; You, S.J. Characterization of SiO<sup>2</sup> Over Poly-Si Mask Etching in Ar/C4F8 Capacitively Coupled Plasma. *Appl. Sci. Converg. Technol.* **2021**, *30*, 176–182. [\[CrossRef\]](http://dx.doi.org/10.5757/ASCT.2021.30.6.176)
- <span id="page-8-3"></span>7. Lee, Y.; Seong, I.; Lee, J.; Lee, S.; Cho, C.; Kim, S.; You, S. Various evolution trends of sample thickness in fluorocarbon film deposition on SiO<sup>2</sup> . *J. Vac. Sci. Technol. A* **2022**, *40*, 013001. [\[CrossRef\]](http://dx.doi.org/10.1116/6.0001466)
- <span id="page-8-4"></span>8. Lee, H.; Chung, C. Electron heating and control of electron energy distribution for the enhancement of the plasma ashing processing. *Plasma Sources Sci. Technol.* **2015**, *24*, 024001. [\[CrossRef\]](http://dx.doi.org/10.1088/0963-0252/24/2/024001)
- 9. Susa, Y.; Ohtake, H.; Jianping, Z.; Chen, L.; Nozawa, T. Characterization of CO<sup>2</sup> plasma ashing for less low-dielectric-constant film damage. *J. Vac. Sci. Technol. A* **2015**, *33*, 061307. [\[CrossRef\]](http://dx.doi.org/10.1116/1.4931785)
- 10. Aizawa, T.; Shimada, T.; Sakurai, T.; Nakano, Y.; Tanaka, Y.; Uesugi, Y.; Ishijima, T. Improved Uniformity of Photoresist Ashing for a Half-Inch Wafer with Double U-shaped Antenna Structure in a Microwave-Excited Water Vapor Plasma. *J. Photopolym. Sci. Technol.* **2021**, *34*, 5. [\[CrossRef\]](http://dx.doi.org/10.2494/photopolymer.34.479)
- <span id="page-8-5"></span>11. Thedjoisworo, B.; Cheung, D.; Crist, V. Comparison of the effects of downstream H2- and O2-based plasmas on the removal of photoresist, silicon, and silicon nitride. *J. Vac. Sci. Technol. B* **2013**, *31*, 021206. [\[CrossRef\]](http://dx.doi.org/10.1116/1.4792254)
- <span id="page-8-6"></span>12. Profijt, H.B.; Potts, S.E.; van de Sanden, M.C.M.; Kessels, W.M.M. Plasma-Assisted Atomic Layer Deposition: Basics, Opportunities, and Challenges. *J. Vac. Sci. Technol. A* **2011**, *29*, 050801. [\[CrossRef\]](http://dx.doi.org/10.1116/1.3609974)
- <span id="page-8-8"></span>13. Kim, H.; Oh, I. Review of plasma-enhanced atomic layer deposition: Technical enabler of nanoscale device fabrication. *Jpn. J. Appl. Phys.* **2014**, *53*, 03DA01. [\[CrossRef\]](http://dx.doi.org/10.7567/JJAP.53.03DA01)
- 14. Potts, S.E.; Keuning, W.; Langereis, E.; Dingemans, G.; van de Sanden, M.C.M.; Kessels, W.M.M. Low Temperature Plasma-Enhanced Atomic Layer Deposition of Metal Oxide Thin Films. *J. Electrochem. Soc.* **2010**, *157*, P66–P74. [\[CrossRef\]](http://dx.doi.org/10.1149/1.3428705)
- 15. King, S.W. Plasma enhanced atomic layer deposition of SiNx:H and SiO<sup>2</sup> . *J. Vac. Sci. Technol. A* **2011**, *29*, 041501. [\[CrossRef\]](http://dx.doi.org/10.1116/1.3584790)
- <span id="page-8-7"></span>16. Lee, D.; Wan, Z.; Bae, J.; Lee, H.; Ahn, J.; Kim, S.; Kim, J.; Kwon, S. Plasma-enhanced atomic layer deposition of SnO<sup>2</sup> thin films using SnCl<sup>4</sup> and O<sup>2</sup> plasma. *Mater. Lett.* **2016**, *166*, 163–166. [\[CrossRef\]](http://dx.doi.org/10.1016/j.matlet.2015.12.049)
- <span id="page-8-9"></span>17. Hamedani, Y.; Macha, P.; Bunning, T.J.; Naik, R.R.; Vasudev, M.C. Plasma-Enhanced Chemical Vapor Deposition: Where we are and the Outlook for the Future. In *Chemical Vapor Deposition, Recent Advances and Applications in Optical, Solar Cells and Solid State Devices*; Sudheer Neralla; IntechOpen: London, UK, 2016; pp. 247–251.
- <span id="page-8-10"></span>18. Vasudev, M.C.; Anderson, K.D.; Bunning, T.J.; Tsukruk, V.V.; Naik, R.R. Exploration of Plasma-Enhanced Chemical Vapor Deposition as a Method for Thin-Film Fabrication with Biological Applications. *ASC Appl. Mater. Interfaces* **2013**, *5*, 3983–3994. [\[CrossRef\]](http://dx.doi.org/10.1021/am302989x)
- <span id="page-8-11"></span>19. Lieberman, M.A.; Lichtenberg, A.J. *Principles of Plasma Discharges and Materials Processing*, 2nd ed.; Wiley&Sons. Inc.: Hobken, NJ, USA, 2005; pp. 1–22.
- <span id="page-8-13"></span>20. Marchack, N.; Buzi, L.; Farmer, D.B.; Miyazoe, H.; Papalia, J.M.; Yan, H.; Totir, G.; Engelmann, S.U. Plasma processing for advanced microelectronics beyond CMOS. *J. Appl. Phys.* **2021**, *130*, 080901. [\[CrossRef\]](http://dx.doi.org/10.1063/5.0053666)
- <span id="page-8-14"></span>21. Brault, P. Multiscale Molecular Dynamics Simulation of Plasma Processsing: Application to Plasma Sputtering. *Front. Phys.* **2018**, *6*, 59. [\[CrossRef\]](http://dx.doi.org/10.3389/fphy.2018.00059)
- <span id="page-8-15"></span>22. Denpoh, K.; Moroz, P.; Kato, T.; Matsukuma, M. Multiscale plasma and feature profile simulations of plasma enhanced chemical vapor deposition and atomic layer deposition processes for titanium thin film fabrication. *Jpn. J. Appl. Phys.* **2020**, *59*, SHHB02. [\[CrossRef\]](http://dx.doi.org/10.7567/1347-4065/ab5bc9)
- <span id="page-8-16"></span>23. Becker, M.; Sierka, M. Atomistic Simulations of Plasma-Enhanced Atomic Layer Deposition. *Materials* **2019**, *12*, 2605. [\[CrossRef\]](http://dx.doi.org/10.3390/ma12162605) [\[PubMed\]](http://www.ncbi.nlm.nih.gov/pubmed/31443331)
- <span id="page-8-17"></span>24. Carbone, E.; Graef, W.; Hagelaar, G.; Boer, D.; Hopkins, M.M.; Stephens, J.C.; Yee, B.T.; Pancheshyi, S.; van Dijk, J.; Pitchford, L. Data Needs for Modeling Low-Temperature Non-equilibrium Plasmas: The LXCat Project, History, Perspectives and a Tutorial. *Atoms* **2021**, *9*, 16. [\[CrossRef\]](http://dx.doi.org/10.3390/atoms9010016)
- <span id="page-8-18"></span>25. Rudenko, K.V. Diagnostics of Plasma Processes in Micro- and Nanoelectronics. *High Energy Chem.* **2009**, *43*, 3. [\[CrossRef\]](http://dx.doi.org/10.1134/S0018143909030072)
- 26. Creatore, M.; Palumbo, F.; d'Agostion, R. Deposition of SiOx Films from Hexamethyldisiloxane/Oxygen Radiofrequency Glow Discharges: Process Optimization by Plasma Diagnostics. *Plasmas Polym.* **2002**, *7*, 3. [\[CrossRef\]](http://dx.doi.org/10.1023/A:1019942625607)
- 27. Kirner, S.; Gabriel, O.; Stannowski, B.; Rech, B.; Schlatmann, R. The growth of microcrystalline silicon oxide thin films studied by in situ plasma diagnostics. *Appl. Phys. Lett.* **2013**, *102*, 051906. [\[CrossRef\]](http://dx.doi.org/10.1063/1.4790279)

*Sensors* **2022**, *22*, 1291 10 of 11

<span id="page-9-0"></span>28. Mackus, A.J.M.; Heil, S.B.S.; Langereis, E.; Knoops, H.C.M.; van de Sanden, M.C.M.; Kessels, W.M.M. Optical emission spectroscopy as a tool for studying, optimizing, and monitoring plasma-assisted atomic layer deposition processes. *J. Vac. Sci. Technol. A* **2010**, *28*, 1. [\[CrossRef\]](http://dx.doi.org/10.1116/1.3256227)

- <span id="page-9-1"></span>29. Seman, M.; Wolden, C.A. Investigation of the role of plasma conditions on the deposition rate and electrochromic performance of tungsten oxide thin films. *J. Vac. Sci. Technol. A* **2003**, *21*, 6. [\[CrossRef\]](http://dx.doi.org/10.1116/1.1619416)
- <span id="page-9-2"></span>30. Gopikishan, S.; Banerjee, I.; Bogle, K.A.; Das, A.K.; Pathak, A.P.; Mahapatra, S.K. Paschen curve approach to investigate electron density and deposition rate of Cu in magnetron sputtering system. *Radiat. Eff. Deffects Solids* **2016**, *171*, 999–1005. [\[CrossRef\]](http://dx.doi.org/10.1080/10420150.2016.1267734)
- <span id="page-9-3"></span>31. Cherrington, B.E. The use of electrostatic probes for plasma diagnostics—A review. *Plasma Chem. Plasma Process.* **1982**, *2*, 113–140. [\[CrossRef\]](http://dx.doi.org/10.1007/BF00633129)
- <span id="page-9-4"></span>32. Lobbia, R.B.; Beal, B.E. Recommended Practice for Use of Langmuir Probes in Electric Propulsion Testing. *J. Propuls. Power* **2017**, *33*, 3. [\[CrossRef\]](http://dx.doi.org/10.2514/1.B35531)
- <span id="page-9-5"></span>33. Engeln, R.; Klarenaar, B.; Guaitella, O. Foundations of optical diagnostics in low-temperature plasmas. *Plasma Sources Sci. Technol.* **2020**, *29*, 063001. [\[CrossRef\]](http://dx.doi.org/10.1088/1361-6595/ab6880)
- <span id="page-9-6"></span>34. Belostotskiy, S.G.; Khandelwal, R.K.; Wang, Q.; Donnelly, V.M.; Economou, D.J.; Sadeghi, N. Measurement of electron temperature and density in an argon microdischarge by laser Thomson scattering. *Appl. Phys. Lett.* **2008**, *92*, 221507. [\[CrossRef\]](http://dx.doi.org/10.1063/1.2939437)
- <span id="page-9-7"></span>35. Kim, J.; Seong, D.; Lim, J.; Chung, K. Plasma frequency measurements for absolute plasma density by means of wave cutoff method. *Appl. Phys. Lett.* **2003**, *83*, 23. [\[CrossRef\]](http://dx.doi.org/10.1063/1.1632026)
- 36. Piejak, R.B.; Godyak, V.A.; Garner, R.; Alexandrovich, M.B.; Sternber, N. The hairpin resonator: A plasma density measuring technique revisited. *J. Appl. Phys.* **2004**, *95*, 7. [\[CrossRef\]](http://dx.doi.org/10.1063/1.1652247)
- 37. Blackwell, D.D.; Walker, D.N.; Amatucci, W.E. Measurement of absolute electron density with a plasma impedance probe. *Rev. Sci. Instrum.* **2005**, *76*, 023503. [\[CrossRef\]](http://dx.doi.org/10.1063/1.1847608)
- <span id="page-9-8"></span>38. Dine, S.; Booth, J.-P.; Curley, G.A.; Corr, C.S.; Jolly, J.; Guillon, J. A novel technique for plasma density measurement using surface-wave transmission spectra. *Plasma Sources Sci. Technol.* **2005**, *14*, 777–786. [\[CrossRef\]](http://dx.doi.org/10.1088/0963-0252/14/4/017)
- <span id="page-9-9"></span>39. Chen, F.F. Lecture Notes on Langmuir Probe Diagnostics. In Proceedings of the The 30th International Conference on Plasma Science, Jeju, Korea, 2–5 June 2003.
- <span id="page-9-10"></span>40. Kim, J.-H.; Choi, S.-C.; Shin, Y.-H.; Chung, K.-H. Wave cutoff method to measure absolute electron density in cold plasma. *Rev. Sci. Instrum.* **2004**, *75*, 2706–2710. [\[CrossRef\]](http://dx.doi.org/10.1063/1.1771487)
- <span id="page-9-11"></span>41. You, K.H.; You, S.J.; Kim, D.W.; Na, B.K.; Seo, B.H.; Kim, J.H.; Seong, D.J.; Chang, H.-Y. Measurement of electron density using reactance cutoff probe. *Phys. Plasmas* **2016**, *23*, 053515. [\[CrossRef\]](http://dx.doi.org/10.1063/1.4951029)
- <span id="page-9-12"></span>42. Sugai, H.; Nakamura, K. Recent innovations in microwave probes for reactive plasma diagnostics. *Jpn. J. Appl. Phys.* **2019**, *58*, 060101. [\[CrossRef\]](http://dx.doi.org/10.7567/1347-4065/ab1a43)
- <span id="page-9-13"></span>43. Kim, D.W.; You, S.J.; Kim, J.H.; Chang, H.Y.; Oh, W.Y. Computational comparative study of microwave probes for plasma density measurement. *Plasma Sources Sci. Technol.* **2016**, *25*, 035026. [\[CrossRef\]](http://dx.doi.org/10.1088/0963-0252/25/3/035026)
- <span id="page-9-14"></span>44. Styrnoll, T.; Harhausen, J.; Lapke, M.; Storch, R.; Brinkmann, R.P.; Foest, R.; Ohl, A.; Awakowicz, P. Process diagnostics and monitoring using the multipole resonance probe in an inhomogeneous plasma for ion-assisted deposition of optical coatings. *Plasma Sources Sci. Technol.* **2013**, *22*, 045008. [\[CrossRef\]](http://dx.doi.org/10.1088/0963-0252/22/4/045008)
- <span id="page-9-15"></span>45. Ogawa, D.; Nakamura, K.; Sugai, H. Experimental validity of double-curling probe method in film-depositing plasma. *Plasma Sources Sci. Technol.* **2021**, *30*, 085009. [\[CrossRef\]](http://dx.doi.org/10.1088/1361-6595/ac1b35)
- <span id="page-9-16"></span>46. Xu, J.; Nakamura, K.; Zhang, Q.; Sugai, H. Simulation of resistive microwave resonator probe for high-pressure plasma diagnostics. *Plasma Sources Sci. Technol.* **2009**, *18*, 045009. [\[CrossRef\]](http://dx.doi.org/10.1088/0963-0252/18/4/045009)
- <span id="page-9-17"></span>47. Jun, H.; Lee, Y.; Na, B.; Chang, H. Pressure limitation of electron density measurement using a wave-cutoff method in weakly ionized plasmas. *Phys. Plasmas* **2008**, *15*, 124504. [\[CrossRef\]](http://dx.doi.org/10.1063/1.3054542)
- <span id="page-9-23"></span>48. Kim, D.W.; You, S.J.; Na, B.K.; Kim, J.H.; Chang, H.Y. An analysis on transmission microwave frequency spectrum of cut-off probe. *Appl. Phys. Lett.* **2011**, *99*, 131502. [\[CrossRef\]](http://dx.doi.org/10.1063/1.3634022)
- <span id="page-9-18"></span>49. Kim, S.J.; Lee, J.J.; Kim, D.W.; Kim, J.H.; You, S.J. A transmission line model of the cutoff probe. *Plasma Sources Sci. Technol.* **2019**, *28*, 055014. [\[CrossRef\]](http://dx.doi.org/10.1088/1361-6595/ab1dc8)
- <span id="page-9-19"></span>50. Kim, D.W.; You, S.J.; Kwon, J.H.; You, K.H.; Seo, B.H.; Kim, J.H.; Yoon, J.-S.; Oh, W.Y. Reproducibility of the cutoff probe for the measurement of electron density. *Phys. Plasmas* **2016**, *23*, 063501. [\[CrossRef\]](http://dx.doi.org/10.1063/1.4947222)
- <span id="page-9-20"></span>51. Seo, B.; Kim, D.; Kim, J.; You, S. Investigation of reliability of the cutoff probe by a comparison with Thomson scattering in high density processing plasmas. *Phys. Plasmas* **2017**, *24*, 123502. [\[CrossRef\]](http://dx.doi.org/10.1063/1.4996220)
- <span id="page-9-21"></span>52. Kim, D.-W.; Youb, S.-J.; Kim, J.-H.; Seong, D.-J.; Chang, H.-Y.; Oh, W.-Y. Computational study on reliability of sheath width measurement by the cutoff probe in low pressure plasmas. In Proceedings of the 1st EPS Conference on Plasma Diagnostics (1STECPD), Frascati, Rome, Italy, 14–17 April 2015.
- <span id="page-9-22"></span>53. Kim, D.W.; You, S.J.; Kim, S.J.; Kim, J.H.; Oh, W.Y. Two-resonance probe for measuring electron density in low-pressure plasmas. *Plasma Sources Sci. Technol.* **2017**, *26*, 045015. [\[CrossRef\]](http://dx.doi.org/10.1088/1361-6595/aa5fe7)
- <span id="page-9-24"></span>54. Godyak, V.A.; Piejak, R.B.; Alexandrovich, B.M. Measurements of electron energy distribution in low-pressure RF discharges. *Plasma Sources Sci. Technol.* **1992**, *1*, 36–58. [\[CrossRef\]](http://dx.doi.org/10.1088/0963-0252/1/1/006)
- <span id="page-9-25"></span>55. Lafleur, T.; Chabert, P.; Booth, J.P. Electron heating in capacitively coupled plasmas revisited. *Plasma Sources Sci. Technol.* **2014**, *23*, 035010. [\[CrossRef\]](http://dx.doi.org/10.1088/0963-0252/23/3/035010)

*Sensors* **2022**, *22*, 1291 11 of 11

<span id="page-10-0"></span>56. Na, B.; Kim, D.; Kwon, J.; Chang, H.; Kim, J.; You, S. Computational characterization of cutoff probe system for the measurement of electron density. *Phys. Plasmas* **2012**, *19*, 053504. [\[CrossRef\]](http://dx.doi.org/10.1063/1.4719699)

- <span id="page-10-1"></span>57. Na, B.; You, K.; Kim, D.; Chang, H.; You, S.; Kim, J. Cutoff probe using Fourier analysis for electron density measurement. *Rev. Sci. Instrum.* **2012**, *83*, 013510. [\[CrossRef\]](http://dx.doi.org/10.1063/1.3680103) [\[PubMed\]](http://www.ncbi.nlm.nih.gov/pubmed/22299954)
- <span id="page-10-2"></span>58. Kim, D.W.; You, S.J.; Kim, J.H.; Chang, H.Y.; Yoon, J.-S.; Oh, W.Y. Measurement of effective sheath width around the cutoff probe based on electromagnetic simulation. *Phys. Plasmas* **2016**, *23*, 053516. [\[CrossRef\]](http://dx.doi.org/10.1063/1.4945640)
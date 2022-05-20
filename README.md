# Mass-spectra-calibration
GUI that allows to load spectra measurement from an excel sheet and easily perform a mass calibration.


The interface looks like the figure below. The first section allows to load the data from an excel sheet. The "load spectrum button" opens your folder window and you have to select the excel sheet that contains your datas. You have to specify the time column and row and the voltage column and row.
In this section you also have a small window to compute theoritical ion time of flight in functionof the mass wanted, the ion energy and the distance of flight. It can helps you if you want to calibrate a mass spectrum from of time-of-flight (ToF) spectrometer. It provides an estimation of the time in µs needed by your ions to reach the detector.

Then the spectrum is plotted. You can then save, zoom and move the spectrum. In the second section, you can enter several masses to calibrate clicking the button "Calibrate and plot". Finally the "save calibration" button allows to save the 2nd degree coefficient of your fit and the covariance matrix in a txt file. Keep in mind that a good fit should have the quadratic coefficient larger than the linear coefficient. Your covariance matrix should also have small values. Finally, you can save the calibrated value with the button 'save spectrum data'


![Capture](https://user-images.githubusercontent.com/80101412/169509754-11a20ea5-affe-4930-b791-677332379afb.PNG)

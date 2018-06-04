# Meteobike - Calibration of DHT 22 Sensors

Table 1: Calibration coefficients derived from the intercomparison between the Temperature of the DHT22 sensors 
and the Campbell Scientific CS 215 T/RH Probe.

| DHT22 T/RH Sensor Number |  a1 (Slope) | a0 (Offset) (K) |
| ------------------ | ----------------- |  ----------------- |
 | 01|      1.00100 |      0.152556
 | 02|      1.04445 |     -0.842947
 | 03|      1.02379 |     -0.477584
 | 04|      1.02396 |    -0.0903425
 | 05|      1.02883 |     -0.630883
 | 06|      1.02982 |     -0.581733
 | 07|      1.02943 |     -0.529979
 | 08|      1.03372 |     -0.511949
 | 09|      1.03075 |     -0.915355
 | 10|      1.03066 |     -0.448447
 | 11|      1.03591 |     -0.775025
 | 12|      1.03148 |     -0.646286
 | 13|      1.02880 |     -0.835757
 | 14|      1.03558 |     -0.476893
 | 15|      1.03696 |     -0.668770
 | 16|      1.03297 |     -0.324306
 | 17|      1.02717 |     -0.479167
 | 19|      1.01206 |      0.286130
 | 20|      1.03318 |     -0.837961
 | 22|      1.03719 |     -0.780249


Table 2: Error estimates of the uncalibrated and calibrated temperature sensors

| DHT22 T/RH Sensor Number |  RMSE uncalibrated (K) | RMSE calibrated (K) |
| ------------------ | ----------------- |  ----------------- |
 | 01 |      0.185224 |     0.0775794
 | 02 |      0.347152 |     0.0927080
 | 03 |      0.212728 |      0.148695
 | 04 |      0.328273 |      0.150591
 | 05 |      0.247962 |     0.0818995
 | 06 |      0.208566 |     0.0915424
 | 07 |      0.191032 |      0.115222
 | 08 |      0.191087 |      0.120900
 | 09 |      0.504503 |      0.161172
 | 10 |      0.160270 |     0.0849142
 | 11 |      0.308383 |      0.100752
 | 12 |      0.256013 |      0.119269
 | 13 |      0.456301 |      0.162927
 | 14 |      0.193820 |      0.104383
 | 15 |      0.224738 |     0.0945140
 | 16 |      0.250331 |      0.123113
 | 17 |      0.170489 |     0.0947255
 | 19 |      0.486867 |      0.123660
 | 20 |      0.403362 |      0.147125
 | 22 |      0.318474 |      0.127041
 | All Sensors | 0.28227875 | 0.11613665


The Error is calculated as the root mean square error between the uncalibrated  DHT22 sensor and the reference sensor (CS 215), and between the calibrated  DHT22 sensor and the reference sensor (CS 215)

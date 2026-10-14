# `s1` … `s237` → feature name

Auto-generated from `dict_cols.json` and `dict_cols_sign.json`.

**The same `sN` label means a different feature in the two datasets.** 119 of the
237 columns disagree, marked ⚠️ below. The absolute-rating files carry
`derivative_sign_p0/p1` inside the feature block; the change-direction files carry
`value_p0/p1` there instead, and the whole block shifts by one. Any code that
hardcodes an `sN` name — or an `iloc` column range — is correct for at most one of
them. See [`data-dictionary.md`](data-dictionary.md#the-sn-trap).

| col | `all_data_05*.csv` (absolute rating) | `all_data_05*_sign.csv` (change direction) |
|---|---|---|
| `s1` | `imbalance` | `imbalance` |
| `s2` | `derivative_sign_p0` | `vad_p0` ⚠️ |
| `s3` | `vad_p0` | `total_talking_time_p0` ⚠️ |
| `s4` | `total_talking_time_p0` | `total_number_turns_p0` ⚠️ |
| `s5` | `total_number_turns_p0` | `gaze_0_x_p0` ⚠️ |
| `s6` | `gaze_0_x_p0` | `gaze_0_y_p0` ⚠️ |
| `s7` | `gaze_0_y_p0` | `gaze_0_z_p0` ⚠️ |
| `s8` | `gaze_0_z_p0` | `gaze_1_x_p0` ⚠️ |
| `s9` | `gaze_1_x_p0` | `gaze_1_y_p0` ⚠️ |
| `s10` | `gaze_1_y_p0` | `gaze_1_z_p0` ⚠️ |
| `s11` | `gaze_1_z_p0` | `gaze_angle_x_p0` ⚠️ |
| `s12` | `gaze_angle_x_p0` | `gaze_angle_y_p0` ⚠️ |
| `s13` | `gaze_angle_y_p0` | `pose_Tx_p0` ⚠️ |
| `s14` | `pose_Tx_p0` | `pose_Ty_p0` ⚠️ |
| `s15` | `pose_Ty_p0` | `pose_Tz_p0` ⚠️ |
| `s16` | `pose_Tz_p0` | `pose_Rx_p0` ⚠️ |
| `s17` | `pose_Rx_p0` | `pose_Ry_p0` ⚠️ |
| `s18` | `pose_Ry_p0` | `pose_Rz_p0` ⚠️ |
| `s19` | `pose_Rz_p0` | `AU01_r_p0` ⚠️ |
| `s20` | `AU01_r_p0` | `AU02_r_p0` ⚠️ |
| `s21` | `AU02_r_p0` | `AU04_r_p0` ⚠️ |
| `s22` | `AU04_r_p0` | `AU05_r_p0` ⚠️ |
| `s23` | `AU05_r_p0` | `AU06_r_p0` ⚠️ |
| `s24` | `AU06_r_p0` | `AU07_r_p0` ⚠️ |
| `s25` | `AU07_r_p0` | `AU09_r_p0` ⚠️ |
| `s26` | `AU09_r_p0` | `AU10_r_p0` ⚠️ |
| `s27` | `AU10_r_p0` | `AU12_r_p0` ⚠️ |
| `s28` | `AU12_r_p0` | `AU14_r_p0` ⚠️ |
| `s29` | `AU14_r_p0` | `AU15_r_p0` ⚠️ |
| `s30` | `AU15_r_p0` | `AU17_r_p0` ⚠️ |
| `s31` | `AU17_r_p0` | `AU20_r_p0` ⚠️ |
| `s32` | `AU20_r_p0` | `AU23_r_p0` ⚠️ |
| `s33` | `AU23_r_p0` | `AU25_r_p0` ⚠️ |
| `s34` | `AU25_r_p0` | `AU26_r_p0` ⚠️ |
| `s35` | `AU26_r_p0` | `AU45_r_p0` ⚠️ |
| `s36` | `AU45_r_p0` | `AU01_c_p0` ⚠️ |
| `s37` | `AU01_c_p0` | `AU02_c_p0` ⚠️ |
| `s38` | `AU02_c_p0` | `AU04_c_p0` ⚠️ |
| `s39` | `AU04_c_p0` | `AU05_c_p0` ⚠️ |
| `s40` | `AU05_c_p0` | `AU06_c_p0` ⚠️ |
| `s41` | `AU06_c_p0` | `AU07_c_p0` ⚠️ |
| `s42` | `AU07_c_p0` | `AU09_c_p0` ⚠️ |
| `s43` | `AU09_c_p0` | `AU10_c_p0` ⚠️ |
| `s44` | `AU10_c_p0` | `AU12_c_p0` ⚠️ |
| `s45` | `AU12_c_p0` | `AU14_c_p0` ⚠️ |
| `s46` | `AU14_c_p0` | `AU15_c_p0` ⚠️ |
| `s47` | `AU15_c_p0` | `AU17_c_p0` ⚠️ |
| `s48` | `AU17_c_p0` | `AU20_c_p0` ⚠️ |
| `s49` | `AU20_c_p0` | `AU23_c_p0` ⚠️ |
| `s50` | `AU23_c_p0` | `AU25_c_p0` ⚠️ |
| `s51` | `AU25_c_p0` | `AU26_c_p0` ⚠️ |
| `s52` | `AU26_c_p0` | `AU28_c_p0` ⚠️ |
| `s53` | `AU28_c_p0` | `AU45_c_p0` ⚠️ |
| `s54` | `AU45_c_p0` | `F0final_sma_p0` ⚠️ |
| `s55` | `F0final_sma_p0` | `voicingFinalUnclipped_sma_p0` ⚠️ |
| `s56` | `voicingFinalUnclipped_sma_p0` | `jitterLocal_sma_p0` ⚠️ |
| `s57` | `jitterLocal_sma_p0` | `jitterDDP_sma_p0` ⚠️ |
| `s58` | `jitterDDP_sma_p0` | `shimmerLocal_sma_p0` ⚠️ |
| `s59` | `shimmerLocal_sma_p0` | `logHNR_sma_p0` ⚠️ |
| `s60` | `logHNR_sma_p0` | `audspec_lengthL1norm_sma_p0` ⚠️ |
| `s61` | `audspec_lengthL1norm_sma_p0` | `audspecRasta_lengthL1norm_sma_p0` ⚠️ |
| `s62` | `audspecRasta_lengthL1norm_sma_p0` | `pcm_RMSenergy_sma_p0` ⚠️ |
| `s63` | `pcm_RMSenergy_sma_p0` | `pcm_zcr_sma_p0` ⚠️ |
| `s64` | `pcm_zcr_sma_p0` | `audSpec_Rfilt_sma[0]_p0` ⚠️ |
| `s65` | `audSpec_Rfilt_sma[0]_p0` | `audSpec_Rfilt_sma[1]_p0` ⚠️ |
| `s66` | `audSpec_Rfilt_sma[1]_p0` | `audSpec_Rfilt_sma[2]_p0` ⚠️ |
| `s67` | `audSpec_Rfilt_sma[2]_p0` | `audSpec_Rfilt_sma[3]_p0` ⚠️ |
| `s68` | `audSpec_Rfilt_sma[3]_p0` | `audSpec_Rfilt_sma[4]_p0` ⚠️ |
| `s69` | `audSpec_Rfilt_sma[4]_p0` | `audSpec_Rfilt_sma[5]_p0` ⚠️ |
| `s70` | `audSpec_Rfilt_sma[5]_p0` | `audSpec_Rfilt_sma[6]_p0` ⚠️ |
| `s71` | `audSpec_Rfilt_sma[6]_p0` | `audSpec_Rfilt_sma[7]_p0` ⚠️ |
| `s72` | `audSpec_Rfilt_sma[7]_p0` | `audSpec_Rfilt_sma[8]_p0` ⚠️ |
| `s73` | `audSpec_Rfilt_sma[8]_p0` | `audSpec_Rfilt_sma[9]_p0` ⚠️ |
| `s74` | `audSpec_Rfilt_sma[9]_p0` | `audSpec_Rfilt_sma[10]_p0` ⚠️ |
| `s75` | `audSpec_Rfilt_sma[10]_p0` | `audSpec_Rfilt_sma[11]_p0` ⚠️ |
| `s76` | `audSpec_Rfilt_sma[11]_p0` | `audSpec_Rfilt_sma[12]_p0` ⚠️ |
| `s77` | `audSpec_Rfilt_sma[12]_p0` | `audSpec_Rfilt_sma[13]_p0` ⚠️ |
| `s78` | `audSpec_Rfilt_sma[13]_p0` | `audSpec_Rfilt_sma[14]_p0` ⚠️ |
| `s79` | `audSpec_Rfilt_sma[14]_p0` | `audSpec_Rfilt_sma[15]_p0` ⚠️ |
| `s80` | `audSpec_Rfilt_sma[15]_p0` | `audSpec_Rfilt_sma[16]_p0` ⚠️ |
| `s81` | `audSpec_Rfilt_sma[16]_p0` | `audSpec_Rfilt_sma[17]_p0` ⚠️ |
| `s82` | `audSpec_Rfilt_sma[17]_p0` | `audSpec_Rfilt_sma[18]_p0` ⚠️ |
| `s83` | `audSpec_Rfilt_sma[18]_p0` | `audSpec_Rfilt_sma[19]_p0` ⚠️ |
| `s84` | `audSpec_Rfilt_sma[19]_p0` | `audSpec_Rfilt_sma[20]_p0` ⚠️ |
| `s85` | `audSpec_Rfilt_sma[20]_p0` | `audSpec_Rfilt_sma[21]_p0` ⚠️ |
| `s86` | `audSpec_Rfilt_sma[21]_p0` | `audSpec_Rfilt_sma[22]_p0` ⚠️ |
| `s87` | `audSpec_Rfilt_sma[22]_p0` | `audSpec_Rfilt_sma[23]_p0` ⚠️ |
| `s88` | `audSpec_Rfilt_sma[23]_p0` | `audSpec_Rfilt_sma[24]_p0` ⚠️ |
| `s89` | `audSpec_Rfilt_sma[24]_p0` | `audSpec_Rfilt_sma[25]_p0` ⚠️ |
| `s90` | `audSpec_Rfilt_sma[25]_p0` | `pcm_fftMag_fband250-650_sma_p0` ⚠️ |
| `s91` | `pcm_fftMag_fband250-650_sma_p0` | `pcm_fftMag_fband1000-4000_sma_p0` ⚠️ |
| `s92` | `pcm_fftMag_fband1000-4000_sma_p0` | `pcm_fftMag_spectralRollOff25.0_sma_p0` ⚠️ |
| `s93` | `pcm_fftMag_spectralRollOff25.0_sma_p0` | `pcm_fftMag_spectralRollOff50.0_sma_p0` ⚠️ |
| `s94` | `pcm_fftMag_spectralRollOff50.0_sma_p0` | `pcm_fftMag_spectralRollOff75.0_sma_p0` ⚠️ |
| `s95` | `pcm_fftMag_spectralRollOff75.0_sma_p0` | `pcm_fftMag_spectralRollOff90.0_sma_p0` ⚠️ |
| `s96` | `pcm_fftMag_spectralRollOff90.0_sma_p0` | `pcm_fftMag_spectralFlux_sma_p0` ⚠️ |
| `s97` | `pcm_fftMag_spectralFlux_sma_p0` | `pcm_fftMag_spectralCentroid_sma_p0` ⚠️ |
| `s98` | `pcm_fftMag_spectralCentroid_sma_p0` | `pcm_fftMag_spectralEntropy_sma_p0` ⚠️ |
| `s99` | `pcm_fftMag_spectralEntropy_sma_p0` | `pcm_fftMag_spectralVariance_sma_p0` ⚠️ |
| `s100` | `pcm_fftMag_spectralVariance_sma_p0` | `pcm_fftMag_spectralSkewness_sma_p0` ⚠️ |
| `s101` | `pcm_fftMag_spectralSkewness_sma_p0` | `pcm_fftMag_spectralKurtosis_sma_p0` ⚠️ |
| `s102` | `pcm_fftMag_spectralKurtosis_sma_p0` | `pcm_fftMag_spectralSlope_sma_p0` ⚠️ |
| `s103` | `pcm_fftMag_spectralSlope_sma_p0` | `pcm_fftMag_psySharpness_sma_p0` ⚠️ |
| `s104` | `pcm_fftMag_psySharpness_sma_p0` | `pcm_fftMag_spectralHarmonicity_sma_p0` ⚠️ |
| `s105` | `pcm_fftMag_spectralHarmonicity_sma_p0` | `mfcc_sma[1]_p0` ⚠️ |
| `s106` | `mfcc_sma[1]_p0` | `mfcc_sma[2]_p0` ⚠️ |
| `s107` | `mfcc_sma[2]_p0` | `mfcc_sma[3]_p0` ⚠️ |
| `s108` | `mfcc_sma[3]_p0` | `mfcc_sma[4]_p0` ⚠️ |
| `s109` | `mfcc_sma[4]_p0` | `mfcc_sma[5]_p0` ⚠️ |
| `s110` | `mfcc_sma[5]_p0` | `mfcc_sma[6]_p0` ⚠️ |
| `s111` | `mfcc_sma[6]_p0` | `mfcc_sma[7]_p0` ⚠️ |
| `s112` | `mfcc_sma[7]_p0` | `mfcc_sma[8]_p0` ⚠️ |
| `s113` | `mfcc_sma[8]_p0` | `mfcc_sma[9]_p0` ⚠️ |
| `s114` | `mfcc_sma[9]_p0` | `mfcc_sma[10]_p0` ⚠️ |
| `s115` | `mfcc_sma[10]_p0` | `mfcc_sma[11]_p0` ⚠️ |
| `s116` | `mfcc_sma[11]_p0` | `mfcc_sma[12]_p0` ⚠️ |
| `s117` | `mfcc_sma[12]_p0` | `mfcc_sma[13]_p0` ⚠️ |
| `s118` | `mfcc_sma[13]_p0` | `mfcc_sma[14]_p0` ⚠️ |
| `s119` | `mfcc_sma[14]_p0` | `value_p0` ⚠️ |
| `s120` | `derivative_sign_p1` | `value_p1` ⚠️ |
| `s121` | `vad_p1` | `vad_p1` |
| `s122` | `total_talking_time_p1` | `total_talking_time_p1` |
| `s123` | `total_number_turns_p1` | `total_number_turns_p1` |
| `s124` | `gaze_0_x_p1` | `gaze_0_x_p1` |
| `s125` | `gaze_0_y_p1` | `gaze_0_y_p1` |
| `s126` | `gaze_0_z_p1` | `gaze_0_z_p1` |
| `s127` | `gaze_1_x_p1` | `gaze_1_x_p1` |
| `s128` | `gaze_1_y_p1` | `gaze_1_y_p1` |
| `s129` | `gaze_1_z_p1` | `gaze_1_z_p1` |
| `s130` | `gaze_angle_x_p1` | `gaze_angle_x_p1` |
| `s131` | `gaze_angle_y_p1` | `gaze_angle_y_p1` |
| `s132` | `pose_Tx_p1` | `pose_Tx_p1` |
| `s133` | `pose_Ty_p1` | `pose_Ty_p1` |
| `s134` | `pose_Tz_p1` | `pose_Tz_p1` |
| `s135` | `pose_Rx_p1` | `pose_Rx_p1` |
| `s136` | `pose_Ry_p1` | `pose_Ry_p1` |
| `s137` | `pose_Rz_p1` | `pose_Rz_p1` |
| `s138` | `AU01_r_p1` | `AU01_r_p1` |
| `s139` | `AU02_r_p1` | `AU02_r_p1` |
| `s140` | `AU04_r_p1` | `AU04_r_p1` |
| `s141` | `AU05_r_p1` | `AU05_r_p1` |
| `s142` | `AU06_r_p1` | `AU06_r_p1` |
| `s143` | `AU07_r_p1` | `AU07_r_p1` |
| `s144` | `AU09_r_p1` | `AU09_r_p1` |
| `s145` | `AU10_r_p1` | `AU10_r_p1` |
| `s146` | `AU12_r_p1` | `AU12_r_p1` |
| `s147` | `AU14_r_p1` | `AU14_r_p1` |
| `s148` | `AU15_r_p1` | `AU15_r_p1` |
| `s149` | `AU17_r_p1` | `AU17_r_p1` |
| `s150` | `AU20_r_p1` | `AU20_r_p1` |
| `s151` | `AU23_r_p1` | `AU23_r_p1` |
| `s152` | `AU25_r_p1` | `AU25_r_p1` |
| `s153` | `AU26_r_p1` | `AU26_r_p1` |
| `s154` | `AU45_r_p1` | `AU45_r_p1` |
| `s155` | `AU01_c_p1` | `AU01_c_p1` |
| `s156` | `AU02_c_p1` | `AU02_c_p1` |
| `s157` | `AU04_c_p1` | `AU04_c_p1` |
| `s158` | `AU05_c_p1` | `AU05_c_p1` |
| `s159` | `AU06_c_p1` | `AU06_c_p1` |
| `s160` | `AU07_c_p1` | `AU07_c_p1` |
| `s161` | `AU09_c_p1` | `AU09_c_p1` |
| `s162` | `AU10_c_p1` | `AU10_c_p1` |
| `s163` | `AU12_c_p1` | `AU12_c_p1` |
| `s164` | `AU14_c_p1` | `AU14_c_p1` |
| `s165` | `AU15_c_p1` | `AU15_c_p1` |
| `s166` | `AU17_c_p1` | `AU17_c_p1` |
| `s167` | `AU20_c_p1` | `AU20_c_p1` |
| `s168` | `AU23_c_p1` | `AU23_c_p1` |
| `s169` | `AU25_c_p1` | `AU25_c_p1` |
| `s170` | `AU26_c_p1` | `AU26_c_p1` |
| `s171` | `AU28_c_p1` | `AU28_c_p1` |
| `s172` | `AU45_c_p1` | `AU45_c_p1` |
| `s173` | `F0final_sma_p1` | `F0final_sma_p1` |
| `s174` | `voicingFinalUnclipped_sma_p1` | `voicingFinalUnclipped_sma_p1` |
| `s175` | `jitterLocal_sma_p1` | `jitterLocal_sma_p1` |
| `s176` | `jitterDDP_sma_p1` | `jitterDDP_sma_p1` |
| `s177` | `shimmerLocal_sma_p1` | `shimmerLocal_sma_p1` |
| `s178` | `logHNR_sma_p1` | `logHNR_sma_p1` |
| `s179` | `audspec_lengthL1norm_sma_p1` | `audspec_lengthL1norm_sma_p1` |
| `s180` | `audspecRasta_lengthL1norm_sma_p1` | `audspecRasta_lengthL1norm_sma_p1` |
| `s181` | `pcm_RMSenergy_sma_p1` | `pcm_RMSenergy_sma_p1` |
| `s182` | `pcm_zcr_sma_p1` | `pcm_zcr_sma_p1` |
| `s183` | `audSpec_Rfilt_sma[0]_p1` | `audSpec_Rfilt_sma[0]_p1` |
| `s184` | `audSpec_Rfilt_sma[1]_p1` | `audSpec_Rfilt_sma[1]_p1` |
| `s185` | `audSpec_Rfilt_sma[2]_p1` | `audSpec_Rfilt_sma[2]_p1` |
| `s186` | `audSpec_Rfilt_sma[3]_p1` | `audSpec_Rfilt_sma[3]_p1` |
| `s187` | `audSpec_Rfilt_sma[4]_p1` | `audSpec_Rfilt_sma[4]_p1` |
| `s188` | `audSpec_Rfilt_sma[5]_p1` | `audSpec_Rfilt_sma[5]_p1` |
| `s189` | `audSpec_Rfilt_sma[6]_p1` | `audSpec_Rfilt_sma[6]_p1` |
| `s190` | `audSpec_Rfilt_sma[7]_p1` | `audSpec_Rfilt_sma[7]_p1` |
| `s191` | `audSpec_Rfilt_sma[8]_p1` | `audSpec_Rfilt_sma[8]_p1` |
| `s192` | `audSpec_Rfilt_sma[9]_p1` | `audSpec_Rfilt_sma[9]_p1` |
| `s193` | `audSpec_Rfilt_sma[10]_p1` | `audSpec_Rfilt_sma[10]_p1` |
| `s194` | `audSpec_Rfilt_sma[11]_p1` | `audSpec_Rfilt_sma[11]_p1` |
| `s195` | `audSpec_Rfilt_sma[12]_p1` | `audSpec_Rfilt_sma[12]_p1` |
| `s196` | `audSpec_Rfilt_sma[13]_p1` | `audSpec_Rfilt_sma[13]_p1` |
| `s197` | `audSpec_Rfilt_sma[14]_p1` | `audSpec_Rfilt_sma[14]_p1` |
| `s198` | `audSpec_Rfilt_sma[15]_p1` | `audSpec_Rfilt_sma[15]_p1` |
| `s199` | `audSpec_Rfilt_sma[16]_p1` | `audSpec_Rfilt_sma[16]_p1` |
| `s200` | `audSpec_Rfilt_sma[17]_p1` | `audSpec_Rfilt_sma[17]_p1` |
| `s201` | `audSpec_Rfilt_sma[18]_p1` | `audSpec_Rfilt_sma[18]_p1` |
| `s202` | `audSpec_Rfilt_sma[19]_p1` | `audSpec_Rfilt_sma[19]_p1` |
| `s203` | `audSpec_Rfilt_sma[20]_p1` | `audSpec_Rfilt_sma[20]_p1` |
| `s204` | `audSpec_Rfilt_sma[21]_p1` | `audSpec_Rfilt_sma[21]_p1` |
| `s205` | `audSpec_Rfilt_sma[22]_p1` | `audSpec_Rfilt_sma[22]_p1` |
| `s206` | `audSpec_Rfilt_sma[23]_p1` | `audSpec_Rfilt_sma[23]_p1` |
| `s207` | `audSpec_Rfilt_sma[24]_p1` | `audSpec_Rfilt_sma[24]_p1` |
| `s208` | `audSpec_Rfilt_sma[25]_p1` | `audSpec_Rfilt_sma[25]_p1` |
| `s209` | `pcm_fftMag_fband250-650_sma_p1` | `pcm_fftMag_fband250-650_sma_p1` |
| `s210` | `pcm_fftMag_fband1000-4000_sma_p1` | `pcm_fftMag_fband1000-4000_sma_p1` |
| `s211` | `pcm_fftMag_spectralRollOff25.0_sma_p1` | `pcm_fftMag_spectralRollOff25.0_sma_p1` |
| `s212` | `pcm_fftMag_spectralRollOff50.0_sma_p1` | `pcm_fftMag_spectralRollOff50.0_sma_p1` |
| `s213` | `pcm_fftMag_spectralRollOff75.0_sma_p1` | `pcm_fftMag_spectralRollOff75.0_sma_p1` |
| `s214` | `pcm_fftMag_spectralRollOff90.0_sma_p1` | `pcm_fftMag_spectralRollOff90.0_sma_p1` |
| `s215` | `pcm_fftMag_spectralFlux_sma_p1` | `pcm_fftMag_spectralFlux_sma_p1` |
| `s216` | `pcm_fftMag_spectralCentroid_sma_p1` | `pcm_fftMag_spectralCentroid_sma_p1` |
| `s217` | `pcm_fftMag_spectralEntropy_sma_p1` | `pcm_fftMag_spectralEntropy_sma_p1` |
| `s218` | `pcm_fftMag_spectralVariance_sma_p1` | `pcm_fftMag_spectralVariance_sma_p1` |
| `s219` | `pcm_fftMag_spectralSkewness_sma_p1` | `pcm_fftMag_spectralSkewness_sma_p1` |
| `s220` | `pcm_fftMag_spectralKurtosis_sma_p1` | `pcm_fftMag_spectralKurtosis_sma_p1` |
| `s221` | `pcm_fftMag_spectralSlope_sma_p1` | `pcm_fftMag_spectralSlope_sma_p1` |
| `s222` | `pcm_fftMag_psySharpness_sma_p1` | `pcm_fftMag_psySharpness_sma_p1` |
| `s223` | `pcm_fftMag_spectralHarmonicity_sma_p1` | `pcm_fftMag_spectralHarmonicity_sma_p1` |
| `s224` | `mfcc_sma[1]_p1` | `mfcc_sma[1]_p1` |
| `s225` | `mfcc_sma[2]_p1` | `mfcc_sma[2]_p1` |
| `s226` | `mfcc_sma[3]_p1` | `mfcc_sma[3]_p1` |
| `s227` | `mfcc_sma[4]_p1` | `mfcc_sma[4]_p1` |
| `s228` | `mfcc_sma[5]_p1` | `mfcc_sma[5]_p1` |
| `s229` | `mfcc_sma[6]_p1` | `mfcc_sma[6]_p1` |
| `s230` | `mfcc_sma[7]_p1` | `mfcc_sma[7]_p1` |
| `s231` | `mfcc_sma[8]_p1` | `mfcc_sma[8]_p1` |
| `s232` | `mfcc_sma[9]_p1` | `mfcc_sma[9]_p1` |
| `s233` | `mfcc_sma[10]_p1` | `mfcc_sma[10]_p1` |
| `s234` | `mfcc_sma[11]_p1` | `mfcc_sma[11]_p1` |
| `s235` | `mfcc_sma[12]_p1` | `mfcc_sma[12]_p1` |
| `s236` | `mfcc_sma[13]_p1` | `mfcc_sma[13]_p1` |
| `s237` | `mfcc_sma[14]_p1` | `mfcc_sma[14]_p1` |

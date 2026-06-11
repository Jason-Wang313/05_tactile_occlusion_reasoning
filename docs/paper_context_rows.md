# Paper Context Rows

Loaded 1332 rows from `docs/related_work_matrix.csv`.
Selected rows combine the top ranked matrix entries with named hostile/context papers.

### 1. TouchAnything: Diffusion-Guided 3D Reconstruction from Sparse Robot Touches (2026)
- authors: Langzhe Gu; Hung-Jui Huang; Mohamad Qadri; Michael Kaess; Wenzhen Yuan
- venue: ArXiv.org
- doi: 
- url: https://arxiv.org/pdf/2604.08945
- problem_claimed: recover object geometry from touch, vision, or multimodal observations
- actual_mechanism_introduced: shape reconstruction; visuotactile fusion
- hidden_assumptions: unobserved surfaces can be filled by priors without testing whether contact has ruled alternatives out | vision and touch provide complementary features over one shared latent object, not competing censoring processes
- what_it_makes_less_novel: using tactile contacts to reconstruct object shape
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 2. Visual-Tactile Fusion for 3D Objects Reconstruction from a Single Depth View and a Single Gripper Touch for Robotics Tasks (2021)
- authors: Mohamed Tahoun; Omar Tahri; Juan Antonio Corrales Ramon; Youcef Mezouar
- venue: 2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)
- doi: https://doi.org/10.1109/iros51168.2021.9636150
- url: https://hal.science/hal-03558917
- problem_claimed: estimate object pose or state under partial/contact observations
- actual_mechanism_introduced: sensor/dataset; pose/state estimation; shape reconstruction
- hidden_assumptions: tactile observations are treated as labeled examples rather than interventions that change what can be inferred | object geometry is sufficiently known or visually initialized before contact estimation starts
- what_it_makes_less_novel: using tactile contacts to reconstruct object shape
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 3. High-Precision 3D Reconstruction Study with Emphasis on Refractive Calibration of GelStereo-Type Sensors (2023)
- authors: Chaofan Zhang; Shaowei Cui; Shuo Wang; Jingyi Hu; Yipeng Huangfu; Boyue Zhang
- venue: Sensors
- doi: https://doi.org/10.3390/s23052675
- url: https://www.mdpi.com/1424-8220/23/5/2675/pdf?version=1677658605
- problem_claimed: estimate object pose or state under partial/contact observations
- actual_mechanism_introduced: sensor/dataset; pose/state estimation; shape reconstruction
- hidden_assumptions: tactile observations are treated as labeled examples rather than interventions that change what can be inferred | object geometry is sufficiently known or visually initialized before contact estimation starts
- what_it_makes_less_novel: using tactile contacts to reconstruct object shape
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 4. Tac2Pose: Tactile object pose estimation from the first touch (2023)
- authors: Maria Bauza; Antonia Bronars; Alberto Rodriguez
- venue: The International Journal of Robotics Research
- doi: https://doi.org/10.1177/02783649231196925
- url: https://journals.sagepub.com/doi/pdf/10.1177/02783649231196925
- problem_claimed: estimate object pose or state under partial/contact observations
- actual_mechanism_introduced: sensor/dataset; pose/state estimation; shape reconstruction
- hidden_assumptions: tactile observations are treated as labeled examples rather than interventions that change what can be inferred | object geometry is sufficiently known or visually initialized before contact estimation starts
- what_it_makes_less_novel: using tactile contacts to reconstruct object shape
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 5. TouchSDF: A DeepSDF Approach for 3D Shape Reconstruction Using Vision-Based Tactile Sensing (2024)
- authors: Mauro Comi; Yijiong Lin; Alex Church; Alessio Tonioni; Laurence Aitchison; Nathan F. Lepora
- venue: IEEE Robotics and Automation Letters
- doi: https://doi.org/10.1109/lra.2024.3396054
- url: https://doi.org/10.1109/lra.2024.3396054
- problem_claimed: estimate object pose or state under partial/contact observations
- actual_mechanism_introduced: sensor/dataset; pose/state estimation; shape reconstruction
- hidden_assumptions: tactile observations are treated as labeled examples rather than interventions that change what can be inferred | object geometry is sufficiently known or visually initialized before contact estimation starts
- what_it_makes_less_novel: using tactile contacts to reconstruct object shape
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 6. End-to-End Diffusion-Based 3D Object Reconstruction From Robotic Tactile Sensing (2025)
- authors: Han Zhang; Xiaohui Zhang; Jun Huang; Zhao Feng; Xiaohui Xiao
- venue: IEEE Robotics and Automation Letters
- doi: https://doi.org/10.1109/lra.2025.3641115
- url: https://doi.org/10.1109/lra.2025.3641115
- problem_claimed: estimate object pose or state under partial/contact observations
- actual_mechanism_introduced: sensor/dataset; pose/state estimation; shape reconstruction
- hidden_assumptions: tactile observations are treated as labeled examples rather than interventions that change what can be inferred | object geometry is sufficiently known or visually initialized before contact estimation starts
- what_it_makes_less_novel: using tactile contacts to reconstruct object shape
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 7. Active Tactile Exploration Based on Cost-Aware Information Gain Maximization (2018)
- authors: Simon Ottenhaus; Lukas Kaul; Nikolaus Vahrenkamp; Tamim Asfour
- venue: International Journal of Humanoid Robotics
- doi: https://doi.org/10.1142/s0219843618500159
- url: https://doi.org/10.1142/s0219843618500159
- problem_claimed: recover object geometry from touch, vision, or multimodal observations
- actual_mechanism_introduced: sensor/dataset; shape reconstruction; visuotactile fusion
- hidden_assumptions: tactile observations are treated as labeled examples rather than interventions that change what can be inferred | unobserved surfaces can be filled by priors without testing whether contact has ruled alternatives out
- what_it_makes_less_novel: using tactile contacts to reconstruct object shape
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 8. Design and Calibration of a Force/Tactile Sensor for Dexterous Manipulation (2019)
- authors: Marco Costanzo; Giuseppe De Maria; Ciro Natale; Salvatore Pirozzi
- venue: Sensors
- doi: https://doi.org/10.3390/s19040966
- url: https://www.mdpi.com/1424-8220/19/4/966/pdf?version=1551084772
- problem_claimed: estimate object pose or state under partial/contact observations
- actual_mechanism_introduced: sensor/dataset; pose/state estimation; visuotactile fusion
- hidden_assumptions: tactile observations are treated as labeled examples rather than interventions that change what can be inferred | object geometry is sufficiently known or visually initialized before contact estimation starts
- what_it_makes_less_novel: generic fusion of visual and tactile streams for manipulation
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 9. DTactive: A Vision-Based Tactile Sensor with Active Surface (2024)
- authors: Jikai Xu; Wu Lei; Changyi Lin; Ding Zhao; Huazhe Xu
- venue: arXiv (Cornell University)
- doi: https://doi.org/10.48550/arxiv.2410.08337
- url: https://arxiv.org/pdf/2410.08337
- problem_claimed: estimate object pose or state under partial/contact observations
- actual_mechanism_introduced: sensor/dataset; pose/state estimation; shape reconstruction
- hidden_assumptions: tactile observations are treated as labeled examples rather than interventions that change what can be inferred | object geometry is sufficiently known or visually initialized before contact estimation starts
- what_it_makes_less_novel: using tactile contacts to reconstruct object shape
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 10. Multi-photon neuron embedded bionic skin for high-precision complex texture and object reconstruction perception research (2025)
- authors: Hongyu Zhou; Chao Zhang; Hengchang Nong; Junjie Weng; Dongying Wang; Yang Yu; Jianfa Zhang; Chaofan Zhang
- venue: Opto-Electronic Advances
- doi: https://doi.org/10.29026/oea.2025.240152
- url: https://doi.org/10.29026/oea.2025.240152
- problem_claimed: recover object geometry from touch, vision, or multimodal observations
- actual_mechanism_introduced: sensor/dataset; shape reconstruction; visuotactile fusion
- hidden_assumptions: tactile observations are treated as labeled examples rather than interventions that change what can be inferred | unobserved surfaces can be filled by priors without testing whether contact has ruled alternatives out
- what_it_makes_less_novel: using tactile contacts to reconstruct object shape
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 11. Proactive Tactile Exploration for Object-Agnostic Shape Reconstruction from Minimal Visual Priors (2025)
- authors: Paris Oikonomou; George Retsinas; Petros Maragos; Costas S. Tzafestas
- venue: 
- doi: https://doi.org/10.1109/icra55743.2025.11127653
- url: https://doi.org/10.1109/icra55743.2025.11127653
- problem_claimed: estimate object pose or state under partial/contact observations
- actual_mechanism_introduced: pose/state estimation; shape reconstruction; visuotactile fusion
- hidden_assumptions: object geometry is sufficiently known or visually initialized before contact estimation starts | unobserved surfaces can be filled by priors without testing whether contact has ruled alternatives out
- what_it_makes_less_novel: using tactile contacts to reconstruct object shape
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 12. Simultaneous Tactile Localization And Reconstruction of an Object During Robotic Manipulation (2021)
- authors: Ghani Kissoum; Veronique Perdereau
- venue: 2021 20th International Conference on Advanced Robotics (ICAR)
- doi: https://doi.org/10.1109/icar53236.2021.9659354
- url: https://doi.org/10.1109/icar53236.2021.9659354
- problem_claimed: estimate object pose or state under partial/contact observations
- actual_mechanism_introduced: sensor/dataset; pose/state estimation; shape reconstruction
- hidden_assumptions: tactile observations are treated as labeled examples rather than interventions that change what can be inferred | object geometry is sufficiently known or visually initialized before contact estimation starts
- what_it_makes_less_novel: using tactile contacts to reconstruct object shape
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 13. Artificial Skin Based on VisuoTactile Sensing for 3D Shape Reconstruction: Material, Method, and Evaluation (2024)
- authors: Shixin Zhang; Yiyong Yang; Yuhao Sun; Nailong Liu; Fuchun Sun; Bin Fang
- venue: Advanced Functional Materials
- doi: https://doi.org/10.1002/adfm.202411686
- url: https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/adfm.202411686
- problem_claimed: recover object geometry from touch, vision, or multimodal observations
- actual_mechanism_introduced: sensor/dataset; shape reconstruction; visuotactile fusion
- hidden_assumptions: tactile observations are treated as labeled examples rather than interventions that change what can be inferred | unobserved surfaces can be filled by priors without testing whether contact has ruled alternatives out
- what_it_makes_less_novel: using tactile contacts to reconstruct object shape
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 14. Play it by Ear: Learning Skills amidst Occlusion through Audio-Visual Imitation Learning (2022)
- authors: Maximilian Du; Olivia Y Lee; Suraj Nair; Chelsea Finn
- venue: 
- doi: https://doi.org/10.15607/rss.2022.xviii.009
- url: https://doi.org/10.15607/rss.2022.xviii.009
- problem_claimed: estimate object pose or state under partial/contact observations
- actual_mechanism_introduced: pose/state estimation; visuotactile fusion; learning/control
- hidden_assumptions: object geometry is sufficiently known or visually initialized before contact estimation starts | vision and touch provide complementary features over one shared latent object, not competing censoring processes
- what_it_makes_less_novel: generic fusion of visual and tactile streams for manipulation
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 15. Model-Based 3D Contact Geometry Perception for Visual Tactile Sensor (2022)
- authors: Jingjing Ji; Yuting Liu; Huan Ma
- venue: Sensors
- doi: https://doi.org/10.3390/s22176470
- url: https://www.mdpi.com/1424-8220/22/17/6470/pdf?version=1661824507
- problem_claimed: estimate object pose or state under partial/contact observations
- actual_mechanism_introduced: sensor/dataset; pose/state estimation; shape reconstruction
- hidden_assumptions: tactile observations are treated as labeled examples rather than interventions that change what can be inferred | object geometry is sufficiently known or visually initialized before contact estimation starts
- what_it_makes_less_novel: using tactile contacts to reconstruct object shape
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 16. ViTaSCOPE: Visuo-tactile Implicit Representation for In-hand Pose and Extrinsic Contact Estimation (2025)
- authors: Jayjun Lee; Nima Fazeli
- venue: 
- doi: https://doi.org/10.15607/rss.2025.xxi.054
- url: https://doi.org/10.15607/rss.2025.xxi.054
- problem_claimed: estimate object pose or state under partial/contact observations
- actual_mechanism_introduced: sensor/dataset; pose/state estimation; shape reconstruction
- hidden_assumptions: tactile observations are treated as labeled examples rather than interventions that change what can be inferred | object geometry is sufficiently known or visually initialized before contact estimation starts
- what_it_makes_less_novel: using tactile contacts to reconstruct object shape
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 17. 3-D Dense Reconstruction of Vision-Based Tactile Sensor With Coded Markers (2023)
- authors: Hongxiang Xue; Fuchun Sun; Haoqiang Yu
- venue: IEEE Transactions on Instrumentation and Measurement
- doi: https://doi.org/10.1109/tim.2023.3301893
- url: https://doi.org/10.1109/tim.2023.3301893
- problem_claimed: estimate object pose or state under partial/contact observations
- actual_mechanism_introduced: sensor/dataset; pose/state estimation; shape reconstruction
- hidden_assumptions: tactile observations are treated as labeled examples rather than interventions that change what can be inferred | object geometry is sufficiently known or visually initialized before contact estimation starts
- what_it_makes_less_novel: using tactile contacts to reconstruct object shape
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 18. Improving the Representation and Extraction of Contact Information in Vision-based Tactile Sensors Using Continuous Marker Pattern (2023)
- authors: Mingxuan Li; Yen Hang Zhou; Tiemin Li; Yao Jiang
- venue: Figshare
- doi: https://doi.org/10.36227/techrxiv.22217653.v2
- url: https://www.techrxiv.org/articles/preprint/Improving_the_Representation_and_Extraction_of_Contact_Information_in_Vision-based_Tactile_Sensors_Using_Continuous_Marker_Pattern/22217653/2/files/41397624.pdf
- problem_claimed: estimate object pose or state under partial/contact observations
- actual_mechanism_introduced: sensor/dataset; pose/state estimation; shape reconstruction
- hidden_assumptions: tactile observations are treated as labeled examples rather than interventions that change what can be inferred | object geometry is sufficiently known or visually initialized before contact estimation starts
- what_it_makes_less_novel: using tactile contacts to reconstruct object shape
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 19. Active Haptic Perception in Robots: A Review (2019)
- authors: Lucia Seminara; Paolo Gastaldo; Simon J. Watt; Kenneth F. Valyear; Fernando Zuher; Fulvio Mastrogiovanni
- venue: Frontiers in Neurorobotics
- doi: https://doi.org/10.3389/fnbot.2019.00053
- url: https://www.frontiersin.org/articles/10.3389/fnbot.2019.00053/pdf
- problem_claimed: estimate object pose or state under partial/contact observations
- actual_mechanism_introduced: sensor/dataset; pose/state estimation; visuotactile fusion
- hidden_assumptions: tactile observations are treated as labeled examples rather than interventions that change what can be inferred | object geometry is sufficiently known or visually initialized before contact estimation starts
- what_it_makes_less_novel: generic fusion of visual and tactile streams for manipulation
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 20. Touch if it's Transparent! ACTOR: Active Tactile-Based Category-Level Transparent Object Reconstruction (2023)
- authors: Prajval Kumar Murali; Bernd Porr; Mohsen Kaboli
- venue: ENLIGHTEN (Jurnal Bimbingan dan Konseling Islam)
- doi: https://doi.org/10.1109/iros55552.2023.10341680
- url: https://doi.org/10.1109/iros55552.2023.10341680
- problem_claimed: estimate object pose or state under partial/contact observations
- actual_mechanism_introduced: sensor/dataset; pose/state estimation; shape reconstruction
- hidden_assumptions: tactile observations are treated as labeled examples rather than interventions that change what can be inferred | object geometry is sufficiently known or visually initialized before contact estimation starts
- what_it_makes_less_novel: using tactile contacts to reconstruct object shape
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 21. A multimodal tactile dataset for dynamic texture classification (2023)
- authors: Bruno Monteiro Rocha Lima; Venkata Naga Sai Siddhartha Danyamraju; Thiago Eustaquio Alves de Oliveira; Vinicius Prado da Fonseca
- venue: Data in Brief
- doi: https://doi.org/10.1016/j.dib.2023.109590
- url: https://doi.org/10.1016/j.dib.2023.109590
- problem_claimed: estimate object pose or state under partial/contact observations
- actual_mechanism_introduced: sensor/dataset; pose/state estimation; shape reconstruction
- hidden_assumptions: tactile observations are treated as labeled examples rather than interventions that change what can be inferred | object geometry is sufficiently known or visually initialized before contact estimation starts
- what_it_makes_less_novel: using tactile contacts to reconstruct object shape
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 22. Capturing forceful interaction with deformable objects using a deep learning-powered stretchable tactile array (2024)
- authors: Chunpeng Jiang; Wenqiang Xu; Yutong Li; Zhenjun Yu; Longchun Wang; Xiaotong Hu; Zhengyi Xie; Qingkun Liu
- venue: Nature Communications
- doi: https://doi.org/10.1038/s41467-024-53654-y
- url: https://www.nature.com/articles/s41467-024-53654-y.pdf
- problem_claimed: estimate object pose or state under partial/contact observations
- actual_mechanism_introduced: pose/state estimation; shape reconstruction; active exploration
- hidden_assumptions: object geometry is sufficiently known or visually initialized before contact estimation starts | unobserved surfaces can be filled by priors without testing whether contact has ruled alternatives out
- what_it_makes_less_novel: using tactile contacts to reconstruct object shape
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 23. NormalFlow: Fast, Robust, and Accurate Contact-Based Object 6DoF Pose Tracking With Vision-Based Tactile Sensors (2024)
- authors: Hung-Jui Huang; Michael Kaess; Wenzhen Yuan
- venue: IEEE Robotics and Automation Letters
- doi: https://doi.org/10.1109/lra.2024.3505815
- url: https://arxiv.org/pdf/2412.09617
- problem_claimed: estimate object pose or state under partial/contact observations
- actual_mechanism_introduced: sensor/dataset; pose/state estimation; shape reconstruction
- hidden_assumptions: tactile observations are treated as labeled examples rather than interventions that change what can be inferred | object geometry is sufficiently known or visually initialized before contact estimation starts
- what_it_makes_less_novel: using tactile contacts to reconstruct object shape
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 24. Design of a Force/Tactile Sensor for Robotic Grippers (2019)
- authors: Marco Costanzo; Giuseppe De Maria; Ciro Natale; Salvatore Pirozzi
- venue: DOAJ (DOAJ: Directory of Open Access Journals)
- doi: https://doi.org/10.3390/proceedings2019015031
- url: https://www.mdpi.com/2504-3900/15/1/31/pdf?version=1564046430
- problem_claimed: improve grasping or manipulation using tactile feedback
- actual_mechanism_introduced: sensor/dataset; visuotactile fusion; planning/physics
- hidden_assumptions: tactile observations are treated as labeled examples rather than interventions that change what can be inferred | vision and touch provide complementary features over one shared latent object, not competing censoring processes
- what_it_makes_less_novel: generic fusion of visual and tactile streams for manipulation
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 25. iCLAP: shape recognition by combining proprioception and touch sensing (2018)
- authors: Shan Luo; Wenxuan Mou; Kaspar Althoefer; Hongbin Liu
- venue: Autonomous Robots
- doi: https://doi.org/10.1007/s10514-018-9777-7
- url: https://link.springer.com/content/pdf/10.1007/s10514-018-9777-7.pdf
- problem_claimed: estimate object pose or state under partial/contact observations
- actual_mechanism_introduced: sensor/dataset; pose/state estimation; shape reconstruction
- hidden_assumptions: tactile observations are treated as labeled examples rather than interventions that change what can be inferred | object geometry is sufficiently known or visually initialized before contact estimation starts
- what_it_makes_less_novel: using tactile contacts to reconstruct object shape
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 26. Measuring Force Intensity and Direction with a Spatially Resolved Soft Sensor for Biomechanics and Robotic Haptic Capability (2019)
- authors: Artemis Llamosi; Severine Toussaint
- venue: Soft Robotics
- doi: https://doi.org/10.1089/soro.2018.0044
- url: https://www.liebertpub.com/doi/pdf/10.1089/soro.2018.0044
- problem_claimed: recover object geometry from touch, vision, or multimodal observations
- actual_mechanism_introduced: sensor/dataset; shape reconstruction; visuotactile fusion
- hidden_assumptions: tactile observations are treated as labeled examples rather than interventions that change what can be inferred | unobserved surfaces can be filled by priors without testing whether contact has ruled alternatives out
- what_it_makes_less_novel: using tactile contacts to reconstruct object shape
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 27. Large-area magnetic skin for multi-point and multi-scale tactile sensing with super-resolution (2024)
- authors: Hao Hu; Chengqian Zhang; Xinyi Lai; Huangzhe Dai; Chengfeng Pan; Haonan Sun; Daofan Tang; Zhezai Hu
- venue: npj Flexible Electronics
- doi: https://doi.org/10.1038/s41528-024-00325-z
- url: https://www.nature.com/articles/s41528-024-00325-z.pdf
- problem_claimed: estimate object pose or state under partial/contact observations
- actual_mechanism_introduced: sensor/dataset; pose/state estimation; shape reconstruction
- hidden_assumptions: tactile observations are treated as labeled examples rather than interventions that change what can be inferred | object geometry is sufficiently known or visually initialized before contact estimation starts
- what_it_makes_less_novel: using tactile contacts to reconstruct object shape
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 28. DexiTac: Soft Dexterous Tactile Gripping (2024)
- authors: Chenghua Lu; Kailuan Tang; Max Yang; Tianqi Yue; Haoran Li; Nathan F. Lepora
- venue: IEEE/ASME Transactions on Mechatronics
- doi: https://doi.org/10.1109/tmech.2024.3384432
- url: https://research-information.bris.ac.uk/en/publications/51b21de3-8bc8-457a-aefd-c6c2ccb6891b
- problem_claimed: estimate object pose or state under partial/contact observations
- actual_mechanism_introduced: sensor/dataset; pose/state estimation; shape reconstruction
- hidden_assumptions: tactile observations are treated as labeled examples rather than interventions that change what can be inferred | object geometry is sufficiently known or visually initialized before contact estimation starts
- what_it_makes_less_novel: using tactile contacts to reconstruct object shape
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 29. Active Tactile Exploration using Shape-Dependent Reinforcement Learning (2022)
- authors: Shuo Jiang; Lawson L. S. Wong
- venue: 2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)
- doi: https://doi.org/10.1109/iros47612.2022.9982266
- url: https://doi.org/10.1109/iros47612.2022.9982266
- problem_claimed: estimate object pose or state under partial/contact observations
- actual_mechanism_introduced: sensor/dataset; pose/state estimation; shape reconstruction
- hidden_assumptions: tactile observations are treated as labeled examples rather than interventions that change what can be inferred | object geometry is sufficiently known or visually initialized before contact estimation starts
- what_it_makes_less_novel: using tactile contacts to reconstruct object shape
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 30. Fabric Classification Using a Finger-Shaped Tactile Sensor via Robotic Sliding (2022)
- authors: Si Ao Wang; Alessandro Albini; Perla Maiolino; Fulvio Mastrogiovanni; Giorgio Cannata
- venue: Frontiers in Neurorobotics
- doi: https://doi.org/10.3389/fnbot.2022.808222
- url: https://www.frontiersin.org/articles/10.3389/fnbot.2022.808222/pdf
- problem_claimed: recover object geometry from touch, vision, or multimodal observations
- actual_mechanism_introduced: sensor/dataset; shape reconstruction; visuotactile fusion
- hidden_assumptions: tactile observations are treated as labeled examples rather than interventions that change what can be inferred | unobserved surfaces can be filled by priors without testing whether contact has ruled alternatives out
- what_it_makes_less_novel: using tactile contacts to reconstruct object shape
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 31. A High-Repeatability Three-Dimensional Force Tactile Sensing System for Robotic Dexterous Grasping and Object Recognition (2024)
- authors: Yaoguang Shi; Xiaozhou Lu; Wenran Wang; Xiaohui Zhou; Zhu Wensong
- venue: Micromachines
- doi: https://doi.org/10.3390/mi15121513
- url: https://www.mdpi.com/2072-666X/15/12/1513/pdf?version=1734686551
- problem_claimed: estimate object pose or state under partial/contact observations
- actual_mechanism_introduced: sensor/dataset; pose/state estimation; shape reconstruction
- hidden_assumptions: tactile observations are treated as labeled examples rather than interventions that change what can be inferred | object geometry is sufficiently known or visually initialized before contact estimation starts
- what_it_makes_less_novel: using tactile contacts to reconstruct object shape
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 32. Manipulation of Boltlike Fasteners Through Fingertip Tactile Perception in Robotic Assembly (2023)
- authors: Riccardo Caccavale; Alberto Finzi; Gianluca Laudante; Ciro Natale; Salvatore Pirozzi; Luigi Villani
- venue: IEEE/ASME Transactions on Mechatronics
- doi: https://doi.org/10.1109/tmech.2023.3320519
- url: https://ieeexplore.ieee.org/ielx7/3516/4785241/10285120.pdf
- problem_claimed: estimate object pose or state under partial/contact observations
- actual_mechanism_introduced: sensor/dataset; pose/state estimation; shape reconstruction
- hidden_assumptions: tactile observations are treated as labeled examples rather than interventions that change what can be inferred | object geometry is sufficiently known or visually initialized before contact estimation starts
- what_it_makes_less_novel: using tactile contacts to reconstruct object shape
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 33. Recent trends and role of large area flexible electronics in shape sensing application a review (2021)
- authors: Riyaz Ali Shaik; Elizabeth Rufus
- venue: Industrial Robot the international journal of robotics research and application
- doi: https://doi.org/10.1108/ir-10-2020-0234
- url: https://doi.org/10.1108/ir-10-2020-0234
- problem_claimed: estimate object pose or state under partial/contact observations
- actual_mechanism_introduced: sensor/dataset; pose/state estimation; shape reconstruction
- hidden_assumptions: tactile observations are treated as labeled examples rather than interventions that change what can be inferred | object geometry is sufficiently known or visually initialized before contact estimation starts
- what_it_makes_less_novel: using tactile contacts to reconstruct object shape
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 34. Fusionsense: Bridging Common Sense, Vision, and Touch for Robust Sparse-View Reconstruction (2025)
- authors: Irving Fang; Kairui Shi; Xujin He; Siqi Tan; Yifan Wang; Hanwen Zhao; Hung-Jui Huang; Wenzhen Yuan
- venue: 
- doi: https://doi.org/10.1109/icra55743.2025.11128188
- url: https://doi.org/10.1109/icra55743.2025.11128188
- problem_claimed: recover object geometry from touch, vision, or multimodal observations
- actual_mechanism_introduced: sensor/dataset; shape reconstruction; visuotactile fusion
- hidden_assumptions: tactile observations are treated as labeled examples rather than interventions that change what can be inferred | unobserved surfaces can be filled by priors without testing whether contact has ruled alternatives out
- what_it_makes_less_novel: using tactile contacts to reconstruct object shape
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 35. Master Micro Residual Correction with Adaptive Tactile Fusion and Force-Mixed Control for Contact-Rich Manipulation (2026)
- authors: Xingting Li; Yifan Xie; Han Liu; Wei Hou; Guangyu Chen; Shoujie Li; Wenbo Ding
- venue: arXiv (Cornell University)
- doi: 
- url: https://arxiv.org/pdf/2603.15152
- problem_claimed: estimate object pose or state under partial/contact observations
- actual_mechanism_introduced: pose/state estimation; visuotactile fusion; active exploration
- hidden_assumptions: object geometry is sufficiently known or visually initialized before contact estimation starts | vision and touch provide complementary features over one shared latent object, not competing censoring processes
- what_it_makes_less_novel: generic fusion of visual and tactile streams for manipulation
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 49. Estimation of Contact Regions Between Hands and Objects During Human Multi-Digit Grasping (2023)
- authors: Frieder Hartmann; Guido Maiello; Constantin A. Rothkopf; Roland W. Fleming
- venue: Journal of Visualized Experiments
- doi: https://doi.org/10.3791/64877
- url: https://www.jove.com/pdf/64877/estimation-contact-regions-between-hands-objects-during-human-multi
- problem_claimed: estimate object pose or state under partial/contact observations
- actual_mechanism_introduced: sensor/dataset; pose/state estimation; shape reconstruction
- hidden_assumptions: tactile observations are treated as labeled examples rather than interventions that change what can be inferred | object geometry is sufficiently known or visually initialized before contact estimation starts
- what_it_makes_less_novel: using tactile contacts to reconstruct object shape
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 101. GelSight360: An Omnidirectional Camera-Based Tactile Sensor for Dexterous Robotic Manipulation (2023)
- authors: Megha H. Tippur; Edward H. Adelson
- venue: arXiv (Cornell University)
- doi: https://doi.org/10.48550/arxiv.2304.04268
- url: https://arxiv.org/pdf/2304.04268
- problem_claimed: recover object geometry from touch, vision, or multimodal observations
- actual_mechanism_introduced: sensor/dataset; shape reconstruction; visuotactile fusion
- hidden_assumptions: tactile observations are treated as labeled examples rather than interventions that change what can be inferred | unobserved surfaces can be filled by priors without testing whether contact has ruled alternatives out
- what_it_makes_less_novel: using tactile contacts to reconstruct object shape
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

### 69. ForceFlow: Learning to Feel and Act via Contact-Driven Flow Matching (2026)
- authors: Shuoheng Zhang; Yifu Yuan; Hongyao Tang; Yan Zheng; Qiaojun Yu; Pengyi Li; Guowei Huang; Helong Huang
- venue: ArXiv.org
- doi: 
- url: https://arxiv.org/pdf/2605.11048
- problem_claimed: estimate object pose or state under partial/contact observations
- actual_mechanism_introduced: pose/state estimation; visuotactile fusion; active exploration
- hidden_assumptions: object geometry is sufficiently known or visually initialized before contact estimation starts | vision and touch provide complementary features over one shared latent object, not competing censoring processes
- what_it_makes_less_novel: generic fusion of visual and tactile streams for manipulation
- what_it_leaves_open: a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives

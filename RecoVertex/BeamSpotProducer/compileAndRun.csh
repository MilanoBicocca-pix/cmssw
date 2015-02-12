setenv _T_ $_BASE_/test

cd $_BASE_ && scram b && cd $_T_ && cmsRun analyze_d0_phi_cfg.py

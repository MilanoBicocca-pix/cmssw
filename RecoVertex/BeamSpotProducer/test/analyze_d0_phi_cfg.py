import FWCore.ParameterSet.Config as cms

process = cms.Process("d0phi")
# initialize MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.load("RecoVertex.BeamSpotProducer.d0_phi_analyzer_cff")

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(

#'root://cms-xrd-global.cern.ch//store/data/Run2016E/JetHT/AOD/22Feb2017-v1/110000/023753BD-18FB-E611-859D-0025905A609A.root'
# runs=  277094 - 277096 - 277127 (fill 5106 in runE)

#'root://cms-xrd-global.cern.ch//store/data/Run2016E/JetHT/AOD/22Feb2017-v1/130000/007C4941-E8FA-E611-B4F5-0CC47A4D76C0.root', # run 277127 (+277305)
#'root://cms-xrd-global.cern.ch//store/data/Run2016E/JetHT/AOD/22Feb2017-v1/130000/0034884F-E8FA-E611-8BB6-0025905B85D8.root', # runs 277096 - 277112

#'root://cmsxrootd.fnal.gov//store/data/Run2016G/JetHT/AOD/22Feb2017-v1/110001/8AF339B2-ABFC-E611-A57C-0CC47A4C8E2E.root', runG

# Fill 5441, runH , run = 283863
#'root://cms-xrd-global.cern.ch//store/data/Run2016H/JetHT/AOD/22Feb2017-v1/90000/8A4BC9C0-DCFD-E611-9AF8-FA163EC17E40.root',

# runG, run = 278820
#'root://xrootd-cms.infn.it//store/data/Run2016G/JetHT/AOD/22Feb2017-v1/130000/243C2213-92F9-E611-B098-001E67E34034.root',
#'root://cms-xrd-global.cern.ch//store/data/Run2016G/JetHT/AOD/22Feb2017-v1/130000/02240243-85F9-E611-AAE5-001E677926E2.root',
#'root://cms-xrd-global.cern.ch//store/data/Run2016G/JetHT/AOD/22Feb2017-v1/130000/02A678F8-81F9-E611-B35E-001E67E6F8D2.root',
#'root://cms-xrd-global.cern.ch//store/data/Run2016G/JetHT/AOD/22Feb2017-v1/130000/08E22706-92F9-E611-8C40-001E67C8050C.root',

# runG, run = 278822
#'root://xrootd-cms.infn.it//store/data/Run2016G/JetHT/AOD/22Feb2017-v1/120000/1016F15B-B4F9-E611-9AF7-001E67E6F5AD.root',
#'root://cms-xrd-global.cern.ch//store/data/Run2016G/JetHT/AOD/22Feb2017-v1/120000/1C9F6024-A1F9-E611-B27D-A4BF0108B60A.root',
#'root://cms-xrd-global.cern.ch//store/data/Run2016G/JetHT/AOD/22Feb2017-v1/120000/54E00AB5-ABF9-E611-B68A-002590200978.root',
						  	  
# runF, run = 278366, Fill = 5181
'root://cms-xrd-global.cern.ch//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/1310000/583756F1-A0FE-E611-B7E7-02163E01A70D.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/1310000/DEF3B79C-A1FE-E611-96F6-FA163E1455AC.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/1310000/E460F6F0-A0FE-E611-954D-02163E019BB1.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/1310000/FE3B2F72-A1FE-E611-B681-FA163EC14324.root',
'''
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90000/18026977-83FD-E611-B777-FA163EE2FFDA.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90000/20D98D49-03FD-E611-A8CA-FA163EDD5282.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90000/42ED6A64-02FD-E611-A7DC-02163E014A62.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90000/5A729935-65FD-E611-A2A5-02163E01A358.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90000/646CC925-05FD-E611-B1BE-FA163E6A92FB.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90000/7C671372-01FD-E611-8773-FA163EFCCFED.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90000/82365ED6-04FD-E611-A2FF-02163E01A843.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90000/9C35E52F-65FD-E611-9978-02163E019E25.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90000/9ED80EA9-04FD-E611-A06F-FA163E4BEB03.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90000/BAB02897-21FD-E611-8A5E-02163E00CE85.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90000/BC32A436-00FD-E611-8D95-FA163EE80735.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90000/D47BCD66-86FD-E611-BA31-FA163E66E225.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90000/E0363804-03FD-E611-8A59-FA163EB12D1D.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90000/EA9A3552-03FD-E611-A389-FA163E3F2846.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90000/F6913AD6-03FD-E611-833C-FA163EE70224.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90001/0CC97308-6EFD-E611-83B6-02163E019CA9.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90001/12FA172E-68FD-E611-AF02-02163E01A539.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90001/26E3D1C6-6DFD-E611-875D-02163E01381A.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90001/4A76D0E4-67FD-E611-A257-02163E0146A7.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90001/4C5317E7-67FD-E611-968B-02163E01A242.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90001/7C9AE7E4-6DFD-E611-8E08-02163E019BBA.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90001/9087E017-6EFD-E611-A994-02163E01A642.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90001/94BCDBDF-67FD-E611-9001-02163E01463B.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90001/9A63EB50-71FD-E611-A7C1-02163E01A2E9.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90001/BA9780D3-73FD-E611-B7A3-02163E01A5D5.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90001/D46826A0-70FD-E611-A2C0-02163E01464C.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90001/D4B160F8-67FD-E611-A091-02163E014324.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90001/F4E988DC-67FD-E611-A299-02163E014670.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90002/08096A18-9FFD-E611-A520-1866DA86CCDF.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90002/38BA825D-BAFD-E611-B060-1866DA87AFB4.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90002/38D4BD7C-B9FD-E611-A04C-1866DA87A864.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90002/3A524611-A4FD-E611-BBA6-D4AE526A0419.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90002/7C1A975D-A7FD-E611-86D8-D4AE5269F611.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90002/842086A9-A9FD-E611-BAF8-1CC1DE18CFEA.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90002/92847158-ACFD-E611-B2ED-1866DA87F44A.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90002/96CF2871-B0FD-E611-A22E-0CC47A7EEF1A.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90002/A6D63D6B-B2FD-E611-88E4-D4AE526A0C89.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90002/B423065B-AEFD-E611-9284-1866DA879B33.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90002/B63F88DE-ADFD-E611-94D0-D4AE526A0A60.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90002/BA7D15B7-B5FD-E611-8F6A-1866DA89061C.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90002/BC0A313B-5FFD-E611-B0B0-02163E011875.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90002/CA405354-B7FD-E611-9528-1866DA879B33.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90002/CA4D5E3B-B8FD-E611-9C30-0CC47A009352.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90002/CAD2E54B-B4FD-E611-AE06-1866DA87F44A.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90002/DC67B654-A7FD-E611-83C7-0CC47A7EEF1A.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90002/F0F1BF5C-B1FD-E611-B325-1866DA87E080.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90002/F2EA5D3F-B8FD-E611-A8A9-1866DA87AF6C.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90002/F6612D95-B3FD-E611-832F-0CC47A7EEE92.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/0065B5A6-BCFD-E611-9C09-1866DA879EDE.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/084CA7FD-E8FD-E611-B051-1866DA87A5A4.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/0A190D77-EFFD-E611-9E0F-0CC47A7EEE80.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/0EB5E153-C6FD-E611-9DFC-842B2B71F663.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/1072C442-BDFD-E611-8E1B-1866DA87AFB4.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/14BDA430-F0FD-E611-B605-1CC1DE192734.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/1AA4BB70-C0FD-E611-B3AE-0CC47A009352.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/1C4B2E47-D3FD-E611-ABAC-D4AE526A0922.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/1CA9DFB9-D8FD-E611-967A-1866DA890789.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/204FE49B-DEFD-E611-A14F-D4AE526A0461.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/20647152-E0FD-E611-B0C3-1866DA87A7E7.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/226423B0-CEFD-E611-903C-0CC47A00A814.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/22AA5BB9-C4FD-E611-AAB6-842B2B71F663.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/22E34DC3-EEFD-E611-8561-1866DA87AFB4.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/249FA623-CDFD-E611-9330-D4AE5269F919.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/264DB50A-EBFD-E611-B5C1-1866DA890388.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/2808D9CB-DAFD-E611-9110-842B2B7680A2.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/28AA83EF-E2FD-E611-AC9F-1866DA890700.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/2A52517D-ECFD-E611-B177-1866DA890A68.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/302F068A-FCFD-E611-BD99-1866DA87B3E6.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/30B827B9-C8FD-E611-8339-1866DA852F52.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/34AFE01E-CDFD-E611-B8FE-1CC1DE18CFEA.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/36C2ED2F-E5FD-E611-9D37-842B2B7680A2.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/3859DA7A-ECFD-E611-A531-1866DA890268.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/40725F63-EFFD-E611-823D-1866DA890789.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/424B7295-BBFD-E611-B255-1866DA890B10.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/446B0A7B-E4FD-E611-A279-1866DA890789.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/46494775-C3FD-E611-A46B-0CC47A01CAFC.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/466BA9FC-E9FD-E611-8C0E-1866DA890AEC.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/4E364406-BEFD-E611-A630-1866DA87F44A.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/5014F225-E8FD-E611-AB0E-D4AE526A33F5.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/56C8D376-ECFD-E611-BFD8-1866DA87C2CD.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/5EC1134C-E0FD-E611-A077-1866DA890879.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/641C3556-C7FD-E611-A6CA-1866DA890370.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/66318C37-E1FD-E611-8667-1866DA890789.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/688023A3-C4FD-E611-8497-1866DA890700.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/6C68B097-DEFD-E611-8A47-1866DA87D585.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/70484D4F-FBFD-E611-AAA2-1866DA87967B.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/706283C5-EEFD-E611-9DF8-1CC1DE19316E.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/707C4D74-C0FD-E611-BE91-842B2B7680DF.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/74087FFD-E8FD-E611-90A6-D4AE526A0D22.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/7A043782-D7FD-E611-A155-0CC47A7EEC70.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/7CD47649-E0FD-E611-B59B-1866DA8908C7.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/80FB6965-DDFD-E611-82A9-1866DA852F52.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/845A99B8-E3FD-E611-AC60-1866DA890388.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/8828D8F5-C7FD-E611-B11B-1866DA87BB03.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/8E6BFB5A-E7FD-E611-9944-1866DA87A664.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/947B4CB6-E3FD-E611-9D18-D4AE526A0B29.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/963B4053-E1FD-E611-BFC9-842B2B5C2299.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/96D7C34C-E1FD-E611-8539-1CC1DE192872.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/9EACC6ED-F6FD-E611-98C7-1866DA87AB73.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/A02CA698-D1FD-E611-B1E3-D4AE526A092E.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/A25A609A-D1FD-E611-966C-D4AE526A0D22.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/A4296B98-BBFD-E611-8F2F-D4AE5269FD24.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/A4B3435A-E7FD-E611-822C-1866DA87D7BF.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/A86786CA-DBFD-E611-8B45-842B2B7669E2.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/AAF518F7-FFFD-E611-9C3F-1866DA89095D.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/ACBA9D19-E2FD-E611-A258-D4AE526A0B29.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/AE546153-C6FD-E611-BB98-1866DA890700.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/B06BAABF-D9FD-E611-B96B-D4AE526A0A7B.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/B209ED8E-E6FD-E611-B7C8-1866DA879B33.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/BEECE7E8-D9FD-E611-83CE-842B2B7680DF.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/C05EF662-DDFD-E611-BF0B-D4AE526A109A.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/C659EA77-ECFD-E611-B4A6-0CC47A7EEE80.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/D01C512A-E8FD-E611-B286-1CC1DE18D026.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/D08748F5-E2FD-E611-8841-842B2B758BAA.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/D658C456-EDFD-E611-AEB2-1CC1DE18CFD4.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/DA39C994-BBFD-E611-B5F5-1866DA8908C7.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/E028D463-DDFD-E611-9ABD-D4AE526A0455.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/E66CDA2E-E5FD-E611-8F43-1866DA890879.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/E6ED83E4-BEFD-E611-A8B7-1866DA87AFB4.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/EAF88062-E4FD-E611-A4D7-1866DA87D585.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/EE802DB6-EEFD-E611-B30A-1866DA890388.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/F2F07B3C-CEFD-E611-88A1-1866DA87AFB4.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/F620B158-E4FD-E611-97BA-D4AE526A33F5.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/F8826646-D3FD-E611-BA79-1866DA89095D.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/F8BF7655-F9FD-E611-96C4-1866DA87AF6C.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/FC5E3D9B-F4FD-E611-82D0-0CC47A7EEE96.root',
'root://xrootd-cms.infn.it//store/data/Run2016F/JetHT/AOD/22Feb2017-v1/90003/FE0A62A7-F7FD-E611-BA04-D4AE526A0B29.root',
'''
  						             ),
									 #firstRun = cms.untracked.uint32(277127)
			   )

#process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange('278366:100-278366:130')

process.maxEvents = cms.untracked.PSet(
                                       input = cms.untracked.int32(-1) #1500
                                      )

process.options   = cms.untracked.PSet(
                                       wantSummary = cms.untracked.bool(False)
                                      )

# this is for filtering on L1 technical trigger bit
process.load('L1TriggerConfig.L1GtConfigProducers.L1GtTriggerMaskTechTrigConfig_cff')
process.load('HLTrigger/HLTfilters/hltLevel1GTSeed_cfi')

process.hltLevel1GTSeed.L1TechTriggerSeeding     = cms.bool(True)
process.hltLevel1GTSeed.L1SeedsLogicalExpression = cms.string('0 AND ( 40 OR 41 )')

#### remove beam scraping events
process.noScraping = cms.EDFilter(
                                  "FilterOutScraping",
    				  applyfilter = cms.untracked.bool(True) ,
    				  debugOn     = cms.untracked.bool(False), ## Or 'True' to get some per-event info
    				  numtrack    = cms.untracked.uint32(10) ,
    				  thresh      = cms.untracked.double(0.20)
                                 )

#process.p = cms.Path(process.hltLevel1GTSeed + process.d0_phi_analyzer)
process.p = cms.Path(process.d0_phi_analyzer)
process.MessageLogger.debugModules = ['BeamSpotAnalyzer']

#######################

process.MessageLogger.cerr.FwkReport.reportEvery = 1000

# run over STA muons
#process.d0_phi_analyzer.BeamFitter.TrackCollection = cms.untracked.InputTag('ALCARECOTkAlMinBias') #,'UpdatedAtVtx')
#process.d0_phi_analyzer.BeamFitter.IsMuonCollection = True

process.d0_phi_analyzer.BeamFitter.WriteAscii                = True
process.d0_phi_analyzer.BeamFitter.AsciiFileName             = 'BS_LUT_run278366_sumptUP_trksDOWN.txt'
process.d0_phi_analyzer.BeamFitter.AppendRunToFileName       = False
process.d0_phi_analyzer.BeamFitter.InputBeamWidth            = -1
process.d0_phi_analyzer.BeamFitter.MaximumImpactParameter    = 1.0
process.d0_phi_analyzer.BeamFitter.MaximumNormChi2           = 10
process.d0_phi_analyzer.BeamFitter.MinimumInputTracks        = 2 #50
process.d0_phi_analyzer.BeamFitter.MinimumPixelLayers        = -1
process.d0_phi_analyzer.BeamFitter.MinimumTotalLayers 	     = 6
process.d0_phi_analyzer.BeamFitter.MinimumPt                 = 1.0
process.d0_phi_analyzer.BeamFitter.OutputFileName 	         = 'BS_LUT_run278366_sumptUP_trksDOWN.root'
process.d0_phi_analyzer.BeamFitter.TrackAlgorithm            = cms.untracked.vstring()
process.d0_phi_analyzer.BeamFitter.TrackCollection           = 'generalTracks'

process.d0_phi_analyzer.BeamFitter.SaveNtuple     	     = False
process.d0_phi_analyzer.BeamFitter.SavePVVertices 	     = False
process.d0_phi_analyzer.BeamFitter.SaveFitResults 	     = False

# defalt values : sumPt= 50.    - NTracks=20 (30 is the new one)
# median values : sumPt= 289.36 - NTracks=76.8
# new median val: sumPt= 301.6  - NTracks=76.54
# LUT median val: sumPt= 300.0 - Ntrakcs= 70
process.d0_phi_analyzer.PVFitter.Apply3DFit       	         = True
process.d0_phi_analyzer.PVFitter.useOnlyFirstPV              = True
process.d0_phi_analyzer.PVFitter.errorScale                  = 1.
process.d0_phi_analyzer.PVFitter.minSumPt                    = 300.0 #50
process.d0_phi_analyzer.PVFitter.maxSumPt                    = 1000.0 #300.0
process.d0_phi_analyzer.PVFitter.minVertexNTracks            = 30 #70
process.d0_phi_analyzer.PVFitter.maxVertexNTracks            = 70 #1000

# fit as function of lumi sections
process.d0_phi_analyzer.BSAnalyzerParameters.fitEveryNLumi   = 1 #2
process.d0_phi_analyzer.BSAnalyzerParameters.resetEveryNLumi = 1 #2

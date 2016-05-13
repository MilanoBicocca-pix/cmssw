import FWCore.ParameterSet.Config as cms

from getfiles import get_files

myfiles = get_files('/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000')
#myfiles = get_files('/store/data/Run2015D/HLTPhysics/ALCARECO/TkAlMinBias-PromptReco-v3/000/257/969/00000')

process = cms.Process("d0phi")

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load("RecoVertex.BeamSpotProducer.d0_phi_analyzer_cff")

process.source = cms.Source("PoolSource",
                   fileNames = cms.untracked.vstring(
		       myfiles
		       #myfiles[:2]
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/0CBA6937-0114-E611-BF18-02163E0120DB.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/0EF089EC-FD13-E611-AE5B-02163E011888.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/10051741-0A14-E611-A395-02163E01471E.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/1080866E-FC13-E611-AE8B-02163E0142C5.root"
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/12F5EA21-FF13-E611-9F51-02163E011ED9.root"
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/12F7AC1B-0514-E611-AC10-02163E012247.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/162F05EC-0414-E611-BF08-02163E011C60.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/18BE7CE0-0214-E611-8A97-02163E014551.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/1EFA18F5-FB13-E611-834E-02163E0138AF.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/26034E61-0314-E611-A5B0-02163E011BDE.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/26EB9026-FF13-E611-BE1F-02163E0118F9.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/2CE6A76A-FD13-E611-A5F2-02163E0143DB.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/3260337E-0114-E611-A99C-02163E013752.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/34021918-0614-E611-AB37-02163E0144CB.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/347CC123-0014-E611-A6F5-02163E012679.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/34D948D8-0214-E611-AD04-02163E01449E.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/3AFB9BF9-0114-E611-B267-02163E0133BE.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/426CD3DE-FD13-E611-92B1-02163E0143EB.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/428972EC-0114-E611-8C53-02163E012177.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/42C09006-FC13-E611-816C-02163E01399D.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/44C04DFB-0114-E611-B0C6-02163E01359C.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/482F2215-0514-E611-B4B8-02163E011A9B.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/4A1CC18F-0114-E611-988A-02163E01471E.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/4CB2FC7F-0114-E611-92CC-02163E01236F.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/4EE49D6A-0014-E611-8652-02163E01256A.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/52EE8A1A-0514-E611-93D4-02163E011E5F.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/5628F1BB-0514-E611-9C59-02163E0144A8.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/58025019-FF13-E611-BC18-02163E01364C.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/58F91245-0014-E611-AE31-02163E013805.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/58FA6A18-FC13-E611-A2A0-02163E011D91.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/5EF7A12A-0514-E611-A1DC-02163E0146DB.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/627811E3-FD13-E611-9FDB-02163E0136FE.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/6AF83088-0114-E611-BED8-02163E0144F0.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/703A21FB-FB13-E611-93BB-02163E01419A.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/72C40B29-FD13-E611-9930-02163E01201A.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/743B948C-0114-E611-9E97-02163E013864.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/74934C69-0014-E611-AF1E-02163E01456D.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/78BD8E1D-FF13-E611-974D-02163E013452.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/7A1D806D-FC13-E611-8F89-02163E0142C5.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/80E01A8D-0014-E611-9D34-02163E014633.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/84F0936E-0014-E611-ACF6-02163E01411E.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/88EAB31D-FC13-E611-88D7-02163E0146BE.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/8A1DC82A-0514-E611-B6F1-02163E013942.root"
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/8A28D364-0514-E611-B8D2-02163E0137F5.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/8AC18F5C-FE13-E611-812F-02163E011EE4.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/8ADAAF2D-FE13-E611-9C1A-02163E014488.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/8C357BAC-0114-E611-89AE-02163E01436A.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/8E28DFFC-0214-E611-9673-02163E0144E5.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/9476C630-FD13-E611-934B-02163E011EB6.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/9CA38131-0714-E611-894E-02163E012A40.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/A26201FC-0114-E611-9AC6-02163E011E1B.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/A4080E5F-0314-E611-A183-02163E011DBE.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/AAC1426E-0014-E611-85A9-02163E013664.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/B246850B-FD13-E611-BCF6-02163E014716.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/C2055AE9-FD13-E611-92B9-02163E0118DF.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/C2F80A92-0114-E611-AA70-02163E011D81.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/C808C71C-FF13-E611-9BE2-02163E013552.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/C81ACC18-0514-E611-B8B6-02163E01385B.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/C8DE0380-0114-E611-BBA9-02163E01236F.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/C8F679DC-FD13-E611-B537-02163E014716.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/CAEDF487-0114-E611-A9E0-02163E0139A3.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/CEE24F12-0014-E611-8099-02163E013502.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/D02774DB-FD13-E611-96DE-02163E0137DA.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/DCB34819-0314-E611-8932-02163E011F4C.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/DEBEDB82-0314-E611-BCD6-02163E0118F9.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/E2D85017-FF13-E611-B36B-02163E0143A4.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/EE7B263C-0014-E611-A48A-02163E011E12.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/F69C831A-0514-E611-B775-02163E0138A1.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/F8D37B32-FD13-E611-A6E9-02163E013813.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/F8EB9030-FF13-E611-BB32-02163E014627.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/FADEA609-FD13-E611-8D98-02163E0142B5.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/FCED44C4-FC13-E611-AB75-02163E0143A2.root",
#    "/store/express/Run2016B/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/272/775/00000/FEF3426F-0014-E611-8B5A-02163E012330.root"
  )
)

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
process.d0_phi_analyzer.BeamFitter.TrackCollection = cms.untracked.InputTag('ALCARECOTkAlMinBias') #,'UpdatedAtVtx')

process.d0_phi_analyzer.BeamFitter.WriteAscii                = True
process.d0_phi_analyzer.BeamFitter.AsciiFileName             = 'result_BeamFit.txt'
process.d0_phi_analyzer.BeamFitter.Debug                     = cms.untracked.bool(True)
process.d0_phi_analyzer.BeamFitter.InputBeamWidth            = -1
process.d0_phi_analyzer.BeamFitter.MaximumImpactParameter    = 1.0  
process.d0_phi_analyzer.BeamFitter.MaximumNormChi2           = 10
process.d0_phi_analyzer.BeamFitter.MinimumInputTracks        = 50   
process.d0_phi_analyzer.BeamFitter.MinimumPt                 = 1.0
process.d0_phi_analyzer.BeamFitter.MinimumTotalLayers        = 6
process.d0_phi_analyzer.BeamFitter.MinimumPixelLayers        = -1

process.d0_phi_analyzer.BeamFitter.OutputFileName            = 'BeamFit.root' #AtVtx10000.root'
process.d0_phi_analyzer.BeamFitter.TrackAlgorithm            = cms.untracked.vstring()
process.d0_phi_analyzer.BeamFitter.SaveFitResults            = True
process.d0_phi_analyzer.BeamFitter.SaveNtuple                = True
process.d0_phi_analyzer.BeamFitter.SavePVVertices            = False

process.d0_phi_analyzer.BeamFitter.MaximumZ                  = 60
process.d0_phi_analyzer.BeamFitter.FractionOfFittedTrks      = 0.9

# process.d0_phi_analyzer.BeamFitter.BunchCrossings            = cms.untracked.vdouble(1)


process.d0_phi_analyzer.PVFitter.Apply3DFit                  = True
process.d0_phi_analyzer.PVFitter.minNrVerticesForFit         = 10
process.d0_phi_analyzer.PVFitter.nSigmaCut                   = 100.0 # Usually 50.0


# fit as function of lumi sections
process.d0_phi_analyzer.BSAnalyzerParameters.fitEveryNLumi   = 1
process.d0_phi_analyzer.BSAnalyzerParameters.resetEveryNLumi = 1

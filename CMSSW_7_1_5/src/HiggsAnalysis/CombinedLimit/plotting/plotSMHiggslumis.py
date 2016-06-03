import ROOT as r
import sys
import numpy as np
import CMS_lumi
from scipy.optimize import curve_fit
outf = r.TFile('PlotCanvas.root','RECREATE')
blind=False

def g_x(mchi, A):
  bracket = (1. - (mchi/62.5)**2)
  return A*bracket**(-0.75)

def fit_pts(mhsin, medsin):
  # split into onshell and offshell
  mhon = []
  mhoff = []
  for mh in mhsin:
    if mh < 62.5:
      mhon.append(mh)
    else:
      mhoff.append(mh)
  medon = medsin[:len(mhon)]
  medoff = medsin[len(mhon):]

  # fit onshell
  popt, pcov = curve_fit(g_x, np.array(mhon), np.array(medon))

  # create a finer data set
  mchison = np.linspace(0,62.49,40)
  gxson = g_x(mchison, popt[0])

  mchis = list(mchison)+mhoff
  gxs = list(gxson)+medoff

  return mchis, gxs

def makePlot():

  # get data from filename
  infilename = []
  luminosity = []
  for i in range(len(sys.argv)-1):
    infilename.append(sys.argv[i+1])
    luminosity.append(infilename[i].split("_")[2][:-7])
  modelname = infilename[0].split("_")[1]
  
  CMS_lumi.lumi_13TeV = ""
  CMS_lumi.writeExtraText = 1
  CMS_lumi.extraText = " "
  iPos=33
  
  canv = r.TCanvas()
  canv.Clear()
  canv.SetLogy(True)
  canv.SetLogx(False)
  canv.SetBottomMargin(0.13)
  mg = r.TMultiGraph()
  leg = r.TLegend(0.6, 0.3, 0.80, 0.50)
  leg.SetFillColor(0)
  leg.SetFillStyle(0)
  leg.SetBorderSize(0)
  leg.SetTextFont(42)

  dummyHist = r.TH1D("dummy","",1,10,200)
  dummyHist.GetXaxis().SetTitle('m_{#chi} [GeV]')
  dummyHist.GetYaxis().SetTitle('g_{#chi}')
  dummyHist.SetTitleSize(.05,"X")
  dummyHist.SetTitleOffset(1.2,"X") #0.75
  dummyHist.SetTitleSize(.05,"Y")
  dummyHist.SetTitleOffset(0.92,"Y")
  # make text box
  lat = r.TLatex()
  lat.SetNDC()
  lat.SetTextFont(42);

  lat2 = r.TLatex()
  lat2.SetNDC()
  lat2.SetTextSize(0.04)
  lat2.SetTextFont(42);

  # get the data 
  tf = [0,0,0]
  tree = [0,0,0]
  values = [0,0,0]
  graph = [0,0,0]
  exp = [0,0,0]
  oneSigma = [0,0,0]
  twoSigma = [0,0,0]
  for k in range(3):
    tf[k] = r.TFile(sys.argv[k+1])
    tree[k] = tf[k].Get('limit')
    values[k]=[]
    #print tree[k].GetEntries()
    for i in range(tree[k].GetEntries()):
        tree[k].GetEntry(i)
        ###################### 
        # apply the transformation that was made to make the limits converge
        mh = 10**(tree[k].mh)
        if i<24: # 6*4 (6 numbers per point)
            lim = tree[k].limit
        if i>=24 and i<30:
            lim = 1000*tree[k].limit
        if i>=30:
            lim = 10000*tree[k].limit
        #####################
        # apply the r -> gchi conversion
        if mh<62.5:
            prefactor = ( 8*3.1415 * (lim/(1.-lim)) * (0.0041/125.0) )**(0.5)
            gchi = prefactor * (1.0 - 4.0*(mh)**2/(125.0)**2)**(-0.75)
        if mh>=62.5:
            gchi = 0.179*lim**0.5 
        # append the results
        values[k].append([mh, gchi])
    values[k].sort(key=lambda x: x[0])

    # make graph from values
    graph[k] = r.TGraphAsymmErrors()
    exp[k] = r.TGraphAsymmErrors()
    oneSigma[k] = r.TGraphAsymmErrors()
    twoSigma[k] = r.TGraphAsymmErrors()

    # extract the values
    point_counter=0
    mhs = []
    medians = []
    for j in range(len(values[k])):
      if (j%6==0):
        mhs.append(values[k][j][0])
        medians.append(values[k][j+2][1])

    # interpolate the results
    mhs, medians = fit_pts(mhs, medians)

    # append the values to the graph
    for i in range(len(mhs)):
      mh = mhs[i]
      median = medians[i]
      exp[k].SetPoint(point_counter,mh,median)
      point_counter+=1

    
    exp[k].SetLineColor(r.kBlack)
    exp[k].SetLineWidth(3)

    mg.Add(exp[k])
    mg.Draw("A")

  exp[0].SetLineStyle(1)
  exp[1].SetLineStyle(7)
  exp[2].SetLineStyle(3)
  exp[0].SetLineColor(205)
  exp[1].SetLineColor(205)
  exp[2].SetLineColor(205)

  # legend
  #leg.SetHeader('95% CL limits')
  leg.AddEntry(exp[0],'3000 fb^{-1}','L')
  leg.AddEntry(exp[1],'300 fb^{-1}','L')
  leg.AddEntry(exp[2],'20 fb^{-1}','L')
  
  # draw dummy hist and multigraph
  dummyHist.SetMinimum(0.001)
  #dummyHist.SetMaximum(mg.GetYaxis().GetXmax())
  dummyHist.SetMaximum(100)
  dummyHist.SetLineColor(0)
  dummyHist.SetStats(0)
  dummyHist.SetLabelSize(0.05, "X")
  dummyHist.SetLabelSize(0.05, "Y")
  dummyHist.Draw("AXIS")
  mg.Draw("3") #3
  mg.Draw("LPX") 
  dummyHist.Draw("AXIGSAME")
 
  CMS_lumi.CMS_lumi(canv, 4, iPos)

  # draw legend
  leg.Draw()
  canv.RedrawAxis()

  # print canvas
  canv.Update()
  canv.Print(modelname+"_multilumi.pdf")
  outf.cd()
  canv.SetName("limit_cavas")
  canv.Write()

makePlot()

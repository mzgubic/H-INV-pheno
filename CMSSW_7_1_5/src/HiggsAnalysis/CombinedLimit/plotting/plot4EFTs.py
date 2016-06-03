import ROOT as r
import sys
import CMS_lumi
outf = r.TFile('PlotCanvas.root','RECREATE')
blind=False
def makePlot():

  # get data from filename
  infilename = []
  luminosity = []
  for i in range(len(sys.argv)-1):
    infilename.append(sys.argv[i+1])
    luminosity.append(infilename[i].split("_")[2][:-7])
  modelname = infilename[0].split("_")[1][:-1]
  print modelname
  
  CMS_lumi.lumi_13TeV = ""
  CMS_lumi.writeExtraText = 1
  #CMS_lumi.extraText = "Model: "+modelname
  iPos=33
  
  canv = r.TCanvas()
  canv.Clear()
  canv.SetLogy(False)
  canv.SetLogx(True)
  canv.SetBottomMargin(.13)
  canv.SetLeftMargin(.12)
  canv.SetRightMargin(.05)
  mg = r.TMultiGraph()
  leg = r.TLegend(0.79, 0.70, 0.95, 0.89)
  leg.SetFillStyle(0)
  leg.SetBorderSize(0)
  leg.SetTextFont(62)
  leg.SetTextSize(0.05)

  dummyHist = r.TH1D("dummy","",1,10,1000)
  dummyHist.GetXaxis().SetTitle('m_{#chi} [GeV]')
  dummyHist.GetYaxis().SetTitle('#Lambda [GeV]')
  dummyHist.SetTitleSize(.05,"X")
  dummyHist.SetLabelSize(.05,"X")
  dummyHist.SetTitleOffset(1.3,"X")
  dummyHist.SetTitleSize(.05,"Y")
  dummyHist.SetLabelSize(.05,"Y") # did somehow cause segfault
  dummyHist.SetTitleOffset(1.2,"Y")
  # make text box
  lat = r.TLatex()
  lat.SetNDC()
  lat.SetTextFont(42);

  lat2 = r.TLatex()
  lat2.SetNDC()
  lat2.SetTextSize(0.04)
  lat2.SetTextFont(42);

  # get the data 
  tf = [0] * len(sys.argv)
  tree = [0] * len(sys.argv)
  values = [0] * len(sys.argv)
  graph = [0] * len(sys.argv)
  exp = [0] * len(sys.argv)
  oneSigma = [0] * len(sys.argv)
  twoSigma = [0] * len(sys.argv)
  for k in range(len(sys.argv)-1):
    tf[k] = r.TFile(sys.argv[k+1])
    tree[k] = tf[k].Get('limit')
    values[k]=[]
    for i in range(tree[k].GetEntries()):
        tree[k].GetEntry(i)
        #values[k].append([tree[k].mh, tree[k].limit])
        values[k].append([10**(tree[k].mh), tree[k].limit])
    values[k].sort(key=lambda x: x[0])
    # make graph from values
    graph[k] = r.TGraphAsymmErrors()
    exp[k] = r.TGraphAsymmErrors()
    oneSigma[k] = r.TGraphAsymmErrors()
    twoSigma[k] = r.TGraphAsymmErrors()

    point_counter=0
    for j in range(len(values[k])):
        if (j%6==0):
          mh = values[k][j][0]
          down95 = values[k][j][1]
          down68 = values[k][j+1][1]
          median = values[k][j+2][1]
          up68 = values[k][j+3][1]
          up95 = values[k][j+4][1]
          obs = values[k][j+5][1]

          # transformation from limit to the excluded lambda
          if modelname == "D5":
            power = 2
            if k in [3, 4, 5]:
              lam = 1500.
            else:
              lam = 800.
          if modelname == "D6":
            power = 4
            lam = 800.
          if modelname == "D7":
            power = 6
            lam = 800.

          # transformation
          down95 = lam*down95**(-1./power)
          down68 = lam*down68**(-1./power)
          median = lam*median**(-1./power)
          up95 = lam*up95**(-1./power)
          up68 = lam*up68**(-1./power)

          # luminosities, color
          if k%3 == 0: # 3000 fb
            exp[k].SetLineStyle(1)
            exp[k].SetLineWidth(3)
          if k%3 == 1: # 300 fb
            exp[k].SetLineStyle(7)
            exp[k].SetLineWidth(3)
          if k%3 == 2: # 20 fb
            exp[k].SetLineStyle(3)
            exp[k].SetLineWidth(3)
          # modelname, style
          if k < 12: # D5d
            exp[k].SetLineColor(205)
          if k < 9: # D5c
            exp[k].SetLineColor(210)
          if k < 6: # D5b
            exp[k].SetLineColor(216)
          if k < 3: # D5a
            exp[k].SetLineColor(0) #6
   
          # add to graph in the same way as before
          exp[k].SetPoint(point_counter, mh, median)
          oneSigma[k].SetPoint(point_counter,mh,median)
          oneSigma[k].SetPointError(point_counter,0,0,abs(median-down68),abs(up68-median))
          twoSigma[k].SetPoint(point_counter,mh,median)
          twoSigma[k].SetPointError(point_counter,0,0,abs(median-down95),abs(up95-median))
          point_counter+=1

    
    oneSigma[k].SetLineColor(r.kGreen)
    twoSigma[k].SetLineColor(r.kYellow)
    oneSigma[k].SetFillColor(r.kGreen)
    twoSigma[k].SetFillColor(r.kYellow)

    mg.Add(exp[k])
    mg.Draw("A")

  
  # draw dummy hist and multigraph
  dummyHist.SetMinimum(0)
  dummyHist.SetMaximum(mg.GetYaxis().GetXmax())
  dummyHist.SetLineColor(0)
  dummyHist.SetStats(0)
  dummyHist.Draw("AXIS")
  mg.Draw("3")
  mg.Draw("CL")
  dummyHist.Draw("AXIGSAME")
 
  CMS_lumi.CMS_lumi(canv, 4, iPos)
  # add text
  if modelname == "D5":
    lat.DrawLatex(0.55,0.92,"#color[205]{D5d}")
    lat.DrawLatex(0.40,0.92,"#color[210]{D5c}")
    lat.DrawLatex(0.25,0.92,"#color[216]{D5b}")
    #lat.DrawLatex(0.10,0.92,"#color[0]{D5a}") #6
  if modelname == "D6":
    lat.DrawLatex(0.55,0.92,"#color[4]{D6b}")
    lat.DrawLatex(0.40,0.92,"#color[6]{D6a}")
  if modelname == "D7":
    lat.DrawLatex(0.55,0.92,"#color[2]{D7d}")
    lat.DrawLatex(0.40,0.92,"#color[3]{D7c}")
    lat.DrawLatex(0.25,0.92,"#color[4]{D7b}")
    lat.DrawLatex(0.10,0.92,"#color[6]{D7a}")

  # draw legend
  dummy3000 = r.TGraphAsymmErrors()
  dummy3000.SetLineColor(r.kBlack)
  dummy3000.SetLineStyle(1)
  dummy3000.SetLineWidth(3)
  dummy300 = r.TGraphAsymmErrors()
  dummy300.SetLineColor(r.kBlack)
  dummy300.SetLineStyle(7)
  dummy300.SetLineWidth(3)
  dummy20 = r.TGraphAsymmErrors()
  dummy20.SetLineColor(r.kBlack)
  dummy20.SetLineStyle(3)
  dummy20.SetLineWidth(3)
  #leg.SetHeader('95% CL')
  leg.AddEntry(dummy3000,'3000fb^{-1}','L')
  leg.AddEntry(dummy300,'300fb^{-1}','L')
  leg.AddEntry(dummy20,'20fb^{-1}','L')
  leg.Draw()
  canv.RedrawAxis()

  # print canvas
  canv.Update()
  canv.Print(modelname+"_multilumi.pdf")
  outf.cd()
  canv.SetName("limit_cavas")
  canv.Write()

makePlot()

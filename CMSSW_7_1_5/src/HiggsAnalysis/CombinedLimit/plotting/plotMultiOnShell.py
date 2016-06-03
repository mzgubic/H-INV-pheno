"""
python plotMultiOffShell.py 40x40_300fb_mha/gridinfosystlumiscale.txt 40x40_3000fb_mha/gridinfosystlumiscale.txt
"""
import ROOT as r
import sys
import CMS_lumi
import math as m
import numpy as np
from array import array
import random
from array import array

col_store=[]
def CreateTransparentColor(color, alpha):
  adapt   = r.gROOT.GetColor(color)
  new_idx = r.gROOT.GetListOfColors().GetSize() + 1
  trans = r.TColor(new_idx, adapt.GetRed(), adapt.GetGreen(), adapt.GetBlue(), '', alpha)
  col_store.append(trans)
  trans.SetName('userColor%i' % new_idx)
  return new_idx

def fillTH2(hist2d, graph):
    for x in xrange(1, hist2d.GetNbinsX()+1):
        for y in xrange(1, hist2d.GetNbinsY()+1):
            xc = hist2d.GetXaxis().GetBinCenter(x)
            yc = hist2d.GetYaxis().GetBinCenter(y)
            val = graph.Interpolate(xc, yc)
            hist2d.SetBinContent(x, y, val)

def makeHist(name, xbins, ybins, graph2d):
    len_x = graph2d.GetXmax() - graph2d.GetXmin()
    binw_x = (len_x * 0.5 / (float(xbins) - 1.)) - 1E-5
    len_y = graph2d.GetYmax() - graph2d.GetYmin()
    binw_y = (len_y * 0.5 / (float(ybins) - 1.)) - 1E-5
    hist = r.TH2F(name, '', xbins, graph2d.GetXmin()-binw_x, graph2d.GetXmax()+binw_x, ybins, graph2d.GetYmin()-binw_y, graph2d.GetYmax()+binw_y)
    return hist

def OnePad():
    pad = r.TPad('pad', 'pad', 0., 0., 1., 1.)
    pad.Draw()
    pad.cd()
    result = [pad]
    return result

def frameTH2D(hist, threshold, mult = 1.0,frameValue=1000):
  # NEW LOGIC:
  #   - pretend that the center of the last bin is on the border if the frame
  #   - add one tiny frame with huge values
  #frameValue = 1000
  # if (TString(in->GetName()).Contains("bayes")) frameValue = -1000;

  xw = hist.GetXaxis().GetBinWidth(1)
  yw = hist.GetYaxis().GetBinWidth(1)

  nx = hist.GetNbinsX()
  ny = hist.GetNbinsY()

  x0 = hist.GetXaxis().GetXmin()
  x1 = hist.GetXaxis().GetXmax()

  y0 = hist.GetYaxis().GetXmin()
  y1 = hist.GetYaxis().GetXmax()
  xbins = array('d', [0]*999)
  ybins = array('d', [0]*999)
  eps = 0.1
  # mult = 1.0

  xbins[0] = x0 - eps * xw - xw * mult
  xbins[1] = x0 + eps * xw - xw * mult
  for ix in xrange(2, nx+1): xbins[ix] = x0 + (ix - 1) * xw
  xbins[nx + 1] = x1 - eps * xw + 0.5 * xw * mult
  xbins[nx + 2] = x1 + eps * xw + xw * mult

  ybins[0] = y0 - eps * yw - yw * mult
  ybins[1] = y0 + eps * yw - yw * mult
  for iy in xrange(2, ny+1): ybins[iy] = y0 + (iy - 1) * yw
  ybins[ny + 1] = y1 - eps * yw + yw * mult
  ybins[ny + 2] = y1 + eps * yw + yw * mult

  framed = r.TH2D('%s framed' % hist.GetName(), '%s framed' % hist.GetTitle(), nx + 2, xbins, ny + 2, ybins)

  # Copy over the contents
  for ix in xrange(1, nx+1):
    for iy in xrange(1, ny+1):
      framed.SetBinContent(1 + ix, 1 + iy, hist.GetBinContent(ix, iy))


  # Frame with huge values
  nx = framed.GetNbinsX()
  ny = framed.GetNbinsY()
  for ix in xrange(1, nx+1):
    framed.SetBinContent(ix, 1, frameValue)
    framed.SetBinContent(ix, ny, frameValue)

  for iy in xrange(2, ny):
    framed.SetBinContent(1, iy, frameValue)
    framed.SetBinContent(nx, iy, frameValue)

  return framed

def contourFromTH2(h2in, threshold, minPoints=10, mult = 1.0):
  # std::cout << "Getting contour at threshold " << threshold << " from "
  #           << h2in->GetName() << std::endl;
  # // http://root.cern.ch/root/html/tutorials/hist/ContourList.C.html

  contoursList = [threshold]
  contours = array('d', contoursList)
  if (h2in.GetNbinsX() * h2in.GetNbinsY()) > 10000: minPoints = 50
  if (h2in.GetNbinsX() * h2in.GetNbinsY()) <= 100: minPoints = 10

  #h2 = h2in.Clone()
  h2 = frameTH2D(h2in, threshold, mult)

  h2.SetContour(1, contours)

  # Draw contours as filled regions, and Save points
  backup = r.gPad
  canv = r.TCanvas('tmp', 'tmp')
  canv.cd()
  h2.Draw('CONT Z LIST')
  r.gPad.Update() # Needed to force the plotting and retrieve the contours in

  conts = r.gROOT.GetListOfSpecials().FindObject('contours')
  contLevel = None

  if conts is None or conts.GetSize() == 0:
    print '*** No Contours Were Extracted!'
    return None
  ret = r.TList()
  for i in xrange(conts.GetSize()):
    contLevel = conts.At(i)
    print 'Contour %d has %d Graphs\n' % (i, contLevel.GetSize())
    for j in xrange(contLevel.GetSize()):
      gr1 = contLevel.At(j)
      print'\t Graph %d has %d points' % (j, gr1.GetN())
      if gr1.GetN() > minPoints: ret.Add(gr1.Clone())
      # // break;
  backup.cd()
  return ret


outf = r.TFile('PlotCanvas.root','RECREATE')
def makePlot():

  # CMS_lumi.lumi_8TeV = "19.2 fb^{-1}"
  # CMS_lumi.writeExtraText = 1
  # CMS_lumi.extraText = "Preliminary"

  contours = []
  modelname = sys.argv[1].split("_")[2][:3]
  modelname2 = sys.argv[2].split("_")[2][:3]
  lumi1 = sys.argv[1].split("_")[1][:-2]
  lumi2 = sys.argv[2].split("_")[1][:-2]
  if modelname!=modelname2:
    print "models must match for two input files"
    exit()
  #Get y values and combine output files from input text file
  for k in range(len(sys.argv)-1):
    infile = open(sys.argv[k+1],"r")
    filestoread=infile.readlines()
    yvalues=[]
    for i in range(len(filestoread)):
      thisline=filestoread[i].split()
      yvalues.append([10**(float(thisline[0])),thisline[1]])
    yvalues.sort(key=lambda x: float(x[0]))

    #loop over y values getting tfiles and extracting x values and limits
    medianvalues=[]
    ybincenters=[]
    xbincenters=[]
    for i in range(len(yvalues)):
      ybincenters.append(float(yvalues[i][0]))
      tf = r.TFile(yvalues[i][1])
      tree = tf.Get('limit')
      xvalues=[]
      for j in range(tree.GetEntries()):
        tree.GetEntry(j)
        xvalues.append([10**(tree.mh), tree.limit])
      xvalues.sort(key=lambda x: float(x[0]))
   
     
      if len(xvalues) != 6*40:  # TODO: check the number!
        xs = []
        for item in xvalues:
          if item[0] not in xs: xs.append(item[0])

        # get how many of them are there in the list
        for x in xs:
          check = [item for item in xvalues if x in item]
          if i==0:
            xbincenters.append(x)
          # if there are less than 6 then add stuff
          for index in range(6-len(check)):
            xvalues.append([x, 10000+random.random()])
    
      # get limits for all x values for this y value
      for j in range(len(xvalues)):
        if (j%6==0):
          if len(xvalues)>j+2 : medianvalues.append([xvalues[j][0],yvalues[i][0],xvalues[j+2][1]])
          else : medianvalues.append([xvalues[j][0],yvalues[i][0],10000])


    graph_expon=r.TGraph2D()
    graph_expoff=r.TGraph2D()

    #Populate TGraph with points # TODO: create separate on and off shell graphs, then get separate contours etc.
    n=0
    m=0
    for j in range(len(ybincenters)):
      for i in range(len(xbincenters)):
        #if ybincenters[j] > 2*xbincenters[i]:
        graph_expon.SetPoint(n,xbincenters[i],ybincenters[j],medianvalues[j*len(xbincenters)+i][2])
        n=n+1
       # if ybincenters[j] < 2*xbincenters[i]:
       #   graph_expoff.SetPoint(m,xbincenters[i],ybincenters[j],medianvalues[j*len(xbincenters)+i][2])
       #   m=m+1

    #Make histogram out of TGraph
    axison = r.TH2D('hist2d','', len(xbincenters), graph_expon.GetXmin(), graph_expon.GetXmax(), len(ybincenters), graph_expon.GetYmin(), graph_expon.GetYmax())

    pointmultiple=5
    h_expon = makeHist("h_expon", pointmultiple*len(xbincenters), pointmultiple*len(ybincenters), graph_expon)
    #h_expoff = makeHist("h_expoff", pointmultiple*len(xbincenters), pointmultiple*len(ybincenters), graph_expoff)
    fillTH2(h_expon, graph_expon)
    #fillTH2(h_expoff, graph_expoff)

    #call getcontour function
    if modelname == 'mha':
      # xsec prop. to g**2
      cont_expon0=contourFromTH2(h_expon, 2.47, minPoints=1, mult = 1.0) # (pi/2)**2
      cont_expon1=contourFromTH2(h_expon, 9.87, minPoints=1, mult = 1.0)
      cont_expon2=contourFromTH2(h_expon, 39.5, minPoints=1, mult = 1.0)
    if modelname == 'mh2':
      # xsec prop. to g**2
      cont_expon0=contourFromTH2(h_expon, 9.87, minPoints=1, mult = 1.0) # (pi)**2
      cont_expon1=contourFromTH2(h_expon, 39.5, minPoints=1, mult = 1.0)
      cont_expon2=contourFromTH2(h_expon, 88.8, minPoints=1, mult = 1.0)

    # merge the two contours and append the merged thing

    contours.append(cont_expon0)
    contours.append(cont_expon1)
    contours.append(cont_expon2)
  # end the contour loop 

  canv = r.TCanvas()
  pads=OnePad()
  pads[0].Draw()
  pads[0].SetLogx(True)
  pads[0].SetLogy(True)
  pads[0].SetLogz(True)
  pads[0].SetBottomMargin(0.12)
  leg = r.TLegend(0.15, 0.50, 0.35, 0.7)
  leg.SetFillStyle(1001)
  leg.SetFillStyle(0)
  leg.SetFillColor(0)
  leg.SetBorderSize(0)
  leg.SetTextFont(42)

  axison.GetXaxis().SetTitle('m_{#chi}[GeV]')
  if modelname == 'mha':
    axison.GetYaxis().SetTitle('m_{A} [GeV]')
  if modelname == 'mh2':
    axison.GetYaxis().SetTitle('m_{H} [GeV]')
  axison.SetTitleSize(.05,"X")
  axison.SetLabelSize(.04,"X")
  axison.SetTitleOffset(1.1,"X")
  axison.SetTitleSize(.05,"Y")
  axison.SetLabelSize(.04,"Y")
  axison.SetTitleOffset(0.9,"Y")
  axison.SetStats(0)
  axison.GetXaxis().SetRangeUser(xbincenters[0],xbincenters[len(xbincenters)-1])
  axison.GetXaxis().SetRangeUser(xbincenters[0],xbincenters[len(xbincenters)-1])
  axison.Draw()

  # make text box
  lat = r.TLatex()
  lat.SetNDC()
  lat.SetTextFont(42);

  lat2 = r.TLatex()
  lat2.SetNDC()
  lat2.SetTextSize(0.04)
  lat2.SetTextFont(42);

  # contours
  for i, contour in enumerate(contours):
    for q, p in enumerate(contour):
      # set the luminosities - style
      if i < 9:
        p.SetLineWidth(3)
        p.SetLineStyle(3)
        p.Draw("L SAME")
      if i < 6:
        p.SetLineWidth(3)
        p.SetLineStyle(7)
        p.Draw("L SAME")
      if i < 3:
        p.SetLineWidth(3)
        p.SetLineStyle(1)
        p.Draw("L SAME")
      # set the couplings - colour
      if i%3 == 0:
        p.SetLineColor(210)
      if i%3 == 1:
        p.SetLineColor(205)
      if i%3 == 2:
        p.SetLineColor(216)

  # draw a line
  line = r.TLine(10,20,500,1000)
  line.Draw()

  # draw text
  #if modelname == 'mha':
  #  lat.DrawLatex(0.24,0.2,"#color[210]{g = #frac{#pi}{2}}")
  #  lat.DrawLatex(0.57,0.2,"#color[205]{g = #pi}")
  #  lat.DrawLatex(0.79,0.2,"#color[216]{g = 2#pi}")
  #if modelname == 'mh2':
  #  lat.DrawLatex(0.23,0.28,"#color[210]{g = #pi}")
  #  lat.DrawLatex(0.475,0.28,"#color[205]{g = 2#pi}")
  #  lat.DrawLatex(0.75,0.28,"#color[216]{g = 3#pi}")

  # add the triangle 
  triangle = r.TPolyLine(3, array('f', [10,500,500]), array('f', [20,20,1000]), "F")
  triangle.SetFillColor(0)
  triangle.SetFillStyle(1001)
  triangle.Draw("f")
  triangle2 = r.TPolyLine(3, array('f', [10,500,500]), array('f', [20,20,1000]), "F")
  triangle2.SetFillColor(1)
  triangle2.SetFillStyle(3004)
  triangle2.Draw("f")
  line = r.TLine(10,20,500,1000)
  line.Draw()

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

  leg.AddEntry(dummy3000,'3000fb^{-1}','L')
  leg.AddEntry(dummy300,'300fb^{-1}','L')
  leg.AddEntry(dummy20,'20fb^{-1}','L')
  leg.Draw("same")
 
  r.gPad.RedrawAxis()

  # print canvas
  canv.Update()
  print 'the bottom margin is', canv.GetBottomMargin()
  canv.Print(modelname+'_onshell_'+lumi1+'fb_'+lumi2+'fb.C')
  outf.cd()
  canv.SetName("limit_cavas")
  canv.Write()

makePlot()



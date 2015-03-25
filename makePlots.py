from ROOT import *
from array import array
import csv
import re

gROOT.SetBatch(kTRUE)

c1 = TCanvas('c1', 'Plots', 1000, 500)
c1.SetFillColor(0)
c1.SetGrid()
c1.SetLogy()

Mean = array('d')
RMS = array('d')
matrix= [ [array('d') for i in range(4)] for j in range(4)]
voltages = array('d',[0, 0.0003, 0.0005, 0.0007, 0.001, 0.0014, 0.0017, 0.0024, 0.003, 0.004, 0.005, 0.0061, 0.0074, 0.009, 0.03, 0.05, 0.07, 0.1, 0.15, 0.2, 0.35, 0.45, 0.5, 0.6, 0.7, 0.85, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0])
#create a data file with the Mean ADC and Mean RMS from the rootfiles
for volts in voltages:
        if (volts <= 4.0):
                f = TFile("dac_chn3_"+str(volts)+".root",'r')
                hist = f.Get("h14")
		#get rid of the 0 ADC points
                hist.SetBinContent(1,0)
                hist.Draw()
                hist.SetTitle("Mean ADC")
                c1.SaveAs("hist_"+str(volts)+"_log.pdf")
                Mean.append(hist.GetMean())
                RMS.append(hist.GetRMS())


                opentext = open("data_test.csv","w")
                writer = csv.writer(opentext, delimiter='\t')
writer.writerows(zip(voltages,Mean,RMS))
#f.Close()
#making plots
m = array('d')
r = array('d')
v = array('d')
file = open('data_test.csv', 'rU') # open file in read universal mode
for line in file:
        v.append(float(line.split()[0]))
        m.append(float(line.split()[1]))
        r.append(float(line.split()[2]))


gr = TGraph(len(m), m , v )
gr.SetLineColor(kBlack)
gr.SetMarkerColor(kBlack)
gr.SetMarkerSize(1.2)
gr.SetMarkerStyle(8)
gr.Draw('AP')
#tempy = gr.GetY()
#tempx = gr.GetX()
#print "bin 0 x: "+str(tempx[0])+" y: "+str(tempy[0])
#print "bin 0 x: "+str(tempx[1])+" y: "+str(tempy[1])
gr.SetTitle("Mean ADC vs DAC Voltage")
gr.GetXaxis().SetTitle("Mean ADC")
gr.GetYaxis().SetRangeUser(.00001,10)
gr.GetYaxis().SetTitle("DAC Volts")
gPad.RedrawAxis()
c1.SaveAs("ADC_chn3.pdf")
gr1 = TGraph(len(r), r , v )
gr1.SetLineColor(kBlack)
gr1.SetMarkerColor(kBlack)
gr1.SetMarkerSize(1.2)
gr1.SetMarkerStyle(8)
c1.Clear()
gr1.Draw('AP')
gr1.SetTitle("Mean RMS vs DAC Voltage")
gr1.GetXaxis().SetTitle("Mean RMS")
gr1.GetYaxis().SetTitle("DAC Volts")
gPad.RedrawAxis()

c1.SaveAs("RMS_chn3.pdf")

gr1 = TGraph(len(r), r , m )
gr1.SetLineColor(kBlack)
gr1.SetMarkerColor(kBlack)
gr1.SetMarkerSize(1.2)
gr1.SetMarkerStyle(8)
c1.Clear()
gr1.Draw('AP')
gr1.SetTitle("Mean RMS vs Mean ADC")
gr1.GetXaxis().SetTitle("Mean RMS")
gr1.GetYaxis().SetTitle("Mean ADC")
gPad.RedrawAxis()

c1.SaveAs("rms_chn3.pdf")


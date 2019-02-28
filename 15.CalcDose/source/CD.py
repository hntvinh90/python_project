#!/usr/bin/python

import wx
import math
from img import Image


class App(wx.App):

    def OnInit(self):
        MainFrame()
        self.MainLoop()
        return True

    def OnExit(self):
        return True


class MainFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Calculating Doses', size=(400, 400), style=wx.DEFAULT_FRAME_STYLE^(wx.RESIZE_BORDER|wx.MAXIMIZE_BOX))
        self.input = InputPanel(self)
        self.output = OutputPanel(self)
        self.show()

    def show(self):
        s1 = wx.BoxSizer(wx.VERTICAL)
        s1.Add(self.input, 0, wx.EXPAND)
        s1.Add(self.output, 1, wx.EXPAND)
        self.SetSizer(s1)
        self.SetIcon(Image['icon'].GetIcon())
        self.Show()


class InputPanel(wx.Panel):

    def __init__(self, parent):
        self.parent = parent
        wx.Panel.__init__(self, parent)
        self.addWidget()
        self.initValue()
        self.addEvents()
        self.show()

    def addWidget(self):
        self.widget_net = [wx.TextCtrl(self, size=(200, 25), style=wx.TE_CENTER),
                           wx.TextCtrl(self, size=(200, 25), style=wx.TE_CENTER),
                           wx.TextCtrl(self, size=(200, 25), style=wx.TE_CENTER),
                           wx.TextCtrl(self, size=(200, 25), style=wx.TE_CENTER)]
        self.btn = wx.Button(self, -1, 'Solve')

    def initValue(self):
        for i in range(4):
            self.widget_net[i].SetValue('10')

    def addEvents(self):
        self.cb_paste = wx.NewId()
        self.parent.Bind(wx.EVT_MENU, self.pastefromCB, id=self.cb_paste)
        self.parent.SetAcceleratorTable(wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('q'), self.cb_paste)]))
        self.btn.Bind(wx.EVT_BUTTON, self.solve)

    def show(self):
        s1 = wx.BoxSizer(wx.VERTICAL)
        s2 = wx.BoxSizer(wx.HORIZONTAL)
        s2.Add(wx.StaticText(self, -1, 'Net_e_1 (OW)'), 1, wx.EXPAND)
        s2.Add(self.widget_net[0], 0)
        s1.Add(s2, 0, wx.EXPAND)
        s1.Add(wx.StaticLine(self), 0, wx.EXPAND)
        s3 = wx.BoxSizer(wx.HORIZONTAL)
        s3.Add(wx.StaticText(self, -1, 'Net_e_2 (Pl)'), 1, wx.EXPAND)
        s3.Add(self.widget_net[1], 0)
        s1.Add(s3, 0, wx.EXPAND)
        s1.Add(wx.StaticLine(self), 0, wx.EXPAND)
        s3 = wx.BoxSizer(wx.HORIZONTAL)
        s3.Add(wx.StaticText(self, -1, 'Net_e_3 (Al)'), 1, wx.EXPAND)
        s3.Add(self.widget_net[2], 0)
        s1.Add(s3, 0, wx.EXPAND)
        s1.Add(wx.StaticLine(self), 0, wx.EXPAND)
        s4 = wx.BoxSizer(wx.HORIZONTAL)
        s4.Add(wx.StaticText(self, -1, 'Net_e_4 (Cu)'), 1, wx.EXPAND)
        s4.Add(self.widget_net[3], 0)
        s1.Add(s4, 0, wx.EXPAND)
        s1.Add(wx.StaticLine(self), 0, wx.EXPAND)
        s1.Add(self.btn, 0, wx.CENTER)
        self.SetSizer(s1)

    def pastefromCB(self, event):
        cb = wx.TheClipboard
        if cb.Open():
            data = wx.TextDataObject()
            if cb.GetData(data):
                data = data.GetText().split()
                for i in range(4):
                    try:
                        self.widget_net[i].SetValue(data[i])
                    except: pass

    def solve(self, event):

        def read():
            self.net_e = []
            try:
                for i in range(4):
                    self.net_e.append(float(self.widget_net[i].GetValue()))
                    if self.net_e[i]<=0:
                        self.parent.output.stdout.SetValue('Error! net_e%d value <= 0.' % (i+1))
                        return False
            except:
                self.parent.output.stdout.SetValue('Error is in net_e%d.\nThe input must be a number.' % (i+1))
                return False
            self.parent.output.stdout.SetValue('Input was readed.\n\n')
            return True

        def calcPhoton():
            # Al/Cu: R34
            self.r34 = self.net_e[2]/self.net_e[3]
            self.r34 = 1.0 if self.r34<1.0 else 7.7 if self.r34>7.7 else self.r34
            self.r34 = 1.0 if (self.net_e[2]<5 or self.net_e[3]<5) else self.r34
            # Pl/Cu: R24
            self.r24 = self.net_e[1]/self.net_e[3]
            self.r24 = 1.0 if self.r24<1.0 else 20.0 if self.r24>20.0 else self.r24
            self.r24 = 1.0 if (self.net_e[1]<5 or self.net_e[3]<5) else self.r24
            # Energy Calc
            k = [-0.0061, 0.0073, 0.0481]
            self.energy   = 1/(k[0] + k[1]*self.r34 + k[2]*math.log(self.r34)/math.pow(self.r34, 2))
            k = [0.0229, 0.0005, -0.0215]
            self.energy24 = 1/(k[0] + k[1]*self.r24*math.log(self.r24) + k[2]/math.pow(self.r24, 2))
            # Correction factor to calculate shallow dose from E4
            k = [1.1307, -2.3377, 0.1857, 4.637]
            self.HsE4 = k[0] + k[1]*self.r34*math.log(self.r34) + k[2]*math.pow(self.r34, 2)*math.log(self.r34) + k[3]*math.pow(math.log(self.r34), 2)
            # Correction factor to calculate deep dose from E4
            k = [3.902, -11.238, 7.4599]
            self.HdE4 = math.exp(k[0] + k[1]/math.pow(self.r34, 0.5) + k[2]/self.r34)
            # Correction factor to calculate E1 photo respone based on E4
            k = [2.3672, 0.0285, -2.402]
            self.E1E4 = math.exp(k[0] + k[1]*math.pow(self.r34, 2) + k[2]/math.pow(self.r34, 0.5))
            # Correction factor to calculate E2 photo respone based on E4
            k = [2.4188, 0.0254, -2.4537]
            self.E2E4 = math.exp(k[0] + k[1]*math.pow(self.r34, 2) + k[2]/math.pow(self.r34, 0.5))
            # Correction factor to calculate shallow dose from E2
            k = [-1.9503, 0.239, 1.8304]
            self.HsE2 = math.exp(k[0] + k[1]*math.pow(self.r34, 0.5) + k[2]/math.pow(self.r34, 2))
            # Correction factor to calculate deep dose from E2
            k = [-0.9278, -0.3476, 1.3903]
            self.HdE2 = math.exp(k[0] + k[1]*math.pow(self.r34, 0.5) + k[2]/math.pow(self.r34, 2))
            # Cs path
            if self.r34<1.05:
                self.energy = 662
                self.HsE2 = 1.02
                self.HdE2 = 1.02
                self.HsE4 = 1.02
                self.HdE4 = 1.02
                self.E1E4 = 0.99
                self.E2E4 = 0.99
            self.HsPREDE4 = self.HsE4*self.net_e[3]
            self.HdPREDE4 = self.HdE4*self.net_e[3]
            self.HsPREDE2 = self.HsE2*self.net_e[1]
            self.HdPREDE2 = self.HdE2*self.net_e[1]
            '''
            self.parent.output.stdout.AppendText('** Only Photon **\n\n')
            for i in range(4):
                self.parent.output.stdout.AppendText('net e(%d): '%(i+1)+str(self.net_e[i])+'\n')
            self.parent.output.stdout.AppendText('r34: '+str(self.r34)+'\n')
            self.parent.output.stdout.AppendText('r24: '+str(self.r24)+'\n')
            self.parent.output.stdout.AppendText('Correction factor to calculate shallow dose from E4'+'\n'+str(self.HsE4)+'\n')
            self.parent.output.stdout.AppendText('Correction factor to calculate deep dose from E4'+'\n'+str(self.HdE4)+'\n')
            self.parent.output.stdout.AppendText('Correction factor to calculate E1 photo respone based on E4'+'\n'+str(self.E1E4)+'\n')
            self.parent.output.stdout.AppendText('Correction factor to calculate E2 photo respone based on E4'+'\n'+str(self.E2E4)+'\n')
            self.parent.output.stdout.AppendText('Correction factor to calculate shallow dose from E2'+'\n'+str(self.HsE2)+'\n')
            self.parent.output.stdout.AppendText('Correction factor to calculate deep dose from E2'+'\n'+str(self.HdE2)+'\n\n')
            #'''
            return True

        def calcBeta():
            # Net Beta Effect
            self.NetE1 = self.net_e[0] - self.net_e[3]*self.E1E4
            self.NetE2 = self.net_e[1] - self.net_e[3]*self.E2E4
            if self.NetE1<=0 or self.NetE2<=0:
                self.r12 = 100
            else:
                self.r12 = self.NetE1/self.NetE2
                if self.r12>100:
                    self.r12 = 100
            #self.parent.output.stdout.AppendText('Net Beta Effect: '+str(self.r12)+'\n\n')
            if self.r12<8 or self.r34>3:
                # Soft Beta
                self.Beta7 = self.NetE1/0.7888
                self.Beta300 = 0.45*self.Beta7
                self.RQPhoton = 'BH'
            else:
                # Beta Hi: Sr-Y
                self.Beta7 = self.NetE1/0.4136
                self.Beta300 = 0
                self.RQPhoton = 'BL'
            # Sensitivity test for beta close
            if self.NetE1>20 and self.r12>1.35 and self.NetE1>self.net_e[0]*0.07:
                self.Betaflag = 'beta'
                self.b7 = self.Beta7
                self.b300 = self.Beta300
            else:
                self.Betaflag = ''
                self.b7 = 0
                self.b300 = 0
            '''
            self.parent.output.stdout.AppendText('** Beta Calculation **\n\n')
            self.parent.output.stdout.AppendText('Net E1\n'+str(self.NetE1)+'\n')
            self.parent.output.stdout.AppendText('Net E1\n'+str(self.NetE2)+'\n')
            self.parent.output.stdout.AppendText('r12\n'+str(self.r12)+'\n')
            self.parent.output.stdout.AppendText('Beta 7\n'+str(self.b7)+'\n')
            self.parent.output.stdout.AppendText('Beta 300\n'+str(self.b300)+'\n\n')
            #'''
            return True

        def calcTotal():
            if self.b7 == 0 and self.r34<4.5 and abs(1-self.energy/self.energy24)>0.15:
                # Correction factor to calculate shallow dose from E4
                k = [0.7712, 0.23098, -0.5042]
                self.HsE4 = k[0] + k[1]*math.pow(self.r34, 1.5) + k[2]*math.log(self.r34)
                # Correction factor to calculate deep dose from E4
                k = [1.018, 0.0579, -0.9561]
                self.HdE4 = k[0] + k[1]*math.pow(self.r34, 1.5) + k[2]*math.log(self.r34)/math.pow(self.r34, 2)
                # Correction factor to calculate shallow dose from E2
                k = [0.2651, 1.1098, -0.8934]
                self.HsE2 = k[0] + k[1]/math.pow(self.r34, 2) + k[2]*math.exp(-self.r34)
                # Correction factor to calculate deep dose from E2
                k = [0.1922, 0.9419, -0.2012]
                self.HdE2 = k[0] + k[1]/math.pow(self.r34, 2) + k[2]*math.exp(-self.r34)
                self.Guess = 'mix'
                self.HsPREDE4 = self.HsE4*self.net_e[3]
                self.HdPREDE4 = self.HdE4*self.net_e[3]
                self.HsPREDE2 = self.HsE2*self.net_e[1]
                self.HdPREDE2 = self.HdE2*self.net_e[1]
            # Shallow dose - only photon
            self.Hsgam = self.HsPREDE2
            # Deep dose - photon only
            if self.r34>5:
                self.Hdgam = self.HdPREDE4
                self.Guess = 'low'
            else:
                self.Hdgam = (self.HdPREDE2 + self.HdPREDE4)/2
                self.Guess = 'mid'
            # Correct for overall bias
            self.Hsgam *= 1.06
            self.Hdgam *= 1.04
            if self.r34<1.05:
                self.Hsgam = self.HsPREDE2
                self.Hdgam = self.HdPREDE2
                self.Guess = 'gamma'
            if self.b7>0:
                if self.r12>5:
                    # Low energy, E2 0K for photons
                    self.Hsgam = self.HsPREDE2
                    if self.r34>5:
                        # High E beta if low E photon
                        self.Hdgam = self.HdPREDE4 - 0.03*self.b7
                        self.Guess = 'low'
                    else:
                        # Mid energy photon
                        self.Hdgam = (self.HdPREDE2 + self.HdPREDE4)/2
                        self.Guess = 'mid'
                else:
                    # High energy beta
                    self.Hsgam = self.HsPREDE4 - 0.02*self.b7
                    self.Hdgam = self.HdPREDE4 - 0.02*self.b7
            # New routine added 12/02/03 to accommodate M30 and beta mix.
            # Reduce beta dose if row e photons
            if self.b7>0 and self.r34>2 and self.r12<10:
                if self.Hsgam>0.1*self.b7:
                    # Do not correct if pure beta
                    self.b7 /= 1.3
                    self.b300 /= 1.3
            # Lens of eye calcs
            if self.r34<1.2:
                self.Hegam = self.Hsgam
            else:
                self.Hegam = self.Hsgam*(1.4-1.04*math.exp(-self.Hdgam/self.Hsgam))
            self.HsPREDE = self.Hsgam + self.b7
            self.HePREDE = self.Hegam +self.b300
            self.HdPREDE = self.Hdgam
            # New +++++
            if self.HsPREDE<0.95*self.HdPREDE:
                self.HsPREDE = 0.95*self.HdPREDE
            if self.HePREDE>self.HsPREDE:
                self.HePREDE = self.HsPREDE
            if self.HePREDE<self.HdPREDE:
                self.HePREDE = self.HdPREDE
            if self.HdPREDE<1.0:
                self.Hp10 = 0
            else:
                self.Hp10 = int(round(self.HdPREDE))
            if self.HePREDE<1.0:
                self.Hp3 = 0
            else:
                self.Hp3 = int(round(self.HePREDE))
            if self.HsPREDE<1.0:
                self.Hp7 = 0
            else:
                self.Hp7 = int(round(self.HsPREDE))
            self.energy = int(round(self.energy))
            if self.b7<20:
                self.b7 = 0.00
                if self.energy<=40:
                    self.RQPhoton = 'PL'
                elif self.energy<=100:
                    self.RQPhoton = 'PM'
                else:
                    self.RQPhoton = 'PH'
            else:
                self.b7 = round(self.b7/100, 2)
            '''
            self.parent.output.stdout.AppendText('** Total Dose Calculation**\n\n')
            self.parent.output.stdout.AppendText('HsE4\n'+str(self.HsE4)+'\n')
            self.parent.output.stdout.AppendText('HdE4\n'+str(self.HdE4)+'\n')
            self.parent.output.stdout.AppendText('Correction factor to calculate shallow dose from E2'+'\n'+str(self.HsE2)+'\n\n')
            self.parent.output.stdout.AppendText('Correction factor to calculate deep dose from E2'+'\n'+str(self.HdE2)+'\n\n')
            #'''
            return True

        def result():
            self.parent.output.stdout.AppendText('** RESULT **\n\n')
            '''
            self.parent.output.stdout.AppendText('HsPREDE = '+str(self.HsPREDE)+'\n')
            self.parent.output.stdout.AppendText('HePREDE = '+str(self.HePREDE)+'\n')
            self.parent.output.stdout.AppendText('HdPREDE = '+str(self.HdPREDE)+'\n\n')
            #'''
            self.parent.output.stdout.AppendText('Hp(10)     = '+str(self.Hp10)+'\n')
            self.parent.output.stdout.AppendText('Hp(3)      = '+str(self.Hp3)+'\n')
            self.parent.output.stdout.AppendText('Hp(0.07)   = '+str(self.Hp7)+'\n')
            self.parent.output.stdout.AppendText('Beta       = '+str(self.b7)+'\n')
            self.parent.output.stdout.AppendText('RQ(Photon) = '+str(self.RQPhoton)+'\n')
            self.parent.output.stdout.AppendText('Energy     = '+str(self.energy)+'\n\n')

        if read():
            calcPhoton()
            calcBeta()
            calcTotal()
            result()
        else:
            self.VarDoseCalcError = 'MCV'


class OutputPanel(wx.Panel):

    def __init__(self, parent):
        self.parent = parent
        wx.Panel.__init__(self, parent)
        self.stdout = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.stdout.SetFont(wx.Font(wx.DEFAULT, wx.MODERN, wx.NORMAL, wx.NORMAL))
        self.btn_hor_copy = wx.Button(self, -1, 'Copy in horizontal')
        self.btn_ver_copy = wx.Button(self, -1, 'Copy in vertical')
        self.btn_hor_copy.Bind(wx.EVT_BUTTON, lambda e:self.copy(1))
        self.btn_ver_copy.Bind(wx.EVT_BUTTON, lambda e:self.copy(0))
        self.show()

    def show(self):
        s1 = wx.BoxSizer(wx.VERTICAL)
        s2 = wx.BoxSizer(wx.HORIZONTAL)
        s2.Add(self.btn_hor_copy, 1)
        s2.Add(self.btn_ver_copy, 1)
        s1.Add(self.stdout, 1, wx.EXPAND)
        s1.Add(s2, 0, wx.EXPAND)
        self.SetSizer(s1)

    def copy(self, index):
        cb = wx.TheClipboard
        if cb.Open():
            data = wx.TextDataObject()
            try:
                if index:
                    data.SetText('\t'.join([str(self.parent.input.Hp10),
                                            str(self.parent.input.Hp3),
                                            str(self.parent.input.Hp7)]))
                else:
                    data.SetText('\n'.join([str(self.parent.input.Hp10),
                                            str(self.parent.input.Hp3),
                                            str(self.parent.input.Hp7)]))
            except: pass
            cb.SetData(data)
            print(data.GetText())


def main():
    App()
    return True

if __name__ == '__main__':
    main()

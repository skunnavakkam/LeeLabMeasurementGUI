Const BOARD_ID = 0 ' GP-IB Interface card
Address
Const osa = 1 ' OSA GP-IB Address
Private Sub AQ637XTEST()
Dim intData As Integer
Dim dblMeanWL As Double
Dim dblSpecWd As Double
Dim strData As String
' === GP-IB Interface setting ===
' send IFC
Call SendIFC(BOARD_ID)
' assert th REN GPIB line
intAddrList(0) = NOADDR
Call EnableRemote(BOARD_ID, intAddrList())
' GPIB time out setting
Call ibtmo(BOARD_ID, T30s) ' Time out = 30sec
' === Set the measurement parameter ===
Call SendGPIB(osa, "*RST") ' Setting initialize
Call SendGPIB(osa, "CFORM1") ' Command mode
set(AQ637X mode)
Call SendGPIB(osa, ":sens:wav:cent 1550nm") ' sweep center wl
Call SendGPIB(osa, ":sens:wav:span 10nm") ' sweep span
Call SendGPIB(osa, ":sens:sens mid") ' sens mode = MID
Call SendGPIB(osa, ":sens:sweep:points:auto on")
' Sampling Point = AUTO
' === Sweep execute ===
Call SendGPIB(osa, ":init:smode 1") ' single sweep mode
Call SendGPIB(osa, "*CLS") ' status clear
Call SendGPIB(osa, ":init") ' sweep start
' === Wait for sweep complete ===
Do
Call SendGPIB(osa, ":stat:oper:even?") ' get Operation Event
Register
strData = RecieveGPIB(osa)
intData = Val(strData)
Loop While ((intData And 1) <> 1) ' Bit0: Sweep status
' === Analysis ===
Call SendGPIB(osa, ":calc:category swth") ' Spectrum width
analysis(THRESH type)
Call SendGPIB(osa, ":calc") ' Analysis Execute
Call SendGPIB(osa, ":calc:data?") ' get data
strData = RecieveGPIB(osa)
2-10IM AQ6374-17EN
' === Capture analytical results ===
dblMeanWL = Val(Left(strData, 16)) ' get mean wavelegnth
dblSpecWd = Val(Mid(strData, 18, 16)) ' get spectrum width
' === Output the result to the screen ===
MsgBox ("MEAN WL: " & dblMeanWL * 1000000000# & " nm" & vbCrLf & _
"SPEC WD: " & dblSpecWd * 1000000000# & " nm")
' === Disconnect ===
Call EnableLocal(BOARD_ID, intAddrList())
End Sub
'==================================================
' Sub routine
' Send Remote Command
'==================================================
Sub SendGPIB(intAddr As Integer, strData As String)
Call Send(BOARD_ID, intAddr, strData, NLend)
If (ibsta And EERR) Then
MsgBox " GP-IB device can't write"
End If
End Sub
'==================================================
' Sub routine
' Recieve query data
'==================================================
Function RecieveGPIB(intAddr As Integer) As String
Const READSIZE = 10000
Dim strBuffer As String
strBuffer = Space(READSIZE)
RecieveGPIB = ""
Do
DoEvents
Call Receive(BOARD_ID, intAddr, strBuffer, STOPend)
If (ibsta And EERR) Then
MsgBox " GP-IB device can't read."
RecieveGPIB = ""
Exit Function
Else
RecieveGPIB = RecieveGPIB & Left(strBuffer, ibcntl)
End If
Loop Until ((ibst
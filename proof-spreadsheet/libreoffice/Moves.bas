Function DARG(inputString As String, n As Integer,Optional show As Boolean) As String
   	If IsMissing(show) Then
   		show = False
   	End If
   	Dim parts() As String
   	Dim result As String
    ' Split the string using delimiters ";" and "/"
    inputString = Replace(inputString, "/",";")
    parts = Split(inputString, ";") 
    ' Check if the requested part exists
    If n >= 1 And n <= UBound(parts)+1 Then
        result = parts(n-1)
    EndIf
    If n = UBound(parts)+1 And show Then
    	result = "Show: " & result
    End If
    DARG = result
End Function

Function SCount(str As String, symbols() as Variant) AS Integer
	Dim original As Integer
	original = Len(str)
	For Each symbol in symbols
		str = Replace(str,symbol,"")
	Next symbol
	SCount=original-len(str)
End Function

Function SiCount(str as String, symbol as Variant)
	SiCount = SCount(str, Array(symbol))
End Function

Function StrReverse(inputString As String) As String
    Dim reversedString As String
    Dim i As Integer
    
    reversedString = ""
    
    For i = Len(inputString) To 1 Step -1
        reversedString = reversedString & Mid(inputString, i, 1)
    Next i
    
    StrReverse = reversedString
End Function

Function ReplaceIgnoreCase(ByVal originalText As String, ByVal findText As String, ByVal replaceText As String) As String
    Dim startPosition As Integer
    Dim result As String
    
    startPosition = Instr(1, LCase(originalText), LCase(findText))
    
    If startPosition > 0 Then
        result = Left(originalText, startPosition - 1)
        result = result & replaceText
        result = result & Mid(originalText, startPosition + Len(findText))
    Else
        result = originalText
    End If
    
    ReplaceIgnoreCase = result
End Function

Function RemoveN(sline As String, symbol As String, n As Integer, Optional lastN As Boolean) As String
	If n = 0 Then
		RemoveN = sline
		Exit Function
	End If
	If IsMissing(lastN) Then
		lastN = False
	End If
    Dim result As String
    Dim i As Integer
    
    result = ""
    
    If lastN Then
        sline = StrReverse(sline)
    End If
    
    For i = 1 To Len(sline)
        Dim c As String
        c = Mid(sline,i,1)
        
        If c = symbol And n > 0 Then
            n = n - 1
        ElseIf lastN Then
            result = c & result
        Else
            result = result & c
        End If
    Next i
    
    RemoveN = result
End Function



Function ID(sline,Optional negative As Boolean) As String
	If IsMissing(negative) Then
		negative = False
	End If
	sline = ReplaceIgnoreCase(sline,"Show: ","")
	If negative Then
		index = InStr(1,sline,"~")
		ID = Right(sline,Len(sline)-index)
	Else
		notHighest = SCount(sline,Array("→","∨","&","↔"))-SCount(sline,Array(")"))
		If notHighest Then
			sline = "(" & sline & ")"
		End If
		ID = "~" & sline
	End If
End Function

Function CD(sline As String, isAfter As Boolean) As String
    Dim startIndex As Integer
    Dim endIndex As Integer
    Dim parenthesesCount As Integer
    Dim i As Integer
    Dim foundIndex As Integer
    
    sline = ReplaceIgnoreCase(sline, "Show: ", "")
    parenthesesCount = 0
    
    ' Iterate through each character in the string
    For i = 1 To Len(sline)
        ' Check if the character is an opening parentheses
        If Mid(sline, i, 1) = "(" Then
            parenthesesCount = parenthesesCount + 1
        ' Check if the character is a closing parentheses
        ElseIf Mid(sline, i, 1) = ")" Then
            parenthesesCount = parenthesesCount - 1
        ' Check if the character is the "→" symbol and not inside parentheses
        ElseIf Mid(sline, i, 1) = "→" And parenthesesCount = 0 Then
            foundIndex = i
            Exit For
        End If
    Next i
    
    ' Determine the start and end indexes based on the flag
    If isAfter Then
        startIndex = foundIndex + 1 
        endIndex = Len(sline)
    Else
        endIndex = foundIndex - 1
        startIndex = 1
    End If
    
    ' Extract the desired portion based on the start and end indexes
    sline = Mid(sline, startIndex, endIndex - startIndex + 1)
    'If isAfter Then
    '    sline = RemoveN(sline, SiCount(sline, ")") - SiCount(sline, "("), 1)
    'Else
    '    sline = RemoveN(sline, SiCount(sline, "(") - SiCount(sline, ")"), 0)
    'End If
    
    CD = sline
End Function

Function UD(sline As String) As String
    sline = ReplaceIgnoreCase(sline, "Show: ", "")
    index = InStr(1, sline, "∀")
    sym = Mid(sline,  index + 1, 1)
    If sym >= "A" And sym <= "Z" Then
        sline = Replace(sline, sym, Chr$(Asc(sym) - 88 + 97))
    Else
        sline = Replace(sline, sym, Chr$(Asc(sym) - 120 + 97))
    End If
    sline = Right(sline, Len(sline) - index - 1)
    ' Check if parentheses wrap the entire string
    If Left(sline, 1) = "(" And Right(sline, 1) = ")" Then
        sline = Mid(sline, 2, Len(sline) - 2)
    End If
    
    UD = "Show: " & sline
End Function

Function HandleAssumption(originalShow AS String,method As String) As String
	Dim result As String 
	result = "Show: "
	originalShow = ReplaceIgnoreCase(originalShow,result,"")
	Select Case method
		Case "CD"
			result = result & CD(originalShow,2)
		Case Else
			result = result & Chr$(10803)
	End Select
	HandleAssumption = result
End Function

Function DMove(ByVal n As Integer, ByVal exercise As String, previous as Variant) As String
    Dim result As String
    Dim row AS Integer
    row = UBound(previous,1)
    Dim col As Integer
    col = LBound(previous,2)
    ' Check if DARG(n, exercise) returns something
    result = DARG(exercise,n,1)
    If result <> "" Then
        DMove = result
        Exit Function
    End If
    
    ' Pattern matching on previous string
    Dim l1 As String
    l1 = UCase(previous(row,col+1))
    Dim sline as String
    sline = previous(row,col)
	sline = LTrim(ReplaceIgnoreCase(sline,"Show: ",""))
    Select Case l1
        Case "DD"
            DMove = ""
        Case "CD"
            DMove = CD(sline,0)
        Case "UD"
        	DMove = UD(sline)
        Case "~D"
        	DMove = ID(sline,1)
        Case "∃D"
        	DMove=ID(sline)
        Case "ID"
            DMove=ID(sline)
        Case "AS"
        	DMove=HandleAssumption(previous(row-1,col),previous(row-1,col+1))
        Case Else
            DMove = ""
    End Select
End Function

Sub Main
End Sub
